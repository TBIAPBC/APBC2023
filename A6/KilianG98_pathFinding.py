#!/usr/bin/env python3
import random
from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Map, Status


class pathFinding:

    def __init__(self, width, height):
        self.distToGold = [[1000 for _ in range(width)] for _ in range(height)]
        self.distToUnexplored = [[1000 for _ in range(width)] for _ in range(height)]
        self.unexplored = [(x, y) for x in range(width) for y in range(height)]

    def updateDistToGold(self,robot, status):
        #updates the distance Matrix, each square gets assigned the distance to the next gold location
        assert len(status.goldPots) > 0
        gLoc = next(iter(status.goldPots))
        self.distToGold[gLoc[0]][gLoc[1]] = 0

        tilesToBeUpdated = set(position for _, position in Map.nonWallNeighbours(robot.map, gLoc))
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
                tilesToBeUpdated.update(position for _, position in Map.nonWallNeighbours(robot.map, (tile[0], tile[1])))

        return
    
    def getNearestUnexplored(self,robot,status):
        #identifies the nearest unexplored squares, returns the one which is closest to the gold
        self.distToUnexplored = [[1000 for _ in range(robot.map.width)] for _ in range(robot.map.height)]
        self.distToUnexplored[status.x][status.y ] = 0
        pos = (status.x, status.y)
        adjacentTiles = set(position for _, position in Map.nonWallNeighbours(robot.map, pos))
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
                adjacentTiles.update(position for _, position in Map.nonWallNeighbours(robot.map, (tile[0], tile[1])))
        

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
        
    def findPathToTarget(self, robot,target, status,targetIsGold):
        #receives target square and returns the path to that square
        #if the target is unknown territory, the last element of the path is removed -> dont step into  a wall

        path = []
        if targetIsGold:

            pos=(status.x,status.y)
            steps = self.distToGold[pos[0]][pos[1]]
            curDistance = self.distToGold[pos[0]][pos[1]]

            for i in range (steps +1):
                neighbors = set(position for _, position in Map.nonWallNeighbours(robot.map,pos))
                for n in neighbors:
                    if self.distToGold[n[0]][n[1]] < curDistance:
                        curDistance -=1
                        path.append(self.get_direction(robot, pos[0], pos[1], n[0], n[1]))
                        pos = n
                        break

        
        else:
            pos=(target[0], target[1])
            steps = self.distToUnexplored[pos[0]] [pos[1]]
            curDistance= self.distToUnexplored [pos[0]][pos[1]]

            for i in range(steps +1):
                neighbors = set(position for _, position in Map.nonWallNeighbours(robot.map,pos))
                for n in neighbors:
                    if self.distToUnexplored[n[0]][n[1]] < curDistance:
                        curDistance -=1
                        path = [self.get_direction(robot,n[0], n[1], pos[0], pos[1])] + path
                        pos = n
                        break
        
            
        return path
    
    def get_direction(self, robot,from_col,from_row, to_col, to_row,):
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

        return robot.directions[direction]

    def trim_path(self, robot,path,status,targetIsGold):
        #receives the path, returns a trimmed version depending on cost & reward
        for key, val in status.goldPots.items():
            reward = val

        pathCost= (len(path)/2) *(len(path) +1 )
        if robot.round <= 150:
            if targetIsGold:
                if pathCost <= robot.status.gold and pathCost < reward:
                    return path
                if status.goldPotRemainingRounds > 1:
                    if len(path) > 2:
                        return([path[0], path[1], path[2]])
                    else:
                        return path
            else:
                if len(path) > 1:
                    return ([path[0], path[1]])
                else:
                    return(path)
        else:       
            if targetIsGold:
                if len(path) <= ((robot.map.width + robot.map.height )/2):
                    if pathCost <= robot.status.gold and pathCost < reward:
                        return path
                elif status.goldPotRemainingRounds > 1:
                    return[path[0]]
            newP = robot.pathsToMid.shortestPathFrom((status.x, status.y))
            if len(newP)>= 4:
                goto = newP[1]
                return [self.get_direction(robot, status.x, status.y, goto[0], goto[1])]
            
        return([])