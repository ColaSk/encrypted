# -*- encoding: utf-8 -*-
'''
@File    :   fileoperator.py
@Time    :   2021/11/16 15:55:31
@Author  :   sk 
@Version :   1.0
@Contact :   kaixuan.sun@boonray.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
from abc import abstractmethod
import yaml

class FileBase(object):

    def __init__(self, path):
        self.path = path
    
    @abstractmethod
    def read(self): pass

    @abstractmethod
    def write(self): pass


class YamlFile(FileBase):

    def read(self):
        with open(self.path, 'r', encoding="utf-8") as f:
            return yaml.load(f, Loader=yaml.FullLoader)
    
    def write(self, data):
        with open(self.path, 'w', encoding='utf-8') as f:
            return yaml.dump(data, f)