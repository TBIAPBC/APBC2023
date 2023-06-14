from collections import deque

def NonWallBorderTiles(map,v,cx,cy):
    tiles = []
    c_xrange = list(range(cx-v, cx+v+1))
    c_yrange = list(range(cy-v, cy+v+1))

    for y in c_yrange:
        if y == c_yrange[0] or y == c_yrange[-1]:
            for x in c_xrange:
                if map[y][x] != '#':
                    tiles.append((y,x))
        else:
            for x in [c_xrange[0],c_xrange[-1]]:
                if map[y][x] != '#':
                    tiles.append((y,x))
    return sorted(tiles)


def BorderPaths(map,pos):
    rows, cols = len(map), len(map[0])
    initial_position = pos

    # Initialize queue and visited set
    queue = deque()
    visited = set()

    # Enqueue the initial position
    queue.append(initial_position)

    # Define valid directions
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    # Initialize result list
    accessible_tiles = []
    paths = {}

    # BFS
    while queue:
        curr_x, curr_y = queue.popleft()
        visited.add((curr_x, curr_y))

        # Check if the current position is on the border
        if curr_x == 0 or curr_x == rows - 1 or curr_y == 0 or curr_y == cols - 1:
            accessible_tiles.append((curr_x, curr_y))

        # Explore neighboring positions
        for dx, dy in directions:
            new_x, new_y = curr_x + dx, curr_y + dy

            # Check if the neighboring position is a valid white tile
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

"""---------------------------------------------------------------"""
# map = """
# # . # # . .
# # $ # . # #
# . # . . . #
# . . . . . . 
# . # . # # .
# . . # # . .
# """
map = """
# . # #
# $ # .
# # . #
. # . .
"""
map = map.strip().split('\n')
for row in range(len(map)):
    map[row] = map[row].split()
# v = 2
# cx,cy = 3,3

for i in map:
    for j in i:
        print(j,end=" ")
    print()
print()

bot = (1,1)
pot = (5,4)



# print(NonWallBorderTiles(map,v,cx,cy), "\n")
borders, paths = BorderPaths(map, bot)
closest_border_tile = MinDistanceToPot(borders, pot)

for key in paths:
    print(key, paths[key])

print()
print(paths[closest_border_tile])



