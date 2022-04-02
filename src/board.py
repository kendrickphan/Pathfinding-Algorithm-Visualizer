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

        # keep looking for user input
        for event in pygame.event.get():

            # if user exits
            if event.type == pygame.QUIT: # if quit button is pressed
                print("MANUAL EXIT")
                running = False

            # making start and end and barriers
            if pygame.mouse.get_pressed()[0]: # left mouse click 
                pos = pygame.mouse.get_pos() # get PIXEL POS of click
                if pos[1] < 800: # handle nodes
                    row, col = get_clicked_pos(pos, ROWS, WIDTH) # GET WHICH NODE INDEX SELECTED
                    node = gameinst.grid[row][col]
                    if not start and node != end: # start node init
                        start = node
                        start.make_start()
                        gameinst.start = start

                    elif not end and node != start: # end node init after start
                        end = node
                        end.make_end()
                        gameinst.end = end
                    
                    elif node != end and node != start: # wall nodes init after start/end
                        node.make_barrier()

                else: # handle buttons
                    button_sel = handle_buttons(win, gameinst, pos)
                    if button_sel == 1: # start game
                        gameinst.grid[0][0].unvisited.clear() # clearing unvisited global arr for astar and bfs
                        for row in gameinst.grid:
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
                        # draw(win, ROWS, WIDTH, gameinst)
                    elif button_sel == 3: # end game
                        print("PLAYER QUIT")
                        running = False

            # resetting nodes
            elif pygame.mouse.get_pressed()[2]: # right mouse
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
            
    print("QUITTING!")
    pygame.quit()


# HANDLES WHEN START IS PRESSED AND GAME BEGINS
def start_game(gameinst):

     # updating list of neighbors in node instances
    for row in gameinst.grid: 
        for node in row:
            node.update_neighbors(gameinst.grid)

    currentnode = gameinst.start # init

    # djikstra's set up
    if gameinst.algorithm == 1:
        unvisited = []
        unvisited.append([gameinst.start])
        for neighbor in gameinst.start.get_neighbors(): # getting start neighbors
            if neighbor != None:
                neighbor.make_open()
                unvisited[0].append(neighbor)

    # choice of algorithm 
    while 1: # algorithm loop
        if gameinst.algorithm == 1:
            unvisited = dijktras(gameinst, unvisited) 
            if unvisited == gameinst.end: # end for dijkstra's
                reconstruct_path(gameinst, gameinst.end)
                break
        elif gameinst.algorithm == 2:
            currentnode = astar(gameinst, currentnode)
            if currentnode == gameinst.start: 
                print("Path not Found.") # no possible path to end
                break
            if currentnode == gameinst.end:  # end condition for astar
                reconstruct_path(gameinst, gameinst.end)
                break
        elif gameinst.algorithm == 3:
            dfs(gameinst, currentnode)
            break
        elif gameinst.algorithm == 4:
            currentnode.unvisited.append(gameinst.start)
            bfs(gameinst, currentnode)
            reconstruct_path(gameinst, gameinst.end)
            break

        draw(gameinst.win, ROWS, WIDTH, gameinst) # updating board after round
        gameinst.end.make_end()


# FUNCTION FOR AFTER ALGORITHM EXECUTION FOR FINDING SHORTEST POSSIBLE PATH
def reconstruct_path(gameinst, currentnode):

    start = gameinst.start
    end = gameinst.end

    if not currentnode:
        return

    # print(end.get_prevnode())
    if currentnode == start: # recursion end
        gameinst.end.make_end()
        return
    # print(currentnode.get_pos())
    if not currentnode.is_end():
        currentnode.make_path()
        draw(gameinst.win, ROWS, WIDTH, gameinst)
        sleep(.05)
    #print (currentnode.get_prevnode().get_pos())
    reconstruct_path(gameinst, currentnode.get_prevnode()) 

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


# EOF board.py