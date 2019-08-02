#!python
# -*- coding:utf-8 -*-
"""
公用函数(数据库处理) oracle_util.py 的测试
Created on 2014/7/16
Updated on 2019/1/18
@author: Holemar
"""
import os
import logging
import unittest
import time, datetime

import __init__
from libs_my import oracle_util


def test_init(DB_CONFIG):
    """测试前的初始化数据库表
    :param DB_CONFIG:数据库配置
    """
    oracle_util.set_conn(DB_CONFIG)

    # 建表
    oracle_util.execute('drop table t_test_table')
    oracle_util.execute(u"""
        CREATE TABLE t_test_table(
            user_id int PRIMARY KEY NOT NULL,
            playlist_id NUMBER(10) default 0 NOT NULL,
            value NUMBER(10, 2) default 4 NOT NULL,
            circle_code VARCHAR2(18) default '-' NOT NULL,
            status VARCHAR2(10) default 'active' CHECK( status IN ('active','inactive') ),
            last_use_time DATE DEFAULT sysdate NOT NULL,
            update_date DATE default sysdate NOT NULL
        ) """)


def test_end():
    """测试结束后，删除测试表，避免遗留测试痕迹"""
    oracle_util.execute('drop table t_test_table')


class OracleToolsTest(unittest.TestCase):
    db = oracle_util

    def setUp(self):
        """初始化"""
        super(OracleToolsTest, self).setUp()
        assert self.db.ping()

    def tearDown(self):
        """销毁"""
        logging.warning(u'%s 类清空数据表,避免影响别的测试用例。。。', self.class_name)
        self.db.execute("TRUNCATE TABLE t_test_table")
        result = self.db.select('select * from t_test_table')
        assert len(result) == 0
        super(OracleToolsTest, self).tearDown()

    def test_insert_select_get(self):
        # 插入一条
        logging.warning('execute 测试')
        rows = self.db.execute("insert into t_test_table(user_id, playlist_id, status) values(1, 1, 'inactive')")
        self.assertEqual(rows, 1, 'execute 新增 返回值不合格')

        logging.warning('select 测试')
        result = self.db.select('select * from t_test_table')
        self.assertTrue(isinstance(result, (tuple, list)), 'select 返回类型不合格')
        assert len(result) == 1
        assert isinstance(result[0], dict)
        assert result[0].get('PLAYLIST_ID') == 1
        assert result[0].get('STATUS') == 'inactive'

        logging.warning('get 测试')
        result = self.db.get('select * from t_test_table')
        assert isinstance(result, dict)
        assert result.get('PLAYLIST_ID') == 1
        assert result.get('STATUS') == 'inactive'

        logging.warning('execute 插入时间 测试')
        rows = self.db.execute("INSERT INTO t_test_table(user_id, playlist_id,status,update_date) VALUES (2, :playlist_id, :status, :update_date)",
                               {'status': 'active', 'playlist_id': 66, 'update_date': datetime.datetime.now()})
        assert rows == 1

        # 不支持 time 类型及 字符串类型
        rows = self.db.execute("INSERT INTO t_test_table(user_id, playlist_id,status,update_date) VALUES (3, :playlist_id, :status, :update_date)",
                               {'status': 'inactive', 'playlist_id': 55, 'update_date': datetime.date.today()})
        assert rows == 1

        logging.warning('execute 插入中文 测试')
        rows = self.db.execute("INSERT INTO t_test_table(user_id, playlist_id, circle_code) VALUES (4, :playlist_id, :circle_code)",
                               {'playlist_id': 24, 'circle_code': '中文字符'})
        self.assertEqual(rows, 1, 'execute 插入中文 返回值不合格')
        result = self.db.get('select * from t_test_table where user_id=:1', 4)
        assert isinstance(result, dict)
        assert result.get('CIRCLE_CODE') == '中文字符'

        logging.warning('select 测试')
        result = self.db.select('select * from t_test_table')
        assert isinstance(result, (tuple, list))
        assert len(result) == 4
        assert isinstance(result[0], dict)

    def test_rowid_select(self):
        # 获取 rowid
        logging.warning('execute 获取 rowid 测试')
        now = datetime.datetime.now()
        rowid = self.db.execute("insert into t_test_table(user_id, status, playlist_id, last_use_time) values(:1, :2, :3, :4)", (4, 'active', 1011, now))
        assert rowid == 1

        rowid = self.db.execute("insert into t_test_table(user_id, status, playlist_id, last_use_time) values(5, :status, :playlist_id, :last_use_time)",
                                {'status': 'active', 'playlist_id': 1011, 'last_use_time': now})
        assert rowid == 1

        rowid = self.db.execute("insert into t_test_table(user_id, status, playlist_id, last_use_time) values(6, :1, :2, :3)", ('active', 1011, now))
        assert rowid == 1

        rows = self.db.execute("insert into t_test_table(user_id, playlist_id, status, last_use_time) values(7, 1, 'inactive', to_date('" + now.strftime('%Y-%m-%d %H:%M:%S') + "', 'yyyy-mm-dd hh24:mi:ss'))")
        assert rows == 1

        result = self.db.select('select * from t_test_table')
        assert len(result) == 4

        # 查询参数
        logging.warning('select 参数测试')
        result = self.db.select('select * from t_test_table where playlist_id=:1', [1011])
        assert len(result) == 3

        result = self.db.select("SELECT * FROM t_test_table WHERE status=:status AND playlist_id=:playlist_id",
                                param={'status': 'active', 'playlist_id': 1})
        assert len(result) == 0

        result = self.db.select("SELECT * FROM t_test_table WHERE status=:1 AND playlist_id=:2", param=['active', 1011])
        assert len(result) == 3

        # fetchone 指定查询结果返回数量
        result = self.db.select("SELECT * FROM t_test_table ")
        assert len(result) == 4
        result = self.db.select("SELECT * FROM t_test_table ", fetchone=2)
        assert len(result) == 2
        # True 与 1 的区分
        result = self.db.select("SELECT * FROM t_test_table ", fetchone=True)
        assert isinstance(result, dict)
        result = self.db.select("SELECT * FROM t_test_table ", fetchone=1)
        assert isinstance(result, (list, tuple))
        assert len(result) == 1
        # False 与 0 的区分
        result = self.db.select("SELECT * FROM t_test_table ", fetchone=0)
        assert len(result) == 4
        result = self.db.select("SELECT * FROM t_test_table ", fetchone=False)
        assert len(result) == 4

    def test_executemany(self):
        # executemany
        logging.warning('executemany 测试')
        rows = self.db.executemany("INSERT INTO t_test_table(user_id, circle_code,playlist_id) VALUES (:1, :2, :3)",
                                   [(21, u"a'e''呵呵", 11), (22, 'a', 12), (23, 'a', 13)])
        self.assertEqual(rows, 3, 'executemany返回值不合格')
        result = self.db.select('select * from t_test_table where circle_code=:1', 'a')
        assert len(result) == 2
        result = self.db.select('select * from t_test_table where circle_code=:1', '-')
        assert len(result) == 0

        rows = self.db.executemany("INSERT INTO t_test_table(user_id, playlist_id,status,update_date) VALUES (:user_id, :playlist_id, :status, :update_date)",
                                   [{'user_id': 8, 'status': 'inactive', 'playlist_id': 55, 'update_date': datetime.date.today()},
                                    {'user_id': 9, 'status': 'active', 'playlist_id': 66, 'update_date': datetime.datetime.now()}])
        assert rows == 2

        result = self.db.select('select * from t_test_table where circle_code=:1', '-')
        assert len(result) == 2

    def test_execute_list(self):
        # execute_list
        logging.warning('execute_list 测试')
        rows = self.db.execute_list([
            "insert into t_test_table(user_id, playlist_id, status) values(10, 33, 'inactive')",
            "insert into t_test_table(user_id, playlist_id, status) values(11, 44, 'inactive')"
            ], must_rows=True)
        self.assertEqual(rows, 2, 'execute_list 返回值不合格')

        rows = self.db.execute_list([
            ("insert into t_test_table(user_id, playlist_id, status) values(:1, :2, :3)", [20, 23, 'inactive']),
            ("insert into t_test_table(user_id, playlist_id, status) values(:user_id, :playlist_id, :status)",
             {'user_id': 29, 'status': 'active', 'playlist_id': 66})
                                     ], must_rows=True)
        self.assertEqual(rows, 2, 'execute_list 返回值不合格')

        result = self.db.select("SELECT * FROM t_test_table ")
        assert len(result) == 4

    def test_doc(self):
        # 每个变量都有文档
        logging.warning('函数文档 测试')
        functions = self.db.__all__
        # logging.warning(functions)
        for function in functions:
            if function.startswith('_'): continue
            self.assertTrue(bool(getattr(self.db, function).__doc__), '%s函数没有文档' % function)


if __name__ == "__main__":
    # 数据库配置
    DB_CONFIG = {
        'host': '127.0.0.1',
        'port': '1521',
        'user': 'system',
        'password': 'oracle',
        'sid': 'xe',
    }

    test_init(DB_CONFIG)  # 数据库初始化连接、建表
    unittest.main()
    test_end()  # 删除表，避免遗留测试痕迹
