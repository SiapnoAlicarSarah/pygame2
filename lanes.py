import pygame


class Lanes:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.lane_width = self.width // 3

        self.lanes = [
            self.lane_width // 2,
            self.lane_width + self.lane_width // 2,
            2 * self.lane_width + self.lane_width // 2
        ]

    def get_lane_x(self, lane_index):
        return self.lanes[lane_index]
