from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import features.db as db
from features.db import addThread,addResponse
from pprint import pprint

app = Flask(__name__)
path = "db.sqlite3"
con = sqlite3.connect(database=path, check_same_thread=False)
con.row_factory = db.dictFactory
cur = con.cursor()


@app.route("/", methods=["GET"])
def index():
    data = dict(threads=[],head=[])
    data["threads"]=db.getThreads(cur)
    for division in db.getDivisions(cur):
        kinds=db.getKindsByDivisionsId(cur,division["id"])
        data["head"].append(dict(division=division,kinds=kinds))
    pprint(data)
    return render_template("index.html", data=data)

@app.route("/kind/<int:kind_id>",methods=["GET","POST"])
def threads(kind_id):
    if request.method=="GET":
        data=dict(threads=db.getThreadsByKindId(cur,kind_id))
        print(data)
        return render_template("threads.html",data=data)
    else:
        title=request.form["title"]
        content=request.form["content"]
        threadId=addThread(cur=cur,title=title,kindId=kind_id)
        addResponse(cur=cur,content=content,threadId=threadId)
        con.commit()
        return redirect(f"/{kind_id}")

@app.route("/thread/<int:thread_id>",methods=["GET","POST"])
def thread(thread_id):
    if request.method=="GET":
        data=dict(thread=db.getThreadById(cur,thread_id),responses=db.getResponsesByThreadId(cur,thread_id))
        return render_template("thread.html",data=data)
        
        
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
