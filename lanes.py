import pygame



class Lanes:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # 2 lanes only
        self.lane_width = self.width // 2

        self.lanes = [
            self.lane_width // 2,                      # left lane
            self.lane_width + self.lane_width // 2    # right lane
        ]

    def get_lane_x(self, lane_index):
        return self.lanes[lane_index]
