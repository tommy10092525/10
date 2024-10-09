import sqlite3
from datetime import datetime
from typing import Any


def get_posts(cur: sqlite3.Cursor) -> list[dict[str, Any]]:
    result = cur.execute("""
        SELECT id,content,created_at
        FROM posts
        ORDER BY created_at DESC
        LIMIT 100"""
        ).fetchall()
    posts = [dict(id=item[0],content=item[1], created_at=item[2])for item in result]
    return posts

def set_post(cur:sqlite3.Cursor,content:str) -> None:
    if content!="":
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
    post=dict(id=result[0],content=result[1],created_at=result[2])

def get_post_count(cur:sqlite3.Cursor):
    cnt=cur.execute("""SELECT COUNT(*)""")
    return cnt

