import numpy as np
import matplotlib.pyplot as plt

from Radar import Radar, Target


radar = Radar(theta_a=3,T_sc=8)
# dis = np.arange(10, 100, 10)
# target = Target(distance=dis)
# # target
# snr = radar.compute_SNR(target.RCS, target.distance)
# print(snr)

# plt.plot(snr)
# plt.show()
print(radar.f_r)
print(radar.n_p)

