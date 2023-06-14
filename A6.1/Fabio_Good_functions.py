from collections import deque
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
import numpy as np

# returns all accessible border tiles of ourMap and their paths
def BorderPaths(ourMap, initpos, status, gLoc):
    height, width = ourMap.height, ourMap.width

    queue = deque()
    visited = set()
    queue.append(initpos)

    accessible_tiles = []
    border_paths = {}

    # BFS
    while queue:
        cur_x, cur_y = queue.popleft()
        visited.add((cur_x, cur_y))

        # Checks if the current position is on the border = has an Unknown neighbor
        for d in D:
            dx,dy = d.as_xy()[0], d.as_xy()[1]
            if (
                0 <= cur_x+dx < width
                and 0 <= cur_y+dy < height
                and ourMap[cur_x +dx , cur_y +dy].status == TileStatus.Unknown # border tile = true wenn mind. 1 unknown neighbor
                ):
                    accessible_tiles.append((cur_x, cur_y))
                    break
        
        # Explores neighboring positions
        for d in D:
            new_x, new_y = cur_x + d.as_xy()[0], cur_y + d.as_xy()[1]

            # Check if neighbor is an empty tile
            if (
                0 <= new_x < width
                and 0 <= new_y < height
                and ourMap[new_x,new_y].status == TileStatus.Empty
                and (new_x, new_y) not in visited
            ):
                 queue.append((new_x, new_y))
                 visited.add((new_x, new_y))
                 border_paths[(new_x, new_y)] = border_paths.get((cur_x, cur_y), []) + [(new_x, new_y)]

    
    if gLoc in list(border_paths.keys()): # if gLoc accessible only take this tile into array
        accessible_tiles = [gLoc]

    for key in border_paths.copy(): # deletes paths that don´t end in a border tile
         if key not in accessible_tiles:
              border_paths.pop(key)
    
    return sorted(accessible_tiles), dict(sorted(border_paths.items()))

# loops over all accessible border tiles and returns one of the tiles that has minimal distance to the gold pot
def ClosestTile(borders, pot):
    min_d = float('inf')
    mintile = ()

    for tile in borders:
        d = max(abs(pot[0]-tile[0]), abs(pot[1]-tile[1]))
        if d < min_d:
            min_d = d
            mintile = tile
    return mintile

def path2dirs_xy(path,dirs_xy):
    for i in range(len(path)-1):
        start = path[i]
        end = path[i+1]
        dirs_xy.append((end[0]-start[0], end[1]-start[1]))
    return dirs_xy

def dir_xy2dir(dir_xy):
    for dir in D:
        if dir.as_xy() == dir_xy:
            return dir
    assert ("no valid dir_xy")
              
