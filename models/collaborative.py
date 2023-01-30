from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np

from database import redis

relations: dict = redis.relation_to_dict(redis.rdb, rel_name="u2p")
df: pd.DataFrame = pd.DataFrame(index=relations["users"], columns=relations["items"])

for user_id in relations["relations"].keys():
    for post_id in relations["relations"][user_id]:
        df.loc[user_id, post_id] = 1
df = df.fillna(0)

standatized_values: np.ndarray = StandardScaler().fit_transform(df)

pca_obj: PCA = PCA(n_components=5)
pca_data: np.ndarray = pca_obj.fit_transform(standatized_values)
pca_df: np.ndarray = pd.DataFrame(data=pca_data, index=relations["users"])
# print(pca_obj.explained_variance_ratio_)

"""

I should use a kmeans / fcm or t-fcm based model for clustering users.
Afterwards I will create a weighted set for each cluster
and determine weight of each posts by no of user who liked that post in that cluster.

"""

kmeans = KMeans(init="k-means++", n_clusters=2)

kmeans.fit(pca_df.values)

result = pd.DataFrame(data=kmeans.labels_, index=pca_df.index)


def get_cluster(user_id: int):
    return result[0][user_id]


class CollaborativeModel():
    def __init__(self):
        self.scalers: StandardScaler = StandardScaler()
        self.pca_obj: PCA = None
        self.k_means: KMeans = None
        self.results: pd.DataFrame = None

    def pull_dataframe(self, rel_name: str, pca_num: int) -> pd.DataFrame:
        relations: dict = redis.relation_to_dict(redis.rdb, rel_name="u2p")
        df: pd.DataFrame = pd.DataFrame(index=relations["users"], columns=relations["items"])

        for user_id in relations["relations"].keys():
            for item_id in relations["relations"][user_id]:
                df.loc[user_id, item_id] = 1
        df = df.fillna(0)

        standatized_values: np.ndarray = self.scalers.fit_transform(df)

        self.pca_obj = PCA(n_components=pca_num)
        pca_data: np.ndarray = self.pca_obj.fit_transform(standatized_values)
        return pd.DataFrame(data=pca_data, index=relations["users"])

    def update_model(self):
        pass

    def recommend(self, user_ids: list) -> dict:
        pass
