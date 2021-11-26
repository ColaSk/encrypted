# -*- encoding: utf-8 -*-
'''
@File    :   really_random.py
@Time    :   2021/11/25 17:38:52
@Author  :   sk 
@Version :   1.0
@Contact :   kaixuan.sun@boonray.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
import sys
from subprocess import Popen, PIPE

def really_random_str(slen=100):

    assert 'linux' in sys.platform

    def urandom_command(slen=32):
        assert slen <= 32
        with Popen(f'cat /dev/urandom | head -n 100 | md5sum | head -c {slen}', 
                   stdout=PIPE, shell=True) as p:
            rt = p.stdout.readline().decode(encoding="utf-8")
        return rt

    quotient, remainder = divmod(slen, 32) # 商, 余数

    str_list = []
    
    if remainder:
        str_list.append(urandom_command(remainder))

    for _ in range(quotient):
        str_list.append(urandom_command())

    return ''.join(str_list)

if __name__ == "__main__":
    really_random_str()