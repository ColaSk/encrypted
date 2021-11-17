# -*- encoding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2021/11/15 14:17:54
@Author  :   sk 
@Version :   1.0
@Contact :   kaixuan.sun@boonray.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib

import random
from rsa import transform
from encrypted.conf.setting import Setting as setting

def random_str(slen=100, seed=setting.seed):
    """Randomly selects a string of the specified length from the seed"""
    sa = ''.join(random.choice(seed) for _ in range(slen))
    return sa

def str2ASCII(string):
    for s in string:
        yield ord(s)

def bytes2hex(b):
    """bytes->10->16"""
    int_ = int.from_bytes(b, byteorder='big')
    hex_ = hex(int_).lstrip("0x")

    return hex_

def hex2bytes(h):
    """16->10->bytes"""
    int_ = int(h, 16)
    bytes_ = transform.int2bytes(int_)

    return bytes_

def str2hexstr(string):
    """Formats a string as a list of hexadecimal characters"""
    rt = [hex(ord(s)).lstrip("0x") for s in string]
    return ''.join(rt)