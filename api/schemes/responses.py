from pydantic import BaseModel


class ObjectOperations(BaseModel):
    status: str
    error: str | None = None


class RelationOperations(BaseModel):
    status: str
    action: str | None = None


class RecommendResponse(BaseModel):
    scores: list | None = list()
    error: str | None = None
