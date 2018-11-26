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
def get_bilibili(name,sql,keys):
    try:
        db = UseSqlite(name)
        results = db.execute(sql)
        datas = []
        for result in results:
            data = dict(zip(keys,result))
            datas.append(data)
    except:
        pass
    else:
        # data=json.dumps(datas,ensure_ascii=False)
        # print(data[1:len(data)-1])
        return datas
def get_data(code,msg,count,data):
    json_data = json.dumps({'code':code,'msg':msg,'count':count,'data':data},ensure_ascii=False)
    return json_data



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/bilibili')
def bilibili():

    return render_template('bilibili.html')

@app.route('/api/data', methods=['POST'])
def http_method_example():
    if request.method == 'POST':
        api_data = get_bilibili('bilibili.db','SELECT * FROM bili_video',key)
        return get_data("200","ok",len(api_data),api_data)

