#!python
# -*- coding:utf-8 -*-
"""
公用函数(oracle数据库的操作)
Created on 2019/7/31
Updated on 2019/7/31
@author: Holemar

依赖第三方库:
    cx_Oracle==7.2.1

使用前必须先设置oracle数据库的连接
"""
import os
import sys
import time
import logging

os.environ['NLS_LANG'] = os.environ.get('NLS_LANG') or 'SIMPLIFIED CHINESE_CHINA.UTF8'  # 防止中文乱码问题
import cx_Oracle as oracle


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    basestring = unicode = str
    long = int


__all__ = ('set_conn', 'get_conn', 'ping', 'select', 'get', 'execute', 'execute_list', 'executemany')

# 数据库连接
db_conn = None

# 请求默认值
CONFIG = {
    'host': '127.0.0.1',
    'port': '1521',
    'user': 'system',
    'password': 'oracle',
    'sid': 'xe',
}


def set_conn(conn_config):
    """
    设置数据库连接,使用前必须先设置
    :param {dict} conn_config: redis数据库连接配置
    :return {bool}: 是否成功连接上数据库,失败时会报异常
    """
    global CONFIG
    global db_conn
    CONFIG.update(conn_config)
    try:
        # 打开数据库连接
        db_conn = oracle.connect('{user}/{password}@{host}:{port}/{sid}'.format(**CONFIG))
    except Exception as e:
        logging.error('oracle connection error:%s', e, exc_info=True)
        raise
    return True


def ping(**kwargs):
    """
    探测oracle数据库是否连上
    :return {bool}: 能连上则返回True, 否则报异常
    """
    try:
        conn = kwargs.get('conn', None)
        cursor = kwargs.get('cursor', None)
        if not conn:
            conn, cursor = get_conn()
        conn.ping()
        return True
    finally:
        close_conn(conn, cursor)


def get_conn(repeat_time=3):
    """
    获取数据库连接
    :return {tuple}: conn, cursor
    """
    conn = None
    cursor = None
    global db_conn, CONFIG
    # 允许出错时重复提交多次,只要设置了 repeat_time 的次数
    while repeat_time > 0:
        try:
            if db_conn is None:
                db_conn = oracle.connect('{user}/{password}@{host}:{port}/{sid}'.format(**CONFIG))
            if db_conn:
                conn = db_conn
                # 尝试连接数据库
                conn.ping()
                cursor = oracle.Cursor(conn)
                return conn, cursor
        # 数据库连接,默认8小时没有使用会自动断开,这里捕获这异常
        except Exception as e:
            repeat_time -= 1
            logging.error('oracle connection error:%s', e, exc_info=True)
            try:
                if cursor:cursor.close()
            except:pass
            try:
                if conn:conn.close()
            except:pass
    return conn, cursor


def close_conn(conn=None, cursor=None):
    """
    关闭数据库连接
    """
    # 每次请求都关闭连接的话,在多线程高并发时会导致报错,性能也会下降。
    # 这里不关闭连接,每次使用时探测可用性,并捕获连接超时断开的异常
    try:
        # if cursor:cursor.close()
        pass
    except:pass
    try:
        # if conn:conn.close()
        pass
    except:pass


def _init_execute(func):
    """处理获取数据库连接、超时记日志问题"""
    def wrapper(*args, **kwargs):
        start_time = time.time()

        # 数据库连接(没有则获取, 有则不用)
        conn = kwargs.get('conn', None)
        cursor = kwargs.get('cursor', None)
        if conn is None and cursor is None:
            conn, cursor = get_conn()
            kwargs['conn'] = conn
            kwargs['cursor'] = cursor
        # 参数处理
        if args and len(args) >= 2:
            if not isinstance(args[1], (tuple, list, dict)):
                args = list(args)
                args[1] = [args[1]]
        elif 'param' in kwargs:
            param = kwargs.get('param')
            if param and not isinstance(param, (tuple, list, dict)):
                kwargs['param'] = [param]
        # 执行SQL
        method = kwargs.pop('function', None) or func
        result = method(*args, **kwargs)
        # 关闭数据库连接
        close_conn(conn, cursor)
        # 判断运行时间是否太长
        use_time = float(time.time() - start_time)
        log_param = str((args, kwargs.get('param', '')))
        # 为了更方便阅读,执行SQL的结果如果很短,则将它提前写
        logging.info(u"SQL, 耗时 %.4f 秒, 执行:%s, 返回:%s", use_time, log_param, result)
        return result

    wrapper.__doc__ = func.__doc__
    return wrapper


def make_dict_factory(cursor):
    """
    将查询返回的 tuple 结果转换成 dict 结果
    :param cursor: 数据库连接的 Cursor Object
    :return:
    """
    column_names = [d[0] for d in cursor.description]
    return lambda *args: dict(zip(column_names, args))


@_init_execute
def select(sql, param=None, fetchone=False, **kwargs):
    """
    查询SQL结果
    :param {string} sql: 要查询的 SQL 语句，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
    :param {tuple|list|dict} param: 可选参数，条件列表值
    :param {bool|int} fetchone: 为 True则只返回第一条结果, 为False则返回所有的查询结果, 为 int 类型则返回指定的条数
    :param conn: 数据库连接(有传则使用传来的,没有则自动获取,便于使用事务)
    :param cursor: 数据库连接的 Cursor Object(有传则使用传来的,没有则自动获取,便于使用事务)
    :return {tuple<dict> | dict}:
        当 参数 fetchone 为 True 时, 返回SQL查询的结果(dict类型),查不到返回 None
        当 参数 fetchone 为 False 时, 返回SQL查询结果集,查不到时返回空的 tuple
    @example
        results = select("SELECT * FROM product_log WHERE flag=:1 AND v=:2", param=('n','1.2.0',))
        或者 results = select("SELECT * FROM product_log WHERE flag=:flag AND v=:v", param={'flag':'n', 'v':'1.2.0'})
    """
    try:
        result = None
        cursor = kwargs.get('cursor', None)
        if param is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, param)
        cursor.rowfactory = make_dict_factory(cursor)
        # count = cursor.rowcount  # 只有执行了 fetchall 之后才知道有多少行，没法预先判断
        # 查不到时
        # if count <= 0:
        #     return None if fetchone is True else tuple()
        # 只返回1行(True 与 1 一样)
        if fetchone is True:
            return cursor.fetchone() or None
        # 返回所有
        elif fetchone is False:
            return cursor.fetchall()
        # 返回指定行数
        elif isinstance(fetchone, (int, long)):
            return cursor.fetchmany(fetchone)
        else:
            return cursor.fetchall()
    except Exception as e:
        logging.error("查询失败:%s, SQL:%s, %s, 返回:%s", e, sql, param, result, exc_info=True)
        return False


def get(sql, param=None, **kwargs):
    """
    查询SQL结果
    :param {string} sql: 要查询的 SQL 语句，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
    :param {tuple|list|dict} param: 可选参数，条件列表值
    :param conn: 数据库连接(有传则使用传来的,没有则自动获取,便于使用事务)
    :param cursor: 数据库连接的 Cursor Object(有传则使用传来的,没有则自动获取,便于使用事务)
    :return {dict}: 返回SQL查询的结果(dict类型),查不到返回 None,执行有异常时返回 False
    @example
        results = get("SELECT * FROM product_log WHERE flag=:1 AND v=:2", param=('n','1.2.0',))
        或者 results = get("SELECT * FROM product_log WHERE flag=:flag AND v=:v", param={'flag':'n', 'v':'1.2.0'})
    """
    kwargs.pop('fetchone', None)
    return select(sql, param=param, fetchone=True, **kwargs)


@_init_execute
def execute(sql, param=None, clash=1, transaction=True, **kwargs):
    """
    执行SQL语句(增删改操作)
    :param {string} sql: 要执行的 SQL 语句，如果有执行条件，请只指定条件列表，并将条件值使用参数[param]传递进来
    :param {tuple|list|dict} param: 可选参数，条件列表值
    :param {bool} transaction: 为  True 则开启事务(成功会commit,失败会rollback),为 False 则不开启事务(默认开启)
    :param {int} clash: 发生主键冲突,或者唯一键冲突时的返回值,默认1
    :param conn: 数据库连接(有传则使用传来的,没有则自动获取,便于使用事务)
    :param cursor: 数据库连接的 Cursor Object(有传则使用传来的,没有则自动获取,便于使用事务)
    :return {int}: 返回执行SQL影响的行数(插入则返回新增的主键值/影响行数),执行有异常时返回 -1
    @example
        row = execute("INSERT INTO product_log(uid,v) VALUES (:1, :2)", (20125412, '1.2.3', ))
        或者 row = execute("INSERT INTO product_log (uid,v) VALUES (:uid, :v)", {'uid':20125412, 'v':'1.2.3'})
    """
    try:
        conn = kwargs.get('conn', None)
        cursor = kwargs.get('cursor', None)
        # 开启事务
        # if transaction: conn.autocommit(0)
        if param is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, param)
        row = cursor.rowcount
        if transaction:
            conn.commit()
        return row
    # 主键冲突,或者唯一键冲突,重复insert,忽略错误
    except oracle.IntegrityError:
        logging.warning(u"主键冲突:%s, %s", sql, param)
        return clash
    except Exception as e:
        logging.error("执行失败:%s, SQL:%s, 参数:%s", e, sql, param, exc_info=True)
        if transaction and conn:
            conn.rollback()
        return -1


@_init_execute
def executemany(sql, param, clash=1, transaction=True, **kwargs):
    """
    执行SQL语句(增删改操作), 同一个SQL语句,执行不同的多个参数
    :param {string} sql: 要执行的 SQL 语句，如果有执行条件，请只指定条件列表，并将条件值使用参数[param]传递进来
    :param {tuple|list|dict} param: 可选参数，条件列表值
    :param {int} clash: 发生主键冲突,或者唯一键冲突时的返回值,默认1
    :param {bool} transaction: 为  True 则开启事务(成功会commit,失败会rollback),为 False 则不开启事务(默认开启)
    :param conn: 数据库连接(有传则使用传来的,没有则自动获取,便于使用事务)
    :param cursor: 数据库连接的 Cursor Object(有传则使用传来的,没有则自动获取,便于使用事务)
    :return {int}: 返回执行SQL影响的行数(插入则返回新增的主键值/影响行数),执行有异常时返回 -1
    @example
        row = executemany("INSERT INTO product_log(uid,v) VALUES (:1, :2)", [(20125412, '1.2.3', ),(20125413, '2.0.3', ),(56721, '2.32.3', )])
        或者 row = executemany("INSERT INTO product_log (uid,v) VALUES (:uid, :v)", [{'uid':20125412, 'v':'1.2.3'},{'uid':56721, 'v':'2.32.3'}])
    """
    try:
        conn = kwargs.get('conn', None)
        cursor = kwargs.get('cursor', None)
        # 开启事务
        # if transaction: conn.autocommit(0)
        if param is None:
            cursor.executemany(sql)
        else:
            cursor.executemany(sql, param)
        if transaction:
            conn.commit()
        row = cursor.rowcount
        return row
    # 主键冲突,或者唯一键冲突,重复insert,忽略错误
    except oracle.IntegrityError:
        logging.warning("主键冲突:%s, %s", sql, param)
        return clash
    except Exception as e:
        logging.error("执行失败:%s, SQL:%s, 参数:%s", e, sql, param, exc_info=True)
        if transaction and conn:
            conn.rollback()
        return -1


def execute_list(sql_list, must_rows=False, transaction=True, **kwargs):
    """
    执行多条SQL语句，并且是一个原子事件(任何一条SQL执行失败，或者返回结果为0，都会全体回滚)
    :param {list<tuple<string,dict>>} sql_list: 形式为 [(sql1, param1),(sql2, param2),(sql3, param3),...]
    :param {bool} must_rows: 为 True则要求每个SQL语句影响的行数都必须大于1,影响行数为0会认为执行出错。为False则允许执行影响数为0
    :param {bool} transaction: 为  True 则开启事务(成功会commit,失败会rollback),为 False 则不开启事务(默认开启)
    :param conn: 数据库连接(有传则使用传来的,没有则自动获取,便于使用事务)
    :param cursor: 数据库连接的 Cursor Object(有传则使用传来的,没有则自动获取,便于使用事务)
    :return {int}: 返回执行SQL影响的行数,执行有异常时返回 -1
    """
    conn = None
    cursor = None
    try:
        # 数据库连接(没有则获取, 有则不用)
        conn = kwargs.get('conn', None)
        cursor = kwargs.get('cursor', None)
        if conn is None and cursor is None:
            conn, cursor = get_conn()
            kwargs['conn'] = conn
            kwargs['cursor'] = cursor
        # 开启事务
        # if transaction: conn.autocommit(0)
        row = 0
        for args in sql_list:
            # 取出 sql 及 参数
            if isinstance(args, (list, tuple)):
                length = len(args)
                if length == 0:
                    continue
                elif length == 1:
                    sql, param = args[0], None
                else:
                    sql, param = args[0], args[1]
            elif isinstance(args, str):
                sql, param = args, None
            else:
                raise RuntimeError('其中一条参数无法解析:%s' % args)
            this_row = execute(sql, param=param, raise_error=True, transaction=False, **kwargs)
            if must_rows and this_row <= 0:
                raise RuntimeError('其中一条执行失败,影响行数为%s, SQL:%s, %s' % (this_row, sql, param))
            row += this_row
        if transaction:
            conn.commit()
        return row
    except Exception as e:
        logging.error("执行失败:%s, SQL:%s", e, sql_list, exc_info=True)
        if transaction and conn:
            conn.rollback()
        return -1
    finally:
        close_conn(conn, cursor)

