from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
from features.db import dictFactory, getThreads,getDivisions,getKindsByDivisionsId
from pprint import pprint

app = Flask(__name__)
path = "db.sqlite3"
con = sqlite3.connect(database=path, check_same_thread=False)
con.row_factory = dictFactory
cur = con.cursor()


@app.route("/", methods=["GET"])
def index():
    data = dict(threads=[],head=[])
    data["threads"]=getThreads(cur)
    for division in getDivisions(cur):
        kinds=getKindsByDivisionsId(cur,division["id"])
        data["head"].append(dict(division=division,kinds=kinds))
    pprint(data)
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
