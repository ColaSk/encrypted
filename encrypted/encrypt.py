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

from .utils import (str2hexstr, hexstr2str, 
                    random_str, de_public_key,
                    get_private_key, YamlFile,
                    str2ASCII, en_public_key)

class EncryptCore(object):

    def __init__(self, public_key, private_key):

        self.__public_key = public_key
        self.__private_key = private_key 

    def __de_public_key(self, private_key, public_key):

        public_key_plaintext = de_public_key(public_key, private_key)

        return public_key_plaintext
    
    def __en_by_public_key_plaintext(self, string, key):

        # 偏移 iv
        iv = random_str(16)
        iv_hex_str = str2hexstr(iv)

        # 补位
        result_length = 16 - len(string) % 16
        string += " "*result_length
        
        # aes 加密
        aes_ = aes.new(bytes(key.encode("utf-8")), aes.MODE_CBC, bytes(iv.encode("utf-8")))
        cipher_bytes = aes_.encrypt(string.encode("utf-8"))

        cipher_int = transform.bytes2int(cipher_bytes)
        cipher_hex = hex(cipher_int).lstrip("0x")
        cipher_str = iv_hex_str + "&" + cipher_hex

        return cipher_str
    
    def __de_by_public_key_plaintext(self, cipher, key):

        iv, cipher_hex = cipher.split("&")
        cipher_int = int(cipher_hex, 16)
        cipher_bytes = transform.int2bytes(cipher_int)

        iv_str = hexstr2str(iv)
        aes_ = aes.new(bytes(key.encode("utf-8")), aes.MODE_CBC, bytes(iv_str.encode("utf-8")))
        
        string = aes_.decrypt(cipher_bytes)
        rt = string.decode("utf-8").replace(" ", "")

        return rt

    def encode(self, string):

        public_key_plaintext = self.__de_public_key(self.__private_key, self.__public_key)
        password_cipher_str = self.__en_by_public_key_plaintext(string, public_key_plaintext)

        return password_cipher_str

    def decode(self, string_cipher):

        public_key_plaintext = self.__de_public_key(self.__private_key, self.__public_key)
        string = self.__de_by_public_key_plaintext(string_cipher, public_key_plaintext)

        return string


def parse_dynamic_key_file_data(data):
    return ''.join([transform.int2bytes(int(d, 16)).decode("utf-8") 
                    for d in data.get('random_int').split('&')])


def create_dynamic_key_file_data(dynamic_key):
    return '&'.join([hex(ord(s)).lstrip("0x") for s in dynamic_key])


def create_dynamic_key_file(path, dynamic_key):
    yfile = YamlFile(path)
    data = create_dynamic_key_file_data(dynamic_key)
    yfile.write({'random_int': data})

    return path


def create_private_key(status_key_plaintext, dynamic_key_plaintext, dynamic_key_file=None):
    static_int_list = str2ASCII(status_key_plaintext)
    dynamic_int_list = str2ASCII(dynamic_key_plaintext)
    
    private_key = get_private_key(static_int_list, dynamic_int_list)
    
    path = None
    if dynamic_key_file:
        path = create_dynamic_key_file(dynamic_key_file, dynamic_key_plaintext)
    
    return private_key, path


def create_public_key(public_key_plaintext, private_key):
    return en_public_key(public_key_plaintext, 
                         private_key)

