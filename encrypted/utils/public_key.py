# -*- encoding: utf-8 -*-
'''
@File    :   get_public_key.py
@Time    :   2021/11/16 17:57:49
@Author  :   sk 
@Version :   1.0
@Contact :   kaixuan.sun@boonray.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
from Crypto.Cipher import AES as aes
from rsa import transform

from .utils import random_str, hex2bytes, bytes2hex, str2hexstr, hexstr2str

def en_public_key(public_key_plaintext, private_key):
    """加密公钥

    Args:
        public_key_plaintext ([str]): 字符串明文
        private_key ([int]): 私钥

    Returns:
        [str]: [description]
    """    

    iv = random_str(16)
    private_key = transform.int2bytes(private_key)

    length = 16 - len(public_key_plaintext) % 16
    public_key_plaintext += " "*length

    aes_ = aes.new(private_key, aes.MODE_CBC, bytes(iv.encode("utf-8")))
   
    # bytes->10->16
    public_secret_bytes = aes_.encrypt(public_key_plaintext.encode("utf-8"))
    public_secret_hex = bytes2hex(public_secret_bytes)

    iv_hex_str = str2hexstr(iv)

    public_key = iv_hex_str + "&" + public_secret_hex

    return public_key


def de_public_key(public_key, private_key):

    private_key = transform.int2bytes(private_key)

    iv, public_key_cipher = public_key.split('&')

    # 16->10->bytes
    public_key_bytes = hex2bytes(public_key_cipher)

    iv_str = hexstr2str(iv)

    aes_ = aes.new(private_key, aes.MODE_CBC, bytes(iv_str.encode("utf-8")))

    public_key_plaintext_bytes = aes_.decrypt(public_key_bytes).strip()
    public_key_plaintext = bytes.decode(public_key_plaintext_bytes)

    return public_key_plaintext