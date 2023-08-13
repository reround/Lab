#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   cv_001.py
@Time    :   2023/08/13 16:52
@Author  :   shun
@Description  :   图像基本操作
"""

import cv2 as cv
import matplotlib.pyplot as plt


filename = "./opencv/body_darkF.png"
img = cv.imread(filename)


cv.imshow("hello",img)
cv.waitKey(0)

plt.imshow(img[:,:,::-1])
plt.show()

cv.imwrite("hhh.png",img)

if __name__ == "__main__":
    pass
