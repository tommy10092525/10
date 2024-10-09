from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)
path = "db.sqlite3"
cur = sqlite3.connect(database=path, check_same_thread=False)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        data = {"posts": []}
        result = cur.execute(
            "select content,created_at from posts limit 100").fetchall()
        data["posts"] = [dict(content=item[0], created_at=item[1])
                         for item in result]
        return render_template("index.html", data=data)
    else:
        content = request.form.get("content")
        cur.execute("insert into posts(content,created_at) values(?,?)",
                    (content, datetime.now()))
        cur.commit()
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
