#!/usr/bin/env python3
import random

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player


class MyNonRandomPlayer(Player): #thic code is from test-RobotRace, I just could not import it somehow
    def reset(self, player_id, max_players, width, height):
        self.player_name = "NonRandom" # nameFromPlayerId(player_id)
        self.ourMap = Map(width, height)

    def round_begin(self, r):
        pass

    def move(self, status):
        # print("-" * 80)
        # print("Status for %s" % self.player_name)
        # print(status)

        ourMap = self.ourMap
        # print("Our Map, before")
        # print(ourMap)
        for x in range(ourMap.width):
            for y in range(ourMap.height):
                if status.map[x, y].status != TileStatus.Unknown:
                    ourMap[x, y].status = status.map[x, y].status
        # print("Our Map, after")
        # print(ourMap)


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

        assert len(status.goldPots) > 0
        gLoc = next(iter(status.goldPots))
        dists = []
        for d, coord in neighbours:
            dist = max(abs(gLoc[0] - coord[0]), abs(gLoc[1] - coord[1]))
            dists.append((d, dist))
        d, dist = min(dists, key=lambda p: p[1])

        #print("Gold is at", gLoc)
        #print("Best non-wall direction is", d, "with distance", dist)
        return [d]

class MyTrappingPlayer(MyNonRandomPlayer):
    def trap_random_player(self, status):
        if status.gold > 20:
            return True


players = [MyTrappingPlayer()]
