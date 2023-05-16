import math as m
import numpy as np
from cell import Cell
from mobile_station import MobileStation
import csv


# Column
col = []
col.append(3)
col.append(4)
col.append(5)
col.append(4)
col.append(3)

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

# The coordinate system of map begins from the surroundings.
# The inner cells on map include the information of the id and neighbors.
# The surroundings doesn't include the information neighbors.


def map():
    ids = []
    n = 0
    for i in (range(5)):
        # "col[i]" rows
        ids.append([])
        for k in range(col[i]):

            ids[i].append([])
            # "i"th col, "k"th row
            # [i[ k[ id(0), neighborhood[ ](1) ] ] ]
            ids[i][k].append(n+1)
            n += 1

    # Adding the surroundings
    # I think there are too many exceptions of id arrangement.
    # It's hard to deal with adding the surroundings and MS moving around.
    # Thus, I do it manually.
    ids.insert(0, [[12], [17], [18], [19]])
    ids[1].insert(col[0], [8])
    ids[1].insert(0, [16])
    ids[2].insert(col[1], [13])
    ids[2].insert(0, [19])
    ids[3].insert(col[2], [17])
    ids[3].insert(0, [3])
    ids[4].insert(col[3], [1])
    ids[4].insert(0, [7])
    ids[5].insert(col[4], [4])
    ids[5].insert(0, [12])
    ids.insert(6, [[1], [2], [3], [8]])

    # Adding the neighbors
    for i in (range(1, 6)):
        for k in range(1, col[i-1]+1):
            # I store them in a list.
            ids[i][k].append([])

            # The above one
            ids[i][k][1].append(ids[i][k+1][0])

            # The right two
            if i < 3:
                ids[i][k][1].append(ids[i+1][k+1][0])
                ids[i][k][1].append(ids[i+1][k][0])

            else:
                ids[i][k][1].append(ids[i+1][k][0])
                ids[i][k][1].append(ids[i+1][k-1][0])

            # The below one
            ids[i][k][1].append(ids[i][k-1][0])

            # The left two
            if i < 4:
                ids[i][k][1].append(ids[i-1][k-1][0])
                ids[i][k][1].append(ids[i-1][k][0])

            else:
                ids[i][k][1].append(ids[i-1][k][0])
                ids[i][k][1].append(ids[i-1][k+1][0])

    return ids


# The function link the id to the coordinate.
# The result coordinate is in the coordinate system of map.
def corresponding(id, column=-2, row=0):
    Map = map()
    col_and_row = []
    if column == -2:  # Finding within the inner cells
        for i in range(1, 6):
            for k in range(1, col[i-1] + 1):
                if Map[i][k][0] == id:
                    col_and_row.append(i)
                    col_and_row.append(k)
                    return col_and_row

    else:
        for i in range(5+2):
            for k in range(len(Map[i])):

                if Map[i][k][0] == id:
                    # Making sure the target is the neighbors of the original one

                    if i <= column + 1 and i >= column - 1 and k <= row + 1 and k >= row - 1:
                        col_and_row.append(i)
                        col_and_row.append(k)
                        return col_and_row

# Better way: Adding the neighbors as class cell, not just an integer
# This way, there's no need to correspond
# and we can access the position of center directly.
# Also, the "SINR" and


# (0, 0) in the map is (-1, 0) in coordinate system of position_deviation.
# And (1, 0) is (0, -1).
def position_deviation(i, k):

    position = []
    position.append((i+1 - 3) * 1.5 * cellRadius)
    if i < 0 or i > 4:
        position.append((k-2)*3**0.5 *
                        cellRadius + (i % 2)*3**0.5 * cellRadius/2)
    else:
        position.append((k-int(col[i]/2))*3**0.5 *
                        cellRadius + (i % 2)*3**0.5 * cellRadius/2)

    return position


# print(position_deviation(1, 0))

class Cells():
    def __init__(self, number_of_cells):
        self.number_of_cells = number_of_cells
        # The coordinate system of map includes the surroundings.
        information = map()
        self.cells = []

        # Cells[i][k] is the "i"th column and "k"th row cell.
        for i in range(5+2):
            self.cells.append([])
            for k in range(len(information[i])):

                # The "if...else..." here stems from the inconsistency between
                # the coordinate systems of map and position_deviation.
                if i <= 5 and i >= 1:
                    self.cells[i].append(
                        Cell(information[i][k], position_deviation(i-1, k-1), i, k))
                else:
                    self.cells[i].append(
                        Cell(information[i][k], position_deviation(i-1, k), i, k))
    '''I need to be more familiar with what the I/Os are and the type of them of each function.'''

    # Given the i and k of the surrounding cells,
    # the function outputs the center and the mobile_stations[] corresponding inner cell.
    def out_to_in(self, i,  k):
        position = corresponding(self.cells[i][k].information[0])
        info = []
        info.append(self.cells[position[0]][position[1]].center)
        info.append(self.cells[position[0]][position[1]].mobile_stations)
        return info

    '''A better design can avoid this problem 
    such as recording in which cell the MS is.
    As I don't know in which cell the MS is, I can only deal with each cases.'''
    # Handling the problem when mobile_stations[i].id_BS is the cell opposite to where mobile_stations[i] is.

    def in_to_out(self, cell, i):
        relative = []
        relative_x = -10000
        if m.dist((cell.mobile_stations[i].x, cell.mobile_stations[i].y), np.array(cell.center)) > 1000:
            relative.append(1)
            if cell.information[0] == 1:
                if abs(cell.mobile_stations[i].y - cell.center[1]) < 320:
                    relative_x = cell.mobile_stations[i].x - \
                        7.5 * cellRadius
                    relative_y = cell.mobile_stations[i].y + 250
                elif cell.mobile_stations[i].y - cell.center[1] <= 1750 and cell.mobile_stations[i].y - cell.center[1] >= 900:

                    relative_x = cell.mobile_stations[i].x - \
                        4.5 * cellRadius
                    relative_y = cell.mobile_stations[i].y - 3.5 * 500

            elif cell.information[0] == 3:
                if cell.center[1] - cell.mobile_stations[i].y <= 800 and cell.center[1] - cell.mobile_stations[i].y >= -300:
                    relative_x = cell.mobile_stations[i].x - \
                        7.5 * cellRadius
                    relative_y = cell.mobile_stations[i].y + 250

                elif cell.mobile_stations[i].y - cell.center[1] < -2.5 * 500 + 100:
                    relative_x = cell.mobile_stations[i].x - \
                        3 * cellRadius
                    relative_y = cell.mobile_stations[i].y + 4 * 500

            elif cell.information[0] == 19:
                if abs(cell.mobile_stations[i].y - cell.center[1]) < 300:
                    relative_x = cell.mobile_stations[i].x + \
                        7.5 * cellRadius
                    relative_y = cell.mobile_stations[i].y - 250
                elif cell.center[1] - cell.mobile_stations[i].y <= 1750 and cell.center[1] - cell.mobile_stations[i].y >= 900:
                    relative_x = cell.mobile_stations[i].x + \
                        4.5 * cellRadius
                    relative_y = cell.mobile_stations[i].y + 3.5 * 500

            elif cell.information[0] == 17:
                if cell.mobile_stations[i].y - cell.center[1] >= -300 and cell.mobile_stations[i].y - cell.center[1] <= 800:
                    relative_x = cell.mobile_stations[i].x + \
                        7.5 * cellRadius
                    relative_y = cell.mobile_stations[i].y - 250

                elif cell.mobile_stations[i].y - cell.center[1] > 2.5 * 500 - 100:
                    relative_x = cell.mobile_stations[i].x + \
                        3 * cellRadius
                    relative_y = cell.mobile_stations[i].y - 4 * 500

            elif cell.information[0] == 8:
                if cell.mobile_stations[i].x - cell.center[0] < 0:
                    relative_x = cell.mobile_stations[i].x + \
                        3 * cellRadius
                    relative_y = cell.mobile_stations[i].y - \
                        4 * 500
                elif cell.mobile_stations[i].x - cell.center[0] > 0:
                    relative_x = cell.mobile_stations[i].x - \
                        4.5 * cellRadius
                    relative_y = cell.mobile_stations[i].y - \
                        3.5 * 500

            elif cell.information[0] == 12:
                if cell.mobile_stations[i].x - cell.center[0] > 0:
                    relative_x = cell.mobile_stations[i].x - \
                        3 * cellRadius
                    relative_y = cell.mobile_stations[i].y + \
                        4 * 500
                elif cell.mobile_stations[i].x - cell.center[0] < 0:
                    relative_x = cell.mobile_stations[i].x + \
                        4.5 * cellRadius
                    relative_y = cell.mobile_stations[i].y + \
                        3.5 * 500

            elif cell.information[0] == 2:
                relative_x = cell.mobile_stations[i].x - \
                    7.5 * cellRadius
                relative_y = cell.mobile_stations[i].y + \
                    250

            elif cell.information[0] == 7:
                relative_x = cell.mobile_stations[i].x - \
                    3 * cellRadius
                relative_y = cell.mobile_stations[i].y + \
                    4 * 500

            elif cell.information[0] == 16:
                relative_x = cell.mobile_stations[i].x + \
                    4.5 * cellRadius
                relative_y = cell.mobile_stations[i].y + \
                    3.5 * 500

            elif cell.information[0] == 18:
                relative_x = cell.mobile_stations[i].x + \
                    7.5 * cellRadius
                relative_y = cell.mobile_stations[i].y - \
                    250

            elif cell.information[0] == 13:
                relative_x = cell.mobile_stations[i].x + \
                    3 * cellRadius
                relative_y = cell.mobile_stations[i].y - \
                    4 * 500

            elif cell.information[0] == 4:
                relative_x = cell.mobile_stations[i].x - \
                    4.5 * cellRadius
                relative_y = cell.mobile_stations[i].y - \
                    3.5 * 500

        if relative_x == -10000:
            relative.clear()

            relative.append(0)

            relative_x = cell.mobile_stations[i].x
            relative_y = cell.mobile_stations[i].y

        relative.append(relative_x)
        relative.append(relative_y)

        return relative

    # Handling the handoff and moving of MS independently

    def handoff(self, time):
        # Times of handoff
        n = 0
        # Iterating over all cells
        for i in range(1, 6):
            for k in range(1, col[i - 1]+1):

                # Iterating over all MSs of each cell
                l = len(self.cells[i][k].mobile_stations)
                j = 0
                while j < l:
                    #print(f"start i= {i}, k= {k}")

                    # Calculating the local SINR of each cell
                    relative_position = self.in_to_out(self.cells[i][k], j)
                    local_SINR = self.cells[i][k].SINR(j, relative_position)
                    # if self.cells[i][k].mobile_stations[j].number == 0:
                    # for o in range(len(self.cells[i][k].mobile_stations)):
                    # print(self.cells[i][k].mobile_stations[o].number)
                    # print(f"local_SINR{local_SINR}")

                    # Calculating the local SINR of the 6 surrounding cells
                    outer_SINR = []

                    max = -1
                    # Iterating over 6 neighbors of each cell
                    for neighbor in range(6):

                        # if self.cells[i][k].mobile_stations[j].number == 0:
                        # print(f"neighbor={neighbor}")

                        # Linking the neighbor's id to its position[i, k]
                        surrounding_pos = corresponding(
                            self.cells[i][k].information[1][neighbor], i, k)

                        info = self.out_to_in(
                            surrounding_pos[0], surrounding_pos[1])

                        # Calculating the SINR of the MS connecting to surrounding cells
                        outer_SINR.append(self.cells[surrounding_pos[0]][surrounding_pos[1]].SINR_outerMS(
                            info, relative_position))

                        # if self.cells[i][k].mobile_stations[j].number == 0:
                        # print(f"outer_SINR{outer_SINR[neighbor]}")

                        if (outer_SINR[neighbor] - local_SINR > 3):  # Threshold

                            # The first condition is to ensure the SINR is larger than the current max one.
                            # The second condition means that the SINR is the first one larger than the local one.
                            if (max != -1 and outer_SINR[neighbor] > outer_SINR[max]) or max == -1:
                                max = neighbor

                    if max != -1:  # There's a better SINR.

                        old = self.cells[i][k].mobile_stations[j].id_BS
                        # Handoff
                        new = self.cells[i][k].information[1][max]
                        self.cells[i][k].mobile_stations[j].id_BS = new

                        # Addng the MS into the new cell's list
                        # Using "corresponding" without giving the second and third parameters,
                        # the function will output the position within the inner cells.
                        max_surrounding_pos = corresponding(
                            self.cells[i][k].information[1][max])

                        # if self.cells[i][k].mobile_stations[j].number == 0:
                        #print(f"old SINR i= {i}, k= {k}")
                        # print(f"max_surrounding_pos{max_surrounding_pos}")
                        self.cells[max_surrounding_pos[0]][max_surrounding_pos[1]].mobile_stations.append(
                            self.cells[i][k].mobile_stations[j])
                        self.cells[i][k].mobile_stations[j].cell_i = max_surrounding_pos[0]
                        self.cells[i][k].mobile_stations[j].cell_k = max_surrounding_pos[1]

                        # if self.cells[i][k].mobile_stations[j].number == 0:
                        #print(f"number = {self.cells[i][k].mobile_stations[j].number}")
                        #print(f"max_out = {outer_SINR[max]}, local = {local_SINR}, j = {j}")

                        #print(f"position: {self.cells[i][k].mobile_stations[j].x}, {self.cells[i][k].mobile_stations[j].y}")
                        if not time < 0:
                            #print(f"Time(s): {round(time, 1)}, Source: {old}, Destination: {new}")
                            n += 1

                            with open('handoff.csv', 'a+') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow([round(time, 1), old, new])

                        ##print(f"max_mobile_stations {self.cells[max_surrounding_pos[0]][max_surrounding_pos[1]].mobile_stations[0].number}")

                        # Deleting the MS from the original cell's list
                        self.cells[i][k].mobile_stations.pop(j)
                        l -= 1
                        j -= 1

                        #print(f"mobile_stations {self.cells[i][k].mobile_stations[0].number}")

                    j += 1

        return n
