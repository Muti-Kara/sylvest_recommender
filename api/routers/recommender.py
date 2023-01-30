from fastapi import APIRouter

from api.schemes import responses
from models import content_based
from database import redis

recommender_router = APIRouter(
    prefix="/recommender",
    tags=["Recommender API"]
)

following_bonus: float = 0.3

post_rec = content_based.PostRecommender()
user_rec = content_based.UserRecommender()

PAGE_SIZE = 10


def paginate(items: list, page: int):
    return items[PAGE_SIZE * (page - 1): PAGE_SIZE * page]


@recommender_router.get("/user/{user_id}/")
def recommend_user(user_id: int) -> responses.RecommendResponse:
    if redis.rdb.sismember("cached_users:", f"{user_id}"):
        try:
            user_scores = user_rec.recommend([user_id])
            return responses.RecommendResponse(
                items=sorted(user_scores.keys(), key=lambda x: user_scores[x])[:30],
            )
        except Exception as e:
            return responses.RecommendResponse(error=str(e))
    else:
        return responses.RecommendResponse(error="This user is not cached")


@recommender_router.get("/post/{user_id}/{page}")
def recommend(user_id: int, page: int) -> responses.RecommendResponse:
    liked_posts = redis.rdb.sinter(f"u2p:{user_id}", "cached_posts:")

    try:
        post_scores: dict = post_rec.recommend([int(bytes) for bytes in liked_posts])
        followings: set = redis.get_relation("u2u", user_id)
        for p_id in post_scores.keys():
            if redis.get_relation("posted", p_id, unique=True) in followings:
                post_scores[p_id] += following_bonus
        return responses.RecommendResponse(
            scores=paginate(
                sorted(post_scores.keys(), key=lambda x: post_scores[x]),
                page=page
            )
        )
    except Exception as e:
        return responses.RecommendResponse(error=str(e))


@recommender_router.post("/update")
def update_recommenders():
    status = update_post_rec()
    status.update(update_user_rec())
    return status


@recommender_router.post("/update/post")
def update_post_rec():
    try:
        post_rec.update_model()
        return {"posts status": "successful"}
    except Exception as e:
        import traceback

        print(traceback.format_exc())
        return {"posts status": "unsuccessful"}


@recommender_router.post("/update/user")
def update_user_rec():
    try:
        user_rec.calculate_similarity_matrix()
        return {"users status": "successful"}
    except Exception as e:
        import traceback

        print(traceback.format_exc())
        return {"users status": "unsuccessful"}
