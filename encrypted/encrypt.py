# -*- encoding: utf-8 -*-
'''
@File    :   encrypt.py
@Time    :   2021/11/15 13:43:08
@Author  :   sk 
@Version :   1.0
@Contact :   kaixuan.sun@boonray.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
from Crypto.Cipher import AES as aes
from rsa import transform
from encrypted.conf.setting import Setting as setting
from .utils.formathex import (disassemble_iv_hex, 
                              iv_hex_to_str, 
                              string_to_hex_format)
from .utils.gen_root_secret_key import gen_root_secret_key_str
from .utils.utils import random_str


class EncryptCore(object):

    def __init__(self,public_key=None, private_key=None):

        self.__public_key = public_key if public_key else setting.work_secret_key_cipher_str
        self.__private_key = private_key if private_key else gen_root_secret_key_str()

    def __de_work_secret_key(self, root_secret_key_str, work_secret_key_cipher_str):
        # 解码工作秘钥明文
        root_secret_key = transform.int2bytes(root_secret_key_str)
        iv, work_secret_key_cipher = work_secret_key_cipher_str.split('&')
        work_secret_key_int = int(work_secret_key_cipher, 16)
        work_secret_key_bytes = transform.int2bytes(work_secret_key_int)
        iv_hex_list = disassemble_iv_hex(iv)
        iv_str = iv_hex_to_str(iv_hex_list)
        aes_obj = aes.new(root_secret_key, aes.MODE_CBC, bytes(iv_str.encode("utf-8")))
        work_secret_key_plaintext = aes_obj.decrypt(work_secret_key_bytes)
        work_secret_key_plaintext = work_secret_key_plaintext.strip()

        return work_secret_key_plaintext
    
    def __en_by_work_key_plaintext(self, string, key):
        # 使用工作秘钥明文对密码进行加密

        # 偏移 iv
        iv = random_str(16)
        iv_hex_list = string_to_hex_format(iv)
        iv_hex_str = "".join(iv_hex_list)

        # 补位
        result_length = 16 - len(string) % 16
        string += " "*result_length
        
        # aes 加密
        aes_ = aes.new(key, aes.MODE_CBC, bytes(iv.encode("utf-8")))
        cipher_bytes = aes_.encrypt(string.encode("utf-8"))

        cipher_int = transform.bytes2int(cipher_bytes)
        cipher_hex = hex(cipher_int).lstrip("0x")
        cipher_str = iv_hex_str + "&" + cipher_hex

        return cipher_str
    
    def __de_by_work_key_plaintext(self, cipher, key):
        # 使用工作秘钥明文对密码进行解密

        iv, cipher_hex = cipher.split("&")
        cipher_int = int(cipher_hex, 16)
        cipher_bytes = transform.int2bytes(cipher_int)

        iv_hex_list = disassemble_iv_hex(iv)
        iv_str = iv_hex_to_str(iv_hex_list)
        aes_ = aes.new(key, aes.MODE_CBC, bytes(iv_str.encode("utf-8")))
        
        string = aes_.decrypt(cipher_bytes)
        rt = string.decode("utf-8").replace(" ", "")

        return rt

    def encode(self, password):

        work_secret_key_plaintext = self.__de_work_secret_key(self.__private_key, self.__public_key)
        password_cipher_str = self.__en_by_work_key_plaintext(password, work_secret_key_plaintext)

        return password_cipher_str

    def decode(self, password_cipher):

        work_secret_key_plaintext = self.__de_work_secret_key(self.__private_key, self.__public_key)
        password = self.__de_by_work_key_plaintext(password_cipher, work_secret_key_plaintext)

        return password