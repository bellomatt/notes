#!python
# -*- coding:utf-8 -*-
"""
公用函数(字符串处理) html_util.py 的测试
Created on 2015/1/19
Updated on 2019/1/18
@author: Holemar
"""
import logging
import unittest

from __init__ import *
from libs_my.abandon import html_util


class TestXhtml(unittest.TestCase):
    # html 测试
    def test_html(self):
        logging.info(u'测试 html_util')
        assert html_util.to_html("  ") == '&nbsp;&nbsp;'
        assert html_util.to_text('&nbsp;xx&nbsp;') == " xx "
        assert html_util.remove_htmlTag("x<div>haha</div>x")=="xhahax"


if __name__ == "__main__":
    unittest.main()

