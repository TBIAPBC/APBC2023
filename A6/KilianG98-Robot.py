#!/usr/bin/env python3
import random

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player

class StupidBot(Player):

    def reset(self, player_id, max_players, width, height):
	
        self.player_name = "stupidBot"
        self.directions= [D.up, D.down, D.left, D.right, D.up_left, D.up_right, D.down_left, D.down_right]
        self.map= Map(width,height)
	
    def round_begin(self, r):
        pass
	
    def move(self, status):
        for x in range(self.map.width):
            for y in range(self.map.height):
                if status.map[x, y].status != TileStatus.Unknown:
                    self.map[x, y].status = status.map[x, y].status

        i = random.randint(1,8)
        moves=[]
        pos =[status.x,status.y]

        for j in range(i):
                dir = self.directions[random.randint(0,len(self.directions)-1)]
                dir_XY= D.as_xy(dir)
                newPos=[pos[0] + dir_XY[0], pos[1] +dir_XY[1]]
                NonWallNeighbors = [list(position) for _, position in Map.nonWallNeighbours(self.map,pos)]
                print(NonWallNeighbors)
                if newPos in NonWallNeighbors:
                     moves.append(dir)
                     pos=newPos
        return(moves)
    
players=[StupidBot()]



