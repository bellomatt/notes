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
        self.assertEqual(html_util.to_html("  "), '&nbsp;&nbsp;')
        self.assertEqual(html_util.to_text('&nbsp;xx&nbsp;'), " xx ")
        self.assertEqual(html_util.remove_html("x<div>haha</div>x"), "xhahax")
        self.assertEqual(html_util.remove_html("""x<div>haha</div>x<!--点点滴滴-->啊啊
        <style>body {margin: 0;}</style>
        <script type="text/javascript" src="/manifest.2be1e4cb32664bc84cf0.js"></script>
        <script type="text/javascript"> function ...</script>"""),
                         "xhahax啊啊")


if __name__ == "__main__":
    unittest.main()

