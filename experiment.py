#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   experiment.py
@Time    :   2023/07/17 15:11
@Author  :   shun
@Description  :   TODO
'''

import numpy as np
import matplotlib.pyplot as plt
from tools import fig_font_size

from constant import *


class Radar:
    """
    雷达类，定义了雷达相关参数
    """

    def __init__(self,
                 *args,
                 P_t=1.5e3,
                 freq=5.6e6,
                 G=45,
                 T_e=290,
                 L=6,
                 F=3,
                 B=5e6,
                 T_c=10e-6,
                 theta_e=1,
                 theta_a=1,
                 Theta_E=1,
                 Theta_A=1,
                 T_sc=2.5,
                 SNR=20,
                 f_r=300,
                 S_min=1) -> None:
        """
        初始化函数

        :param _type_ P_t: 峰值功率 W, defaults to 1.5e3
        :param _type_ freq: 雷达中心频率 Hz, defaults to 5.6e6
        :param int G: 天线增益 dB, defaults to 45
        :param int T_e: 有效噪声温度 K, defaults to 290
        :param int L: 雷达损失 dB, defaults to 6
        :param int F: 噪声系数 dB, defaults to 3
        :param _type_ B: 带宽 Hz, defaults to 5e6
        :param _type_ T_c: 调制周期 s, defaults to 10.e-6
        :param int theta_e: 俯仰角 °, 为角度制, defaults to 1
        :param int theta_a: 方位角 °, 为角度制, defaults to 1
        :param int Theta_E: 搜索俯仰角 °, 为角度制, defaults to 1
        :param int Theta_A: 搜索方位角 °, 为角度制, defaults to 1
        :param float T_sc: 扫描立体角 Omega 所用时间 s, defaults to 2.5
        :param int SNR: 信噪比 db, defaults to 2.5
        :param int f_r: 雷达的脉冲重复频率（PRF） Hz, defaults to 2.5
        :param int S_min: 最小探测功率 W, defaults to 1
        """
        self.P_t = P_t
        self.freq = freq
        self.G = G
        self.T_e = T_e
        self.L = L
        self.F = F
        self.B = B
        self.T_c = T_c
        self.theta_e = theta_e
        self.theta_a = theta_a
        self.Theta_E = Theta_E
        self.Theta_A = Theta_A
        self.T_sc = T_sc
        self.SNR = SNR
        self.f_r = f_r
        self.S_min = S_min

        # 波长
        self.lambda_ = c / self.freq
        # 目标反射脉冲数
        self.n_p = (
            (self.theta_a / 57.296) * self.T_sc * self.f_r) / (2 * np.pi)
        # 调制斜率
        self.slope = self.B / self.T_c

        # 搜索立体角
        self.Omega = self.Theta_E * self.Theta_A / (57.296**2)
        # 天线波束立体角
        self.omega = self.theta_e * self.theta_e / (57.296**2)
        # 覆盖立体角 Omega 的天线波束位置数
        self.nb = (self.Theta_E * self.Theta_A) / (self.theta_e * self.theta_a)

        # 将峰值功率转换为 dB
        self.p_peak = 10 * np.log10(self.P_t)
        # 以 dB 为单位的计算波长平方
        self.lambda_sqdb = 10 * np.log10(self.lambda_**2)
        # 以 dB 为单位的有效噪声温度
        self.T_e_db = 10 * np.log10(self.T_e)
        # 以 dB 为单位的带宽
        self.B_db = 10 * np.log10(self.B)
        # 以 dB 为单位的天线波束立体角
        self.omega_db = 10 * np.log10(self.omega)

    def get_PD(self, R: float) -> float:
        """
        计算功率密度

        :param float R: 距离
        :return float: 功率密度
        """
        return (self.P_t / (4 * np.pi * R**2))

    def compute_SNR(self, sigma, r):
        """
        使用分贝（db）计算 SNR

        :param _type_ sigma: 目标截面
        :param _type_ r: 目标距离, 单值或矢量
        """
        # 转换目标截面 sigma 到 dB
        sigmadb = 10 * np.log10(sigma)
        # 转换 (4pi)^3 到 dB
        four_pi_cub = 10 * np.log10(np.power((4.0 * np.pi), 3))
        # 目标距离的向量^4，单位为dB
        range_pwr4_db = 10 * np.log10(np.power(r, 4))

        num = self.p_peak + self.G + self.G + self.lambda_sqdb + sigmadb
        den = four_pi_cub + k_db + self.T_e_db + self.B_db + self.F + self.L + range_pwr4_db
        return (num - den)

    def compute_PAP(self, SNR, sigma, r):
        """
        使用分贝（db）计算功率孔径积

        :param _type_ SNR: 灵敏度 snr db
        :param _type_ sigma: 目标截面
        :param _type_ r: 目标距离, 单值或矢量
        """
        # 转换目标截面 sigma 到 dB
        Sigma = 10 * np.log10(sigma)
        # 4pi
        four_pi = 10 * np.log10(4.0 * np.pi)
        # 目标距离的向量^4，单位为dB
        range_pwr4_db = 10 * np.log10(np.power(r, 4))
        PAP = SNR + four_pi + k_db + self.T_e_db + self.F + self.L + range_pwr4_db + self.omega_db - Sigma - self.T_sc
        return PAP

    def chirp(self, sweep="up"):
        """
        返回合成的 LFM

        :return _type_: 时间 : t_x 和 波形 : LFM
        """
        def LFM(t_x):
            mu = 2 * np.pi * self.slope
            # 计算复数形式 LFM 的波形
            Ichannal = np.cos(mu * np.power(t_x, 2) / 2.)  # 实部
            Qchannal = np.sin(mu * np.power(t_x, 2) / 2.)  # 虚部
            # 返回合成 LFM
            return t_x, Ichannal + 1j * Qchannal
        
        # 上扫频
        if sweep=="up":
            print(sweep)
            return LFM(np.linspace(0, self.T_c, 10001))
            
        # 下扫频
        elif sweep=="down":
            print(sweep)
            return LFM(np.linspace(-self.T_c, 0, 10001))

        # 三角扫频
        elif sweep=="triangle":
            print(sweep)
            t_x_fore = np.linspace(0, self.T_c/2.0, 5001)
            t_x_behind = np.linspace(-self.T_c/2.0, 0, 5000)
            t_x = np.hstack([t_x_behind, t_x_fore])
            _, fore = LFM(t_x_fore)
            _, behind = LFM(t_x_behind)
            return t_x, np.hstack([fore, behind])
        else:
            raise Exception("The sweep mode is not exist.")
        
        
    def draw(self):
        # 设置字体样式
        plt.rcParams['font.sans-serif'] = "Consolas"
        # 设置字体大小
        plt.rcParams['font.size'] = 24
        # 设置刻度向内
        plt.tick_params(axis='both', direction='in')
        # 添加刻度
        plt.grid()
        
        LFM = self.chirp()
        # 计算 LFM 的傅里叶变换
        LFM_fft = np.fft.fftshift(np.fft.fft(LFM))

        # 绘图

        plt.plot(abs(LFM_fft))
        plt.title("LFM fft")
        plt.show()


class Pulsed_lidar(Radar):
    pass


class Coherent_lidar(Radar):
    pass


class Target:
    """
    目标类，定义了目标相关参数
    """

    def __init__(self, distance=[40], sigma=0.1) -> None:
        """
        初始化

        :param list distance: 目标距离, defaults to [40]
        :param float sigma: 截面积, defaults to 0.1
        """
        self.distance = distance
        self.sigma = sigma
        self.RCS = 10 * np.log10(self.sigma)


class TargetSet:
    """
    目标组
    """

    def __init__(self) -> None:
        self.targets = []
        self.distances = []
        self.sigma = []
        self.RCSS = 10 * np.log10(self.sigma)
        
        self.num = 0
        
    def add_Target(self, target):
        """
        添加目标

        :param Target target: 需要添加的目标
        """
        self.targets.append(target)
        self.num += 1


def Maximum_coherent_accumulation_time_limit(lambda_, a_r):
    """
    最大相干积累时间限制

    :param _type_ lambda_: 激光波长
    :param _type_ a_r: 目标径向加速度
    """
    return np.sqrt(lambda_ / (2 * a_r))


if __name__ == '__main__':
    radar = Radar()
    dis = np.arange(10, 100, 10)
    target = Target(distance=dis)
    # target
    snr = radar.compute_SNR(target.RCS, target.distance)
    print(snr)
