#!python
# -*- coding:utf-8 -*-
"""
公用函数(aes加密)，依赖 C 库
Created on 2016/10/18
Updated on 2019/1/18
@author: Holemar

需要安装： pip PyCrypto==2.6.1
"""
import sys
import base64

from Crypto.Cipher import AES
from Crypto import Random

bs = AES.block_size
# 定义向量 iv
IV = [200, 90, 200, 144, 210, 109, 121, 45, 153, 144, 236, 208, 235, 133, 119, 152]
iv2 = ''.join([chr(i) for i in IV])

system_encoding = "utf-8"
defaultencoding = sys.getdefaultencoding()

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    basestring = unicode = str


def pad(s):
    if PY3:
        s = s.encode()
    # return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
    return s + (bs - len(s) % bs) * b'\x00'


def unpad(s):
    if PY3:
        s = s.decode()
    return s[0:-ord(s[-1])]


def to_str(text):
    """
    中文转换，将 unicode、gbk、big5 编码转成 str 编码(utf-8)
    :param {string} text: 原字符串
    :return {string}: 返回转换后的字符串
    """
    if PY3:
        return text
    try:
        # py2 的处理
        if defaultencoding and isinstance(defaultencoding, basestring):
            encoding_tuple = ("gbk", "big5", defaultencoding)
        else:
            encoding_tuple = ("gbk", "big5")
        if isinstance(text, unicode):
            return text.encode(system_encoding)
        elif isinstance(text, str):
            try:
                text.decode(system_encoding)
                return text  # 如果上面这句执行没报异常，说明是 utf-8 编码，不用再转换
            except:
                pass
            for encoding in encoding_tuple:
                try:
                    text = text.decode(encoding)
                    return text.encode(system_encoding)
                    break  # 如果上面这句执行没报异常，说明是这种编码
                except:
                    pass
        return str(text)
    except NameError:
        # py3 的处理
        return text


def encryptData(data, key):
    """
    将明文字符串，用AES加密成密文
    :param {string} data: 明文的字符串
    :param {string} key: 加密/解密的key值
    :return {string}: 返回加密后的密文
    """
    if not data:
        return data
    if not key:
        raise RuntimeError(u'缺少加密的key!')
    data = to_str(data)
    # iv = iv2
    iv = Random.new().read(bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = cipher.encrypt(pad(data))
    data = iv + data
    return base64.b64encode(data)


def decryptData(data, key):
    """
    将AES加密后的密文，解密出来
    :param {string} data: 加密后的密文
    :param {string} key: 加密/解密的key值
    :return {string}: 返回解密后的明文
    """
    if not data:
        return data
    if not key:
        raise RuntimeError(u'缺少解密的key!')
    try:
        data = base64.b64decode(data)
    except:  # base64 解码异常，很可能传来的是明文，直接返回
        return data
    if len(data) <= bs:
        return data
    iv = data[:bs]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = unpad(cipher.decrypt(data[bs:]))
    return data


if __name__ == '__main__':
    cleartext = u"This is a test with several blocks!中文坎坎坷坷吞吞吐吐yy语音男男女女"  # 加密、解密的字符串
    key = 'fgjtjirj4o234234'  # 必须16、24、32 位

    encrypt_data = encryptData(cleartext, key)
    print('encrypt_data:')
    print(encrypt_data)

    decrypt_data = decryptData(encrypt_data, key)
    print('decrypt_data:')
    print(decrypt_data)
