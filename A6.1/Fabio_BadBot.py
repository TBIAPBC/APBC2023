from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player
from collections import deque
import Fabio_Bad_functions


class NaiveBot(Player):
    def reset(self, player_id, max_players, width, height): # at start
        self.player_name = "NaiveBot"
        self.ourMap = Map(width, height)
    
    def round_begin(self,r): # buy stuff etc
        pass

    def move(self, status):
        print("Status for %s" % self.player_name)
        print(status)
        print("end of status")

        ourMap = self.ourMap # = Map(width, heigth) -> object from class 'Map' (initiated with unknown tiles)
        # updated map (uknown tiles outside v remain unknwon, inside v are updated 
        # with their actual status). Note: update after each round not after each step.
        for y in range(ourMap.height):
            for x in range(ourMap.width):
                if status.map[y,x].status != TileStatus.Unknown:
                    ourMap[y,x].status = status.map[y,x].status
                    
            
        assert len(status.goldPots) > 0
        gLoc = next(iter(status.goldPots))
        print("Gold is at", gLoc)

       
        # Approach:
        # 1) Identify all empty tiles at the border of the visible and their paths if they can be reached, 
        # that can be reached from current position. Store as list.
        # 2) For every of those tiles identify the distance to the gold pot and pick the closest as destination in this turn
        curpos = (status.x,status.y) # lables wrong tile (?), class map and string map different in orientation? update: yes(have to fix)

        visMap = str(ourMap)
        visMap = visMap.strip().split('\n')
        for row in range(len(visMap)):
                visMap[row] = visMap[row].split()

        visMap[status.y][status.x] = 'X'
        
        visMap = [[i for i in j if i != '_'] for j in visMap]
        visMap = [i for i in visMap if i != []]
        
        for i,row in enumerate(visMap):
            for j,col in enumerate(row):
                if col == 'X':
                    curpos = (i,j)

        bordertiles, paths = Fabio_functions.BorderPaths(visMap, curpos) # 1) 
        closest_border_tile = Fabio_functions.MinDistanceToPot(bordertiles, (0,0)) # 2),  change (0,0) to actual pot coordinates
        bestpath = paths[closest_border_tile]

        coorDirs = [(bestpath[0][0]-curpos[0], bestpath[0][1]-curpos[1])] # initialised with diff from current tile to next tile
        Fabio_functions.Coords2coorDirs(bestpath, coorDirs)
        
        directions = []
        for coorDir in coorDirs:
            directions.append(Fabio_functions.fromCoordinatesToDirections(coorDir))

        # return directions
        return [] # only until i have pot coordinates (with repsect to visMap)

        


players = [NaiveBot()]

"""_______________________________________________________________________________________________________
Adjustments:
- auf Einsperren antworten (ja nein)
- Different orientations in the class and string maps
"""
