from pydantic import BaseModel


class Relation(BaseModel):
    user_id: int
    item_id: int


class User2User(Relation):
    pass


class User2Post(Relation):
    pass


class User2Comm(Relation):
    pass
