import math as m
import numpy as np
import matplotlib.patches as pc
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

# parameters
temperature = 300
bandwidth = 10000000
ISD = 500
cellRadius = 500 / (3**0.5)
numberOfCell = 19
powerTx = 3  # in dB
powerRx = -30  # in dB
gainRx = 14
gainTx = 14
h_base = 51.5
h_mobile = 1.5
devices = 50
k = 1.38*10**-23
size_BS_buffer = 6000000
total_time = 1000
bandwidth_MS = bandwidth / devices

# Column
col = []
col.append(3)
col.append(4)
col.append(5)
col.append(4)
col.append(3)

# 1.

# Mobile devices
x = []
y = []

# Generating mobile devices
for i in range(devices):
    x.append(np.random.uniform(-1*cellRadius, cellRadius))
    y.append(np.random.uniform(-3**0.5 * cellRadius/2, 3**0.5 * cellRadius/2))
    while ((x[i] <= -1 * cellRadius / 2) and (y[i] > 3**0.5 * (x[i] + cellRadius) or y[i] < -3**0.5 * (x[i] + cellRadius))) or \
            ((x[i] >= 1 * cellRadius / 2) and (y[i] > -3**0.5 * (x[i] - cellRadius) or y[i] < 3**0.5 * (x[i] - cellRadius))) or m.dist([x[i], y[i]], [0, 0]) < 1:
        x.pop(i)
        y.pop(i)
        x.append(np.random.uniform(-1*cellRadius, cellRadius))
        y.append(np.random.uniform(-3**0.5 * cellRadius/2, 3**0.5 * cellRadius/2))

# Generating background
fig = plt.figure(0)
ax1 = fig.add_subplot(111, aspect='equal')
ax1.add_patch(
    pc.Rectangle(
        (-cellRadius/2, -3**0.5*cellRadius/2),
        cellRadius,
        cellRadius * 3**0.5,

        color='#7FC080'
    )
)
triangleX = [-cellRadius, -cellRadius/2, -cellRadius/2]
triangleY = [0, -3**0.5*cellRadius/2, 3**0.5*cellRadius/2]
plt.fill(triangleX, triangleY, '#7FC080')
trianglex = [cellRadius, cellRadius/2, cellRadius/2]
triangley = [0, -3**0.5*cellRadius/2, 3**0.5*cellRadius/2]
plt.fill(trianglex, triangley, '#7FC080')

# Generating points
plt.scatter(x, y, c='r', label="Mobile Devices")
plt.scatter(0, 0, c='b', label="Base Station")

plt.xlabel('x(m)')
plt.ylabel('y(m)')
plt.title("Location of BS and users")
plt.axhline(y=0)
plt.axvline(x=0)
plt.legend()

# 2.
'''
The noise can be ignored compared with interference.
Proof:
Noise = kTB = 1.38 * 10**-23 * 300 * 10**7 / 50 ~= 10 ** -15
Pt * Gt * Gr in W = 10** ((14 + 14 + 3)/10) ~ 10**3
Min interference = (51.5 * 1.5)**2 / 750**4 (min_dist) * 10**3 = 2 * 10**(-5)
Q.E.D.
'''
# center of 19 cells
center_BS_x = []
center_BS_y = []
for i in range(5):
    for k in range(col[i]):
        center_BS_x.append((i+1 - 3) * 1.5 * cellRadius)
        center_BS_y.append((k-int(col[i]/2))*3**0.5 *
                           cellRadius + (i % 2)*3**0.5 * cellRadius/2)
distance_BS_MS = []
Shannon_capacity = []
for i in range(devices):
    distance_BS_MS.append(m.dist([x[i], y[i]], [0, 0]))
    surroundings = [4, 5, 8, 10, 13, 14]
    interference = 0

    # The interference from the nearest 6 BS dominates so I ignore the remaining BS.
    for k in surroundings:
        interference += (h_base * h_mobile)**2 / m.dist([center_BS_x[k], center_BS_y[k]], [
            x[i], y[i]])**4 * 10**((gainRx + gainTx + powerTx) / 10)

    signal = (h_base * h_mobile)**2 / \
        distance_BS_MS[i]**4 * 10**((gainRx + gainTx + powerTx) / 10)
    Shannon_capacity.append(bandwidth_MS * m.log2(1 + signal / interference))

fig = plt.figure(1)
plt.scatter(distance_BS_MS, Shannon_capacity, c='blue')
plt.xlabel('distance(m)')
plt.ylabel('Shannon capacity of the BS (bits/s)')
plt.axhline(y=0)
plt.axvline(x=0)

# 3.
fig = plt.figure(2)
# Assuming the traffic arrival for each mobile device follows constant bit rate (CBR)
# We further assume that the parameter of CBR, X bits/s, is the same for each mobile station.
CBR = [40 / 50 * 10**6, 50 / 50 * 10**6, 60 / 50 * 10**6]

output_BS = sum(Shannon_capacity)
bits_loss_p = []
# print(f"output BS{output_BS}")

for i in range(3):
    buffer = 0
    bits_loss_p.append([])
    for k in range(total_time):
        if CBR[i]*50 - output_BS + buffer > 0:
            if CBR[i]*50 - output_BS + buffer <= size_BS_buffer:
                buffer = CBR[i]*50 - output_BS + buffer
                bits_loss_p[i].append(0)

            else:
                buffer = size_BS_buffer
                bits_loss_p[i].append(
                    (CBR[i]*50 - output_BS + buffer - size_BS_buffer)/(CBR[i]*50))

        else:
            bits_loss_p[i].append(0)

    bits_loss_p[i] = sum(bits_loss_p[i]) / total_time


plt.bar(CBR, bits_loss_p, color='b', width=5 * 10**4)
plt.xlabel('traffic load(bits/s)')
plt.ylabel('bits loss probability')
plt.title("CBR")

############### Bonus #################

fig = plt.figure(3)
Lambda = [48 * 10**6, 55 * 10**6, 60 * 10**6]
bits_loss_p_Poisson = []


'''Poisson distribution, which means x bits arrives per second at the traffic buffer of the BS in the simulation duration 
We further assume that the parameter λ bits/s, is the same for each mobile station.'''
for i in range(3):
    buffer = 0
    bits_loss_p_Poisson_each = 0
    for k in range(total_time):
        temp = np.random.poisson(lam=Lambda[i])
        if temp - output_BS + buffer > 0:
            if temp + buffer - output_BS < size_BS_buffer:
                buffer = temp + buffer - output_BS

            else:
                buffer = size_BS_buffer
                bits_loss_p_Poisson_each += (temp + buffer -
                                             output_BS - size_BS_buffer) / temp

    bits_loss_p_Poisson.append(bits_loss_p_Poisson_each/total_time)


plt.bar(Lambda, bits_loss_p_Poisson, color='r', width=10**6)
plt.xlabel('traffic load(bits/s)')
plt.ylabel('bits loss probability')
plt.title("Poisson Packet Arrival")

plt.show()
