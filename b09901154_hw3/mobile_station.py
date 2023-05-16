import math as m
import random


class MobileStation:
    def __init__(self, x, y, range_of_velocity, range_of_time, id_BS, number, cell_i, cell_k):
        self.x = x
        self.y = y
        self.range_of_velocity = range_of_velocity
        self.range_of_time = range_of_time
        self.id_BS = id_BS
        self.number = number
        self.cell_i = cell_i
        self.cell_k = cell_k
        self.sync_time = 0
        self.v = 0
        self.direction = 0

    def moving_microsecond(self, time, time_interval):
        if time >= self.sync_time:
            self.direction = random.uniform(0, 2 * m.pi)
            self.v = random.uniform(
                self.range_of_velocity[0], self.range_of_velocity[1])
            more_time = random.uniform(
                self.range_of_time[0], self.range_of_time[1])
            self.sync_time += more_time
            '''
            if self.number == 0:
                print(f"direction = {self.direction}")
                print(f"velocity = {self.v}")
                print(f"more_time = {more_time}")
            '''

        self.x += time_interval * self.v * m.cos(self.direction)
        self.y += time_interval * self.v * m.sin(self.direction)

    # "t" should be put in elsewhere.

    # Original: MS itself deals with the handoff.
    # However, MS can't know the whole situation, and neither does a cell.
    # Thus, I put the handoff function in the Class Cells.
