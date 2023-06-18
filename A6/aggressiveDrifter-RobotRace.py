#!/usr/bin/env python3
import random
import math
from collections import deque
import numpy as np
from scipy.stats import skewnorm
from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player


class AggressiveDrifter(Player):
    def __init__(self):
        # translation of moves to output
        self.move_translator = {0: D.up_left, 1: D.up, 2: D.up_right, 3: D.left, 4: None, 5: D.right, 6: D.down_left, 7: D.down, 8: D.down_right}
        self.cum_map = None

    def reset(self, player_id, max_players, width, height):
        # the player_id is an int, which can be converted to the name printed in the board
        self.player_name = "AggressiveDrifter"
        self.visMap = Map(width, height)

    def round_begin(self, r):
        print("Welcome to round ", r, "---", self.status.params.rounds - r + 1, " to go.")
        pass

    def dist(self, my_pos, other_pos):
        x_diff = abs(my_pos[0] - other_pos[0])
        y_diff = abs(my_pos[1] - other_pos[1])
        return ((x_diff**2)+(y_diff**2))**0.5

    def where_to_mine(self, player_pos, gold_pos):
        tiles = np.zeros((3, 3))
        if player_pos[0] < gold_pos[0]:
            tiles[:, 2] += 1
        elif player_pos[0] > gold_pos[0]:
            tiles[:, 0] += 1
        else:
            tiles[:, 1] += 1

        if player_pos[1] < gold_pos[1]:
            tiles[0, :] += 1
        elif player_pos[1] > gold_pos[1]:
            tiles[2, :] += 1
        else:
            tiles[1, :] += 1

        best_pos = [arr.tolist()[0] for arr in np.where(tiles == np.max(tiles))]

        secondary_mines = []

        if best_pos[0] == 0:
            if best_pos[1] == 0:
                secondary_mines.append((int(player_pos[0] - 1), int(player_pos[1])))
                secondary_mines.append((int(player_pos[0]), int(player_pos[1]) - 1))
            elif best_pos[1] == 2:
                secondary_mines.append((int(player_pos[0] + 1), int(player_pos[1])))
                secondary_mines.append((int(player_pos[0]), int(player_pos[1]) + 1))

        elif best_pos[0] == 2:
            if best_pos[1] == 2:
                secondary_mines.append((int(player_pos[0]), int(player_pos[1]) + 1))
                secondary_mines.append((int(player_pos[0] + 1), int(player_pos[1])))
            elif best_pos[1] == 0:
                secondary_mines.append((int(player_pos[0] - 1), int(player_pos[1])))
                secondary_mines.append((int(player_pos[0]), int(player_pos[1]) - 1))

        print(f'SEC MINES: {secondary_mines}')

        relative_y = -(best_pos[0] - 1)
        relative_x = best_pos[1] - 1

        primary_mine = int(player_pos[0] + relative_x), int(player_pos[1] + relative_y)
        return primary_mine, secondary_mines

    def set_mines(self, status):
        """
		set mines for fun
		"""
        # my position
        my_pos = (status.x, status.y)
        gold_pos = next(iter(status.goldPots))

        # find others
        other_player_pos = {}

        for p_idx, other_player in enumerate(status.others):
            if other_player is not None and p_idx != status.player:
                if 100 < status.gold < other_player.gold:
                    other_player_pos[p_idx] = (other_player.x, other_player.y)

        to_mine_up = []
        mines = []

        for p, p_pos in other_player_pos.items():
            if 2 < self.dist(my_pos, p_pos) < 5:
                to_mine_up.append(p_pos)

        if random.randint(0,10) < 8:
            for p_pos in to_mine_up:
                mine_pos, secondary_mines = self.where_to_mine(p_pos, gold_pos)
                assert 0 <= mine_pos[0] < self.visMap.width and 0 <= mine_pos[1] < self.visMap.height
                print(f'Tile at {mine_pos} will be mined.')
                mines.append(mine_pos)
                if random.randint(0, 10) < 5:
                    if len(secondary_mines):
                        print(f'As will be Tiles at {secondary_mines}.')
                        mines = mines + secondary_mines

        for m in mines:
            x, y = m
            self.visMap[x, y].status = TileStatus.Mine

        return mines


    def update_map(self, status):
        for x in range(self.visMap.width):
            for y in range(self.visMap.height):
                if status.map[x, y].status != TileStatus.Unknown:
                    self.visMap[x, y].status = status.map[x, y].status

    def _as_direction(self, curpos, nextpos):
        for d in D:
            diff = d.as_xy()
            if (curpos[0] + diff[0], curpos[1] + diff[1]) == nextpos:
                return d
        return None

    def _as_directions(self,curpos,path):
        return [self._as_direction(x,y) for x,y in zip([curpos]+path,path)]

    def move(self, status):
        # my position
        my_pos = (status.x, status.y)
        # update the current map
        self.update_map(status)
        #print(f'VIS MAP:\n{self.visMap}')

        # find gold
        assert len(status.goldPots) > 0
        gold_pos = next(iter(status.goldPots))
        my_paths = MyShortestPaths(gold_pos, self.visMap)
        bestpath = my_paths.shortestPathFrom(my_pos)
        bestpath = bestpath[1:]
        bestpath.append(gold_pos)

        distance = len(bestpath)

        numMoves = 3

        ## don't move if the pot is too far away
        if numMoves > 0 and distance / numMoves > status.goldPotRemainingRounds:
            numMoves = 0
            # print("SillyScout: I rather wait")

        return self._as_directions(my_pos, bestpath[:numMoves])

    def fight_target_player(self, status):
        health_others = [p.health for p in status.others]
        gold_others = [p.gold for p in status.others]
        max_index = np.argmax(gold_others)
        # this ensures that the robot just hits down at poorer and weaker fellows
        if max_index != status.player:
            for other in health_others:
                if other is not None and status.health >= other:
                    return other.player
        else:
            return None

    def trap_random_player(self, status):
        gold_others = [p.gold for p in status.others]
        if max(gold_others) > status.gold > 20:
            return True



class MyShortestPaths:
    def __init__(self,sink,map):
        self.sink = sink
        self.map = map

        self.width=map.width
        self.height=map.height

        wm = [ [ self.map[x,y].status == TileStatus.Wall for y in range(self.height) ]
               for x in range(self.width) ]

        self.wallmap = np.array(wm,dtype='bool')

        self.dist = np.negative(np.ones((self.height, self.width), dtype='int'))

        self._calcDistances()

    # return the non-Wall neighbors of a field (x,y)
    def nonWallNeighborsIter(self,xy):

        (x,y) = xy
        xs=[x]
        if x>0: xs.append(x-1)
        if x<self.width-1: xs.append(x+1)

        ys=[y]
        if y>0: ys.append(y-1)
        if y<self.height-1: ys.append(y+1)

        for x in xs:
            for y in ys:
                if not self.wallmap[x,y]:
                    if (x,y)==xy: continue
                    yield (x,y)

    def _calcDistances(self):
        front = deque()
        front.append(self.sink)

        assert type(self.sink) == tuple
        self.dist[self.sink] = 0

        while front:
            xy=front.popleft()
            for neighbor in self.nonWallNeighborsIter(xy):
                if self.dist[neighbor]<0:
                    front.append(neighbor)
                    self.dist[neighbor] = self.dist[xy] + 1

    def shortestPathFrom(self, xy):
        if self.dist[xy]<0:
            return []

        path = list()
        curdist = self.dist[xy]

        while xy != self.sink:
            path.append(xy)

            # find preceeding neighbor
            for neighbor in self.nonWallNeighborsIter(xy):
                if self.dist[neighbor] <  curdist:
                    curdist = self.dist[neighbor]
                    xy = neighbor
                    break
        return path

    def randomShortestPathFrom(self, xy):
        if self.dist[xy]<0:
            return []

        path = list()
        curdist = self.dist[xy]

        while xy != self.sink:
            path.append(xy)

            potentialNextXYs = list()
            # find preceeding neighbor
            for neighbor in self.nonWallNeighborsIter(xy):
                if self.dist[neighbor] ==  curdist-1:
                    potentialNextXYs.append(neighbor)
            assert len(potentialNextXYs)>0
            xy = random.choice(potentialNextXYs)
            curdist -= 1
        return path


players = [AggressiveDrifter()]
