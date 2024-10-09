import sqlite3
from datetime import datetime

def get_posts(cur:sqlite3.Cursor):
    result = cur.execute("select content,created_at from posts limit 100").fetchall()
    posts = [dict(content=item[0], created_at=item[1])
                         for item in result]
    return posts
    