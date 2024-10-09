import sqlite3
from datetime import datetime


def get_posts(cur: sqlite3.Cursor):
    result = cur.execute(
        "select content,created_at from posts order by created_at desc limit 100").fetchall()
    posts = [dict(content=item[0], created_at=item[1])for item in result]
    return posts

def set_post(cur:sqlite3.Cursor,content:str):
    if content!="":
        cur.execute("insert into posts(content,created_at) values(?,?)",
                    (content, datetime.now()))
        cur.commit()