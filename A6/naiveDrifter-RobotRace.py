#!/usr/bin/env python3
import random
import numpy as np

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player


class NaiveDrifter(Player):
    def reset(self, player_id, max_players, width, height):
        # the player_id is an int, which can be converted to the name printed in the board
        self.player_name = "Erratic"
        # we will draw a random move every round
        self.moves = [D.up, D.left, D.down, D.right, D.up_left, D.down_left,
                      D.down_right, D.up_right]

    # print("Hi there! We are playing ",self.status.params.rounds," rounds.")

    def round_begin(self, r):
        print("Welcome to round ", r, "---", self.status.params.rounds - r + 1, " to go.")
        pass

    def set_mines(self, status):
        """
		set mines for fun
		"""

        map = status.map
        mines = []
        for i in range(5):
            if random.randint(0, 100) < 10:
                x, y = status.x, status.y
                x += random.randint(0, 3)
                y += random.randint(0, 3)

                if (x >= 0 and x < map.width and y >= 0 and y < map.height
                        and not map[x, y].is_blocked() and map[x, y].obj is None):
                    mines.append((x, y))
            else:
                break
        return mines

    def move(self, status):
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
        # print(status.map)  # the map can be printed too, but printing the status
        # does this as well
        # for illustration, we go through the map and find stuff
        for x in range(status.map.width):
            for y in range(status.map.height):
                tile = status.map[x, y]
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
                        if obj.is_player(status.player):
                            # we found our selfs
                            assert (x, y) == (status.x, status.y)
                        else:
                            # we found someone else!
                            other_player_id = obj.as_player()
        radsd





        # make a random number of moves in a random direction
        numMoves = random.randint(0, 5)
        moves = []
        for i in range(numMoves):
            m = self.moves[random.randint(0, len(self.moves) - 1)]
            moves.append(m)
        return moves


players = [NaiveDrifter()]
