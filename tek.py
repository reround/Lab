#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tek.py
@Time    :   2023/07/18 17:05
@Author  :   shun
@Description  :   针对 Tek 示波器文件的类
'''
import numpy as np

class Tek(object):
    """
    Tek 示波器文件类
    """

    def __init__(self, filename) -> int:
        self.filename = filename
        self.parameters = self.read_parameters()
        self.t, self.s = self.read_data()
        self.frequency = 1 / self.parameters['Sample Interval'].astype(
            np.float64)

    def read_parameters(self) -> dict:
        """
        读取 tex 文件设置

        :return dict: 参数和值对应的字典
        """
        try:
            data = np.loadtxt(self.filename,
                              dtype="str",
                              delimiter=",",
                              usecols=(0, 1),
                              unpack=True)
            temp = {
                key: value
                for key, value in zip(data[0][:18], data[1][:18]) if key != ''
            }
            return temp
        except Exception as e:
            print(e)

    def read_data(self) -> tuple:
        """
        读取 tex 文件数据

        :return tuple: 返回第3、4列，两个列表，需要两个变量接收
        """
        try:
            data = np.loadtxt(self.filename,
                              delimiter=",",
                              usecols=(3, 4),
                              unpack=True)
            return (data[0], data[1])
        except Exception as e:
            print(e)

if __name__ == '__main__':
    pass