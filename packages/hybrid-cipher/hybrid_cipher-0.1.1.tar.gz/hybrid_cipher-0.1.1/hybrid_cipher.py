#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import (
    absolute_import,
    division,
    generators,
    nested_scopes,
    print_function,
    unicode_literals,
    with_statement,
)

import json
import base64
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

__all__ = [
    "HybridCipher",
]


def _base64encode(data):
    return "".join(base64.encodebytes(data).decode().splitlines())


def _base64decode(data):
    return base64.decodebytes(data.encode("utf-8"))


class HybridCipher(object):
    """混合加密。

    加密步骤：
    1. 生成随机32位临时密钥。
    2. 使用RSA公钥加密临时密钥。
    3. 使用临时密钥及AES GCM算法加密数据内容。
    4. 把临时密钥的密文及数据密文相关字段拼接在一起，作为整体密文。

    解密步骤：
    1. 分割密文为：临时密钥密文、数据密文相关字段。
    2. 使用RSA私钥解密临时密钥密文，得到临时密钥明文。
    3. 使用临时密钥明文及AES GCM解密算法解密数据密文相关字段，得到数据明文。
    """

    # AES MOD_GCM 要求密钥必须为32位长度
    tmp_key_size = 32

    def __init__(self, key, passphrase=None, random_header_size=32):
        """
        @parameter: key 要求key的类型为：RSA PublicKey、RSAPrivateKey或其导出的字符串类型
            当key为公钥时，只能进行加密。
            当key为私钥时，可以进行加密或解密。

            注意：即使使用私钥进行加密，但实际上仍然使用了私钥所对应的公钥进行加密。

        @parameter: passphrase key的解密密钥。
        """
        if isinstance(key, str):
            self.key = RSA.import_key(key, passphrase=passphrase)
        else:
            self.key = key
        self.tmp_key_cipher = PKCS1_OAEP.new(self.key)
        self.random_header_size = random_header_size

    def encrypt(self, data):
        # 数据内容转化为字节流
        if not isinstance(data, (str, bytes)):
            data = json.dumps(data)
        if isinstance(data, str):
            data = data.encode("utf-8")
        # 生成临时密钥
        tmp_key = get_random_bytes(self.tmp_key_size)
        # 临时密钥加密
        tmp_key_safe = self.tmp_key_cipher.encrypt(tmp_key)
        # 生成随机header
        header = get_random_bytes(self.random_header_size)
        # 数据内容加密
        cipher = AES.new(tmp_key, AES.MODE_GCM)
        cipher.update(header)
        data_safe, tag = cipher.encrypt_and_digest(data)
        nonce = cipher.nonce
        # 结果封装
        return ".".join(
            [
                _base64encode(tmp_key_safe),
                _base64encode(header),
                _base64encode(nonce),
                _base64encode(tag),
                _base64encode(data_safe),
            ]
        )

    def decrypt(self, data):
        # 结果解封
        tmp_key_safe, header, nonce, tag, data_safe = data.split(".")
        tmp_key_safe = _base64decode(tmp_key_safe)
        header = _base64decode(header)
        nonce = _base64decode(nonce)
        tag = _base64decode(tag)
        data_safe = _base64decode(data_safe)
        # 解密临时密钥
        tmp_key = self.tmp_key_cipher.decrypt(tmp_key_safe)
        # 数据内容解密
        cipher = AES.new(tmp_key, AES.MODE_GCM, nonce=nonce)
        cipher.update(header)
        data = cipher.decrypt_and_verify(data_safe, tag)
        # 还原数据内容
        # 注意：如果你加密的是json.dumps后的字符串，这里会还原成json.loads后的数据
        try:
            return json.loads(data)
        except:
            try:
                return data.decode("utf-8")
            except:
                return data
