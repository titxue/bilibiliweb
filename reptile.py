# -*- coding:utf8 -*-
"""
Xiaoniao
"""


import time
import requests
from bili.sqlite_bili import UseSqlite
from bili.thread_bili import Mythread,lock

class Mydata(object):
    '''
    bilibili视频数据
    gethtmltext发送get请求
    getvideo获取bilibili视频数据
    '''
    def __init__(self):
        self.data = "data"

    # 发送GET请求
    def getHtmlText(self,url, datatype=False, headers=None,):
        try:
            r = requests.get(url, headers, timeout=30)
            # 如果状态码不是200 则应发HTTOError异常
            r.raise_for_status()
            # 设置正确编码方式
            r.encoding = r.apparent_encoding
            if datatype == True:
                return r.text
            else:
                return r.json()
        except:
            return "发现问题"
    
    #解析数据
    def getVideo(self,url):
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        videos = self.getHtmlText(url,headers=headers)
        #print(videos)
        #time.sleep(0.1)
        try:
            data = videos["data"]
            # print(data)
            if videos["code"] == 0:
                video = [
                    data['aid'],  # 视频编号
                    data['title'],  # 视频标题
                    data['stat']['view'],  # 播放数
                    data['stat']['danmaku'],  # 弹幕数
                    data['stat']['reply'],  # 回复数
                    data['stat']['favorite'],  # 收藏数
                    data['stat']['coin'],  # 硬币数
                    data['stat']['share'],  # 转发数
                    data['stat']['like'],  # 好评数
                    data['stat']['dislike'],  # 差评数
                    data['desc'],  # 简介
                    data['tname'],  # 分类
                    data['owner']['mid'],  # 作者id
                    data['owner']['name'],  # 作者昵称
                ]
                return video

        except:
            pass


#写入数据到数据库
def write_sqlite(id):

    sql1 = """create table if not exists bili_video (
                            b_aid int primary key,
                            b_title text,
                            b_view int,
                            b_danmaku int,
                            b_reply int,
                            b_favorite int,
                            b_coin int,
                            b_share int,
                            b_like int,
                            b_dislike int,
                            b_desc text,
                            b_tname text,
                            b_mid int,
                            b_name text
                            )"""

    sql2= """insert into bili_video(b_aid,
                                        b_title,
                                        b_view,
                                        b_danmaku,
                                        b_reply,
                                        b_favorite,
                                        b_coin,
                                        b_share,
                                        b_like,
                                        b_dislike,
                                        b_desc,
                                        b_tname,
                                        b_mid,
                                        b_name) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
    m = Mydata()
    db = UseSqlite("bilibili.db")
    db.execute("DROP TABLE IF EXISTS b_video")
    db.execute(sql1)
    url = "https://api.bilibili.com/x/web-interface/view?aid={}".format(id)
    result = m.getVideo(url)
    if result == None:
        pass
    else:
        try:
            db.execute(sql2, result)
            with open("Real_bilibili_id.txt","a+") as f:
                f.write("{aid},".format(aid=result[0]))
            # print(result)
        except:
            pass

#添加线程锁
def multi(id):
    write_sqlite(id)
    # if lock.acquire():
            #加锁爬的太慢 废弃
            #重新启用把需要加锁的添加到这里
    #     lock.release()
        
#主函数
def main():
    aid = []
    maxs = [0]
    times = time.time() #记录初始执行时间
    while True:
        for i in range(max(maxs),max(maxs)+2000):
            aid.append(i)
        maxs.append(max(aid))
        mt = []
        for x in aid:
            t = Mythread(multi,(x),"") #创建线程
            # t.start()
            mt.append(t) #添加到线程队列
            
        for m in mt:
            m.start() #启动线程

        for m in mt: 
            m.join() #等待进程队列里面的进程结束
        print("运行时间：{}".format(time.time()-times)) #打印开始到现在执行时间
        aid.clear()
#入口
if __name__ == "__main__":
    lock = lock() #可以注释掉
    main()

    
