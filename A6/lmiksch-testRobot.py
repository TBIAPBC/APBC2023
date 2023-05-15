#!/usr/bin/env python3
import random

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player
from shortestpaths import AllShortestPaths



class lmiksch_bot(Player):
    def __init__(self):
        self.map = map



    def reset(self, player_id, max_players, width, height):
        self.player_name = "lmiksch_test"
        self.ourMap = Map(width,height)
        #raise NotImplementedError("'reset' not implemented in '%s'." % self.__class__)
    
    def round_begin(self, r):
        pass
        #raise NotImplementedError("'round_begin' not implemented in '%s'." % self.__class__)
    
    def move(self, status):
        # the status object (see game_utils.Status) contains:
        # - .player, our id, if we should have forgotten it
        # - .x and .y, our position
        # - .health and .gold, how much health and gold we have
        # - .map, a map of what we can see (see game_utils.Map)
        #   The origin of the map is in the lower left corner.
        # - .goldPots, a dict from positions to amounts
        ourMap = self.ourMap
       
        for x in range(ourMap.width):
                for y in range(ourMap.height):
                        if status.map[x, y].status != TileStatus.Unknown:
                                ourMap[x, y].status = status.map[x, y].status
        
        moves = []
        
        pos = (status.x,status.y)
       
        for coord,amount in status.goldPots.items():
            x_goldPot = coord[0]
            y_goldPot = coord[1]
            gold = amount
      

        gLoc = next(iter(status.goldPots))

        paths = AllShortestPaths(gLoc,ourMap)
        #calculate min distance to goldpot if distance < gold do nothing
        d_to_pot = abs(pos[0] - x_goldPot) + abs(pos[1] - y_goldPot)

        if d_to_pot > gold:
            print("Too far won't move ","-"*80)
            return []

        bestpath = paths.shortestPathFrom(pos)
        #print(bestpath)

        best_d = self.conv_path_to_directions(pos,bestpath[1:],gLoc)

        print(best_d)


        #adding final move to goldpot

        


        numMoves = round((len(best_d)/d_to_pot)*5)

        

        print("numMoves: ",numMoves)
        
        return best_d[0:numMoves]



    def conv_path_to_directions(self,pos,path,gLoc):
        #move_dict = {"up": ( 0,  1),"down": ( 0,  -1),"left": ( -1,  0),"right": ( 1,  0),"up_left": ( -1,  1),"up_right": ( 1,  1),"down_left": ( -1,  -1),"down_right": ( 1,  -1)}
        directions = []
        
        for pathpos in path:
            
            x_pos, x_path = pos[0], pathpos[0]
            y_pos, y_path = pos[1], pathpos[1]
            move = (x_path - x_pos,y_path - y_pos)
           

            for d in D:
                 d_xy = d.as_xy()
                 
                 if d_xy[0] == move[0] and d_xy[1] == move[1]:
                      directions.append(d)
                      
                      pos = (x_path,y_path) #update position
                      break
        #adding final move to pot
        for d in D: 
             d_xy = d.as_xy()
             
             move = (gLoc[0] - pos[0], gLoc[1] - pos[1])
             
             if d_xy[0] == move[0] and d_xy[1] == move[1]:
                      directions.append(d)
                      
                      
                      break


        return directions


              
              
        

   

    

players = [lmiksch_bot()]