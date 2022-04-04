# draws board/lines in pygame gui board
# mainly handles drawing gui components

from node import *
import pygame

def draw_board(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, TEAL, (0, i * gap), (width, i * gap)) # HORIZ LINE
		for j in range(rows):
			pygame.draw.line(win, TEAL, (j * gap, 0), (j * gap, width)) # VERT LINES
	pygame.draw.line(win, BLACK, (0, rows * gap), (width, rows * gap), 3) # FINAL HORIZ LINE
def draw_barriers(win, gameinst):
	for barrier in gameinst.barriers:
		barrier.make_barrier(win)
def draw_path(win, gameinst):
	for path in gameinst.paths:
		path.make_path(win)
def draw_start(win, gameinst):
	gameinst.start.make_start(win)
def draw_end(win, gameinst):
	gameinst.end.make_end(win)

def draw_cost(win, gameinst):
	if gameinst.cost == 0:
		coststr = pygame.font.SysFont("Arial", 16)
		text_render = coststr.render("", 1, BLACK)
		win.blit(text_render, (450, 950))
	else:
		coststr = pygame.font.SysFont("Arial", 16)
		text_render = coststr.render("Path Cost = " + str(gameinst.cost), 1, BLACK)
		win.blit(text_render, (432, 960))

# draws nodes in pygame
def draw(win, rows, width, gameinst):
	win.fill(GREY)

	for row in gameinst.grid:
		for node in row:
			node.draw(win)

	draw_board(win, rows, width) # draw grid lines
	draw_barriers(win, gameinst)
	draw_path(win, gameinst)
	if gameinst.start:
		draw_start(win, gameinst)
	if gameinst.end:
		draw_end(win, gameinst)
	draw_buttons(win, gameinst) # draw buttons
	draw_key(win)
	draw_cost(win, gameinst)

	pygame.display.update()

def create_buttons(win):
	djikstra_button = Button(win, (250, 900), "Dijkstra's", BLACK, WHITE)
	astar_button = Button(win, (100, 900), "     A*    ", BLACK, YELLOW)
	dfs_button = Button(win, (450, 900), "    DFS    ", BLACK, WHITE)
	bfs_button = Button(win, (600, 900), "    BFS   ", BLACK, WHITE)
	start_button = Button(win, (350, 950), " START ", BLACK, GREEN)		
	reset_button = Button(win, (25, 950), " RESET ", BLACK, ORANGE)
	exit_button = Button(win, (750, 950), " X ", BLACK, RED)
	return [djikstra_button, astar_button, dfs_button, bfs_button, start_button, reset_button, exit_button]

def draw_buttons(win, gameinst):
	for button in gameinst.buttons:
		button.draw(win)


# finding button pressed, handle button press
def handle_buttons(win, gameinst, pos):
	x, y = pos
	if y < 925 and y > 900: # selecting a button
		if x > 100 and x < 200:
			turn_to_white(gameinst)
			gameinst.buttons[1].bgcolor = YELLOW
			gameinst.algorithm = 2
		elif x > 250 and x < 350:
			turn_to_white(gameinst)
			gameinst.buttons[0].bgcolor = YELLOW
			gameinst.algorithm = 1
		elif x > 450 and x < 550:
			turn_to_white(gameinst)
			gameinst.buttons[2].bgcolor = YELLOW
			gameinst.algorithm = 3
		elif x > 600 and x < 700:
			turn_to_white(gameinst)
			gameinst.buttons[3].bgcolor = YELLOW
			gameinst.algorithm = 4
		button_sel = 0 
	elif y < 1000 and y > 950 and x > 350 and x < 450: # start
		button_sel = 1
	elif y < 1000 and y > 950 and x > 25 and x < 125: # reset
		button_sel = 2
	elif y < 1000 and y > 950 and x > 750 and x < 800: # exit
		button_sel = 3
	else: # none
		button_sel = 5

	draw_buttons(win, gameinst)

	return button_sel

# helper function to draw buttons
def turn_to_white(gameinst):
	for button in gameinst.buttons[0:4]:
		button.bgcolor = WHITE

# main function to draw keys
def draw_key(win):
	key_start = Keys((100, 850) , "- start", GREEN)
	key_end = Keys((210, 850) , "- end", RED)
	key_wall = Keys((320, 850) , "- wall", BLACK)
	key_searched = Keys((430, 850), "- visited", TURQUOISE2)
	key_possible = Keys((540, 850) , "- unvisited", TURQUOISE)
	key_path = Keys((650, 850) , "- shortest path", PURPLE)

	key_start.draw(win)
	key_end.draw(win)
	key_wall.draw(win)
	key_searched.draw(win)
	key_possible.draw(win)
	key_path.draw(win)


