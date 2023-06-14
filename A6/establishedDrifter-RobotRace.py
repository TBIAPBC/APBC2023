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


class EstablishedDrifter(Player):
    def __init__(self):
        # translation of moves to output
        self.move_translator = {0: D.up_left, 1: D.up, 2: D.up_right, 3: D.left, 4: None, 5: D.right, 6: D.down_left, 7: D.down, 8: D.down_right}
        self.cum_map = None

    def reset(self, player_id, max_players, width, height):
        # the player_id is an int, which can be converted to the name printed in the board
        self.player_name = "Established Drifter"
        self.visMap = Map(width, height)

    def round_begin(self, r):
        print("Welcome to round ", r, "---", self.status.params.rounds - r + 1, " to go.")
        pass

    def set_mines(self, status):
        """
		set mines for fun
		"""

        #map = status.map
        #for i in range(map.height):
         #   print(f'THE MAP IS: {[tile.status.__str__() for tile in map._data[i]]}')
        mines = []
        return mines


    def update_map(self, status):
        visMap = self.visMap
        for x in range(visMap.width):
            for y in range(visMap.height):
                if status.map[x, y].status != TileStatus.Unknown:
                    visMap[x, y].status = status.map[x, y].status

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
                if self.dist[neighbor] ==  curdist-1:
                    curdist -= 1
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


players = [EstablishedDrifter()]
