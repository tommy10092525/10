import sqlite3
from datetime import datetime
from typing import Any
from features.time_handler import generateTimeCaption

# 取得した―データのカラムにcreated_at含まれている場合、datetime.datetime型に変換する。
def dateConverter(result: list[dict[str, str]] | dict[str, str]) -> list[dict[str, str]]|dict[str,str]:
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


def getThreadById(cur: sqlite3.Cursor, id: int) -> list[dict[str, str]] | dict[str, str]:
    result = cur.execute("""--sql:
        select *
        from threads
        where id=?""", (id,)).fetchone()
    return dateConverter(result)


def getThreadsWithKindId(cur: sqlite3.Cursor) -> list[dict[str, str]] | dict[str, str]:
    result = cur.execute("""--sql
        select
            threads.id as thread_id,
            threads.title as thread_title,
            threads.created_at as thread_created_at,
            kinds.name as kind_name,
            kinds.id as kind_id
        from threads
        inner join kinds
        on threads.kind_id=kinds.id
        order by threads.created_at desc
        limit 10""").fetchall()

    return dateConverter(result)


def getThreadsByKindId(cur: sqlite3.Cursor, kindId: int) -> list[dict[str, str]]:
    result = cur.execute("""--sql
        select *
        from threads
        where kind_id=?
        order by created_at desc
        limit 100""", (kindId,)).fetchall()
    return dateConverter(result)


def getThreadCountByKindId(cur:sqlite3.Cursor,kindId:int) -> str | None:
    result=cur.execute("""--sql:
        select count(*)
        as count
        from threads
        where kind_id=?""",(kindId,)).fetchone()["count"]
    if type(result) is int:
        return result
    else:
        return None


def getDivisions(cur: sqlite3.Cursor) -> list[dict[str, str]]:
    result = cur.execute("""--sql
        select *
        from divisions""").fetchall()
    return dateConverter(result)

def getKindById(cur:sqlite3.Cursor,id) -> list[dict[str, str]] | dict[str, str]:
    result=cur.execute("""--sql
        select *
        from kinds
        where id=?""",(id,)).fetchone()
    return dateConverter(result)

def getKindsByDivisionId(cur: sqlite3.Cursor, divisionsId: int) -> list[dict[str, str]]:
    result = cur.execute("""--sql
        select *
        from kinds
        where division_id=?""", (divisionsId,)).fetchall()
    return dateConverter(result)


def getKindCountById(cur:sqlite3.Cursor,id:int) -> int | None:
    result=cur.execute("""--sql
        select count(*)
        as count
        from threads
        where kind_id=?""",(id,)).fetchone()["count"]
    if type(result) is int:
        return result
    else:
        return None


def getResponsesByThreadId(cur: sqlite3.Cursor, threadId) -> list[dict[str, str]] | dict[str, str]:
    result = cur.execute("""--sql
        select *
        from responses
        where thread_id=?""", (threadId,)).fetchall()
    return dateConverter(result)


def addThread(cur: sqlite3.Cursor, title: str, kindId: int) -> int | None:
    cur.execute("""--sql
        insert into threads(title,kind_id,created_at)
        values(?,?,?)""", (title, kindId, datetime.now()))
    threadId = cur.execute("""--sql
        select max(id)
        as max
        from threads""").fetchone()["max"]
    if type(threadId) is int:
        return threadId
    else:
        return None


def addResponse(cur: sqlite3.Cursor, content: str, threadId: int):
    cur.execute("""--sql
        insert into responses(content,thread_id,created_at)
        values(?,?,?)""", (content, threadId, datetime.now()))
    responseId=cur.execute("""--sql
        select max(id)
        as max
        from responses""").fetchone()["max"]
    if type(responseId) is int:
        return responseId
    else:
        return None
