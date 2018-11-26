# -*- coding:utf8 -*-
from app.main.sqlite_bili import UseSqlite
from flask import Flask, render_template, request
from app import app
import json

key = (
    'b_aid',
    'b_title',
    'b_view',
    'b_danmaku',
    'b_reply',
    'b_favorite',
    'b_coin',
    'b_share',
    'b_like',
    'b_dislike',
    'b_desc',
    'b_tname',
    'b_mid',
    'b_name',
)
def get_bilibili():
    try:
        db = UseSqlite('bilibili.db')
        results = db.execute('SELECT * FROM bili_video')
        datas = []
        for result in results:
            data = dict(zip(key,result))
            datas.append(data)
    except:
        print("0")
    else:
        # data=json.dumps(datas,ensure_ascii=False)
        # print(data[1:len(data)-1])
        return datas

def getpost(code,msg,count,data):
    json_data = json.dumps({'code':code,'msg':msg,'count':count,'data':data},ensure_ascii=False)
    return json_data


posts = get_bilibili()
data = getpost("0","","100",posts)
@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html')

@app.route('/api/', methods=['GET'])
def http_method_example():
    if request.method == 'GET':
        return data

