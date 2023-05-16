import math as m
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

# parameters
temperature = 300
bandwidth = 10000000
powerTx = 3  # in dB
gainRx = 14
gainTx = 14
H_base = 51.5
H_mobile = 1.5
k = 1.38*10**-23

distance = np.arange(200, 3000)

# two-ray ground model
gainChannelDB = 10 * np.log10((H_base * H_mobile)**2 / distance ** 4)
powerRx = powerTx + gainRx + gainTx + gainChannelDB
plt.subplot(3, 2, 1)
plt.xlabel('distance(m)')
plt.ylabel('power_received(dB)')
plt.plot(distance, powerRx)
plt.title("considering only path loss")

plt.subplot(3, 2, 2)
noiseDB = 10 * m.log10(k * 300 * bandwidth)
SINR = powerRx - noiseDB
plt.xlabel('distance(m)')
plt.ylabel('SINR(dB)')
plt.plot(distance, SINR)
plt.title("considering noise")

plt.subplot(3, 2, 5)
distanceShadowing = np.arange(200, 700)
shadowing = np.random.normal(loc=0.0, scale=6, size=500)
gainChannelDB_s = 10 * \
    np.log10((H_base * H_mobile)**2 / distanceShadowing ** 4)
powerRx_s = powerTx + gainRx + gainTx + gainChannelDB_s
powerRxWithShadowing = powerRx_s + shadowing
plt.xlabel('distance(m)')
plt.ylabel('power_received(dB)')
plt.plot(distanceShadowing, powerRxWithShadowing)
plt.title("also considering shadowing")

plt.subplot(3, 2, 6)

powerRx_s = powerTx + gainRx + gainTx + gainChannelDB_s
SINRWithShadowing = powerRxWithShadowing - noiseDB
plt.xlabel('distance(m)')
plt.ylabel('SINR(dB)')
plt.plot(distanceShadowing, SINRWithShadowing)
plt.title("considering noise")

plt.show()
