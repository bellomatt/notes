#!python
# -*- coding:utf-8 -*-
"""
公用函数(数据库处理) oracle_util.py 的测试
Created on 2019/8/1
Updated on 2019/8/2
@author: Holemar
"""
import os
import logging
import unittest
import time, datetime

from __init__ import *
from libs_my import oracle_util


def test_init(DB_CONFIG):
    """测试前的初始化数据库表
    :param DB_CONFIG:数据库配置
    """
    oracle_util.set_conn(DB_CONFIG)
    assert oracle_util.ping()

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
        self.assertTrue(self.db.ping())

    def tearDown(self):
        """销毁"""
        logging.warning(u'%s 类清空数据表,避免影响别的测试用例。。。', self.class_name)
        self.assertTrue(self.db.ping())
        self.db.execute("TRUNCATE TABLE t_test_table")
        result = self.db.select('select * from t_test_table')
        self.assertEqual(len(result), 0)
        super(OracleToolsTest, self).tearDown()

    def test_insert_select_get(self):
        # 插入一条
        logging.warning('execute 测试')
        rows = self.db.execute("insert into t_test_table(user_id, playlist_id, status) values(1, 1, 'inactive')")
        self.assertEqual(rows, 1, 'execute 新增 返回值不合格')

        logging.warning('select 测试')
        result = self.db.select('select * from t_test_table')
        self.assertTrue(isinstance(result, (tuple, list)), 'select 返回类型不合格')
        self.assertEqual(len(result), 1)
        self.assertTrue(isinstance(result[0], dict))
        self.assertEqual(result[0].get('PLAYLIST_ID'), 1)
        self.assertEqual(result[0].get('STATUS'), 'inactive')

        logging.warning('get 测试')
        result = self.db.get('select * from t_test_table')
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(result.get('PLAYLIST_ID'), 1)
        self.assertEqual(result.get('STATUS'), 'inactive')

        logging.warning('execute 插入时间 测试')
        rows = self.db.execute("INSERT INTO t_test_table(user_id, playlist_id,status,update_date) VALUES (2, :playlist_id, :status, :update_date)",
                               {'status': 'active', 'playlist_id': 66, 'update_date': datetime.datetime.now()})
        self.assertEqual(rows, 1)

        # 不支持 time 类型及 字符串类型
        rows = self.db.execute("INSERT INTO t_test_table(user_id, playlist_id,status,update_date) VALUES (3, :playlist_id, :status, :update_date)",
                               {'status': 'inactive', 'playlist_id': 55, 'update_date': datetime.date.today()})
        self.assertEqual(rows, 1)

        logging.warning('execute 插入中文 测试')
        rows = self.db.execute("INSERT INTO t_test_table(user_id, playlist_id, circle_code) VALUES (4, :playlist_id, :circle_code)",
                               {'playlist_id': 24, 'circle_code': '中文字符'})
        self.assertEqual(rows, 1, 'execute 插入中文 返回值不合格')
        result = self.db.get('select * from t_test_table where user_id=:1', 4)
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(result.get('CIRCLE_CODE'), '中文字符')

        logging.warning('select 测试')
        result = self.db.select('select * from t_test_table')
        self.assertTrue(isinstance(result, (tuple, list)))
        self.assertEqual(len(result), 4)
        self.assertTrue(isinstance(result[0], dict))

    def test_rowid_select(self):
        # 获取 rowid
        logging.warning('execute 获取 rowid 测试')
        now = datetime.datetime.now()
        rowid = self.db.execute("insert into t_test_table(user_id, status, playlist_id, last_use_time) values(:1, :2, :3, :4)", (4, 'active', 1011, now))
        self.assertEqual(rowid, 1)

        rowid = self.db.execute("insert into t_test_table(user_id, status, playlist_id, last_use_time) values(5, :status, :playlist_id, :last_use_time)",
                                {'status': 'active', 'playlist_id': 1011, 'last_use_time': now})
        self.assertEqual(rowid, 1)

        rowid = self.db.execute("insert into t_test_table(user_id, status, playlist_id, last_use_time) values(6, :1, :2, :3)", ('active', 1011, now))
        self.assertEqual(rowid, 1)

        rows = self.db.execute("insert into t_test_table(user_id, playlist_id, status, last_use_time) values(7, 1, 'inactive', to_date('2019-07-28 13:54:11', 'yyyy-mm-dd hh24:mi:ss'))")
        self.assertEqual(rows, 1)

        result = self.db.select('select * from t_test_table')
        self.assertEqual(len(result), 4)

        # 查询参数
        logging.warning('select 参数测试')
        result = self.db.select('select * from t_test_table where playlist_id=:1', [1011])
        self.assertEqual(len(result), 3)

        result = self.db.select("SELECT * FROM t_test_table WHERE status=:status AND playlist_id=:playlist_id",
                                param={'status': 'active', 'playlist_id': 1})
        self.assertEqual(len(result), 0)

        result = self.db.select("SELECT * FROM t_test_table WHERE status=:1 AND playlist_id=:2", param=['active', 1011])
        self.assertEqual(len(result), 3)

        # fetchone 指定查询结果返回数量
        result = self.db.select("SELECT * FROM t_test_table ")
        self.assertEqual(len(result), 4)
        result = self.db.select("SELECT * FROM t_test_table ", fetchone=2)
        self.assertEqual(len(result), 2)
        # True 与 1 的区分
        result = self.db.select("SELECT * FROM t_test_table ", fetchone=True)
        self.assertTrue(isinstance(result, dict))
        result = self.db.select("SELECT * FROM t_test_table ", fetchone=1)
        self.assertTrue(isinstance(result, (list, tuple)))
        self.assertEqual(len(result), 1)
        # False 与 0 的区分
        result = self.db.select("SELECT * FROM t_test_table ", fetchone=0)
        self.assertEqual(len(result), 4)
        result = self.db.select("SELECT * FROM t_test_table ", fetchone=False)
        self.assertEqual(len(result), 4)

    def test_executemany(self):
        # executemany
        logging.warning('executemany 测试')
        rows = self.db.executemany("INSERT INTO t_test_table(user_id, circle_code,playlist_id) VALUES (:1, :2, :3)",
                                   [(21, u"a'e''呵呵", 11), (22, 'a', 12), (23, 'a', 13)])
        self.assertEqual(rows, 3, 'executemany返回值不合格')
        result = self.db.select('select * from t_test_table where circle_code=:1', 'a')
        self.assertEqual(len(result), 2)
        result = self.db.select('select * from t_test_table where circle_code=:1', '-')
        self.assertEqual(len(result), 0)

        rows = self.db.executemany("INSERT INTO t_test_table(user_id, playlist_id,status,update_date) VALUES (:user_id, :playlist_id, :status, :update_date)",
                                   [{'user_id': 8, 'status': 'inactive', 'playlist_id': 55, 'update_date': datetime.date.today()},
                                    {'user_id': 9, 'status': 'active', 'playlist_id': 66, 'update_date': datetime.datetime.now()}])
        self.assertEqual(rows, 2)

        result = self.db.select('select * from t_test_table where circle_code=:1', '-')
        self.assertEqual(len(result), 2)

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
        self.assertEqual(len(result), 4)

    def test_doc(self):
        # 每个变量都有文档
        logging.warning('函数文档 测试')
        functions = self.db.__all__
        # logging.warning(functions)
        for function in functions:
            if function.startswith('_'): continue
            self.assertTrue(bool(getattr(self.db, function).__doc__), '%s函数没有文档' % function)


class Test_Atom1(OracleToolsTest):
    db = None

    def setUp(self):
        u"""初始化"""
        self.class_name = self.__class__.__name__
        logging.info(u'%s 类的 %s 函数测试开始...', self.class_name, self._testMethodName)
        self.db = oracle_util.Atom()
        assert self.db.ping()

    def tearDown(self):
        u"""销毁"""
        logging.info(u'%s 类清空数据表,避免影响别的测试用例。。。', self.class_name)
        assert self.db.ping()
        self.db.execute("TRUNCATE TABLE t_test_table")
        result = self.db.select('select * from t_test_table')
        assert len(result) == 0

        self.db.dispose()
        self.db = None
        logging.info(u'%s 类的 %s 函数测试完毕。。。\r\n', self.class_name, self._testMethodName)

    def test_doc(self):
        # 每个变量都有文档
        logging.warning('Atom 文档 测试')
        functions = dir(oracle_util.Atom)
        # logging.warning(functions)
        for function in functions:
            if function.startswith('_'): continue
            # logging.warning("%s.__doc__: %s" % (function, getattr(oracle_util.Atom, function).__doc__))
            assert bool(getattr(oracle_util.Atom, function).__doc__)

    def test_threads(self):
        # 异步 测试
        logging.warning('Atom 异步测试, 此功能已去掉, 故无法测试')

    def test_rollback(self):
        logging.warning('Atom rollback 测试')
        # 插入一条
        rows = self.db.execute("insert into t_test_table(user_id, playlist_id, status) values(1101, 1, 'inactive')")
        assert rows == 1
        # 类内查询
        result = self.db.select('select * from t_test_table')
        assert len(result) == 1
        # 类外查询
        result = oracle_util.select('select * from t_test_table')
        assert len(result) == 0
        # 回滚
        self.db.rollback(dispose=False)
        # 类外查询
        result = oracle_util.select('select * from t_test_table')
        assert len(result) == 0

    def test_commit(self):
        logging.warning('Atom commit 测试')
        # 插入一条
        rows = self.db.execute("insert into t_test_table(user_id, playlist_id, status) values(:1, :2, :3)", (1102, 1, 'inactive'))
        assert rows == 1
        # 类内查询
        result = self.db.select('select * from t_test_table where playlist_id=:1', 1)
        assert len(result) == 1
        # 类外查询
        result = oracle_util.select('select * from t_test_table where playlist_id=:playlist_id', {'playlist_id': 1})
        assert len(result) == 0
        # 提交
        self.db.commit(dispose=False)
        # 类外查询
        result = oracle_util.select('select * from t_test_table')
        assert len(result) == 1


class Test_Atom2(unittest.TestCase):
    # 原子操作类 Atom 的测试2:连接多个数据库
    def test_Atom2(self):
        fail = False
        try:
            mydb = oracle_util.Atom(**{
                 'host': '127.1.1.3',
                 'port': '1521',
                 'user': 'root',
                 'password': 'keepc@2014..',
                 'sid': 'test',
                 })
            assert mydb.ping()
        except:
            fail = True
            logging.warning('Atom连接不上,测试通过, 上面报错是必须的。。。')
        assert fail


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
