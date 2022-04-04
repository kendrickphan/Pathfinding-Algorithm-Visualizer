#Main game file for pathfinding algorithm

import pygame

class Game:
    def __init__(self, win, grid, buttons):
        self.win = win
        self.grid = grid
        self.buttons = buttons
        self.algorithm = 2
        self.start = None
        self.end = None
        self.barriers = []
        self.paths = []
        self.cost = 0

    

#EOF game.py