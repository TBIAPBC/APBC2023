#!/usr/bin/env python3
import random

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player

class MyRandomPlayer(Player): # inherits from base class Player
	def reset(self, player_id, max_players, width, height):
		# the player_id is an int, which can be converted to the name printed in the board
		self.player_name = "Erratic"
		# we will draw a random move every round
		self.moves = [D.up, D.left, D.down, D.right, D.up, D.up_left, D.down_left,
						D.down_right, D.up_right]
		#print("Hi there! We are playing ",self.status.params.rounds," rounds.") # optional
	
	def round_begin(self, r): # prints sentence at every round begin
		print("Welcome to round ",r,"---",self.status.params.rounds-r+1," to go.")
		pass # probl. forgotten to delete

	def set_mines(self, status): # self= instance of the class, status= status object
		"""
		set mines for fun
		"""

		map = status.map # map retrieved from status object
		mines = [] # over the function i choose where to set mines and return the coordinates as list
		for i in range(5): # 5 times or until a rnd generated number is >= 10 (see else: break)
			if random.randint(0,100)<10: # ..in the random player this is used to randomly determine wether to set a mine or not
				x,y = status.x,status.y # coordinates of current tile
				x += random.randint(0,3) # preferred proximate tile to set a mine (here rndmly)
				y += random.randint(0,3)

				if (x>=0 and x<map.width and y>=0 and y<map.height # to avoid suicide and within the map
					and not map[x,y].is_blocked() and map[x,y].obj is None): # .. and if blocked, None to check if tile is not occupied by an object
					mines.append((x,y))
			else: break
		return mines


	def move(self, status): #1) Scans visible area 2) moves
		# the status object (see game_utils.Status) contains:
		# - .player, our id, if we should have forgotten it
		# - .x and .y, our position
		# - .health and .gold, how much health and gold we have
		# - .map, a map of what we can see (see game_utils.Map)
		#   The origin of the map is in the lower left corner.
		# - .goldPots, a dict from positions to amounts
		# print("-" * 80)
		# print("Status for %s" % self.player_name)
		# # print the map as we can see it, along with health and gold
		# print(status)
		# print(status.map)  # the map can be printed too, but printing the status does this as well
		# for illustration, we go through the map and find stuff
		for x in range(status.map.width): # status.map is die begrenzte sicht, i guess it scans over the visible tiles
			for y in range(status.map.height):
				tile = status.map[x, y] # status of a tile (?)
				# A tile has a 'status' and an object 'obj'.
				# See game_utils.TileStatus and game_utils.TileObject
				if tile.status == TileStatus.Wall:
					# we have discovered a wall!
					# which definitely shouldn't have any objects
					assert tile.obj is None
				obj = tile.obj
				if obj is not None:
					if obj.is_gold():
						# uhh, a pot of gold!
						amount = status.goldPots[x, y]
					else:
						assert obj.is_player()
						if obj.is_player(status.player): # our id
							# we found our selfs
							assert (x, y) == (status.x, status.y) # our coordinates
						else:
							# we found someone else!
							other_player_id = obj.as_player()
		# now the player nows all objects in visible area

		# make a random number of moves in a random direction
		numMoves = random.randint(0, 5)
		moves = []
		for i in range(numMoves):
			m = self.moves[random.randint(0, len(self.moves) - 1)] # m = move
			moves.append(m)
		return moves

class MyNonRandomPlayer(Player): # inherits from base class Player
	def reset(self, player_id, max_players, width, height): # initializes player with provided parameters
		self.player_name = "NonRandom" # nameFromPlayerId(player_id)
		self.ourMap = Map(width, height) # creates map object with specified dimensions and unknwon tiles

	def round_begin(self, r): # called at beginning of each round
		pass

	def move(self, status): # determines players next move, takes status parameter with information about the game state
		# print("-" * 80)
		# print("Status for %s" % self.player_name)
		# print(status)

		ourMap = self.ourMap # in def reset definiert = Map(width,height) which is an own class "Classname(attribute1, attribute2)""
		# print("Our Map, before")
		# print(ourMap)
		for x in range(ourMap.width): # player updates his internal map (ourMap) based on the known information in the 'status' object
			for y in range(ourMap.height): # .. by iterating over every tile
				if status.map[x, y].status != TileStatus.Unknown:
					ourMap[x, y].status = status.map[x, y].status # updates my map of unknown tiles with objects of visible tiles, instances x,y (on of the tiles) attribute 'status' ..
		# print("Our Map, after")								  # status is an object of the Status (?) class, which contains attribute map..
		# print(ourMap)											  # .. which has a status (status.map contains limited info about the map)


		neighbours = [] # non wall neighboring tiles are stored in the neighbours list (als directions - unterschied zum vorigen block)
		for d in D: # .. in diesem bot wird immer nur ein schritt gemacht ansonsten bräucht ich einen for loop für jedens schritt
			diff = d.as_xy()
			coord = status.x + diff[0], status.y + diff[1]
			if coord[0] < 0 or coord[0] >= status.map.width: # wenn nachbar außerhalb der map liegt wird er übersprungen
				continue
			if coord[1] < 0 or coord[1] >= status.map.height:
				continue
			tile = ourMap[coord]
			if tile.status != TileStatus.Wall:
				neighbours.append((d, coord))
		if len(neighbours) == 0:
			print("Seriously map makers? Thanks!")
			assert False

		assert len(status.goldPots) > 0 # Status.goldPots is a dictionary (x,y) -> amount (provided to player)
		gLoc = next(iter(status.goldPots))
		dists = []
		for d, coord in neighbours: # stores distances from every neighbour (excluding walls) to the gold pot and takes the minimal distanced neighbour to be the next move
			dist = max(abs(gLoc[0] - coord[0]), abs(gLoc[1] - coord[1])) # distance to gold pot is the bigger of the x and the y distance
			dists.append((d, dist))
		d, dist = min(dists, key=lambda p: p[1]) # lambda function to pick minimum of 'dist's not 'd's

		#print("Gold is at", gLoc)
		#print("Best non-wall direction is", d, "with distance", dist)
		return [d] # returned is the next direction as list (more moves not implemented in this bot)


players = [MyNonRandomPlayer(),
           MyRandomPlayer()]
