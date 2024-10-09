import sqlite3
from datetime import datetime
from typing import Any


def dict_factory(cur:sqlite3.Cursor,row):
    d={}
    for idx,col in enumerate(cur.description):
        d[col[0]]=row[idx]
    return d

def get_posts(cur: sqlite3.Cursor) -> list[dict[str, Any]]:
    result = cur.execute("""
        SELECT id,content,created_at
        FROM posts
        ORDER BY created_at DESC
        LIMIT 100"""
        ).fetchall()
    return result

def set_post(cur:sqlite3.Cursor,content:str) -> None:
    if content!="" and len(content)<=1000:
        cur.execute("""
            INSERT INTO posts(content,created_at)
            VALUES(?,?)""",
            (content, datetime.now()))
        cur.commit()

def get_post_by_id(cur:sqlite3.Cursor,id:int):
    result=cur.execute("""
        SELECT id,content,created_at
        FROM posts
        WHERE id=?""",(id,)).fetchone()
    return result
def get_post_count(cur:sqlite3.Cursor):
    result=cur.execute("""SELECT COUNT(*)
                    FROM posts""").fetchone()
    return result["COUNT(*)"]


