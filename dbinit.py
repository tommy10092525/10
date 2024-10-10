import sqlite3
from features.db import dictFactory
from datetime import datetime
import os

if __name__ == "__main__":
    path = "db.sqlite3"
    os.remove(path)
    
    con = sqlite3.connect(database=path, check_same_thread=False)
    con.row_factory = dictFactory
    cur = con.cursor()
    cur.execute("""--sql
        CREATE TABLE
        divisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name STRING,
            created_at DATETIME
        )""")
    cur.execute("""--sql
        CREATE TABLE
        kinds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name STRING,
            division_id INTEGER REFERENCES divisions,
            created_at DATETIME
        )""")
    cur.execute("""--sql
        CREATE TABLE
        threads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title STRING,
            kind_id INTEGER,
            created_at DATETIME
        )""")
    cur.execute("""--sql
        CREATE TABLE
        responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content STRING,
            thread_id INTEGER,
            created_at DATETIME
        )""")
    d={
        "学校生活":["天候","交通","課外活動"],
        "授業":["講義情報","履修登録"],
        "学習":["勉強","資格取得"],
        "その他":["就活","ゼミ","その他"]}
    for i in d.keys():
        cur.execute("""--sql
            INSERT INTO divisions(name,created_at)
            VALUES(?,?)""",(i,datetime.now()))
        for j in d[i]:
            # 直近のdivisionのidを取得
            m=cur.execute("""--sql
                SELECT max(id) AS max
                FROM divisions""").fetchone()["max"]
            cur.execute("""--sql
                INSERT INTO kinds(name,division_id,created_at)
                VALUES(?,?,?)""",(j,m,datetime.now()))
    con.commit()
    con.close()
