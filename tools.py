#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tools.py
@Time    :   2023/07/18 16:26
@Author  :   shun
@Description  :   TODO
'''
import matplotlib.pyplot as plt

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

    


if __name__ == '__main__':
    pass