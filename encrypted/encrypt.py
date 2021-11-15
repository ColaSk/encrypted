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
from Crypto.Cipher import AES
from rsa import transform
from encrypted.conf.setting import Setting as setting
from .utils.formathex import (disassemble_iv_hex, 
                              iv_hex_to_str, 
                              format_string_hex_data)
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
        aes_obj = AES.new(root_secret_key, AES.MODE_CBC, bytes(iv_str.encode("utf-8")))
        work_secret_key_plaintext = aes_obj.decrypt(work_secret_key_bytes)
        work_secret_key_plaintext = work_secret_key_plaintext.strip()

        return work_secret_key_plaintext
    
    def __en_by_work_key_plaintext(self, password, work_secret_key_plaintext):
        # 使用工作秘钥明文对密码进行加密
        pass_iv = random_str(16)
        pass_iv_hex_list = format_string_hex_data(pass_iv)
        pass_iv_hex_str = "".join(pass_iv_hex_list)
        aes_encrypt_obj = AES.new(work_secret_key_plaintext, AES.MODE_CBC, bytes(pass_iv.encode("utf-8")))
        password_length = len(password)
        result_length = 16 - password_length % 16

        password += " "*result_length

        password_cipher_bytes = aes_encrypt_obj.encrypt(password.encode("utf-8"))
        password_cipher_int = transform.bytes2int(password_cipher_bytes)
        password_cipher_hex = hex(password_cipher_int)
        password_cipher_hex = password_cipher_hex.lstrip("0x")
        password_cipher_str = pass_iv_hex_str + "&" + password_cipher_hex

        return password_cipher_str
    
    def __de_by_work_key_plaintext(self, password_cipher, work_secret_key_plaintext):
        # 使用工作秘钥明文对密码进行解密
        password_iv, password_cipher_hex = password_cipher.split("&")
        password_cipher_int = int(password_cipher_hex, 16)
        password_cipher_bytes = transform.int2bytes(password_cipher_int)
        password_iv_hex_list = disassemble_iv_hex(password_iv)
        password_iv_str = iv_hex_to_str(password_iv_hex_list)
        aes_decrypt_obj = AES.new(work_secret_key_plaintext, AES.MODE_CBC, bytes(password_iv_str.encode("utf-8")))
        password = aes_decrypt_obj.decrypt(password_cipher_bytes)

        return password.decode("utf-8").replace(" ", "")

    def encode(self, password):

        work_secret_key_plaintext = self.__de_work_secret_key(self.__private_key, self.__public_key)
        password_cipher_str = self.__en_by_work_key_plaintext(password, work_secret_key_plaintext)

        return password_cipher_str

    def decode(self, password_cipher):

        work_secret_key_plaintext = self.__de_work_secret_key(self.__private_key, self.__public_key)
        password = self.__de_by_work_key_plaintext(password_cipher, work_secret_key_plaintext)

        return password