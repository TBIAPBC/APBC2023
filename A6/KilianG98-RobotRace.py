#!/usr/bin/env python3
import random

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player

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
        self.distToGold = [[1000 for _ in range(width)] for _ in range(height)]
        self.distToUnexplored = [[1000 for _ in range(width)] for _ in range(height)]
        self.unexplored = [(x, y) for x in range(width) for y in range(height)]

    def round_begin(self, r):
        self.round = r
        pass

    def move(self, status):

        assert len(status.goldPots) > 0
        gLoc = next(iter(status.goldPots))

        if self.distToGold[gLoc[0]][gLoc[1]] != 0:
            #update distance to gold, if gold location has changed
            self.distToGold = [[1000 for _ in range(self.map.width)] for _ in range(self.map.height)]
            self.updateDistToGold(status)

        MapIsUpdated = False

        for tile in self.unexplored:
            #check if any of the unexplored tiles have now been explored
            if status.map[tile].status != TileStatus.Unknown:
                MapIsUpdated = True
                self.map[tile].status = status.map[tile].status
                self.unexplored.remove(tile)
        
        if MapIsUpdated:
            #if the map is updated, the distance to gold matrix may also need to be updated
            self.updateDistToGold(status)

        if self.distToGold[status.x][status.y] < 1000:
            #set gold as target, if path is known
            target = gLoc
            targetIsGold= True
        else:
            #explore map, if path to gold is not known
            target = self.getNearestUnexplored(status)
            targetIsGold = False

        path = self.findPathToTarget(target, status, targetIsGold)

        trimmedPath = self.trim_path(path, status, targetIsGold)
        return trimmedPath
        
    def updateDistToGold(self, status):
        #updates the distance Matrix, each square gets assigned the distance to the next gold location
        assert len(status.goldPots) > 0
        gLoc = next(iter(status.goldPots))
        self.distToGold[gLoc[0]][gLoc[1]] = 0

        tilesToBeUpdated = set(position for _, position in Map.nonWallNeighbours(self.map, gLoc))
        distance = 0

        while tilesToBeUpdated:
            
            distance += 1
            updatedTiles = set()

            for tile in tilesToBeUpdated:
                if tile not in self.unexplored:
                    if self.distToGold[tile[0]][tile[1]] > distance:
                        self.distToGold[tile[0]][tile[1]] = distance
                        updatedTiles.add(tile)

            if not updatedTiles:
                break

            tilesToBeUpdated = set()
            for tile in updatedTiles:
                tilesToBeUpdated.update(position for _, position in Map.nonWallNeighbours(self.map, (tile[0], tile[1])))

        return
    
    def getNearestUnexplored(self,status):
        #identifies the nearest unexplored squares, returns the one which is closest to the gold
        self.distToUnexplored = [[1000 for _ in range(self.map.width)] for _ in range(self.map.height)]
        self.distToUnexplored[status.x][status.y ] = 0

        pos = (status.x, status.y)
        adjacentTiles = set(position for _, position in Map.nonWallNeighbours(self.map, pos))
        distance = 0
        nearestUnexplored = []

        while True:
            
            distance += 1
            updatedTiles = set()

            for tile in adjacentTiles:
                if tile not in self.unexplored:
                    if self.distToUnexplored[tile[0]][tile[1]] > distance:
                        self.distToUnexplored[tile[0]][tile[1]] = distance
                        updatedTiles.add(tile)
                else: 
                    nearestUnexplored.append(tile)
                    self.distToUnexplored[tile[0]][tile[1]] = distance

            if nearestUnexplored != []:
                break

            adjacentTiles = set()
            for tile in updatedTiles:
                adjacentTiles.update(position for _, position in Map.nonWallNeighbours(self.map, (tile[0], tile[1])))
        

        assert len(status.goldPots) > 0
        gLoc = next(iter(status.goldPots))
        min = 99999
        targetTile = pos

        for t in nearestUnexplored:
            tmp = abs(gLoc[0] -t[0]) + abs(gLoc[1] - t[1])
            if tmp < min:
                min = tmp
                targetTile = t
        return targetTile
        
    def findPathToTarget(self,target, status,targetIsGold):
        #receives target square and returns the path to that square
        #if the target is unknown territory, the last element of the path is removed -> dont step into  a wall

        path = []
        if targetIsGold:

            pos=(status.x,status.y)
            steps = self.distToGold[pos[0]][pos[1]]
            curDistance = self.distToGold[pos[0]][pos[1]]

            for i in range (steps +1):
                neighbors = set(position for _, position in Map.nonWallNeighbours(self.map,pos))
                for n in neighbors:
                    if self.distToGold[n[0]][n[1]] < curDistance:
                        curDistance -=1
                        path.append(self.get_direction(pos[0], pos[1], n[0], n[1]))
                        pos = n
                        break

        
        else:
            pos=(target[0], target[1])
            steps = self.distToUnexplored[pos[0]] [pos[1]]
            curDistance= self.distToUnexplored [pos[0]][pos[1]]

            for i in range(steps +1):
                neighbors = set(position for _, position in Map.nonWallNeighbours(self.map,pos))
                for n in neighbors:
                    if self.distToUnexplored[n[0]][n[1]] < curDistance:
                        curDistance -=1
                        path = [self.get_direction(n[0], n[1], pos[0], pos[1])] + path
                        pos = n
                        break
        

        return path
    
    def get_direction(self,from_col,from_row, to_col, to_row,):
        #returns the direction one needs to go between to neighboring squares

        direction = ""
        # Determine vertical direction
        if from_row > to_row:
            direction += "down"
        elif from_row < to_row:
            direction += "up"

        # Determine horizontal direction
        if from_col > to_col:
            direction += "left"
        elif from_col < to_col:
            direction += "right"

        return self.directions[direction]

    def trim_path(self,path,status,targetIsGold):
        #receives the path, returns a trimmed version depending on cost & reward
        for key, val in status.goldPots.items():
            reward = val

        pathCost= (len(path)/2) *(len(path) +1 )
        if self.round <= 100:
            if targetIsGold:
                if pathCost <= self.status.gold and pathCost < reward:
                    return path
                if self.status.gold > 70:
                    if len(path) > 1:
                        return([path[0], path[1]])
                    else:
                        return path
            else:
                if self.status.gold > 90:
                    if len(path) > 1:
                        return([path[0], path[1]])
                    else:
                        return path
        else:
            if targetIsGold:
                if len(path) <= ((self.map.width + self.map.height )/2):
                    if pathCost <= self.status.gold and pathCost < reward:
                        return path
                    else:
                        return[path[0]]
        return([])



players = [GandolfTheGrey(), GandolfTheWhite()]



