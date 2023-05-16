import math as m
import numpy as np
import random
from cell import Cell
from mobile_station import MobileStation
from cell_structure import Cells
import matplotlib.pyplot as plt
import matplotlib
import csv
matplotlib.use('TKAgg')

# Constants
T = 300
number_of_cell = 19
IST = 500
BW = 1e7
power_of_BS = 3
power_of_MS = -7
gain_of_trx = 14
h_of_BS = 1.5 + 50
h_of_MS = 1.5
cellRadius = 500 / (3**0.5)

col = []
col.append(3)
col.append(4)
col.append(5)
col.append(4)
col.append(3)

# Parameters
range_of_velocity = [1, 15]
range_of_time = [1, 6]

number_of_MS = 100
total_time = 900

with open('handoff.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Time(s)', 'Source cell ID', 'Destination cell ID'])


def gen_19_num():
    one_hundred_MS = []
    for i in range(19):
        one_hundred_MS.append(random.randrange(10, 100))
    s = sum(one_hundred_MS)

    for i in range(19):
        one_hundred_MS[i] = int(100 * one_hundred_MS[i] / s)

    remaining = 100 - sum(one_hundred_MS)
    integer = 0
    while remaining != 0:
        adding = random.randrange(0, 2)
        if adding == 1:
            one_hundred_MS[integer] += 1
            remaining -= 1
        integer += 1
        if integer == 19:
            integer = 0

    return one_hundred_MS


one_hundred_MS = gen_19_num()
the_structure = Cells(number_of_cell)

all_MS = []
number = 0
initialization = 0
X = []
Y = []
testx = []
testy = []
for i in range(7):
    for k in range(len(the_structure.cells[i])):
        testx.append(the_structure.cells[i][k].center[0])
        testy.append(the_structure.cells[i][k].center[1])

for i in range(1, 6):
    for k in range(1, len(the_structure.cells[i])-1):
        for j in range(one_hundred_MS[initialization]):

            c = the_structure.cells[i][k].center
            x = random.uniform(-1 * cellRadius +
                               c[0], cellRadius + c[0])
            y = random.uniform(-3**0.5 * cellRadius/2 +
                               c[1], 3**0.5 * cellRadius/2 + c[1])
            while ((x - c[0] <= -1 * cellRadius / 2) and (y - c[1] > 3**0.5 * (x - c[0] + cellRadius) or y - c[1] < -3**0.5 * (x - c[0] + cellRadius))) or \
                    ((x - c[0] >= 1 * cellRadius / 2) and (y - c[1] > -3**0.5 * (x - c[0] - cellRadius) or y - c[1] < 3**0.5 * (x - c[0] - cellRadius))):
                x = random.uniform(-1 * cellRadius +
                                   c[0], cellRadius + c[0])
                y = random.uniform(-3**0.5 * cellRadius/2 +
                                   c[1], 3**0.5 * cellRadius/2 + c[1])
            X.append(x)
            Y.append(y)
            all_MS.append(MobileStation(
                x, y, range_of_velocity, range_of_time, the_structure.cells[i][k].information[0], number, i, k))

            the_structure.cells[i][k].mobile_stations.append(all_MS[number])

            number += 1

        initialization += 1


# B-2 Plotting the map

fig = plt.figure(0)
plt.scatter(X, Y, c='r', label="Mobile Devices")
plt.scatter(testx, testy, c='b', label="Base Station")
plt.xlabel('x(m)')
plt.ylabel('y(m)')
plt.title("Location of BS and users")
plt.axhline(y=0)
plt.axvline(x=0)
plt.legend()


##### B-2 ##################


the_structure.handoff(-0.1)
time_interval = 0.1

#print(f"MS[0].x = {all_MS[0].x}")
#print(f"MS[0].y = {all_MS[0].y}")
#print(f"MS[0].id_BS = {all_MS[0].id_BS}")

total_times_of_handoff = 0
for time in np.arange(0, 900, time_interval):
    #print(f"t = {time}")
    # Times of handoff

    for i in range(number_of_MS):
        # Moving
        all_MS[i].moving_microsecond(time, time_interval)

        # Moving the MS in the surroundings to the inner cells
        check = 0
        for p in range(1, 6):
            if the_structure.cells[p][0].is_within_cell(all_MS[i], the_structure.out_to_in(p, 0)) == True:
                check = 1
                break
        if check == 1:
            continue

        for p in range(4):
            if the_structure.cells[0][p].is_within_cell(all_MS[i], the_structure.out_to_in(0, p)) == True:
                check = 1
                break
        if check == 1:
            continue
        for p in range(4):
            if the_structure.cells[6][p].is_within_cell(all_MS[i], the_structure.out_to_in(6, p)) == True:
                check = 1
                break
        if check == 1:
            continue
        for p in range(1, 4):
            if the_structure.cells[p][p+3].is_within_cell(all_MS[i], the_structure.out_to_in(p, p+3)) == True:
                check = 1
                break
        if check == 1:
            continue

        for p in range(4, 6):
            if the_structure.cells[p][9-p].is_within_cell(all_MS[i], the_structure.out_to_in(p, 9-p)) == True:
                check = 1
                break
        if check == 1:
            continue

    total_times_of_handoff += the_structure.handoff(time)

    '''
    if time % 10 == 0:
        print(f"MS[0].x = {all_MS[0].x}")
        print(f"MS[0].y = {all_MS[0].y}")
        print(f"MS[0].id_BS = {all_MS[0].id_BS}")

    if time % 100 == 0 and time != 0:
        X.clear()
        Y.clear()
        for w in range(100):
            X.append(all_MS[w].x)
            Y.append(all_MS[w].y)

        fig = plt.figure(int(time/100))
        plt.scatter(X, Y, c='r', label="Mobile Devices")
        plt.scatter(testx, testy, c='b', label="Base Station")
        plt.xlabel('x(m)')
        plt.ylabel('y(m)')
        plt.title("Location of BS and users")
        plt.axhline(y=0)
        plt.axvline(x=0)
        plt.legend()
        '''


print(f"total_times_of_handoff = {total_times_of_handoff}")
plt.show()
