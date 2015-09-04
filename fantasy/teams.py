import config as cfg
from operator import mul


class Roster:
    def __init__(self, ):
        self.starter_list = cfg.starter_list
        self.position_ID = cfg.starter_num_list
        self.product = reduce(mul, self.position_ID)
        self.picked_team = [-1] * cfg.num_roster_spots
        self.points = 0

    def open(self, position_num):
        if self.product % position_num == 0:
            return True
        else:
            return False


class Player:
    def __init__(self, name, position, position_num, points):
        self.name = name
        self.position = position
        self.position_num = position_num
        self.points = float(points)
        self.taken = False
        self.round_taken = -1