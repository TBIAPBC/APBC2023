#!/usr/bin/env python3
from collections import deque
import copy
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
import random

import numpy as np

class AllShortestPaths:
    def __init__(self,sink,map):
        self.sink = sink # pot
        self.map = map # ourMap (including visible area and unknwon tiles around)

        self.width=map.width
        self.height=map.height

        # self.wallmap = np.zeros((self.height, self.width), dtype='bool')

        # for x in range(self.width):
        #     for y in range(self.height):
        #         self.wallmap[x,y] = self.map[x,y].status == TileStatus.Wall

        wm = [ [ self.map[x,y].status == TileStatus.Wall for y in range(self.height) ] # wallmap (binary, wall or not)
               for x in range(self.width) ]

        self.wallmap = np.array(wm,dtype='bool')

        self.dist = np.negative(np.ones((self.height, self.width), dtype='int')) # initialization. 2D array filled with -1´s 

        self._calcDistances() 

    # return the non-Wall neighbors of a field (x,y)
    def nonWallNeighborsIter(self,xy): # returns non wall neighbours of a given field

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
                    yield (x,y) # fills generator that is returned 

    # BFS collects distances from pot to all other points in the map
    # Not "as the eagle flies", mauern werden umgangen, the distance is not the direct distance
    # but this accounts only for the visible area, i guess a.e.f for the unknown tiles
    def _calcDistances(self):
        front = deque() # double ended queue (popping/adding from both sides)
        front.append(self.sink) # pot appended to the right end of the front deque

        assert type(self.sink) == tuple
        self.dist[self.sink] = 0

        while front: # starting the BFS at the sink
            xy=front.popleft() # xy = sinkvalue, front = deqe([]), always one member or empty
            for neighbor in self.nonWallNeighborsIter(xy):
                if self.dist[neighbor]<0: # distances arr initiated with -1`s (means non visited)   
                    front.append(neighbor)
                    self.dist[neighbor] = self.dist[xy] + 1

    # shortest path from curr to pot by getting their distance from self.dist
    # .. in while loop checking every neighbor and take it as next tile if
    # .. distance decreases by one
    def shortestPathFrom(self, xy):
        if self.dist[xy]<0:
            return []

        path = list()
        curdist = self.dist[xy] # distance from curr to pot

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
