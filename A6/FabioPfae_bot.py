from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player
import FabioPfae_functions as fabio

class FabioPfae_bot(Player):
    def reset(self, player_id, max_players, width, height): # at start
        self.player_name = "FabioPfae_GoodBot"
        self.ourMap = Map(width, height)
    
    def round_begin(self,r): # buy stuff etc
        self.r = r

    def move(self, status):
#         print("Status for %s" % self.player_name)
        # print(status)
#         print("end of status")
        ourMap = self.ourMap # = Map(width, heigth) -> object from class 'Map' (initiated with unknown tiles)

        # ourMap extends every round with the new visible area of status.map
        for y in range(ourMap.height):
            for x in range(ourMap.width):
                if status.map[y,x].status != TileStatus.Unknown:
                    ourMap[y,x].status = status.map[y,x].status 
        
        assert len(status.goldPots) > 0
        gLoc = next(iter(status.goldPots))
#         print("Gold is at", gLoc)
              
        """
        __________________________________________________________________________________________"""
        curpos = (status.x, status.y)     

        bordertiles, borderpaths = fabio.BorderPaths(ourMap,curpos,status,gLoc)
        if len(bordertiles) == 0: print("Jesus christ, I am stuck!"); return [] # wait if locked
        closest_bordertile = fabio.ClosestTile(bordertiles, gLoc)
        bestpath = borderpaths[closest_bordertile]
        
        dirs_xy = [(bestpath[0][0]-curpos[0], bestpath[0][1]-curpos[1])] # initialised with diff from current tile to first tile in my path array
        dirs_xy = fabio.path2dirs_xy(bestpath,dirs_xy)

        dirs = []
        for dir_xy in dirs_xy:
            dirs.append(fabio.dir_xy2dir(dir_xy))
        
        v = status.params.visibility
        d = len(dirs)
        arithmetic_series = (d/2)*(d+1)
        steps = 11
        if self.r < 5:
            return dirs[:3]
        elif arithmetic_series > status.goldPots[gLoc] or arithmetic_series > status.gold:
            return dirs[:3]
        
        else:
            return dirs[:5]
        """__________________________________________________________________________________________"""
players = [FabioPfae_bot()]

# up = 0 
# down = 1
# left = 2
# right = 3
# up_left = 4
# up_right = 5
# down_left = 6
# down_right = 7

#         curpos = (status.x, status.y)
#         d = max(abs(gLoc[0]-curpos[0]), abs(gLoc[1]-curpos[1])) # if the cost of reaching the pot is higher than the pots content, no steps
#         arithmetic_series = (d/2)*(d+1)
#         print(curpos,d,arithmetic_series, status.goldPots[gLoc], self.r)
#         if arithmetic_series > status.goldPots[gLoc]:
#             if self.r < 5:
#                 return dirs[:4]
#             else:
#                 return dirs[:7]
            