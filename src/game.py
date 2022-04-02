#Main game file for pathfinding algorithm

import pygame

class Game:
    def __init__(self, win, grid, buttons):
        self.win = win
        self.grid = grid
        self.buttons = buttons
        self.algorithm = 1
        self.start = None
        self.end = None
        self.barriers = []
        self.paths = []

    

#EOF game.py