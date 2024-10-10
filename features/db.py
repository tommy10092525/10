import sqlite3
from datetime import datetime
from typing import Any
from features.time_handler import generateTimeCaption

def dateConverter(result:list[dict[str,Any]]) -> list[dict[str, Any]]:
    for i in result:
        for j in i.keys():
            if j=="created_at":
                i[j]=generateTimeCaption(i[j])
    return result

def dictFactory(cur: sqlite3.Cursor, row):
    d = {}
    for idx, col in enumerate(cur.description):
        d[col[0]] = row[idx]
    return d

def getThreads(cur:sqlite3.Cursor) -> list[dict[str, Any]]:
    result=cur.execute("""--sql
        select *
        from threads
        order by created_at
        limit 10""").fetchall()
    
    return dateConverter(result)

def getThreadsByKindId(cur:sqlite3.Cursor,id:int) -> list[dict[str, Any]]:
    result=cur.execute("""--sql
        select *
        from threads
        where kind_id=?
        limit 100""",(id,)).fetchall()
    return dateConverter(result)
    
def getDivisions(cur:sqlite3.Cursor) -> list[dict[str, Any]]:
    result=cur.execute("""--sql
        select *
        from divisions""").fetchall()
    return dateConverter(result)
    
def getKindsByDivisionsId(cur:sqlite3.Cursor,divisionsId:int) -> list[dict[str, Any]]:
    result=cur.execute("""--sql
        select *
        from kinds
        where division_id=?""",(divisionsId,)).fetchall()
    return dateConverter(result)

# def getPosts(cur: sqlite3.Cursor) -> list[dict[str, Any]]:
#     result = cur.execute("""--sql
#         SELECT id,content,created_at
#         FROM posts
#         ORDER BY created_at DESC
#         LIMIT 100""").fetchall()
#     return result


# def setPost(cur: sqlite3.Cursor, content: str) -> None:
#     if content != "" and len(content) <= 1000:
#         cur.execute("""--sql
#             INSERT INTO posts(content,created_at)
#             VALUES(?,?)""",
#                     (content, datetime.now()))


# def getPostById(cur: sqlite3.Cursor, id: int):
#     result = cur.execute("""--sql
#         SELECT id,content,created_at
#         FROM posts
#         WHERE id=?""", (id,)).fetchone()
#     return result


# def getPostCount(cur: sqlite3.Cursor):
#     result = cur.execute("""--sql
#         SELECT COUNT(*)
#         AS count
#         FROM posts""").fetchone()
#     return result["count"]


