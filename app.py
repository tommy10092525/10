from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
from features.db import get_posts,set_post
from features.time_handler import generate_caption

app = Flask(__name__)

path = "db.sqlite3"
cur = sqlite3.connect(database=path, check_same_thread=False)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        data = {"posts": []}
        data["posts"] = [
            dict(content=i["content"],created_at=generate_caption(i["created_at"]))
            for i in get_posts(cur)]
        return render_template("index.html", data=data)
    else:
        content = request.form.get("content")
        set_post(cur,content)
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
