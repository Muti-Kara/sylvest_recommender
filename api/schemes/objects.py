from pydantic import BaseModel
from typing import List

from preprocess.nlp import nlp

"""
These models have two common functions:
    get_object_dict -> returns a dictionary for the pydantic model for sql queries
    get_tables_name -> returns the table name in postgresql for sql queries (s in tables are just for alignment :) )

Besides here some of the preprocessing part is being done (such as computationally expensive but regular nlp tasks)
There are 2 objects:
    Users
    Posts
"""


class PostModel(BaseModel):
    id: int
    community: str | None = ""
    title: str
    tags: List[str] | None = []
    author: int
    contents: List[dict]
    date: str

    @staticmethod
    def prepare_content(x) -> str:
        x = str(x).replace("[", " ").replace("]", " ").replace("{", " ").replace("}", " ")
        x = x.replace("contentItems", " ").replace("paragraphs", " ").replace("bullets", " ")
        return x

    def get_object_dict(self) -> dict:
        author: str = f"{self.author}US"
        if self.community is None:
            community: str = ""
        else:
            community: str = f"{self.community}CO"
        if self.tags is None:
            tags: str = ""
        else:
            tags: str = nlp.process(" ".join(self.tags))

        contents = nlp.process( self.prepare_content(self.contents) + " " + self.title + f" COMMON{self.id}")
        metadata = f"{author} {community} {tags}"
        return {
            "id": self.id,
            "contents": contents,
            "metadata": metadata,
            "date": self.date
        }

    def get_tables_name(self) -> str:
        return "posts"


class UserModel(BaseModel):
    id: int
    about: str | None = ""

    def get_object_dict(self) -> dict:
        data: str = nlp.process(self.about) + " COMMON" + str(self.id)
        return {"id": self.id, "data": data}

    def get_tables_name(self) -> str:
        return "users"
