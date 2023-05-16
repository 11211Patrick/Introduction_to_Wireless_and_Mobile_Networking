import math as m
import numpy as np


# Constants
T = 300
number_of_cells = 19
IST = 500
cellRadius = 500 / (3**0.5)
BW = 1e7
power_of_BS = 3
power_of_MS = -7
gain_of_trx = 14
h_of_BS = 1.5 + 50
h_of_MS = 1.5

# A cell includes the information of the id, neighbors, and the position of center.


class Cell:
    def __init__(self, information, center, i, k):

        # "information" = [id, [neighbors]]
        self.information = information
        # "center" = [x,y]
        self.center = center
        # mobile_stations is a list of object of class MobileStation
        self.mobile_stations = []
        self.col = i
        self.row = k

    # Calculating the SINR of a specific MS
    def SINR(self, number, pos):

        total_power = 0
        signal = 0

        for i in range(len(self.mobile_stations)):
            '''Error: I should iterate over the MS in the specific radius.
                Otherwise, when a MS moving quickly, it may interfere the BS
                but not in the mobile_stations[] yet. 
                However, in this problem, every Ms moves slowly
                and the time unit is small. A MS that can interfere the most 
                but not in mobile_stations[] is 251m away from the BS.
                Thus, I choose "signal / ((h_of_BS * h_of_MS) ** 2 / 251 **4)"
                when there's nothing in the mobile_stations[].
                In addition, if MS A is phsically in cell B 
                but in the mobile_stations[] of cell C, A can't sensed by B's neighbors.
                I assume when A is phsically in the mobile_stations[] of C, 
                A is also physically close to C.'''

            if i != number:
                distance = m.dist(
                    (self.mobile_stations[i].x, self.mobile_stations[i].y), np.array(self.center))
                if distance == 0:
                    distance = 1e-13
                interference = (h_of_BS * h_of_MS) ** 2 / distance ** 4
                total_power += interference

            else:
                distance = m.dist(
                    (pos[1], pos[2]), np.array(self.center))
                if distance == 0:
                    distance = 1e-13
                signal = (h_of_BS * h_of_MS) ** 2 / distance ** 4
        #print(f"local_signal= {signal}")
        if total_power == 0:
            # If there's no interference
            # The least interfernce is (h_of_BS * h_of_MS) ** 2 / 251 ** 4

            return 10 * m.log10(251 ** 4 / (h_of_BS * h_of_MS) ** 2 * signal)
        #print(f"MS.id {self.mobile_stations[number].number}")
        #print(f"signal = {signal}")
        #print(f"total_power = {total_power}")
        SINR = 10 * m.log10(signal / total_power)

        return SINR

    # Calculating the SINR of the MS outside the cell

    def SINR_outerMS(self, info, pos):

        if pos[0] == 1 and self.information[0] in [5, 6, 9, 10, 11, 14, 15] or m.dist((pos[1], pos[2]), np.array(self.center)) > 1000:
            # if pos[0] == 1 and self.information[0] in [5, 6, 9, 10, 11, 14, 15]:
            #print(f"pos[0]=1, BS= {self.information[0]}")
            #print(f"MS.x= {pos[1]}, MS.y= {pos[2]}")
            return -20000

        # "info" is the information of the corresponding inner cells
        # because the surrounding cells don't have mobile_stations[].
        # But the interference neighbors are subject to need their mobile_stations[].
        # Better way, linking the surrounding cells to the inner ones (sharing the information)

        total_power = 0
        signal = 0

        for i in range(len(info[1])):

            distance = m.dist(
                (info[1][i].x, info[1][i].y), np.array(info[0]))
            if distance == 0:
                distance = 1e-13
            interference = (h_of_BS * h_of_MS) ** 2 / distance ** 4
            total_power += interference
        # The distance
        distance = m.dist(
            (pos[1], pos[2]), np.array(self.center))
        #print(f"total= {total_power}")
        if distance == 0:
            distance = 1e-13
        signal = (h_of_BS * h_of_MS) ** 2 / distance ** 4
        #print(f"signal= {signal}")
        #print(f"default= {(251 ** 4 / (h_of_BS * h_of_MS) ** 2)**(-1)}")
        if total_power == 0:  # If there's no interference
            return 10 * m.log10(251 ** 4 / (h_of_BS * h_of_MS) ** 2 * signal)

        SINR = 10 * m.log10(signal / total_power)
        #print(f"cell.id = {self.information[0]}")
        #print(f"signal = {signal}")
        #print(f"total_power = {total_power}")
        return SINR

    # For the surrounding cells to detect whether there's any cell within it
    # If yes, moving the MS to the corresponding inner cell
    def is_within_cell(self, MS, info):

        relative_x = MS.x - self.center[0]
        relative_y = MS.y - self.center[1]

        if not(((relative_x < -1 * cellRadius / 2) and (relative_y > 3**0.5 * (relative_x + cellRadius) or relative_y < -3**0.5 * (relative_x + cellRadius))) or
               ((relative_x > 1 * cellRadius / 2) and (relative_y > -3**0.5 *
                (relative_x - cellRadius) or relative_y < 3**0.5 * (relative_x - cellRadius)))
               or (abs(relative_x) <= cellRadius and abs(relative_y) > 3**0.5 * cellRadius / 2)):

            # if MS.number == 0:
            #print(f"within this cell {self.information[0]}")
            #print(f"relative_x = {relative_x}")
            #print(f"relative_y = {relative_y}")

            MS.x = info[0][0] + relative_x
            MS.y = info[0][1] + relative_y

            # In the surroundings
            return True

        return False

    def print_cell(self):
        print("id: " + str(self.information[0]))
        if len(self.information) > 1:
            print("neighbors " + str(self.information[1]))
        else:
            print("None")
        print("position of center:", self.center)
        print("# of MS: " + str(len(self.mobile_stations)))
        print(f"column:{self.col}, row:{self.row}")
