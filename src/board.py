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
            if pygame.mouse.get_pressed()[0]: # left mouse
                pos = pygame.mouse.get_pos() 
                if pos[1] < 800: # handle nodes
                    row, col = get_clicked_pos(pos, ROWS, WIDTH) # GET WHICH NODE SELECTED
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
                        gameinst.grid[0][0].unvisited.clear() # clearing unvisited global arr
                        for row in gameinst.grid:
                            for node in row:
                                if node.is_open() or node.is_closed() or node.is_path():
                                    node.reset()
                        if start and end:
                            start_game(gameinst)
                    elif button_sel == 2: # reset game
                        gameinst.start, start = None, None
                        gameinst.end, end = None, None
                        newboard = make_board(gameinst.win, ROWS, WIDTH) # remaking board
                        gameinst.grid = newboard
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

    unvisited = []
    unvisited.append([gameinst.start])

    # djikstra's set up
    if gameinst.algorithm == 1:
        for neighbor in gameinst.start.get_neighbors(): # getting start neighbors
            if neighbor != None:
                neighbor.make_open()
                unvisited[0].append(neighbor)
        #print("Getting weights")

        # get box
        #board = get_weights(gameinst.grid, gameinst.start, gameinst.end)

    # choice of algorithm 
    while 1: # algorithm loop
        if gameinst.algorithm == 1:
            unvisited = dijktras(gameinst, unvisited) 
            if unvisited == gameinst.end: # end for dijkstra's
                reconstruct_path(gameinst, gameinst.end)
                gameinst.end.make_end()
                break
        elif gameinst.algorithm == 2:
            currentnode = astar(gameinst, currentnode)
            if currentnode == gameinst.start: 
                print("Path not Found.") # no possible path to end
                break
            if currentnode == gameinst.end:  # end condition for astar
                reconstruct_path(gameinst, gameinst.end)
                gameinst.end.make_end()
                break
        elif gameinst.algorithm == 3:
            ret = dfs(gameinst, currentnode)
            break
        elif gameinst.algorithm == 4:
            currentnode.unvisited.append(gameinst.start)
            ret = bfs(gameinst, currentnode)
            # reconstructing path
            # node = gameinst.start
            # while node != gameinst.end:
            #     nextnode = None
            #     leastdist = float("inf")
            #     print("here")
            #     for neighbor in node.get_neighbors():
            #         if neighbor:
            #             if neighbor.get_dist() < leastdist:
            #                 leastdist = neighbor.get_dist()
            #                 nextnode = neighbor
            #     nextnode.make_path()
            #     node = nextnode
            reconstruct_path(gameinst, gameinst.end)
            gameinst.end.make_end()
            break

        draw(gameinst.win, ROWS, WIDTH, gameinst) # updating board after round
        gameinst.end.make_end()

        # if len(unvisited) == 0:
            #print("Path not found.")
            #break
        

# def get_weights(board, start, end):
#     x1, y1 = start.get_pos()
#     x2, y2 = end.get_pos()

#     if x1 < x2:
#         maxx = x2
#         minx = x1
#     else:
#         maxx = x1 
#         minx = x2 
#     if y1 < y2:
#         maxy = y2 
#         miny = y1
#     else:
#         maxy = y1
#         miny = y2 

#     if not minx < 4:
#         minx -= 3
#     if not miny < 4:
#         miny -= 3
#     if not maxx > ROWS - 3:
#         maxx += 3
#     if not maxy > ROWS - 3:
#         maxy += 3

#     for x in range(minx, maxx + 1):
#         for y in range(miny, maxy + 1):
#             board[x][y].set_weight(randint(1,10))

#     return board

# FUNCTION FOR AFTER ALGORITHM EXECUTION FOR FINDING SHORTEST POSSIBLE PATH
def reconstruct_path(gameinst, currentnode):

    start = gameinst.start
    end = gameinst.end

    # print(end.get_prevnode())
    if currentnode == start: # recursion end
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