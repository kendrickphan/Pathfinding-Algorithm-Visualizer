# Board handler/gui

from node import Node
from algo import *
from game import Game
from drawboard import *

import pygame

from random import randint
from time import sleep


# MAIN FUNCTION FOR GAME EXECUTION
def gui():
    pygame.display.init() # INIT PYGAME FOR GUI
    pygame.font.init()
    win = pygame.display.set_mode((WIDTH, WIDTH + 200))
    pygame.display.set_caption("Pathfinding Algorithm Visualizer v2.0")
    #pygame.display.flip()

    board = make_board(win, ROWS, WIDTH) # INIT 2D ARRAY OF NODE INSTANCE OBJECTS
    buttons = create_buttons(win) # CREATING BUTTONS
    
    gameinst = Game(win, board, buttons) # init game class for easy handling

    start = None
    end = None

    # GAME LOOP
    running = True 
    while running: 
        draw(gameinst.win, ROWS, WIDTH, gameinst) # draws board at the top of every loop

        
     # updating list of neighbors in node instances
        for row in gameinst.grid: 
            for node in row:
                node.update_neighbors(gameinst.grid)

        # keep looking for user input
        for event in pygame.event.get():

            # if user exits
            if event.type == pygame.QUIT: # MAIN QUIT BUTTON
                print("MANUAL EXIT")
                running = False

            # making start and end and barriers/button select
            if pygame.mouse.get_pressed()[0]: # LEFT MOUSE 
                pos = pygame.mouse.get_pos() # get PIXEL POS of click
                if pos[1] < 800: # handle nodes
                    row, col = get_clicked_pos(pos, ROWS, WIDTH) # GET WHICH NODE INDEX SELECTED
                    node = gameinst.grid[row][col]
                    if not start and node != end: # start node init
                        start = node
                        start.make_start(gameinst.win)
                        gameinst.start = start

                    elif not end and node != start: # end node init after start
                        end = node
                        end.make_end(gameinst.win)
                        gameinst.end = end
                    
                    elif node != end and node != start: # wall nodes init after start/end
                        node.make_barrier(gameinst.win) 
                        gameinst.barriers.append(node) # add to arr of barriers

                else: # handle buttons
                    button_sel = handle_buttons(win, gameinst, pos)
                    if button_sel == 1: # start game
                        gameinst.grid[0][0].unvisited.clear() # clearing unvisited global arr for astar and bfs
                        reset_dist(gameinst) # resets node distances attribute
                        gameinst.paths.clear() # clears list of paths for gui
                        gameinst.end.make_end(gameinst.win) # remakes end
                        for row in gameinst.grid: # resetting color for gui
                            for node in row:
                                if node.is_open() or node.is_closed() or node.is_path(): # resetting board 
                                    node.reset()
                        if start and end: # starting game only if start/end node exist
                            start_game(gameinst)
                    elif button_sel == 2: # reset game
                        gameinst.start, start = None, None
                        gameinst.end, end = None, None
                        newboard = make_board(gameinst.win, ROWS, WIDTH) # remaking board
                        gameinst.grid = newboard # reassigning board
                        gameinst.barriers.clear() # clearing barriers arr for gui
                        gameinst.paths.clear() # clearing paths arr for gui
                        draw(win, ROWS, WIDTH, gameinst)
                    elif button_sel == 3: # end game
                        print("PLAYER QUIT")
                        running = False
                    
                    button_sel = 0

            # resetting nodes
            elif pygame.mouse.get_pressed()[2]: # RIGHT MOUSE
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)

                node = gameinst.grid[row][col]
                node.reset()
                if node == start: #if selected node is start/end
                    gameinst.start = None
                    start = None
                elif node == end:
                    gameinst.end = None
                    end = None
                elif node in gameinst.barriers:
                    gameinst.barriers.remove(node)
            
    print("QUITTING!")
    pygame.quit()


# HANDLES WHEN START IS PRESSED AND GAME BEGINS
def start_game(gameinst):

     # updating list of neighbors in node instances
    for row in gameinst.grid: 
        for node in row:
            node.update_neighbors(gameinst.grid)

    currentnode = gameinst.start # init
    if gameinst.algorithm == 1:
        currentnode.unvisited.append(currentnode)
        currentnode.set_dist(0)

    cost = 0
    gameinst.cost = cost

    # choice of algorithm 
    while 1: # algorithm loop
        if gameinst.algorithm == 1:
            # unvisited = dijktras(gameinst, unvisited) 
            # if unvisited == gameinst.end: # end for dijkstra's
            #     reconstruct_path(gameinst, gameinst.end)
            #     break
            currentnode = dijkstras(gameinst, currentnode)
            if not currentnode:
                print("Path not Found")
                break
            if currentnode.is_end():
                cost = reconstruct_path(gameinst, gameinst.end, cost)
                break
        elif gameinst.algorithm == 2:
            currentnode = astar(gameinst, currentnode)
            if currentnode == gameinst.start: 
                print("Path not Found.") # no possible path to end
                currentnode.unvisited.clear()
                break
            if currentnode == gameinst.end:  # end condition for astar
                cost = reconstruct_path(gameinst, gameinst.end, cost)
                currentnode.unvisited.clear()
                break
        elif gameinst.algorithm == 3:
            currentnode = dfs(gameinst, currentnode)
            if currentnode == gameinst.end:
                cost = reconstruct_path(gameinst, gameinst.end, cost)
                break
        elif gameinst.algorithm == 4:
            currentnode.unvisited.append(gameinst.start)
            bfs(gameinst, currentnode)
            cost = reconstruct_path(gameinst, gameinst.end, cost)
            break
        

        draw(gameinst.win, ROWS, WIDTH, gameinst) # updating board after round
        gameinst.end.make_end(gameinst.win)
    
    gameinst.cost = cost
    print(gameinst.cost)


# FUNCTION FOR AFTER ALGORITHM EXECUTION FOR FINDING SHORTEST POSSIBLE PATH
def reconstruct_path(gameinst, currentnode, cost):

    start = gameinst.start
    end = gameinst.end

    if not currentnode:
        return

    # print(end.get_prevnode())
    if currentnode == start: # recursion end
        gameinst.end.make_end(gameinst.win)
        return cost
    # print(currentnode.get_pos())
    if not currentnode.is_end():
        gameinst.paths.append(currentnode)
        currentnode.make_path(gameinst.win)
        cost += 1
        draw(gameinst.win, ROWS, WIDTH, gameinst)
        sleep(.05)
    #print (currentnode.get_prevnode().get_pos())
    return reconstruct_path(gameinst, currentnode.get_prevnode(), cost) 

# create board list and populate with node instances
def make_board(win, rows, width):
    board = []
    gaps = width // rows
    for i in range(rows):
        board.append([])
        for j in range(rows):
            node = Node(win, i, j, gaps, rows)
            board[i].append(node)

    return board

# fetches user click position for node object
def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

def reset_dist(gameinst):
    for row in gameinst.grid:
        for node in row:
            node.set_dist(float("inf"))


# EOF board.py