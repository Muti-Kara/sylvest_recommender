from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from random import seed, random
import pandas as pd
import numpy as np
import datetime

from database.scripts import postgres_scripts
from database import postgresql, redis

seed(42)


class ContentBasedModel():
    def __init__(self):
        self.id_to_index: pd.Series = None
        self.index_to_id: pd.Series = None
        self.sim_matrix: np.ndarray = None
        self.tfdif = TfidfVectorizer(lowercase=False, stop_words=None, token_pattern="(?u)\\b\\w\\w*\\b")
        self.count = CountVectorizer(lowercase=False, stop_words=None, token_pattern="(?u)\\b\\w\\w*\\b")

    def random_idx(self):
        return random() % self.id_to_index

    def set_id_index(self, df: pd.DataFrame):
        self.id_to_index = pd.Series(df.index, index=df["id"])
        self.index_to_id = pd.Series(df["id"])

    def cache_to_redis(self, cache_name: str):
        redis.rdb.delete(f"{cache_name}:")
        for id in self.index_to_id:
            redis.add_relation(cache_name, "", id)

    def update_model(self):
        pass

    def recommend(self, item_ids: list) -> dict:
        if len(item_ids) == 0:
            item_ids = [self.random_idx(), self.random_idx(), self.random_idx()]
        index_in_matrix = self.id_to_index[item_ids]
        enum = [(int(self.index_to_id[item_indice]), float(sim_score)) for item_indice, sim_score in
                                        enumerate(np.sum(self.sim_matrix[index_in_matrix], axis=0))]
        return dict(enum)


class UserRecommender(ContentBasedModel):
    follow_weight: float = .75
    data_weight: float = .25

    @staticmethod
    def follows_by_id(id: int):
        following_set: set = redis.get_relation("follow", id)
        following_set.add("b" + str(id))
        return str(following_set).replace(",", "").replace("'", "").strip("{}")

    def update_model(self):
        df: pd.DataFrame = pd.read_sql_query(postgres_scripts.get_users, postgresql.conn)
        self.set_id_index(df)

        df["follows"] = df["id"]
        df["follows"] = df["follows"].apply(self.follows_by_id)

        tfidf_matrix = self.tfdif.fit_transform(df["follows"])
        count_matrix = self.count.fit_transform(df["data"])

        tfidf_matrix = linear_kernel(tfidf_matrix, tfidf_matrix)
        count_matrix = cosine_similarity(count_matrix, count_matrix)

        self.sim_matrix = count_matrix * self.data_weight + tfidf_matrix * self.follow_weight

        self.cache_to_redis("cached_users")


class PostRecommender(ContentBasedModel):
    delay_rate: float = 1.2
    contents_weight: float = .4
    metadata_weight: float = .8

    def calculate_delays(self, df: pd.DataFrame) -> np.ndarray:
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        df["date"] = tomorrow - df["date"]
        df["date"] = df["date"].apply(lambda x: x.days)
        delay_arr = np.array(df["date"])
        return np.array(list(map(lambda x: self.delay_rate ** x, delay_arr)))

    def update_model(self):
        df: pd.DataFrame = pd.read_sql_query(postgres_scripts.get_posts, postgresql.conn)
        self.set_id_index(df)

        tfdif_matrix = self.tfdif.fit_transform(df["contents"])
        count_matrix = self.count.fit_transform(df["metadata"])

        tfidf_matrix = linear_kernel(tfdif_matrix, tfdif_matrix)
        count_matrix = cosine_similarity(count_matrix, count_matrix)

        self.sim_matrix = (tfidf_matrix * self.contents_weight + count_matrix * self.metadata_weight) /\
            self.calculate_delays(df)

        self.cache_to_redis("cached_posts")
