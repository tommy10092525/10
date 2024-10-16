from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import features.db as db
from pprint import pprint

app = Flask(__name__)
path = "db.sqlite3"
con = sqlite3.connect(database=path, check_same_thread=False)
# con.row_factory = db.dictFactory
cur = con.cursor()


@app.route("/", methods=["GET"])
def index():
    data = dict(threads=[],head=[])
    data["threads"]=dict(db.supabase.table("threads").select("*,children(name)").limit(10).execute())["data"]
    for parent in dict(db.supabase.table("parents").select("*").execute())["data"]:
        childCountPairs=[]
        children=dict(db.supabase.table("children").select("*").execute())["data"]
        for child in children:
            childCountPairs.append(dict(child=child,count=dict(db.supabase.table("children").select("*",count="exact",head=True).execute())["count"]))
        data["head"].append(dict(parent=parent,childCountPairs=childCountPairs))
    pprint(data)
    return render_template("index.html", data=data)

@app.route("/child/<int:child_id>",methods=["GET","POST"])
def threads(child_id):
    if request.method=="GET":
        data=dict(child=dict(db.supabase.table("children").select("*").eq("id",child_id).execute())["data"][0]
            ,threads=dict(db.supabase.table("threads").select("*").eq("child_id",child_id).execute())["data"]
        )
        data["threads_count"]=len(data["threads"])
        pprint(data)
        return render_template("threads.html",data=data)
    else:
        title=request.form["title"]
        db.supabase.table("threads").insert(dict(title=title,child_id=child_id)).execute()
        return redirect(f"/child/{child_id}")

@app.route("/thread/<int:thread_id>",methods=["GET","POST"])
def thread(thread_id):
    if request.method=="GET":
        data=dict(thread=dict(db.supabase.table("threads").select("*").eq("id",thread_id).execute())["data"][0]
            ,responses=dict(db.supabase.table("responses").select("*").eq("thread_id",thread_id).execute())["data"])
        pprint(data)
        return render_template("thread.html",data=data)
    else:
        content=request.form["content"]
        db.supabase.table("responses").insert(dict(content=content,thread_id=thread_id)).execute()
        return redirect(f"/thread/{thread_id}")
        
        
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",port=51565)
