import os

p_dburl = os.getenv("DATABASE_URL")
r_dburl = os.getenv("REDIS_URL")

auth_user = os.getenv("VALID_USERNAME")
auth_pass = os.getenv("VALID_PASSWORD")
