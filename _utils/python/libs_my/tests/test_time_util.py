#!python
# -*- coding:utf-8 -*-
"""
公用函数 time_util.py 的测试
Created on 2014/10/16
Updated on 2019/1/18
@author: Holemar
"""
import time
import datetime
import calendar
import unittest

from __init__ import *
from libs_my.time_util import *

class TimeUtilTest(unittest.TestCase):

    # to_string 测试
    def test_to_string(self):
        now_str = lambda: datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 测试默认值及当前时间
        assert to_string() == now_str() # 默认返回当前时间
        assert to_string(None) == now_str() # 默认返回当前时间
        assert to_string('') == now_str() # 默认返回当前时间
        assert to_string(time.time()) == now_str() # 时间戳
        assert to_string(0) == to_string(time.localtime(0)) # 时间戳为0时
        # datetime.timedelta 类型
        assert to_string(datetime.timedelta()) == to_string(0)
        assert to_string(datetime.timedelta(0, 3602)) == to_string(3602)
        assert to_string(datetime.timedelta(5, 3602)) == to_string(5*24*3600 + 3602)
        # 多种格式的日期格式
        assert to_string('2014-02-06 08:51:06') == '2014-02-06 08:51:06' # 字符串
        assert to_string('2014-2-6 8:51:06') == '2014-02-06 08:51:06' # 字符串
        assert to_string('2014/02/06') == '2014-02-06 00:00:00' # 字符串
        assert to_string('2014/2/6 23:59:59') == '2014-02-06 23:59:59' # 字符串
        assert to_string('2014/2/6 23:59') == '2014-02-06 23:59:00' # 字符串
        assert to_string('2014-2-06 23:59') == '2014-02-06 23:59:00' # 字符串
        assert to_string('2014年2月6日 23:59') == '2014-02-06 23:59:00' # 字符串
        assert to_string('2014年2月6日 23时59分') == '2014-02-06 23:59:00' # 字符串
        assert to_string('2014年02月6日 23时59分0秒') == '2014-02-06 23:59:00' # 字符串
        assert to_string('2014年2月06日 23:59:00') == '2014-02-06 23:59:00' # 字符串
        assert to_string('2014-2-6T23:59') == '2014-02-06 23:59:00' # 字符串
        assert to_string('2014-2-6T23:59:00') == '2014-02-06 23:59:00' # 字符串
        assert to_string('1900-1-1') == '1900-01-01 00:00:00' # 字符串
        assert to_string('197011') == '1970-01-01 00:00:00' # 字符串
        assert to_string('197011810') == '1970-01-01 08:01:00' # 字符串
        assert to_string('2014-2-6 下午 11:59:00') == '2014-02-06 23:59:00' # 字符串
        assert to_string('2014-2-6 下午 11:59') == '2014-02-06 23:59:00' # 字符串
        assert to_string('2014-2-6 PM 11:59:00') == '2014-02-06 23:59:00' # 字符串
        assert to_string('2014-2-6 PM 11:59') == '2014-02-06 23:59:00' # 字符串
        assert to_string('2014/02/06 下午 11:59') == '2014-02-06 23:59:00' # 字符串
        assert to_string('2014/02/06 PM 11:59:00') == '2014-02-06 23:59:00' # 字符串
        #assert to_string('2014-02/06 08:51:06') == '2014-02-06 08:51:06' # 字符串(这本应是错误格式)
        # 不同类型的参数
        test_time = datetime.datetime(2014, 2, 6, 8, 51, 6)
        assert to_string(test_time) == '2014-02-06 08:51:06' # datetime
        assert to_string(time.strptime('2014/03/25 19:05:33', '%Y/%m/%d %H:%M:%S')) == '2014-03-25 19:05:33' # time
        assert to_string(datetime.date.today()) == datetime.datetime.now().strftime('%Y-%m-%d 00:00:00') # datetime.date
        # 指定格式化输出
        assert to_string(test_time, '%Y/%m/%dxx') == '2014/02/06xx'
        assert to_string(test_time, '%Y-%m/%dxx%H+%M+%S') == '2014-02/06xx08+51+06'
        assert to_string('2014-02-06 08:51:06', '%Y/%m/%d %H:%Mxx') == '2014/02/06 08:51xx'


    # 公用测试
    def fun_test(self, fun, default_time, test_time, test_date):
        # 测试默认值及当前时间
        assert fun() == default_time() # 默认返回当前时间
        assert fun(None) == default_time() # 默认返回当前时间
        assert fun('') == default_time() # 默认返回当前时间
        assert fun(time.time()) == default_time() # 时间戳
        assert fun(0) == fun(time.localtime(0)) # 时间戳为0时
        # 测试指定时间
        assert fun('2014-02-06 08:51:06') == test_time # 字符串
        assert fun('2014/02-6 8xx51mm06::YY', '%Y/%m-%d %Hxx%Mmm%S::YY') == test_time # 格式化测试
        assert fun(datetime.datetime(2014, 2, 6, 8, 51, 6)) == test_time # datetime
        assert fun(time.strptime('2014-02-06 08:51:06','%Y-%m-%d %H:%M:%S')) == test_time # time
        assert fun(datetime.date(2014,2,6)) == test_date # datetime.date
        # 多种格式的日期格式
        assert fun('2014/02/06 08:51:06') == test_time
        assert fun('20142685106') == test_time
        assert fun('2014268516') == test_time
        assert fun('2014/2/6 8:51:6') == test_time
        assert fun('2014/2/06 08:51:6') == test_time
        assert fun('2014-02-06T08:51:06') == test_time
        assert fun('2014-02-06T08:51:06+08:00') == test_time
        assert fun('2014-02-06T08:51:06.000Z') == test_time
        assert fun('2014-02-06 AM 08:51:06') == test_time
        assert fun('2014-02-06 上午 08:51:06') == test_time
        assert fun(u'2014-02-06 上午 08:51:06') == test_time
        assert fun('2014/2/06 AM 08:51:06') == test_time
        assert fun('2014/02/06 上午 08:51:06') == test_time
        # 测试日期
        assert fun('2014-02-06') == test_date
        assert fun('2014-2-6') == test_date
        assert fun('2014/02/06') == test_date
        assert fun('2014/2/6') == test_date
        assert fun('201426') == test_date
        # datetime.timedelta 类型
        if fun == to_time:
            assert fun(datetime.timedelta())[:6] == fun(0)[:6]
            assert fun(datetime.timedelta(0, 3602))[:6] == fun(3602)[:6]
            assert fun(datetime.timedelta(5, 3602))[:6] == fun(5*24*3600 + 3602)[:6]
        else:
            assert fun(datetime.timedelta()) == fun(0)
            assert fun(datetime.timedelta(0, 3602)) == fun(3602)
            assert fun(datetime.timedelta(5, 3602)) == fun(5*24*3600 + 3602)


    # to_time 测试
    def test_to_time(self):
        now_time = time.localtime
        test_time = time.strptime('2014-02-06 08:51:06','%Y-%m-%d %H:%M:%S') # 测试时间
        test_date = time.strptime('2014-02-06','%Y-%m-%d') # 测试日期
        self.fun_test(to_time, now_time, test_time, test_date)


    # to_datetime 测试
    def test_to_datetime(self):
        now_time = datetime.datetime.now
        test_time = datetime.datetime(2014, 2, 6, 8, 51, 6) # 测试时间
        test_date = datetime.datetime(2014, 2, 6) # 测试日期
        self.fun_test(to_datetime, now_time, test_time, test_date)


    # to_date 测试
    def test_to_date(self):
        now_time = datetime.date.today
        test_time = datetime.date(2014, 2, 6) # 测试时间
        test_date = datetime.date(2014, 2, 6) # 测试日期
        self.fun_test(to_date, now_time, test_time, test_date)


    # to_timestamp 测试
    def test_to_timestamp(self):
        now_time = time.time
        test_time = time.mktime(time.strptime('2014-02-06 08:51:06','%Y-%m-%d %H:%M:%S')) # 测试时间
        test_date = time.mktime(time.strptime('2014-02-06','%Y-%m-%d')) # 测试日期
        self.fun_test(to_timestamp, now_time, test_time, test_date)


    # to_datetime_time 测试
    def test_to_datetime_time(self):
        test_time = datetime.time(12, 9, 2)
        assert to_datetime_time("12:9:2") == test_time
        assert to_datetime_time("12:09:02") == test_time
        assert to_datetime_time(test_time) == test_time
        assert to_datetime_time('0:0:0') == datetime.time()
        assert to_datetime_time(datetime.datetime(2017,9,5,15,53,2)) == datetime.time(15,53,2)
        # 没有秒
        test_time2 = datetime.time(12, 9)
        assert to_datetime_time("12:9") == test_time2
        assert to_datetime_time("12:09:00") == test_time2
        assert to_datetime_time("12:9:0") == test_time2
        assert to_datetime_time('0:0') == datetime.time()
        # 错误类型
        assert to_datetime_time(None) == None
        assert to_datetime_time('') == None
        assert to_datetime_time(12345) == None
        #assert to_datetime_time("2014-02-06 12:09:00") == None
        # datetime 类型字符串
        assert to_datetime_time('2014-02-06 08:51:06') == datetime.time(8, 51, 6)
        assert to_datetime_time('2014/02/06') == datetime.time(0, 0, 0)
        assert to_datetime_time('2014/2/6 23:59:59') == datetime.time(23, 59, 59)
        assert to_datetime_time('2014/2/6 23:59') == datetime.time(23, 59, 0)
        assert to_datetime_time('2014-2-06 23:59') == datetime.time(23, 59, 0)
        assert to_datetime_time('2014年2月6日 23:59') == datetime.time(23, 59, 0)
        assert to_datetime_time('2014年2月6日 23时59分') == datetime.time(23, 59, 0)
        assert to_datetime_time('2014年02月6日 23时59分0秒') == datetime.time(23, 59, 0)
        assert to_datetime_time('2014年2月06日 23:59:00') == datetime.time(23, 59, 0)
        assert to_datetime_time('1900-1-1') == datetime.time(0, 0, 0)
        assert to_datetime_time('197011') == datetime.time(0, 0, 0)
        assert to_datetime_time('197011810') == datetime.time(8, 1, 0)
        # datetime.timedelta 类型
        assert to_datetime_time(datetime.timedelta()) == datetime.time(0, 0, 0)
        assert to_datetime_time(datetime.timedelta(0, 3602)) == datetime.time(1, 0, 2)
        assert to_datetime_time(datetime.timedelta(5, 3602)) == datetime.time(1, 0, 2)


    # datetime_time_to_str 测试
    def test_datetime_time_to_str(self):
        test_time = datetime.time(12, 9, 2)
        assert datetime_time_to_str(test_time) == "12:09:02"
        assert datetime_time_to_str(test_time, '%H:%M') == "12:09"
        assert datetime_time_to_str("12:9") == "12:09:00"
        assert datetime_time_to_str("12:9:2") == "12:09:02"
        assert datetime_time_to_str(datetime.time()) == "00:00:00"
        assert datetime_time_to_str('0:0:0') == "00:00:00"
        assert datetime_time_to_str('0:0') == "00:00:00"
        # 错误类型
        assert datetime_time_to_str(None) == None
        assert datetime_time_to_str('') == None
        assert datetime_time_to_str(12345) == None
        assert datetime_time_to_str("2014-02-06 12:09:00") == "12:09:00"
        # datetime.timedelta 类型
        assert datetime_time_to_str(datetime.timedelta()) == "00:00:00"
        assert datetime_time_to_str(datetime.timedelta(0, 3602)) == "01:00:02"
        assert datetime_time_to_str(datetime.timedelta(5, 3602)) == "01:00:02"
        assert datetime_time_to_str(datetime.timedelta(0, -2)) == "23:59:58"


    # add 测试
    def test_add(self):
        now_time = datetime.datetime.now # 上面运行这么久,有可能导致时间延后而报错
        test_time = datetime.datetime(2014, 10, 16) # 测试时间
        assert add() == now_time() # 默认返回当前时间
        assert add(days=11) == now_time() + datetime.timedelta(days=11)
        assert add(days=11, number=2) == now_time() + datetime.timedelta(days=22)
        assert add(test_time) == test_time
        # 参数是否被修改测试
        tem_time = test_time
        assert id(add(tem_time, days=1)) != id(test_time) #  日期不同,不能修改传进去的参数值
        assert id(add(tem_time, months=1)) != id(test_time) #  日期不同,不能修改传进去的参数值
        assert id(tem_time) == id(test_time) # 传进去的参数不能被修改
        #add(years=1, months=0, days=0, hours=0, minutes=0, seconds=0)
        assert add(test_time, years=1) == datetime.datetime(2015, 10, 16) # 加 1 年
        assert add(test_time, years=-1) == datetime.datetime(2013, 10, 16) # 减 1 年
        assert add(test_time, months=1) == datetime.datetime(2014, 11, 16) # 加 1 月
        assert add(test_time, months=-1) == datetime.datetime(2014, 9, 16) # 减 1 月
        assert add(test_time, months=12) == add(test_time, years=1) # 加 12 月
        assert add(datetime.datetime(2014, 9, 30), days=1) == datetime.datetime(2014, 10, 1) # 加 1 天
        assert add(datetime.datetime(2014, 10, 1), days=-1) == datetime.datetime(2014, 9, 30) # 减 1 天
        assert add(datetime.datetime(2014, 10, 31), days=1) == datetime.datetime(2014, 11, 1) # 加 1 天
        assert add(datetime.datetime(2014, 2, 28), days=1) == datetime.datetime(2014, 3, 1) # 加 1 天
        assert add(datetime.datetime(2000, 2, 28), days=1) == datetime.datetime(2000, 2, 29) # 加 1 天
        assert add(datetime.datetime(2000, 2, 28), days=2) == datetime.datetime(2000, 3, 1) # 加 2 天
        assert add(test_time, days=365) == add(test_time, years=1) # 加 1 年
        assert add(test_time, days=-365) == add(test_time, years=-1) # 减 1 年
        assert add(test_time, hours=1) == datetime.datetime(2014, 10, 16, 1) # 加 1 小时
        assert add(test_time, hours=-1) == datetime.datetime(2014, 10, 15, 23) # 减 1 小时
        assert add(test_time, minutes=1) == datetime.datetime(2014, 10, 16, 0, 1) # 加 1 分钟
        assert add(test_time, minutes=-1) == datetime.datetime(2014, 10, 15, 23, 59) # 减 1 分钟
        assert add(test_time, seconds=1) == datetime.datetime(2014, 10, 16, 0, 0, 1) # 加 1 秒
        assert add(test_time, seconds=-1) == datetime.datetime(2014, 10, 15, 23, 59, 59) # 减 1 秒
        # 特殊日期(闰月)
        assert add(datetime.datetime(2000, 2, 1), months=1) == datetime.datetime(2000, 3, 1)
        assert add(datetime.datetime(2000, 2, 1), months=1, days=-1) == datetime.datetime(2000, 2, 29)
        assert add(datetime.datetime(1999, 2, 1), years=1, months=1) == datetime.datetime(2000, 3, 1)
        assert add(datetime.datetime(1999, 2, 1), years=1, months=1, days=-1) == datetime.datetime(2000, 2, 29)
        assert add(datetime.datetime(2000, 2, 1), years=1, months=1, days=-1) == datetime.datetime(2001, 2, 28)
        # 倍数计算
        assert add(test_time, years=1, number=2) == datetime.datetime(2016, 10, 16) # 加 1 年 * 2 倍
        assert add(test_time, years=-1, number=2) == datetime.datetime(2012, 10, 16) # 减 1 年 * 2 倍
        assert add(test_time, months=1, number=2) == datetime.datetime(2014, 12, 16) # 加 1 月 * 2 倍
        assert add(test_time, months=-1, number=2) == datetime.datetime(2014, 8, 16) # 减 1 月 * 2 倍
        assert add(datetime.datetime(2014, 9, 29), days=1, number=2) == datetime.datetime(2014, 10, 1) # 加 1 天 * 2 倍
        assert add(datetime.datetime(2014, 10, 1), days=-1, number=2) == datetime.datetime(2014, 9, 29) # 减 1 天 * 2 倍
        assert add(test_time, hours=1, number=2) == datetime.datetime(2014, 10, 16, 2) # 加 1 小时 * 2 倍
        assert add(test_time, hours=-1, number=2) == datetime.datetime(2014, 10, 15, 22) # 减 1 小时 * 2 倍
        assert add(test_time, hours=1, number=1.5) == datetime.datetime(2014, 10, 16, 1, 30) # 加 1 小时 * 1.5 倍


    # sub 测试
    def test_sub(self):
        now = datetime.datetime.now
        # 没差异判断
        zero_secends = {'years' : 0, 'months' : 0, 'days' : 0, 'hours' : 0, 'minutes' : 0, 'seconds' : 0,'sum_days':0, 'sum_seconds':0}
        assert sub() == zero_secends # 默认返回全是0
        assert sub(now(), now()) == zero_secends
        assert sub(None, now()) == zero_secends
        assert sub(now(), None) == zero_secends
        # 相差天数判断
        one_days = {'years' : 0, 'months' : 0, 'days' : 1, 'hours' : 0, 'minutes' : 0, 'seconds' : 0,'sum_days':1, 'sum_seconds':24 * 60 * 60} # 1 天的时间差
        assert sub(now(), now() - datetime.timedelta(days=1)) == one_days # 相差 1 天
        t1 = now() + datetime.timedelta(days=1)
        assert sub(t1, now()) == one_days # 相差 1 天
        assert sub(now(), t1) == {'years' : 0, 'months' : 0, 'days' : -1, 'hours' : 0, 'minutes' : 0, 'seconds' : 0, 'sum_days':-1, 'sum_seconds':-24 * 60 * 60} # 相差 -1 天
        assert sub(now(), t1, abs=True) == one_days # 绝对值相差 1 天
        # 时分秒判断
        assert sub(now(), now() - datetime.timedelta(hours=1)) == {'years' : 0, 'months' : 0, 'days' : 0, 'hours' : 1, 'minutes' : 0, 'seconds' : 0,'sum_days':0, 'sum_seconds':60 * 60} # 相差 1 小时
        assert sub(now(), now() + datetime.timedelta(hours=2)) == {'years' : 0, 'months' : 0, 'days' : 0, 'hours' : -2, 'minutes' : 0, 'seconds' : 0,'sum_days':0, 'sum_seconds':-2*60 * 60} # 相差 -2 小时
        assert sub(now(), now() + datetime.timedelta(hours=2), abs=True) == {'years' : 0, 'months' : 0, 'days' : 0, 'hours' : 2, 'minutes' : 0, 'seconds' : 0,'sum_days':0, 'sum_seconds':2*60 * 60} # 相差 2 小时
        assert sub(now(), now() - datetime.timedelta(minutes=35)) == {'years' : 0, 'months' : 0, 'days' : 0, 'hours' : 0, 'minutes' : 35, 'seconds' : 0,'sum_days':0, 'sum_seconds':35 * 60} # 相差 35 分钟
        assert sub(now(), now() + datetime.timedelta(minutes=32)) == {'years' : 0, 'months' : 0, 'days' : 0, 'hours' : 0, 'minutes' : -32, 'seconds' : 0,'sum_days':0, 'sum_seconds':-32 * 60} # 相差 -32 分钟
        assert sub(now(), now() - datetime.timedelta(seconds=35)) == {'years' : 0, 'months' : 0, 'days' : 0, 'hours' : 0, 'minutes' : 0, 'seconds' : 35,'sum_days':0, 'sum_seconds':35} # 相差 35秒
        assert sub(now(), now() + datetime.timedelta(seconds=32)) == {'years' : 0, 'months' : 0, 'days' : 0, 'hours' : 0, 'minutes' : 0, 'seconds' : -32,'sum_days':0, 'sum_seconds':-32} # 相差 -32 秒
        assert sub(now(), now() - datetime.timedelta(minutes=62)) == {'years' : 0, 'months' : 0, 'days' : 0, 'hours' : 1, 'minutes' : 2, 'seconds' : 0, 'sum_days':0, 'sum_seconds':62*60} # 相差 62 分钟
        assert sub(now(), now() - datetime.timedelta(hours=2, minutes=3, seconds=2)) == {'years' : 0, 'months' : 0, 'days' : 0, 'hours' : 2, 'minutes' : 3, 'seconds' : 2, 'sum_days':0, 'sum_seconds':2*3600+3*60+2} # 相差 2 时 3 分 2 秒
        assert sub(now(), now() + datetime.timedelta(hours=2, minutes=3, seconds=2)) == {'years' : 0, 'months' : 0, 'days' : 0, 'hours' : -2, 'minutes' : -3, 'seconds' : -2, 'sum_days':0, 'sum_seconds':-(2*3600+3*60+2)} # 相差 2 时 3 分 2 秒
        assert sub(now(), now() - datetime.timedelta(seconds=2.9)) == {'years' : 0, 'months' : 0, 'days' : 0, 'hours' : 0, 'minutes' : 0, 'seconds' : 2, 'sum_days':0, 'sum_seconds':2} # 相差 2 秒, 小数忽略
        # 年月判断
        res = sub(now(), now() - datetime.timedelta(days=32))
        assert res.get('sum_days')==32 and res.get('years')==0 and res.get('months')==1 and res.get('days') in (1,2,3,4) and res.get('hours')==0 and res.get('minutes')==0 and res.get('seconds')==0 and res.get('sum_seconds')==32*24*60*60
        assert sub(datetime.datetime(2014, 12, 18, 11, 8, 6), datetime.datetime(2013, 12, 16, 10, 7, 13)) == {'years' : 1, 'months' : 0, 'days' : 2, 'hours' : 1, 'minutes' : 0, 'seconds' : 53, 'sum_days':367, 'sum_seconds':367*24*60*60+3653}
        assert sub(datetime.datetime(2013, 12, 16, 10, 7, 13), datetime.datetime(2014, 12, 18, 11, 8, 6)) == {'years' : -1, 'months' : 0, 'days' : -2, 'hours' : -1, 'minutes' : 0, 'seconds' : -53, 'sum_days':-367, 'sum_seconds':-(367*24*60*60+3653)}
        assert sub(datetime.datetime(2014, 8, 30), datetime.datetime(2014, 7, 30)) == {'years' : 0, 'months' : 1, 'days' : 0, 'hours' : 0, 'minutes' : 0, 'seconds' : 0, 'sum_days':31, 'sum_seconds':31*24*60*60}
        assert sub(datetime.datetime(2014, 9, 16), datetime.datetime(2014, 8, 15)) == {'years' : 0, 'months' : 1, 'days' : 1, 'hours' : 0, 'minutes' : 0, 'seconds' : 0, 'sum_days':32, 'sum_seconds':32*24*60*60}
        assert sub(datetime.datetime(2014, 10, 30), datetime.datetime(2014, 9, 30)) == {'years' : 0, 'months' : 1, 'days' : 0, 'hours' : 0, 'minutes' : 0, 'seconds' : 0, 'sum_days':30, 'sum_seconds':30*24*60*60}
        assert sub(datetime.datetime(2014, 11, 1), datetime.datetime(2014, 10, 2)) == {'years' : 0, 'months' : 0, 'days' : 30, 'hours' : 0, 'minutes' : 0, 'seconds' : 0, 'sum_days':30, 'sum_seconds':30*24*60*60}
        assert sub(datetime.datetime(2014, 10, 2), datetime.datetime(2014, 11, 1)) == {'years' : 0, 'months' : 0, 'days' : -30, 'hours' : 0, 'minutes' : 0, 'seconds' : 0, 'sum_days':-30, 'sum_seconds':-30*24*60*60}
        # 特殊日期(闰月)
        assert sub(datetime.datetime(2000, 3, 1), datetime.datetime(2000, 2, 1)) == {'years' : 0, 'months' : 1, 'days' : 0, 'hours' : 0, 'minutes' : 0, 'seconds' : 0, 'sum_days':29, 'sum_seconds':29*24*60*60} # 闰月 29 天
        assert sub(datetime.datetime(2001, 3, 1), datetime.datetime(2001, 2, 1)) == {'years' : 0, 'months' : 1, 'days' : 0, 'hours' : 0, 'minutes' : 0, 'seconds' : 0, 'sum_days':28, 'sum_seconds':28*24*60*60} # 平月 28 天
        assert sub(datetime.datetime(2000, 3, 1), datetime.datetime(1999, 2, 1)) == {'years' : 1, 'months' : 1, 'days' : 0, 'hours' : 0, 'minutes' : 0, 'seconds' : 0, 'sum_days':394, 'sum_seconds':394*24*60*60} # 平月 28 天


    # get_datetime 测试
    def test_get_datetime(self):
        assert get_datetime("2017-9-5", "12:9:2") == datetime.datetime(2017,9,5,12,9,2)
        assert get_datetime(datetime.date(2017,9,5), datetime.time(13,9,52)) == datetime.datetime(2017,9,5,13,9,52)
        assert get_datetime("2017-9-5", datetime.time(13,9,52)) == datetime.datetime(2017,9,5,13,9,52)
        assert get_datetime(datetime.date(2017,9,5), "12:9:2") == datetime.datetime(2017,9,5,12,9,2)
        assert get_datetime("2014-02-06 12:09:00", '12:9:2') == datetime.datetime(2014,2,6,12,9,2)
        # 没有 时分秒
        assert get_datetime("2017-9-5", '0:0:0') == datetime.datetime(2017,9,5)
        assert get_datetime("2017-9-5", None) == datetime.datetime(2017,9,5)
        assert get_datetime("2017-9-5", '') == datetime.datetime(2017,9,5)
        # 错误类型
        assert get_datetime(None, "12:9:2") == None
        assert get_datetime('', "12:9:2") == None
        # datetime.timedelta 类型
        assert get_datetime("2017-9-5", datetime.timedelta()) == datetime.datetime(2017,9,5,0,0,0)
        assert get_datetime("2017-9-5", datetime.timedelta(0, 3602)) == datetime.datetime(2017,9,5,1,0,2)
        assert get_datetime("2017-9-5", datetime.timedelta(5, 3602)) == datetime.datetime(2017,9,10,1,0,2)
        assert get_datetime("2017-9-5", datetime.timedelta(0, -2)) == datetime.datetime(2017,9,4,23,59,58)


    # add_datetime_time 测试
    def test_add_datetime_time(self):
        test_time = datetime.time(12, 9, 2)
        assert add_datetime_time(test_time) == test_time
        assert add_datetime_time('12:9:2') == test_time
        assert add_datetime_time(test_time, hours=1, minutes=1, seconds=1) == datetime.time(13, 10, 3)
        assert add_datetime_time(test_time, seconds=3601) == datetime.time(13, 9, 3)
        assert add_datetime_time(test_time, minutes=61) == datetime.time(13, 10, 2)
        assert add_datetime_time(test_time, seconds=58) == datetime.time(12, 10, 0)
        assert add_datetime_time(test_time, seconds=-2) == datetime.time(12, 9, 0)
        assert add_datetime_time(test_time, seconds=-3) == datetime.time(12, 8, 59)
        assert add_datetime_time(test_time, seconds=-61) == datetime.time(12, 8, 1)
        assert add_datetime_time(test_time, minutes=51) == datetime.time(13, 0, 2)
        assert add_datetime_time(test_time, minutes=-9) == datetime.time(12, 0, 2)
        assert add_datetime_time(test_time, minutes=-3) == datetime.time(12, 6, 2)
        assert add_datetime_time(test_time, minutes=-61) == datetime.time(11, 8, 2)
        assert add_datetime_time(test_time, hours=11) == datetime.time(23, 9, 2)
        assert add_datetime_time(test_time, hours=12) == datetime.time(0, 9, 2)
        assert add_datetime_time(test_time, hours=13) == datetime.time(1, 9, 2)
        assert add_datetime_time(test_time, hours=-3) == datetime.time(9, 9, 2)
        assert add_datetime_time(test_time, hours=-11) == datetime.time(1, 9, 2)
        assert add_datetime_time(test_time, hours=-12) == datetime.time(0, 9, 2)
        assert add_datetime_time(test_time, hours=-13) == datetime.time(23, 9, 2)
        # 错误类型
        assert add_datetime_time(datetime.time(), seconds=0) == datetime.time()
        assert add_datetime_time(None) == None
        assert add_datetime_time('') == None
        assert add_datetime_time(12345) == None
        assert add_datetime_time("2014-02-06 12:09:00") == datetime.time(12, 9, 0)
        # 不允许跨天
        assert add_datetime_time(test_time, hours=1, minutes=1, seconds=1, cross_day=False) == datetime.time(13, 10, 3)
        assert add_datetime_time(test_time, seconds=3601, cross_day=False) == datetime.time(13, 9, 3)
        assert add_datetime_time(test_time, minutes=61, cross_day=False) == datetime.time(13, 10, 2)
        assert add_datetime_time(test_time, seconds=58, cross_day=False) == datetime.time(12, 10, 0)
        assert add_datetime_time(test_time, seconds=-2, cross_day=False) == datetime.time(12, 9, 0)
        assert add_datetime_time(test_time, seconds=-3, cross_day=False) == datetime.time(12, 8, 59)
        assert add_datetime_time(test_time, seconds=-61, cross_day=False) == datetime.time(12, 8, 1)
        assert add_datetime_time(test_time, minutes=51, cross_day=False) == datetime.time(13, 0, 2)
        assert add_datetime_time(test_time, minutes=-9, cross_day=False) == datetime.time(12, 0, 2)
        assert add_datetime_time(test_time, minutes=-3, cross_day=False) == datetime.time(12, 6, 2)
        assert add_datetime_time(test_time, minutes=-61, cross_day=False) == datetime.time(11, 8, 2)

        assert add_datetime_time(test_time, hours=11, cross_day=False) == datetime.time(23, 9, 2)
        assert add_datetime_time(test_time, hours=12, cross_day=False) == datetime.time(23, 59, 59)
        assert add_datetime_time(test_time, hours=13, cross_day=False) == datetime.time(23, 59, 59)
        assert add_datetime_time(test_time, hours=-3, cross_day=False) == datetime.time(9, 9, 2)
        assert add_datetime_time(test_time, hours=-11, cross_day=False) == datetime.time(1, 9, 2)
        assert add_datetime_time(test_time, hours=-12, cross_day=False) == datetime.time(0, 9, 2)
        assert add_datetime_time(test_time, hours=-13, cross_day=False) == datetime.time(0, 0, 0)


    # sub_datetime_time 测试
    def test_sub_datetime_time(self):
        assert sub_datetime_time(datetime.time(12, 9, 2), datetime.time(12, 8, 0)) == 62
        assert sub_datetime_time(datetime.time(12, 8, 0), datetime.time(12, 9, 2)) == -62
        assert sub_datetime_time('12:9:2', '12:8:0') == 62
        assert sub_datetime_time('12:8:0', '12:9:2') == -62
        assert sub_datetime_time('0:0:0', '0:8:0') == -480
        assert sub_datetime_time('8:8:0', '0:0:0') == 3600*8+480
        # 错误类型
        assert sub_datetime_time(None, None) == None
        assert sub_datetime_time('8:8:0', None) == None
        assert sub_datetime_time('', '0:8:0') == None


    # get_week_range 测试
    def test_get_week_range(self):
        # 默认时间
        today = datetime.date.today
        this_week_star, this_week_end = get_week_range() # 默认返回当前周的开始及结束时间
        assert this_week_star <= today()
        assert this_week_end >= today()
        assert this_week_star.weekday() == 0
        assert this_week_end.weekday() == 6
        # 指定测试时间
        test_time = datetime.date(2016, 8, 2)
        test_week_star, test_week_end = get_week_range(test_time)
        assert test_week_star == datetime.date(2016, 8, 1)
        assert test_week_end == datetime.date(2016, 8, 7)
        # 指定测试时间
        test_time = datetime.date(2016, 8, 1)
        test_week_star, test_week_end = get_week_range(test_time)
        assert test_week_star == datetime.date(2016, 8, 1)
        assert test_week_end == datetime.date(2016, 8, 7)
        # 指定测试时间
        test_time = datetime.date(2016, 8, 7)
        test_week_star, test_week_end = get_week_range(test_time)
        assert test_week_star == datetime.date(2016, 8, 1)
        assert test_week_end == datetime.date(2016, 8, 7)


    # get_month_range 测试
    def test_get_month_range(self):
        # 指定测试时间
        test_month_star, test_month_end = get_month_range(2016, 8)
        assert test_month_star == datetime.date(2016, 8, 1)
        assert test_month_end == datetime.date(2016, 8, 31)
        # 指定测试时间(特殊月份，闰年2月)
        test_month_star, test_month_end = get_month_range(2016, 2)
        assert test_month_star == datetime.date(2016, 2, 1)
        assert test_month_end == datetime.date(2016, 2, 29)
        # 指定测试时间(特殊月份，平年2月)
        test_month_star, test_month_end = get_month_range(2015, 2)
        assert test_month_star == datetime.date(2015, 2, 1)
        assert test_month_end == datetime.date(2015, 2, 28)


    # get_month_list 测试
    def test_get_month_list(self):
        # 指定测试时间
        month_list = get_month_list(2016, 8)
        assert len(month_list) == 31
        assert month_list[0] == datetime.date(2016, 8, 1)
        assert month_list[-1] == datetime.date(2016, 8, 31)
        # 指定测试时间(特殊月份，闰年2月)
        month_list = get_month_list(2016, 2)
        assert len(month_list) == 29
        assert month_list[0] == datetime.date(2016, 2, 1)
        assert month_list[-1] == datetime.date(2016, 2, 29)
        # 指定测试时间(特殊月份，平年2月)
        month_list = get_month_list(2015, 2)
        assert len(month_list) == 28
        assert month_list[0] == datetime.date(2015, 2, 1)
        assert month_list[-1] == datetime.date(2015, 2, 28)


if __name__ == "__main__":
    unittest.main()
