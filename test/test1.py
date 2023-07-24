#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test.py
@Time    :   2023/07/20 16:19
@Author  :   shun
@Description  :   用于测试
'''
import numpy as np
import matplotlib.pyplot as plt
from tek import Tek

# tek = Tek("D:/物理192 201711020222 张雨顺/shiyan/TEK0068.CSV")

# t, s = tek.read_data()

# f = np.fft.fft(s)
# plt.subplot(211)
# plt.plot(abs(f))
# plt.subplot(212)
# plt.plot(t, s)
# plt.show()
a=np.linspace(0, 2, 3)
b=np.linspace(0, 2, 3)
# a=a[::-1]
print(np.hstack([a,b]))

if __name__ == '__main__':
    pass