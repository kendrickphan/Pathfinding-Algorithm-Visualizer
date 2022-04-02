# NODE/KEY/BUTTON CLASSES

import pygame

WIDTH = 800
ROWS = 50

RED = (253, 70, 70)                 # END
GREEN = (30, 250, 25)                # START
BLUE = (0, 255, 0)                 
YELLOW = (255, 255, 0)                # UNVISITED
WHITE = (255, 255, 255)               # RESET
BLACK = (0, 0, 0)                     # WALL
PURPLE = (216, 130, 219)              # PATH
ORANGE = (255, 165 ,0)             
GREY = (128, 128, 128)                
TURQUOISE = (200, 253, 237)           # OPEN
TURQUOISE2 = (1, 202, 175)            # CLOSED

class Node:

    unvisited = []

    def __init__(self, win, row, col, width, total_rows):
        self.row = row # INDEX
        self.col = col
        self.x = row * width # PIXEL VAL
        self.y = col * width
        self.color = WHITE # TYPE OF NODE
        self.neighbors = [] # LIST OF NEIGHBORS 
        self.prevnode = None
        self.dist = float("inf") 
        self.width = width # PIXEL WIDTH OF NODE
        self.total_rows = total_rows 
        self.win = win
        self.weight = 1


    # all unvisited neighbor functions: append and removing    
    def append_unvisited(self, node):
        self.unvisited.append(node)
    def remove_unvisited(self, node):
        self.unvisited.remove(node)

    # instance methods
    def get_pos(self):
        return self.row, self.col
    def get_coord(self):
        return self.x, self.y
    
    def get_dist(self):
        return self.dist
    def set_dist(self, dist):
        self.dist = dist
    
    def get_weight(self):
        return self.weight
    def set_weight(self, weight):
        self.weight = weight
    
    def get_prevnode(self):
        return self.prevnode
    def set_prevnode(self, prev):
        self.prevnode = prev

    def is_unvisited(self):
        return self.color == WHITE
    def is_closed(self):
        return self.color == TURQUOISE2
    def is_open(self):
        return self.color == TURQUOISE
    def is_barrier(self):
        return self.color == BLACK
    def is_start(self):
        return self.color == GREEN
    def is_end(self):
        return self.color == RED
    def is_path(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE
    def make_start(self):
        self.color = GREEN
    def make_closed(self):
        self.color = TURQUOISE2
    def make_open(self):
        self.color = TURQUOISE
    def make_barrier(self):
        self.color = BLACK
    def make_end(self):
        self.color = RED
    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, pygame.Rect(self.x, self.y, self.width, self.width))
        # if self.weight > 1:
        #     font = pygame.font.SysFont('arial', 18)
        #     if self.weight == 10:
        #         font = pygame.font.SysFont('arial', 15)
        #     text = font.render(str(self.weight), True, BLACK)
        #     win.blit(text, self.get_coord())

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1: # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        else:
            self.neighbors.append(None)
        if self.row > 0 :                  # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        else:
            self.neighbors.append(None)
        if self.col < self.total_rows - 1: # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        else:
            self.neighbors.append(None)
        if self.col > 0:                   # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
        else:
            self.neighbors.append(None)

    def get_neighbors(self):
        return self.neighbors

class Button:
    def __init__(self, win, position, text, textcolor, backgroundcolor):
        self.pos = position
        self.text = text
        self.textcolor = textcolor
        self.bgcolor = backgroundcolor

    def draw(self, win):
        # draw buttons
        font = pygame.font.SysFont("Arial", 24)
        text_render = font.render(self.text, 1, self.textcolor)
        x, y, w, h = text_render.get_rect()
        x, y = self.pos
        pygame.draw.line(win, (150, 150, 150), (x,y), (x+w,y), 5)
        pygame.draw.line(win, (150, 150, 150), (x, y - 2), (x, y + h), 5)
        pygame.draw.line(win, (50, 50, 50), (x, y + h), (x + w, y + h), 5)
        pygame.draw.line(win, (50, 50, 50), (x + w, y + h), (x + w, y), 5)
        pygame.draw.rect(win, self.bgcolor, (x, y, w, h))
        return win.blit(text_render, (x, y))
        
class Keys:
    def __init__(self, position, text, boxcolor):
        self.pos = position
        self.text = text
        self.boxcolor= boxcolor
        self.font = pygame.font.SysFont("Arial", 12)

    def draw(self, win):
        # display node with borders
        pygame.draw.rect(win, self.boxcolor, pygame.Rect(self.pos[0], self.pos[1], 16, 16))
        pygame.draw.line(win, BLACK, (self.pos[0], self.pos[1]), (self.pos[0] + 16, self.pos[1]))
        pygame.draw.line(win, BLACK, (self.pos[0], self.pos[1]), (self.pos[0], self.pos[1] + 16))
        pygame.draw.line(win, BLACK, (self.pos[0] + 16, self.pos[1]), (self.pos[0] + 16, self.pos[1] + 16))
        pygame.draw.line(win, BLACK, (self.pos[0], self.pos[1] + 16), (self.pos[0] + 16, self.pos[1] + 16))
        text_render = self.font.render(self.text, 1, BLACK)
        win.blit(text_render, (self.pos[0] + 20, self.pos[1]))

        # display header KEYS
        keyfont = pygame.font.SysFont("Arial", 16)
        text_render2 = keyfont.render("KEY: ", 1, BLACK)
        win.blit(text_render2, (50, 830))

        # display keys box outline
        pygame.draw.line(win, BLACK, (40, 820), (760, 820))
        pygame.draw.line(win, BLACK, (40, 820), (40, 880))
        pygame.draw.line(win, BLACK, (40, 880), (760, 880))
        pygame.draw.line(win, BLACK, (760, 820), (760, 880))
        pygame.draw.line(win, BLACK, (390, 835), (390, 870))
        


        

