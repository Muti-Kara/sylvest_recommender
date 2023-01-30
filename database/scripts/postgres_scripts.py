create_tables: str = """

CREATE TABLE IF NOT EXISTS posts (
    id int,
    metadata varchar(500),
    contents varchar(500),
    date date,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS users (
    id int,
    data varchar(500),
    PRIMARY KEY (id)
);

"""

get_users: str = """SELECT * FROM users;"""

get_posts: str = """SELECT * FROM posts;"""
