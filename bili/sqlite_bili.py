# -*- coding:utf8 -*-
import sqlite3


class UseSqlite:
    """
    sqlite数据库操作类
    database: 数据库文件地址，例如：db/bilibili.db
    """
    _connection = None

    def __init__(self, database):
        # 连接数据库
        self._connection = sqlite3.connect(database)

    def execute(self, sql, args=[], commit=True):
        # 获取游标
        _cursor = self._connection.cursor()
        # 执行SQL获取结果

        _cursor.execute(sql, args)
        if commit:
            self._connection.commit()
        data = _cursor.fetchall()
        _cursor.close()
        return data


