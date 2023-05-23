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
	"""ToDo:
	Implement plant mines/trapping
		if other player would be faster trap 

	Avoid other players --> take alternative path if another player is in the way and alternative path is good 

	maybe adjust speed based on other players
		if it sees that other players are fast and better positioned stay

		
	"""

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
		   # print("Too far won't move ","-"*80)
			return []

		bestpath = paths.shortestPathFrom(pos)
		

		best_d = self.conv_path_to_directions(pos,bestpath[1:],gLoc)


		#calculates the number steps based on the distance to the pot. Steps increase with shorter distance 
		numMoves = round((len(best_d)/d_to_pot)*5)

		

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


			  
			  
 
class lmiksch_naive(Player):
	"""Naive bot which tries to move to the goldpot based on the position
		
	"""

	def __init__(self):
		self.map = map
		
		



	def reset(self, player_id, max_players, width, height):
		self.player_name = "lmiksch_naive"
		self.visited = [[0] * width  for x in range(height)]
		self.ourMap = Map(width,height)
		self.gLoc = None
		
		
	
	def round_begin(self, r):
		
		pass
	  
	def move(self, status):
		print("hello")
		# the status object (see game_utils.Status) contains:
		# - .player, our id, if we should have forgotten it
		# - .x and .y, our position
		# - .health and .gold, how much health and gold we have
		# - .map, a map of what we can see (see game_utils.Map)
		#   The origin of the map is in the lower left corner.
		# - .goldPots, a dict from positions to amounts
		
		moves = []
		self.gLoc
		
		ourMap = self.ourMap
	   
		for x in range(ourMap.width):
				for y in range(ourMap.height):
						if status.map[x, y].status != TileStatus.Unknown:
								ourMap[x, y].status = status.map[x, y].status
		pos = (status.x,status.y)
	   
		for coord,amount in status.goldPots.items():
			x_goldPot = coord[0]
			y_goldPot = coord[1]
			gold = amount
	  

		gLoc = next(iter(status.goldPots))

		
		#calculate min distance to goldpot if distance < gold do nothing
		d_to_pot = abs(pos[0] - x_goldPot) + abs(pos[1] - y_goldPot)

		if d_to_pot > gold:
		   # print("Too far won't move ","-"*80)
			return []

		
		move = self.possible_moves(status,ourMap,self.visited)



		#print(self.visited)
		print(move,"hello")

		
		return [move]


	def possible_moves(self,status,ourMap,visited):
		

		neighbours = []
		for d in D:
			diff = d.as_xy()
			coord = status.x + diff[0], status.y + diff[1]
			if coord[0] < 0 or coord[0] >= status.map.width:
				continue
			if coord[1] < 0 or coord[1] >= status.map.height:
				continue
			tile = ourMap[coord]
			if tile.status != TileStatus.Wall:
				neighbours.append((d, coord))
		if len(neighbours) == 0:
			print("Seriously map makers? Thanks!")
			assert False

		#print("X"*50)
		#print(neighbours)
		#print("x"*50)
		best_move = []
		best_dir = None
		best_move_diff = 999
		gLoc = next(iter(status.goldPots))
		
		
		for d, dir in neighbours:
			diff = d.as_xy()
			c_diff = abs(gLoc[0] - dir[0]) + abs(gLoc[1] - dir[1])
			print(d,c_diff)
			
			if c_diff < best_move_diff and self.visited[dir[0]][dir[1]] == 0:
				
				best_move_diff = c_diff
				best_move.append(d)
				best_dir = dir
				
					
		print("Error: 1",best_move[-1])
		

		#self.visited[dir[0]][dir[1]] = 1 

		#print(best_move,best_dir)
		
		return best_move[-1]

			

			







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


			  
					 

   

	

players = [lmiksch_bot(),lmiksch_naive()]