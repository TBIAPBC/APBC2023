from collections import deque
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
import numpy as np

def BorderPaths(map,pos):
    rows, cols = len(map), len(map[0])
    initial_position = pos

    queue = deque()
    visited = set()

    queue.append(initial_position)

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    accessible_tiles = []
    paths = {}

    # BFS approach
    while queue:
        curr_x, curr_y = queue.popleft()
        visited.add((curr_x, curr_y))

        # Checks if the current position is on the border
        if curr_x == 0 or curr_x == rows - 1 or curr_y == 0 or curr_y == cols - 1:
            accessible_tiles.append((curr_x, curr_y))

        # Explores neighboring positions
        for dx, dy in directions:
            new_x, new_y = curr_x + dx, curr_y + dy

            # Check if the neighbor is an empty tile
            if (
                0 <= new_x < rows
                and 0 <= new_y < cols
                and map[new_x][new_y] == "."
                and (new_x, new_y) not in visited
            ):
                queue.append((new_x, new_y))
                visited.add((new_x, new_y))
                paths[(new_x, new_y)] = paths.get((curr_x, curr_y), []) + [(new_x, new_y)]

    for key in paths.copy():
        if key not in accessible_tiles:
            paths.pop(key)
    
    return sorted(accessible_tiles), paths

def MinDistanceToPot(borders, pot):
    min_d = float('inf')
    mintile = ()

    for tile in borders:
        d = max(abs(pot[0]-tile[0]), abs(pot[1]-tile[1]))
        if d < min_d:
            min_d = d
            mintile = tile
    return mintile

def fromCoordinatesToDirections(codir):
    for direction in D:
        if direction.as_xy() == codir:
            return direction
    return None 