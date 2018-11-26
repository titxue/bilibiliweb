# -*- coding:utf8 -*-
from app.main.sqlite_bili import UseSqlite
from flask import Flask,render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    db = UseSqlite("bilibili.db")
    results = db.execute("SELECT * FROM bili_video")
    posts = []
    for result in results:
        posts.append(result)
    return render_template("index.html",posts=posts)