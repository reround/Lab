import numpy as np
import matplotlib.pyplot as plt

from radar.experiment import Radar, Target

radar = Radar(B=200.0e6, theta_a=3, T_sc=8)
# dis = np.arange(10, 100, 10)
# target = Target(distance=dis)
# # target
# snr = radar.compute_SNR(target.RCS, target.distance)
# print(snr)

# plt.plot(snr)
# plt.show()
# print(radar.B)
# print(radar.T_c)
# # t, LFM = radar.chirp(sweep="up")
t, LFM = radar.chirp(sweep="triangle")
# t, LFM = radar.chirp(sweep="t")
plt.plot(LFM)
plt.show()

# print(help(Radar.chirp))
