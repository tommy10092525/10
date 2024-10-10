import sqlite3
from datetime import datetime
from typing import Any
from features.time_handler import generateTimeCaption


def dateConverter(result: list[dict[str, Any]] | dict[str, Any]) -> list[dict[str, Any]]:
    print(type(result))
    if type(result) is list:
        for i in result:
            for j in i.keys():
                if j == "created_at":
                    i[j] = generateTimeCaption(i[j])
    else:
        for j in result.keys():
            if j == "created_at":
                result[j] = generateTimeCaption(result[j])
    return result


def dictFactory(cur: sqlite3.Cursor, row):
    d = {}
    for idx, col in enumerate(cur.description):
        d[col[0]] = row[idx]
    return d


def getThreadById(cur: sqlite3.Cursor, id: int):
    result = cur.execute("""--sql:
        select *
        from threads
        where id=?""", (id,)).fetchone()
    return dateConverter(result)


def getThreads(cur: sqlite3.Cursor) -> list[dict[str, Any]]:
    result = cur.execute("""--sql
        select *
        from threads
        order by created_at
        limit 10""").fetchall()

    return dateConverter(result)


def getThreadsByKindId(cur: sqlite3.Cursor, kindId: int) -> list[dict[str, Any]]:
    result = cur.execute("""--sql
        select *
        from threads
        where kind_id=?
        limit 100""", (kindId,)).fetchall()
    return dateConverter(result)


def getDivisions(cur: sqlite3.Cursor) -> list[dict[str, Any]]:
    result = cur.execute("""--sql
        select *
        from divisions""").fetchall()
    return dateConverter(result)


def getKindsByDivisionsId(cur: sqlite3.Cursor, divisionsId: int) -> list[dict[str, Any]]:
    result = cur.execute("""--sql
        select *
        from kinds
        where division_id=?""", (divisionsId,)).fetchall()
    return dateConverter(result)


def getResponsesByThreadId(cur: sqlite3.Cursor, threadId):
    result = cur.execute("""--sql
        select *
        from responses
        where thread_id=?""", (threadId,)).fetchall()
    return dateConverter(result)


def addThread(cur: sqlite3.Cursor, title: str, kindId: int):
    cur.execute("""--sql
        insert into threads(title,kind_id,created_at)
        values(?,?,?)""", (title, kindId, datetime.now()))
    result = cur.execute("""--sql
        select max(id)
        as max
        from threads""").fetchone()["max"]
    return dateConverter(result)


def addResponse(cur: sqlite3.Cursor, content: str, threadId: int):
    cur.execute("""--sql
        insert into responses(content,thread_id,created_at)
        values(?,?,?)""", (content, threadId, datetime.now()))
