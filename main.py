from fastapi import FastAPI, Depends

from api.routers import objects, relations, recommender
from api.auth import auth

app = FastAPI(dependencies=[Depends(auth.validate_credentials)])

app.include_router(objects.user_router)
app.include_router(objects.post_router)
app.include_router(relations.u2u_router)
app.include_router(relations.u2p_router)
app.include_router(relations.u2c_router)
app.include_router(recommender.recommender_router)
