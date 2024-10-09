from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
from features.db import getPosts, setPost, dictFactory, getPostCount
from features.time_handler import generateTimeCaption

app = Flask(__name__)

path = "db.sqlite3"
con = sqlite3.connect(database=path, check_same_thread=False)
con.row_factory = dictFactory
cur = con.cursor()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        data = {"posts": [],"post_count":getPostCount(cur)}
        data["posts"] = [dict(id=i["id"], content=i["content"], created_at=generateTimeCaption(
            i["created_at"]))for i in getPosts(cur)]
        print(getPostCount(cur))
        return render_template("index.html", data=data)
    else:
        content = request.form.get("content")
        setPost(cur, content)
        con.commit()
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
