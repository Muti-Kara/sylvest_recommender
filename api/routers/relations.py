from fastapi import APIRouter

from api.schemes import relations, responses
from database import redis


def add_relation(rel: relations.Relation, rel_name: str) -> responses.RelationOperations:
    if redis.add_relation(rel_name, rel.user_id, rel.item_id):
        return responses.RelationOperations(status="successful")
    return responses.RelationOperations(status="unsuccessful", action="relate")


def rem_relation(rel: relations.Relation, rel_name: str) -> responses.RelationOperations:
    if redis.rem_relation(rel_name, rel.user_id, rel.item_id):
        return responses.RelationOperations(status="successful")
    return responses.RelationOperations(status="unsuccessful", action="unrelate")


u2u_router = APIRouter(
    prefix="/u2u",
    tags=["User2User API"]
)


@u2u_router.post("")
def add_user(u2u: relations.User2User) -> responses.RelationOperations:
    add_relation(rel=u2u, rel_name="u2u")


@u2u_router.delete("")
def rem_user(u2u: relations.User2User) -> responses.RelationOperations:
    rem_relation(rel=u2u, rel_name="u2u")


u2p_router = APIRouter(
    prefix="/u2p",
    tags=["User2Post API"]
)


@u2p_router.post("")
def add_post(u2p: relations.User2Post) -> responses.RelationOperations:
    add_relation(rel=u2p, rel_name="u2p")


@u2p_router.delete("")
def rem_post(u2p: relations.User2Post) -> responses.RelationOperations:
    rem_relation(rel=u2p, rel_name="u2u")


u2c_router = APIRouter(
    prefix="/u2c",
    tags=["User2Comm API"]
)


@u2c_router.post("")
def add_comm(u2c: relations.User2Comm) -> responses.RelationOperations:
    add_relation(rel=u2c, rel_name="u2c")


@u2c_router.delete("")
def rem_comm(u2c: relations.User2Comm) -> responses.RelationOperations:
    rem_relation(rel=u2c, rel_name="u2c")
