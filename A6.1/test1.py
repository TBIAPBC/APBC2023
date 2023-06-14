from enum import Enum
import random
from collections import deque
import copy
class Direction(Enum):
	up = 0 #enumeration names and values 
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
	
a = Direction.up
b = (0,1)
print(Direction.as_xy[0])
print(a)