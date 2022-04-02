# algo.py
# algorithms : A*, Dijkstra's, DFS, BFS

from node import *
from drawboard import *

# ASTAR
def astar(gameinst, currentnode):

    board = gameinst.grid
    start = gameinst.start
    end = gameinst.end

    neighbors = []

    for neighbor in currentnode.get_neighbors():
        if not neighbor.is_closed() and not neighbor.is_barrier():
            neighbors.append(neighbor) # getting neighbors

    for node in neighbors:
        if node.is_unvisited() or node.is_open() or node.is_end(): # a little redundant check for posteriety
            node.make_open() 
            currentnode.append_unvisited(node) # adds to unvisited list
            dist = calc_dist(board, start, end, node) 
            if node.get_dist() > dist: # if new distance is smaller than exisiting
                node.set_dist(dist)
                node.set_prevnode(currentnode)
            if currentnode != start:   
                currentnode.make_closed() # marking node as closed
                if currentnode in currentnode.unvisited:
                    node.remove_unvisited(currentnode) # removes from unvisited list

    
    if len(neighbors) == 0: # IF NO VALID NEIGHBOR NODES edge condition
        #if currentnode.unvisited[0] == start: # if no possible way to get to end node
        currentnode.make_closed()
        if currentnode in currentnode.unvisited:
            currentnode.remove_unvisited(currentnode)
        if len(currentnode.unvisited) == 0:
            return start # if no open/unvisited nodes, then return start FAILURE TO FIND ROUTE
        else:
            return calc_unvisited(board, start, end, currentnode) # FINDING NEXTNODE IF NO NEIGHBORS
        #else:
            #return currentnode.get_prevnode()
        #loop through previous nodes and check for legal neigbors
        #if completely blocked, return error of blockage and possible reset the board

    leastdist = float("inf")
    
    for node in currentnode.unvisited: # finding next current node REGULAR CONDITION
        dist = node.get_dist()
        if dist <= leastdist:
            leastdist = dist
            currentnode = node
    #print(currentnode.get_pos()) for debugging
    return currentnode

# helper function for no valid neighbors edge condition
def calc_unvisited(board, start, end, currentnode):
    leastdist = -1
    for node in currentnode.unvisited: # FINDING NEXT CURRENT NODE
        dist = calc_dist2(board, end, node)
        if leastdist < 0:
            leastdist = dist
            currentnode = node
        elif dist <= leastdist:
            leastdist = dist
            currentnode = node
    #print(currentnode.get_pos()) for debugging
    return currentnode

# distance from end to node
def calc_dist2(board, end, node):
    x1, y1 = node.get_pos()
    x2, y2 = end.get_pos()
    return abs(x1 - x2) + abs(y1 - y2)

# distance from end and start to node
def calc_dist(board, start, end, node):
    x1, y1 = node.get_pos()
    x2, y2 = start.get_pos()
    x3, y3 = end.get_pos()
    #print(str(abs((abs(x1 - x2) + abs(y1 - y2)))) + ", " + str((abs(x1 - x3) + abs(y1 - y3))))
    return abs((abs(x1 - x2) + abs(y1 - y2)) + (abs(x1 - x3) + abs(y1 - y3)))
                # distance from start           # distance from end
# EOF aster.py

# bfs
def bfs(gameinst, currentnode):

    win = gameinst.win
    board = gameinst.grid
    start = gameinst.start
    end = gameinst.end

    while len(currentnode.unvisited) != 0: # WHILE QUEUE IS NOT EMPTY
        nownode = currentnode.unvisited.pop(0) # POP FROM QUEUE
        for node in nownode.get_neighbors(): # HANDLE NEIGHBORS
            if node.is_unvisited(): 
                currentnode.unvisited.append(node)
                node.make_open()
                node.set_prevnode(nownode)
            elif node.is_end(): # EMD COND
                nownode.unvisited.clear() # CLEAR IN CASE OF RESET
                node.set_prevnode(nownode) 
                return 0
            elif node is None:
                continue
            draw(win, ROWS, WIDTH, gameinst)
        if not nownode.is_start(): # CLOSE POPPED NODE
            nownode.set_dist(calc_dist(board, start, end, nownode))
            nownode.make_closed()
            draw(win, ROWS, WIDTH, gameinst)

# EOF bfs.py

#dfs
def dfs(gameinst, currentnode):

    win = gameinst.win
    board = gameinst.grid
    start = gameinst.start
    end = gameinst.end

    neighbors = get_neighbors(currentnode)
    for node in neighbors:

        if node is None or node.is_closed() or node.is_start() or node.is_barrier():
            continue
        if node.is_end(): # END COND
            return 0
        
        node.make_open()
        draw(win, ROWS, WIDTH, gameinst)
    for node in neighbors: # CHECKING NEIGHBORS
        if node is None:
            continue
        if not node.is_closed() and not node.is_barrier() and not node.is_start(): 
            node.make_closed() # close node
            draw(win, ROWS, WIDTH, gameinst)

            if dfs(gameinst, node) == 0: # RECURSIVELY CALL DFS
                return 0
            
# HELPER FUNCTION TO GET NEIGHBORS IN PROPER ORDER
def get_neighbors(currentnode):
    neighbors = []

    # fill list "neighbors"
    for neighbor in currentnode.get_neighbors():
            neighbors.append(neighbor)
    
    #convert ordering to clockwise    
    new_neighbors = [neighbors[1], neighbors[2], neighbors[0], neighbors[3]]
    return new_neighbors
# EOF dfs.py

#Adjusting weights + potential gradient of path (light to dark)
def dijktras(gameinst, unvisited):

    board = gameinst.grid
    start = gameinst.start
    end = gameinst.end
    win = gameinst.win

    # unvisited = [[prevnode, neighbor node 1, 2, 3, 4], []]
    for setof in unvisited:
        # print("prev node = " + str(setof[0].get_pos()))
        for currentnode in setof:
            # print("currentnode = " + str(currentnode.get_pos()))
            if currentnode == None: # if out of bounds
                continue
            if currentnode.is_unvisited() or currentnode.is_open() or currentnode.is_end():
                currentnode.make_closed() 
                
                # has to be here
                draw(win, ROWS, WIDTH, gameinst)
                dist = calc_dist3(board, currentnode, setof[0]) # getting distance with weight
                if currentnode.get_dist() > dist: # if new distance is smaller than exisiting
                    currentnode.set_dist(dist) # assigning new distance
                    currentnode.set_prevnode(setof[0]) # setting new previous node for reconstruct_path
                    # print(setof[0].get_pos())
    
                if currentnode == end: # algorithm finish
                    return end

                tempunvisited = []
                tempunvisited.append(currentnode) # new list of prev/neighbor with currentnode
                for neighbor in currentnode.get_neighbors(): # appending (4 times) neighbors of each neighbor
                    if neighbor == None: # if out of bounds
                        continue
                    if neighbor.is_unvisited() or neighbor.is_open() or neighbor.is_end():
                        if not neighbor.is_end():
                            neighbor.make_open()
                        draw(win, ROWS, WIDTH, gameinst)
                        tempunvisited.append(neighbor) # adding to temp unvisited
                        
                unvisited.append(tempunvisited) # adding to unvisited

            else: # error condition for node
                continue
        if setof in unvisited: # after using neighbor list, remove from unlisted
            unvisited.remove(setof)
            return unvisited
        else: # no path condition
            print("Path Not Found.")
            return


def calc_dist3(board, origin, neighbor):
    x1, y1 = neighbor.get_pos()
    x2, y2 = origin.get_pos()
    return (abs(x1 - x2) + abs(y1 - y2)) # taking into account weight
