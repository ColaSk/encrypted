# -*- encoding: utf-8 -*-
'''
@File    :   formathex.py
@Time    :   2021/11/15 13:52:36
@Author  :   sk 
@Version :   1.0
@Contact :   kaixuan.sun@boonray.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib

from rsa import transform

def format_string_hex_data(random_str):
    rt = [hex(ord(s)).lstrip("0x") for s in random_str]
    return rt

def disassemble_iv_hex(iv_str):
    parts = [iv_str[i:i+2] for i in range(len(iv_str)) if i%2==0]
    return parts


def iv_hex_to_str(iv_hex_list):
    single_ivs_int = [int(single_hex, 16) for single_hex in iv_hex_list]
    single_ivs_b = [transform.int2bytes(single_iv_int) for single_iv_int in single_ivs_int]
    single_ivs_str = [single_iv_b.decode("utf-8") for single_iv_b in single_ivs_b]
    iv_str = "".join(single_ivs_str)

    return iv_str
