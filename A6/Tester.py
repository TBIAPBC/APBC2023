import random

import numpy as np


def cum_maps(p_map):
    c_map = np.zeros((3, 3))
    cum = 0
    for idx_r, r in enumerate(p_map):
        for idx_c, c in enumerate(r):
            cum += c
            c_map[idx_r, idx_c] = cum
    return c_map.flatten()

class Status(object):
    def __init__(self):
        self.x = 5
        self.y = 13

status = Status()
# MY TEST MOVES
map_chooser = np.array([[6, 7, 8],
                        [3, 4, 5],
                        [0, 1, 2]])
# define the probability maps
map_up = np.array([25, 33, 25, 5, 0, 5, 3, 1, 3]).reshape(3, 3)
map_left = np.rot90(map_up)
map_down = np.rot90(map_left)
map_right = np.rot90(map_down)
map_up_left = np.array([33, 25, 5, 25, 0, 3, 5, 3, 1]).reshape(3, 3)
map_down_left = np.rot90(map_up_left)
map_down_right = np.rot90(map_down_left)
map_up_right = np.rot90(map_down_right)
stay = map_up_left = np.array([0, 0, 0, 0, 100, 0, 0, 0, 0]).reshape(3, 3)
maps = [map_down_left, map_down, map_down_right, map_left, stay, map_right, map_up_left, map_up, map_up_right]
# define move translator
translator = {0: 'up_left', 1: 'up', 2: 'up_right', 3: 'left', 4: 'stay', 5: 'right', 6: 'down_left', 7: 'down', 8: 'down_right'}
gold_pos = (10, 10)
row = 1
col = 1
# find out horizontal direction
if status.x < gold_pos[0]:
    col = 2
elif status.x > gold_pos[0]:
    col = 0

# find out vertical direction
if status.y < gold_pos[1]:
    row = 0
elif status.y > gold_pos[1]:
    row = 2

map_index = map_chooser[row, col]
print(f'Use map at index {map_index}')
print(f'This is the map:\n{maps[map_index]}')

cum_map = cum_maps(maps[map_index])
print(f'The corresponding cum_map:\n{cum_map.reshape(3, 3)}')

selected = []
for t in range(100):
    prob = random.randint(1,100)
    # print(f'Random number: {prob}')
    at = np.where(cum_map[:] >= prob)[0][0]
    print(f'Move to: {translator[at]}')
    selected.append(translator[at])

print(f'DOWN RIGHT: {selected.count("down_right")}')
print(f'UP LEFT: {selected.count("up_left")}')
print(f'DOWN: {selected.count("down")}')
print(f'RIGHT: {selected.count("right")}')




