#!/usr/bin/env python3
import random
import argparse

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player

parser = argparse.ArgumentParser(description="Robot Race Simulator 7000")
parser.add_argument('--viz', help="filename for the visualization of the race", type=str)
parser.add_argument('--number', help="number of rounds", type=int, default=1000)
parser.add_argument('--density', help="map density", type=float, default=0.4)
parser.add_argument('--framerate', help="specify framerate of the visualization", type=int, default=8)
parser.add_argument('--map', help="specify map file", type=str,default=None)

args = parser.parse_args()

# robot_module_names = {"Test":"test-RobotRace", # maps player names to their respective module names
# 					"Beatme": "beatme-RobotRace"}
# robot_module_names = {"Beatme": "beatme-RobotRace"}
robot_module_names = {"Fabio":"Fabio_GoodBot"}

robotmodules = { m:__import__(m) for m in robot_module_names.values() } # imports modules

if args.map is not None:
   m = Map.read(args.map) # if map file is passed
else:
   m = Map.makeRandom(20, 20, args.density) # random map if no map passed

sim = Simulator(map=m, vizfile=args.viz, framerate=args.framerate)

for name,module_name in robot_module_names.items():
	for p in robotmodules[module_name].players:
		p.player_modname = name
		sim.add_player(p)

sim.play(rounds=args.number)
