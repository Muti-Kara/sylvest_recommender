from fastapi import APIRouter

from api.schemes import objects, responses
from database import postgresql, redis

"""
This file has 2 routers which for insertion, updates, and deletion of objects.
"""

user_router = APIRouter(
    prefix="/users",
    tags=["User API"]
)


@user_router.post("")
def insert(user: objects.UserModel) -> responses.ObjectOperations:
    try:
        postgresql.insert(user.get_tables_name(), user.get_object_dict())
        return responses.ObjectOperations(status="successful")
    except Exception as e:
        return responses.ObjectOperations(status="unsuccessfull", 
                                          error=str(e))


@user_router.put("")
def update(user: objects.UserModel) -> responses.ObjectOperations:
    try:
        postgresql.update(user.get_tables_name(), user.get_object_dict())
        return responses.ObjectOperations(status="successful")
    except Exception as e:
        return responses.ObjectOperations(status="unsuccessfull", error=str(e))


@user_router.delete("")
def delete(user: objects.UserModel) -> responses.ObjectOperations:
    try:
        postgresql.delete(user.get_tables_name(), user.id)
        return responses.ObjectOperations(status="successful")
    except Exception as e:
        return responses.ObjectOperations(status="unsuccessfull", error=str(e))


post_router = APIRouter(
    prefix="/posts",
    tags=["Post API"]
)


@post_router.post("")
def insert(post: objects.PostModel) -> responses.ObjectOperations:
    try:
        postgresql.insert(post.get_tables_name(), post.get_object_dict())
        redis.add_relation("posted", post.id, post.author, unique=True)
        return responses.ObjectOperations(status="successful")
    except Exception as e:
        return responses.ObjectOperations(status="unsuccessfull", error=str(e))


@post_router.put("")
def update(post: objects.PostModel) -> responses.ObjectOperations:
    try:
        postgresql.update(post.get_tables_name(), post.get_object_dict())
        return responses.ObjectOperations(status="successful")
    except Exception as e:
        return responses.ObjectOperations(status="unsuccessfull", error=str(e))


@post_router.delete("")
def delete(post: objects.PostModel) -> responses.ObjectOperations:
    try:
        postgresql.delete(post.get_tables_name(), post.id)
        redis.rem_relation("posted", post.id, post.author, unique=True)
        return responses.ObjectOperations(status="successful")
    except Exception as e:
        return responses.ObjectOperations(status="unsuccessfull", error=str(e))
