from enum import Enum
import random
from collections import deque
import copy

def nameFromPlayerId(i): # convert numeric ID into alphabetic name
	assert i >= 0
	assert i <= ord("z") - ord("a") + 1
	return chr(ord("a") + i)


class Direction(Enum):
	up = 0 
	down = 1
	left = 2
	right = 3
	up_left = 4
	up_right = 5
	down_left = 6
	down_right = 7

	def as_xy(self): # movement in the 2D space as dictionary with enumerations as keys and tuples as values
		return {
			self.up:         ( 0,  1),
			self.down:       ( 0, -1),
			self.left:       (-1,  0),
			self.right:      ( 1,  0),
			self.up_left:    (-1,  1),
			self.up_right:   ( 1,  1),
			self.down_left:  (-1, -1),
			self.down_right: ( 1, -1),
		}[self] # just regular dictionary call of self, dct[key] = value

	def __str__(self): # as_xy as string representation, called by concatenation str(Direction.up) -> "UP"
		return {
			self.up:         "UP",
			self.down:       "DOWN",
			self.left:       "LEFT",
			self.right:      "RIGHT",
			self.up_left:    "UP LEFT",
			self.up_right:   "UP RIGHT",
			self.down_left:  "DOWN LEFT",
			self.down_right: "DOWN RIGHT",
		}[self]
# print(Direction.up.as_xy()) -> (0,1)
# print(str(Direction.up)) -> "UP" (as string)
# print(Direction.up) -> "UP" (as enum object)

class MoveStatus(Enum): 
	Pending = 0
	Done = 1
	CrashWall = 2 # includes crashing into mines
	CrashPlayer = 3
	OutOfGold = 4
	OutOfHealth = 5
	Cancelled = 6  # used for any move after something went wrong

class TileStatus(Enum): # after entering a tile what happens
	Unknown = 0 # 4 states
	Empty = 1
	Wall = 2
	Mine = 3

	def is_blocked(self):
		"""
		Tiles can be blocked by either walls or mines
		"""
		return self==self.Wall or self==self.Mine
	
	@staticmethod # can be called on the class without needing an instance
	def strings():
		return ["_", ".", "#"] # TileStatus.strings() returns this list used for the unstr method
	# why not just strings = [...]? To ensure that the list is encapsulated and associated within the class

	@classmethod # method bound to class rather than instance of the class
	def unstr(cls,x): # ..it has access to the class attributes but not on the instance specific data
		return cls(cls.strings().index(x)) # conventionally first parameter cls is the class itself
	# cls.strings().index('.') accesses the index of 1 of the 3 chars and cls(1) creates the TileStatus object enum Tilestatus.Empty 

	def __str__(self): # returns string representation of each tile status
		return { # str(TileStatus.Unknown) will return the string "_"
			self.Unknown: "_",
			self.Empty:  ".",
			self.Wall: "#",
			self.Mine: "&"
		}[self]


class TileObject(object): # creats different types of objects, check their properties, also takes an object as argument and obtain their string representations
	@staticmethod
	def makePlayer(i): # ID of the player as input
		assert i >= 0
		return TileObject(i)

	@staticmethod
	def makeGold():
		return TileObject(-1) # ID -1 is reserved for a gold object

	def __init__(self, i): # constructor, called upon creation of new tile object, with player ID as parameter
		self._i = i # assign the value of i to the i attribute of the instance
		assert i >= -1

	def is_gold(self):
		return self._i == -1

	def is_player(self, pId=None): # pId is an optional parameter and is None if none passed
		if pId is None:
			return self._i >= 0 # True if the player has a positive Id as attribute, if not its not a player object
		else:
			return self._i == pId # If an Id is passed the method is asked the question..
		# ..."is this the Id of this player" if true it is per se automatically also a player
		# if i would pass -1 it also returned True (but why should I pass it in the first place)

	def as_player(self): # returns Id	
		assert self.is_player()
		return self._i

	def __str__(self):
		sym="."
		if self.is_gold():
			sym = "$"
		elif self.is_player():
			sym = chr(ord('A') + self._i)
		return '\033[91m'+'\033[1m'+sym+'\033[0m'

class Tile(object): # tile with a status and an optinal object		
	def __init__(self, status, obj=None):
		if obj is not None and not isinstance(obj, TileObject): # checks if object is provided and if its a valid TileObject instance
			raise TypeError("Tile.obj must be a TileObject or None.")
		self.status = status
		self.obj = obj
		if obj is not None:
			assert not is_blocked() # tile is free (status.is_blocke?)

	def is_blocked(self):
		return self.status.is_blocked() # delegetes to the Tilestatus analog method ot check if the status is wall or mine

	def __str__(self):
		if self.obj is not None:
			return str(self.obj) # returns string representation of object
		else:
			return str(self.status) # returns string representation of tile status


#The Map class provides methods for creating maps, accessing and modifying tiles, 
# checking connectivity, and generating random maps. It serves as a representation 
# of a grid-based map in the application or game using this code.
class Map(object):
	def __init__(self, width, height):
		"""Make a map full of 'unknown'."""
		self.width = int(width)
		self.height = int(height)
		assert width > 0
		assert height > 0
		self._data = []
		for y in range(height): # every tile status is set to unknown and represented as a 2D grid
			row = []
			for x in range(width):
				row.append(Tile(TileStatus.Unknown))
			self._data.append(row)

	def __str__(self): # string representation of the map (drawing)
		return "\n".join(" ".join(str(tile) for tile in row) 
			# for row in self._data) + "\n"
			for row in reversed(self._data)) + "\n" # mirrors map vertically (but why?)

	def __getitem__(self, coord): # access individual tiles, coord is a tuple 
		assert coord[0] >= 0
		assert coord[1] >= 0
		assert coord[0] < self.width
		assert coord[1] < self.height
		return self._data[coord[1]][coord[0]] # tile retrieved from data grid

	def __setitem__(self, coord, val):
		assert coord[0] >= 0
		assert coord[1] >= 0
		assert coord[0] < self.width
		assert coord[1] < self.height
		self._data[coord[1]][coord[0]] = val # set value of a tile

	@staticmethod
	def makeEmpty(width, height): # creates new map instance with empty tiles
		m = Map(width, height)
		for y in range(height):
			for x in range(width):
				m._data[y][x] = Tile(TileStatus.Empty)
		return m

	# return the non-Wall (actually, non-blocked) neighbors of a field (x,y)
	def nonWallNeighbours(self,xy):
		neighbours = []
		for d in Direction: # iterates over all direction defined in the Direction enum
			diff = d.as_xy() # coordinates of neighbouring tiles calculated by adding corresponding..
			coord = xy[0] + diff[0], xy[1] + diff[1] # .. x and y differences
			if coord[0] < 0 or coord[0] >= self.width: # if tile is within the boundaries and not blocked
				continue
			if coord[1] < 0 or coord[1] >= self.height:
				continue
			tile = self[coord]
			if not tile.is_blocked():
				neighbours.append((d, coord)) # .. it is added to the neighbours list as tuple of direction d and coordinates
		return neighbours

	def _find_first_if(self,testfun): # finds first tile in map	that satisfies a specified condition..
		for x in range(self.width): # .. specified by the 'testfun' function ("find first tile that fullfills testfunction condition"). It checks every tile.
			for y in range(self.height): # .. see def connected
				if testfun(self._data[y][x]):
					return (x,y) # if a tile is found its coordinates are returned, else None is returned.
		return None

	def _count_if(self,testfun): # counts number of tiles in the map that satisfy condnition..
		count = 0 # .. specified by 'testfun' function
		for x in range(self.width):
			for y in range(self.height):
				if testfun(self._data[y][x]):
					count += 1
		return count

	def _connected(self): # checks if all the empty tiles are connected to each other (all empty files must be reachable)
		def is_empty(x): return x.status == TileStatus.Empty # return True if tile x is empty

		xy = self._find_first_if(is_empty) # xy = first empty tile

		front = deque() # double-ended queue (imported module). Add/Removal from both ends.
		front.append(xy) # append right end, left would be ".appendleft()"

		accessible=set() # keep track of visited coordinates
		accessible.add(xy)

		# mark all accessible fields via BFS (breadth first search to visit all empty tiles..
		while front:# ..connected to the initial tile
			xy=front.popleft()
	
			for d,neighbour in self.nonWallNeighbours(xy): # nonWallneighbours returns a list of tuples (direction, coordinates) the non wall neighbours of a field
				if neighbour not in accessible:
					front.append(neighbour) # If a neighbor is not already marked as accessible, 
					accessible.add(neighbour) # ..it is added to the front deque and marked as accessible in the accessible set.


		return len(accessible) == self._count_if(is_empty) # right term describes number of empty tiles on the map,..
		# if the number matches the number of connected tiles, we can state that ALL empty tiles are connected

	@staticmethod
	def makeRandom(width, height, p):
		## assume that p is not too large; otherwise
		## resampling is very uneffective

		assert p<=0.4

		while True: # until connected map is found
			m = Map(width, height)
			for y in range(height):
				for x in range(width):
					if random.random() < p: # for probability <p a wall is set, else tile remains empty
						s = TileStatus.Wall
					else:
						s = TileStatus.Empty
					m._data[y][x] = Tile(s)

			if m._connected():
				return m
			#print("Resample map")
			#print(m)

	@staticmethod
	def read(filename): # reads a map from the given file (containing string map)
		## assume that p is not too large; otherwise
		## resampling is very uneffective

		def toTile(x): # not in use so far
			return { '_': TileStatus.Unknown, #invisible
					'.': TileStatus.Empty,
					'#': TileStatus.Wall
					}[x]

		with open(filename) as fh:
			data = [[ Tile(TileStatus.unstr(x)) for x in line.strip() ] # from the file it generates a grid with the..
				for line in fh.readlines() ] # .. status of each tile in unstring/enum format (converted from string format)

		height = len(data)
		width=0
		if height>0: width = len(data[0])

		m = Map(width,height)
		m._data = data
		return m

## The game parameters
class GameParameters(object):
	def __init__(self):
		self.maxNumGoldPots = 1
		self.initialGoldPotAmount = 100
		self.initialGoldPerPlayer = 99
		self.goldPerRound = 1
		self.goldPotTimeOut = 20 # after how many rounds the pot is emptied and replaced
		self.goldDecrease = True #does the amount of gold in the pot(s) decrease after a certain time
		self.goldDecreaseTime = self.goldPotTimeOut/2; #after which time does the amount of gold in the pot(s) decrease 
		self.healthPerRound = 10
		self.minMoveHealth = 30 # minimum health that allows to move
		self.maxHealth = 100
		self.visibility = 6
		self.healthPerWallCrash = 25
		self.healthPerPlayerCrash = 15
		self.healthPerPlayerCrashRandom = 5

		self.moveTimeout = 2 # players get at most moveTimeout seconds to answer each move request

		self.mineExpiryTime = 3 # how many rounds do mines exist

		self._cost = [0]

	# the cost of actions
	def cost(self,actions):
		assert actions >= 0
		if actions >= len(self._cost):
			self._cost.append( self.cost(actions-1)+actions )
		return self._cost[actions]


# The Status class encapsulates the relevant information about a player's status in the game. 
# It provides a convenient way to access and manipulate the player's position, health, 
# gold, and other relevant game information associated with the player.
class Status(object): # Player status
	def __init__(self, player, *, x, y, health, gold=0, params=None):
		self.player = player
		self.x = x
		self.y = y
		self.health = health
		self.gold = gold

		# info in the public status provided to players
		self.params = copy.deepcopy(params) # copy of the game parameters object

		self.map = None # limited info about map
		self.others = None # limited info about other players in the visibility range
		self.goldPots = None # dict: (x, y) -> amount (arbitrary amount of pots in the game)

	def __str__(self): # string representation of the players status
		s="Player "+str(self.player)+"\n"
		if self.map is not None: s += str(self.map)
		s += "Health: %d\nGold:   %d\n" % (self.health, self.gold)

		if self.goldPots is not None:
			for coord, amount in self.goldPots.items():
				s += "Gold pot, ({:>3}, {:>3}): {}\n".format(coord[0], coord[1], amount)
		return s
