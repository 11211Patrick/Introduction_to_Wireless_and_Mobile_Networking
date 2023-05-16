import matplotlib.patches as pc
import math as m
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TKAgg')

# Constants
temperature = 300
bandwidth = 10000000
cellRadius = 500 / (3**0.5)
numberOfCell = 19
powerTx = 3  # in dB
powerRx = -13  # in dB
gainRx = 14
gainTx = 14
H_base = 51.5
H_mobile = 1.5
devices = 50
k = 1.38*10**-23

# Mobile devices
x = []
y = []

# Generating mobile devices
for i in range(devices):
    x.append(np.random.uniform(-1*cellRadius, cellRadius))
    y.append(np.random.uniform(-3**0.5 * cellRadius/2, 3**0.5 * cellRadius/2))
    while ((x[i] <= -1 * cellRadius / 2) and (y[i] > 3**0.5 * (x[i] + cellRadius) or y[i] < -3**0.5 * (x[i] + cellRadius))) or \
            ((x[i] >= 1 * cellRadius / 2) and (y[i] > -3**0.5 * (x[i] - cellRadius) or y[i] < 3**0.5 * (x[i] - cellRadius))):
        x.pop(i)
        y.pop(i)
        x.append(np.random.uniform(-1*cellRadius, cellRadius))
        y.append(np.random.uniform(-3**0.5 * cellRadius/2, 3**0.5 * cellRadius/2))

# Generating background
fig1 = plt.figure()
ax1 = fig1.add_subplot(111, aspect='equal')
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

fig2 = plt.figure()
distance = []
powerReceived = []
for i in range(devices):
    distance.append((x[i]**2 + y[i]**2)**0.5)
    # The formula of two-ray ground model
    gainChannelDB = 10*m.log10((H_base*H_mobile)**2 / distance[i]**4)
    # Using sum in dB
    powerReceived.append(powerTx + gainRx + gainTx + gainChannelDB)

plt.scatter(distance, powerReceived, c='g')
plt.xlabel('distance(m)')
plt.ylabel('received power(dB)')
plt.title("Only considering path loss")
plt.axhline(y=0)
plt.axvline(x=0)


fig3 = plt.figure()
# The formula of thermal noise
thermalNoise = k * temperature * bandwidth

# The position of surrounding BS
BS_x = []
BS_x.append(-1.5 * cellRadius)
BS_x.append(0)
BS_x.append(1.5 * cellRadius)
BS_x.append(1.5 * cellRadius)
BS_x.append(0)
BS_x.append(-1.5 * cellRadius)
BS_y = []
BS_y.append(3**0.5 * cellRadius/2)
BS_y.append(3**0.5 * cellRadius)
BS_y.append(3**0.5 * cellRadius/2)
BS_y.append(-3**0.5 * cellRadius/2)
BS_y.append(-3**0.5 * cellRadius)
BS_y.append(-3**0.5 * cellRadius/2)

interference = []

for i in range(devices):
    # Interference from the 6 BS
    I = []
    for k in range(6):
        d = ((x[i] - BS_x[k])**2 + (y[i] - BS_y[k])**2)**0.5
        iInW = 10**(powerTx/10) * ((H_base*H_mobile)**2/d**4) * \
            10**(gainRx/10) * 10**(gainTx/10)
        # Turning the gain into W
        I.append(iInW)
    interference.append(sum(I) + thermalNoise)


# Turning W into dB
interference = [10 * m.log10(i) for i in interference]

SINR = []
for i in range(devices):
    SINR.append(powerReceived[i] - interference[i])

plt.scatter(distance, SINR, c='y')
plt.xlabel('distance(m)')
plt.ylabel('SINR(dB)')
plt.title("SINR considering inteference and noise")
plt.axhline(y=0)
plt.axvline(x=0)


fig4 = plt.figure()

powerReceivedByBS = []
for i in range(devices):
    # The formula of two-ray ground model
    gainChannelDB = 10*m.log10((H_base*H_mobile)**2 / distance[i]**4)
    # Using sum in dB
    powerReceivedByBS.append(powerRx + gainRx + gainTx + gainChannelDB)

plt.scatter(distance, powerReceivedByBS, c='purple')
plt.xlabel('distance(m)')
plt.ylabel('received power by the BS(dB)')
plt.title("Only considering path loss")
plt.axhline(y=0)
plt.axvline(x=0)


fig5 = plt.figure()

# Interference from the 50 users
interferenceByMs = []
SINROfBS = []
powerReceivedByBSInW = [10**(i/10) for i in powerReceivedByBS]
sumOfPower = sum(powerReceivedByBSInW)
for i in range(devices):
    # Turning into dB; All the signals are inteference except for the original one
    interferenceByMs.append(
        10 * m.log10(sumOfPower - 10**(powerReceivedByBS[i]/10) + thermalNoise))
    SINROfBS.append(powerReceivedByBS[i] - interferenceByMs[i])

plt.scatter(distance, SINROfBS, c='blue')
plt.xlabel('distance(m)')
plt.ylabel('SINR of the BS(dB)')
plt.title("SINR considering inteference and noise")
plt.axhline(y=0)
plt.axvline(x=0)

################################### BONUS ###################################

# Mobile devices
X = []
Y = []

for i in range(numberOfCell):
    X.append([])
    Y.append([])

# Generating mobile devices

b = []
b.append(3)
b.append(4)
b.append(5)
b.append(4)
b.append(3)

fig6 = plt.figure()
c = -1
for a in range(5):
    for k in range(b[a]):
        c += 1
        for i in range(devices):

            X[c].append(np.random.uniform(-1*cellRadius + (a+1 - 3) * 1.5 *
                                          cellRadius, cellRadius + (a+1 - 3) * 1.5 * cellRadius))

            Y[c].append(np.random.uniform(-3**0.5 * cellRadius/2 + (k-int(b[a]/2))*3**0.5*cellRadius + (a % 2)*3**0.5 *
                                          cellRadius/2, 3**0.5 * cellRadius/2 + (k-int(b[a]/2))*3**0.5*cellRadius + (a % 2)*3**0.5*cellRadius/2))

            while ((X[c][i] <= -1 * cellRadius / 2 + (a+1 - 3) * 1.5 * cellRadius) and (Y[c][i] > 3**0.5 * (X[c][i] + (a+1 - 3) * 1.5 * cellRadius + cellRadius) or Y[c][i] < -3**0.5 * (X[c][i] + (a+1 - 3) * 1.5 * cellRadius + cellRadius))) or \
                    ((X[c][i] >= 1 * cellRadius / 2 + (a+1 - 3) * 1.5 * cellRadius) and (Y[c][i] > -3**0.5 * (X[c][i] + (a+1 - 3) * 1.5 * cellRadius - cellRadius) or Y[c][i] < 3**0.5 * (X[c][i] + (a+1 - 3) * 1.5 * cellRadius - cellRadius))):

                X[c].pop(i)
                Y[c].pop(i)

                X[c].append(np.random.uniform(-1*cellRadius +
                                              (a+1 - 3) * 1.5 * cellRadius, cellRadius + (a+1 - 3) * 1.5 * cellRadius))

                Y[c].append(np.random.uniform(-3**0.5 * cellRadius/2 + (k-int(b[a]/2))*3**0.5*cellRadius + (a % 2)*3**0.5 *
                                              cellRadius/2, 3**0.5 * cellRadius/2 + (k-int(b[a]/2))*3**0.5*cellRadius + (a % 2)*3**0.5*cellRadius/2))

        #plt.scatter(X, Y, c='r', label="Mobile Devices")
        # plt.legend()

for i in range(numberOfCell):
    plt.scatter(X[i], Y[i], c='r', label="Mobile Devices")
center_x = []
center_y = []
for a in range(5):
    for k in range(b[a]):
        center_x.append((a+1 - 3) * 1.5 * cellRadius)
        center_y.append((k-int(b[a]/2))*3**0.5 *
                        cellRadius + (a % 2)*3**0.5 * cellRadius/2)
        plt.scatter(center_x,  center_y, c='b', label="Base Station")
plt.xlabel('x(m)')
plt.ylabel('y(m)')
plt.title("Location of 19 BS and users")
plt.axhline(y=0)
plt.axvline(x=0)


fig7 = plt.figure()

powerBonus = []
distanceBonus = []
for i in range(numberOfCell):
    powerBonus.append([])
    distanceBonus.append([])

for k in range(numberOfCell):
    for i in range(devices):
        distanceBonus[k].append(
            ((X[k][i] - center_x[k])**2 + (Y[k][i]-center_y[k])**2)**0.5)
        # The formula of two-ray ground model
        gainBonus = 10*m.log10((H_base*H_mobile)**2 / distanceBonus[k][i]**4)
        # Using sum in dB
        powerBonus[k].append(powerRx + gainRx + gainTx + gainBonus)
    plt.scatter(distanceBonus[k], powerBonus[k], c='black')


plt.xlabel('distance(m)')
plt.ylabel('received power by BSs across 19 cells(dB)')
plt.title("Only considering path loss")
plt.axhline(y=0)
plt.axvline(x=0)


fig8 = plt.figure()

# Interference from the 50 users
interferenceBonus = []
IBonus = []
SINRBonus = []
for i in range(numberOfCell):
    interferenceBonus.append([])
    SINRBonus.append([])
    for k in range(numberOfCell):
        for j in range(devices):
            # 50 devices for each cell
            interferenceBonus[i].append((H_base*H_mobile)**2/((X[k][j] - center_x[i])**2 + (
                # Turning dB into W
                Y[k][j]-center_y[i])**2)**2 * 10**((powerRx + gainRx + gainTx)/10) + thermalNoise)
    # Sum of inteference 50 devices for 19 cells
    IBonus.append(sum(interferenceBonus[i]))
    print(i)
    print(IBonus[i])

    for l in range(devices):
        SINRBonus[i].append(powerBonus[i][l] - 10 *
                            m.log10(IBonus[i] - 10**(powerBonus[i][l]/10)))

for i in range(numberOfCell):
    col = (np.random.random(), np.random.random(), np.random.random())
    plt.scatter(distanceBonus[i], SINRBonus[i],
                c=col, label=f"{i}line")


plt.xlabel('distance(m)')
plt.ylabel('SINR of the 19 BSs(dB)')
plt.title("Also considering inteference and noise")
plt.axhline(y=0)
plt.axvline(x=0)
plt.legend()

plt.show()
