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
from encrypted.conf.setting import Setting as setting

def random_str(slen=100, seed=setting.seed):
    sa = ''.join(random.choice(seed) for _ in range(slen))
    return sa