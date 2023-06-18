#!/usr/bin/env python3
import random
import math
import numpy as np
from scipy.stats import skewnorm
from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player


class NaiveDrifter(Player):
    def __init__(self):
        # Step amount
        a = -2  # skewness parameter
        loc = 12  # mode
        scale = 8  # standard deviation
        # Create the distribution object
        self.rv = skewnorm(a, loc=loc, scale=scale)

        # movement maps
        map_up = np.array([25, 33, 25, 1, 0, 1, 1, 1, 1]).reshape(3, 3)
        map_left = np.rot90(map_up)
        map_down = np.rot90(map_left)
        map_right = np.rot90(map_down)
        map_up_left = np.array([33, 20, 5, 20, 0, 1, 5, 3, 1]).reshape(3, 3)
        map_down_left = np.rot90(map_up_left)
        map_down_right = np.rot90(map_down_left)
        map_up_right = np.rot90(map_down_right)
        stay = np.array([0, 0, 0, 0, 100, 0, 0, 0, 0]).reshape(3, 3)
        self.maps = [map_down_left, map_down, map_down_right, map_left, stay, map_right, map_up_left, map_up, map_up_right]

        # map chooser depending on where the gold pot is
        self.map_chooser = np.array([[6, 7, 8],
                                    [3, 4, 5],
                                    [0, 1, 2]])

        # translation of moves to output
        self.move_translator = {0: D.up_left, 1: D.up, 2: D.up_right, 3: D.left, 4: None, 5: D.right, 6: D.down_left, 7: D.down, 8: D.down_right}


    def reset(self, player_id, max_players, width, height):
        # the player_id is an int, which can be converted to the name printed in the board
        self.player_name = "Drifter"

    def round_begin(self, r):
        print("Welcome to round ", r, "---", self.status.params.rounds - r + 1, " to go.")
        pass

    def set_mines(self, status):
        """
		set mines for fun
		"""

        map = status.map
        mines = []
        for i in range(5):
            if random.randint(0, 100) < 10:
                x, y = status.x, status.y
                x += random.randint(0, 3)
                y += random.randint(0, 3)

                if (x >= 0 and x < map.width and y >= 0 and y < map.height
                        and not map[x, y].is_blocked() and map[x, y].obj is None):
                    mines.append((x, y))
            else:
                break
        return mines

    def cum_maps(self, p_map):
        c_map = np.zeros((3, 3))
        cum = 0
        for idx_r, r in enumerate(p_map):
            for idx_c, c in enumerate(r):
                cum += c
                c_map[idx_r, idx_c] = cum
        return c_map.flatten()

    def move(self, status):
        # the status object (see game_utils.Status) contains:
        # - .player, our id, if we should have forgotten it
        # - .x and .y, our position
        # - .health and .gold, how much health and gold we have
        # - .map, a map of what we can see (see game_utils.Map)
        #   The origin of the map is in the lower left corner.
        # - .goldPots, a dict from positions to amounts
        # print("-" * 80)
        # print("Status for %s" % self.player_name)
        # # print the map as we can see it, along with health and gold
        # print(status)
        # print(status.map)  # the map can be printed too, but printing the status
        # does this as well
        # for illustration, we go through the map and find stuff

        # find gold
        assert len(status.goldPots) > 0
        gold_pos = next(iter(status.goldPots))

        # find out horizontal direction
        selfX = status.x
        selfY = status.y
        col = 1
        if selfX < gold_pos[0]:
            col = 2
        elif selfX > gold_pos[0]:
            col = 0

        # find out vertical direction
        row = 1
        if selfY < gold_pos[1]:
            row = 0
        elif selfY > gold_pos[1]:
            row = 2

        # chose the map
        map_chosen = self.maps[self.map_chooser[row, col]].copy()
        # check every direction to see if it is free
        up = down = left = right = False
        tile_down_left = tile_down = tile_down_right = tile_left = tile_right = tile_up_left = tile_up = tile_up_right = None
        if selfX > 0:
            left = True
            tile_left = status.map[selfX - 1, selfY]
        if selfY > 0:
            down = True
            tile_down = status.map[selfX, selfY - 1]
        if selfX < status.map.width - 1:
            right = True
            tile_right = status.map[selfX + 1, selfY]
        if selfY < status.map.height - 1:
            up = True
            tile_up = status.map[selfX,   selfY+1]
        if up:
            if left:
                tile_up_left = status.map[selfX - 1, selfY + 1]
            if right:
                tile_up_right = status.map[selfX + 1, selfY + 1]
        if down:
            if left:
                tile_down_left = status.map[selfX - 1, selfY - 1]
            if right:
                tile_down_right = status.map[selfX + 1, selfY - 1]

        tiles = [tile_down_left, tile_down, tile_down_right, tile_left, 'space', tile_right, tile_up_left, tile_up, tile_up_right]
        for idx, tile in enumerate(tiles):
            if tile == 'space':
                continue
            if tile is None or tile.status == TileStatus.Wall:
                d_col = idx % 3
                d_row = abs(int(math.floor(idx / 3)) - 2)
                map_chosen[d_row, d_col] = 0

        cum_map = self.cum_maps(map_chosen)
        max_rand = int(np.sum(map_chosen))

        # choose how many steps
        diff = abs(selfX - gold_pos[0]) + abs(selfY - gold_pos[1])
        #step_amount = math.floor(25/diff) % 7
        step_amount = round(self.rv.pdf(15)*100)


        # make a move
        moves = []
        for i in range(step_amount):
            prob = random.randint(1, max_rand)
            at = np.where(cum_map[:] >= prob)[0][0]
            moves.append(self.move_translator[at])
        return moves

    def fight_target_player(self, status):
        others = status.others
        gold_others = [p.gold for p in status.others if p is not None]
        if gold_others:
            max_index = np.argmax(gold_others)
            # this ensures that the robot just hits down at poorer and weaker fellows
            if max_index != status.player:
                for other in others:
                    if other is not None and status.health >= other.health:
                        return other.player
        return False

    def trap_random_player(self, status):
        gold_others = [p.gold for p in status.others if p is not None]
        if gold_others:
            if max(gold_others) > status.gold > 20:
                return True



players = [NaiveDrifter()]
