#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tools.py
@Time    :   2023/07/18 16:26
@Author  :   shun
@Description  :   TODO
'''
from matplotlib import pyplot as plt
import numpy as np
import scipy



def find_heighest_peak(sequence: list) -> tuple:
    """
    寻找最大峰值索引和最大峰值

    :param list sequence: 待求序列
    :return tuple: 返回最大峰值索引和最大峰值
    """
    # 寻找峰值
    pks, locs = scipy.signal.find_peaks(sequence, height=0)
    # 最大峰值在峰值列表 pks_up 中的索引
    max_index_pks = np.argmax(locs['peak_heights'])
    # 最大峰值
    max_value = np.amax(locs['peak_heights'])
    # 最大值在序列中的索引
    max_index = pks[max_index_pks]
    # 返回最大峰值索引和最大峰值
    return (max_index, max_value)


def fig_font_size(func):
    """
    设置 matplotlib 绘图样式的装饰器，只会进行样式的设置，并不会绘图。
    原理是进行全局设置样式。

    :param _type_ func: 被装饰函数
    """
    def inner(*args, **kwargs):
        # 设置字体样式
        plt.rcParams['font.sans-serif'] = "Consolas"
        # 设置字体大小
        plt.rcParams['font.size'] = 24
        # 设置刻度向内
        plt.tick_params(axis='both', direction='in')
        # 添加刻度
        plt.grid()
        
        func(*args, **kwargs)
    
    return inner
    


if __name__ == '__main__':
    pass