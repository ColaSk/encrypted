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
                    get_private_key,str2ASCII, 
                    en_public_key, hex2bytes)

class EncryptCore(object):

    def __init__(self, public_key: str, private_key: int):

        self.__public_key = public_key
        self.__private_key = private_key 

    def __de_public_key(self):
        """解密公钥

        Args:
            private_key (int): 私钥
            public_key (str): 公钥

        Returns:
            [str]: 公钥明文
        """        

        public_key_plaintext = de_public_key(self.__public_key, self.__private_key)

        return public_key_plaintext
    
    def __en_by_public_key_plaintext(self, string: str, key: str):
        """使用公钥明文加密字符串

        Args:
            string (str): 待加密的字符串
            key (str): 密钥

        Returns:
            [str]: 字符串密文
        """        

        # 偏移 iv
        iv = random_str(16)
        iv_hex_str = str2hexstr(iv)

        # 补位
        result_length = 16 - len(string) % 16
        string += " "*result_length
        
        # aes 加密
        aes_ = aes.new(bytes(key.encode("utf-8")), 
                       aes.MODE_CBC, 
                       bytes(iv.encode("utf-8")))

        cipher_bytes = aes_.encrypt(string.encode("utf-8"))

        cipher_int = transform.bytes2int(cipher_bytes)
        cipher_hex = hex(cipher_int).lstrip("0x")
        cipher_str = iv_hex_str + "&" + cipher_hex

        return cipher_str
    
    def __de_by_public_key_plaintext(self, cipher: str, key: str):
        """解密字符串密文

        Args:
            cipher (str): 密文
            key (str): 密钥

        Returns:
            [str]: 字符串明文
        """        

        iv, cipher_hex = cipher.split("&")
        cipher_bytes = hex2bytes(cipher_hex)

        iv_str = hexstr2str(iv)
        aes_ = aes.new(bytes(key.encode("utf-8")), 
                       aes.MODE_CBC, 
                       bytes(iv_str.encode("utf-8")))
        
        string = aes_.decrypt(cipher_bytes)

        rt = string.decode("utf-8").replace(" ", "")

        return rt

    def encode(self, string):

        public_key_plaintext = self.__de_public_key()
        password_cipher_str = self.__en_by_public_key_plaintext(string, public_key_plaintext)

        return password_cipher_str

    def decode(self, string_cipher):

        public_key_plaintext = self.__de_public_key()
        string = self.__de_by_public_key_plaintext(string_cipher, public_key_plaintext)

        return string


def create_private_key(status_key_plaintext: str, 
                       dynamic_key_plaintext: str):
    """创建私钥

    Args:
        status_key_plaintext (str): 静态密钥明文, 永久硬编码的安全超长随机字符串
                                    ex: uYdMvnFxS$KTjb8C9f)Z7_yeKSzn-iYW)BodWsZ4$g5OZThwl5)
                                        FSx$zfiYj6!oqfhd2FeIKsmRO+hNqJAKY_AGFdbnym8^CDwM%
                                    
        dynamic_key_plaintext (str): 动态密钥明文, 可动态更新的安全超长随机字符串, 需要保证与静态密钥明文保持相同长度
                                    ex: uYdMvnFxS$KTjb8C9f)Z7_yeKSzn-iYW)BodWsZ4$g5OZThwl5)
                                        FSx$zfiYj6!oqfhd2FeIKsmRO+hNqJAKY_AGFdbnym8^CDwM%
    Returns:
        [int]: 生成密钥
    """    
    static_int_list = str2ASCII(status_key_plaintext)
    dynamic_int_list = str2ASCII(dynamic_key_plaintext)
    
    private_key = get_private_key(static_int_list, dynamic_int_list)
    
    return private_key


def create_public_key(public_key_plaintext: str, 
                      private_key: str):
    """创建私钥

    Args:
        public_key_plaintext (str): 公共密钥明文，当前明文支持(16, 24, 32)长度
        private_key (str): [description]

    Returns:
        [str]: 生成公钥
    """    
    return en_public_key(public_key_plaintext, 
                         private_key)


__all__ = [
    "EncryptCore",
    "create_private_key",
    "create_public_key"
]