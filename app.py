from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
from features.db import get_posts, set_post, dict_factory, get_post_count
from features.time_handler import generate_caption

app = Flask(__name__)

path = "db.sqlite3"
con = sqlite3.connect(database=path, check_same_thread=False)
con.row_factory = dict_factory
cur = con.cursor()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        data = {"posts": []}
        data["posts"] = [dict(id=i["id"], content=i["content"], created_at=generate_caption(
            i["created_at"]))for i in get_posts(cur)]
        print(get_post_count(cur))
        return render_template("index.html", data=data)
    else:
        content = request.form.get("content")
        set_post(cur, content)
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
