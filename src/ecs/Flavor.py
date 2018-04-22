# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 11:42:36 2018

@author: DoctorSRn
"""

"""
@brief:虚拟机类型结构体
"""
class Flavor(object):
    def __init__(self, num, core, mem):
        self.num = num  #该类型总数
        self.core = core #该类型cpu core数
        self.mem = mem  #该类型mem数
   