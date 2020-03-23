#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
以 markdown 形式来显示本笔记的内容。尽量兼顾 py2 及 py3 的形式。
"""
import os
import sys

from bottle import route, run, static_file
current_dir, _ = os.path.split(os.path.abspath(__file__))
current_dir = current_dir or os.getcwd()  # 当前目录
BASE_PATH = os.path.dirname(current_dir)  # 上一层目录，认为是项目源目录

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY2:
    from codecs import open  # 打开文件时，可以指定编码

# 文件的编码尝试列表
CODING_LIST = ["utf-8", 'gb18030', "gbk", 'big5']
# 自动改编码的文件后缀列表
CHANGE_EXT = ('.py', '.js', '.md', '.html', '.txt', '.java', '.cs', '.jsp', '.go', '.php', '.css', '.conf')


def read_file(file_path):
    """读取文件，并返回其内容
    :param file_path: 相对路径(以本笔记首目录为基准)
    :return: 文件内容
    """
    file_path = os.path.join(BASE_PATH, file_path)
    file_path = os.path.abspath(file_path)
    # 如果是目录，则找里面的"README.md"，没有则遍历目录文件
    if os.path.isdir(file_path):
        tem = os.path.join(file_path, 'README.md')
        if os.path.exists(tem):
            file_path = tem
        else:
            folders, files = [], []
            source_files = list(os.listdir(file_path))
            for file_name in source_files:
                # 系统自动生成的无用文件
                if file_name in ('.DS_Store', 'Thumbs.db', 'folder.ini',):
                    continue
                if os.path.isdir(os.path.join(file_path, file_name)):
                    folders.append("**[%s](./%s/)**" % (file_name, file_name))
                else:
                    files.append("[%s](./%s)" % (file_name, file_name))
            # 排序
            folders.sort()
            files.sort()
            return '  \r\n'.join(folders) + '  \r\n' + '  \r\n'.join(files)
    # 文件找不到
    if not os.path.exists(file_path):
        return '没有您需要的页面!'
    # 按不同编码尝试读取文件
    for encode in CODING_LIST:
        try:
            # 没报异常，正常返回了，则说明是这种编码
            with open(file_path, 'r', encoding=encode) as f:
                result = f.read()
            # 自动改编码
            if result and encode != CODING_LIST[0] and not file_path.lower().endswith(CHANGE_EXT):
                with open(file_path, 'w', encoding="utf-8") as f:
                    f.write(result)
            return result
        except UnicodeDecodeError as e:
            pass


@route('/notes_web/markdeep.js')
def markdeep():
    """markdeep.js加载"""
    return static_file('/notes_web/markdeep.js', root=BASE_PATH)


@route('/:file_path#.*#')
def page(file_path):
    """打开页面"""
    # 去掉参数
    if '?' in file_path:
        file_path = file_path[:file_path.index('?')]
    p = file_path.lower()
    # 压缩包，不能读
    if p.endswith(('.zip', '.rar', '.arj', '.z')):
        return '压缩文件，无法打开'
    text = read_file(file_path)
    text += '\r\n <META http-equiv="Content-Type" content="text/html; charset=utf-8"/>'
    # 对 markdown 文件，自动加载样式。其它文件显示原文。
    if not p or p.endswith(('/', '.md')):
        text += '\r\n <!-- Markdeep: --><script src="/notes_web/markdeep.js" charset="utf-8"></script>'
    else:
        text = text.replace('\n', '\n<br/>')
    return text


if __name__ == '__main__':  # pragma: no coverage
    run(host='localhost', port=8080)
