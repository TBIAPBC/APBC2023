#!/usr/bin/env python3
import random

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player
from shortestpaths import AllShortestPaths
from KilianG98_pathFinding import pathFinding

class GandolfTheGrey(Player):

    def reset(self, player_id, max_players, width, height):
	
        self.player_name = "GandolfTheGrey"
        self.directions = [D.up, D.down, D.left, D.right, D.up_left, D.up_right, D.down_left, D.down_right]
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
                if newPos in NonWallNeighbors:
                     moves.append(dir)
                     pos=newPos
        return(moves)
    
class GandolfTheWhite(Player):

    def reset(self, player_id, max_players, width, height):
        self.player_name = "GandolfTheWhite"
        self.directions=  {"up": D.up, "down": D.down,"left": D.left,"right": D.right,"upleft": D.up_left,"upright": D.up_right,"downleft": D.down_left, "downright": D.down_right}
        self.map = Map(width, height)
        self.allPaths = pathFinding(width,height)
        

    def round_begin(self, r):
        self.round = r
        if r == 150:
            #it can be assumed that the the middle has been explored after 150 rounds. 
            #The nonwall tile, that is colesest to the middle of the map is identified.
            idealTile = (int(self.map.width/2), int(self.map.height/2))
            minDist = 1000
            for x in range(self.map.width):
                for y in range (self.map.height):
                    tmp = abs(idealTile[0] - x) + abs(idealTile[1] - y)
                    if tmp < minDist and self.map[(x,y)].status == TileStatus.Empty:
                        minDist = tmp
                        self.midTile = (x,y)
            self.pathsToMid = AllShortestPaths(self.midTile, self.map)

    def fight_target_player(self, status):
        others = status.others
        for other in others:
            if other != None:
                return other.player
            
    def move(self, status):
        self.viz = status.params.visibility
        enemies = self.findPlayers(status)

        assert len(status.goldPots) > 0
        gLoc = next(iter(status.goldPots))

        if self.allPaths.distToGold[gLoc[0]][gLoc[1]] != 0:
            #update distance to gold, if gold location has changed
            self.allPaths.distToGold = [[1000 for _ in range(self.map.width)] for _ in range(self.map.height)]
            self.allPaths.updateDistToGold(self, status)

        MapIsUpdated = False

        for tile in self.allPaths.unexplored:
            #check if any of the unexplored tiles have now been explored
            if status.map[tile].status != TileStatus.Unknown:
                MapIsUpdated = True
                self.map[tile].status = status.map[tile].status
                self.allPaths.unexplored.remove(tile)
        if MapIsUpdated:
            #if the map is updated, the distance to gold matrix may also need to be updated
            self.allPaths.updateDistToGold(self,status)
            if self.round >= 150:
                self.pathsToMid = AllShortestPaths(self.midTile,self.map)
        if self.allPaths.distToGold[status.x][status.y] < 1000:
            for ePos in enemies:
                if self.allPaths.distToGold[ePos[0]][ePos[1]] < self.allPaths.distToGold[status.x][status.y]:
                    return[]
            #set gold as target, if path is known
            target = gLoc
            targetIsGold= True
        else:
            #explore map, if path to gold is not known
            target = self.allPaths.getNearestUnexplored(self,status)
            targetIsGold = False
        path = self.allPaths.findPathToTarget(self,target, status, targetIsGold)
        trimmedPath = self.allPaths.trim_path(self, path, status, targetIsGold)
        return trimmedPath

    def findPlayers(self, status):
        pos = (status.x, status.y)
        enemies = []
        for x in range(pos[0]-self.viz,pos[0]+self.viz):
             for y in range(pos[1]-self.viz,pos[1]+self.viz):
                try:
                    tile = status.map[x,y]
                    if tile.obj is not None and tile.obj.is_player():
                        # The tile is occupied by a player
                        if x != pos[0] or y != pos[1]:
                            enemies.append((x,y))
                except:
                    continue
        return enemies

players= [GandolfTheWhite()]
