from psycopg2 import sql
import psycopg2 as db
import os

from database.scripts import postgres_scripts
import settings

try:
    conn: db.extensions.connection = db.connect(settings.p_dburl)
    conn.set_session(autocommit=True)
except Exception as e:
    print(e)
    os.abort()

with conn.cursor() as cur:
    cur: db.extensions.cursor
    cur.execute(postgres_scripts.create_tables)

insert_statement: str = """INSERT INTO {} {} VALUES {}"""
update_statement: str = """UPDATE {} SET {} WHERE id = %s"""
delete_statement: str = """DELETE FROM {} WHERE id = %s"""


def insert(table_name: str, item_dict: dict):
    with conn.cursor() as cur:
        cur.execute(
            sql.SQL(insert_statement.format(
                    table_name,
                    str(tuple(item_dict.keys())).replace("'", ""),
                    "(" + ("%s, " * len(item_dict))[:-2] + ")"
                )
            ),
            tuple(item_dict.values())
        )

def update(table_name: str, item_dict: dict):
    with conn.cursor() as cur:
        id = item_dict.pop("id")
        cur.execute(
            sql.SQL(update_statement.format(
                    table_name,
                    ', '.join('{} = %s'.format(k) for k in item_dict) 
                )
            ),
            (*tuple(item_dict.values()), id)
        )

def delete(table_name: str, id: int):
    with conn.cursor() as cur:
        cur.execute(
            sql.SQL(delete_statement.format(table_name)),
            (id,)
        )
