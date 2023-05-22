#!/usr/bin/env python3

from game_utils import Direction as D
from game_utils import TileStatus
from game_utils import Map
from player_base import Player
import random
from shortestpaths import AllShortestPaths

class MyDumbPlayer(Player):
    def reset(self, player_id, max_players, width, height):
        self.player_name = "Dumb Kat"
        self.ourMap = Map(width, height)
        self.moves = [D.up, D.left, D.down, D.right, D.up_left, D.down_left,D.down_right, D.up_right]

    def round_begin(self, r):
        pass

    def move(self, status):
        ourMap = self.ourMap
        # print("Our Map, before")
        for x in range(ourMap.width):
            for y in range(ourMap.height):
                if status.map[x, y].status != TileStatus.Unknown:
                    ourMap[x, y].status = status.map[x, y].status

        self.ourMap = ourMap
        x,y = status.x, status.y
        numMoves = random.randint(0, 5)
        moves = []
        for i in range(numMoves):
            while True:
                m = self.moves[random.randint(0, len(self.moves) - 1)]
                d_x, d_y = m.as_xy()
                new_x, new_y = x + d_x, y + d_y
                if 0 <= new_y < ourMap.height and 0 <= new_x < ourMap.width:
                    if status.map[new_x, new_y].status != TileStatus.Wall:
                        moves.append(m)
                        x, y = new_x, new_y
                        break
        return moves


class MyNotSoDumbPlayer(Player):
    def reset(self, player_id, max_players, width, height):
        self.player_name = "smart Kat"
        self.ourMap = Map(width, height)
        self.moves = [D.up, D.left, D.down, D.right, D.up_left, D.down_left, D.down_right, D.up_right]
        self.gold = None
        # self.players = list(range(max_players))
        # self.players.remove(player_id)
        # self.players = {key: None for key in self.players}

    def round_begin(self, r):
        pass

    def move(self, status):
        self.gold = status.gold
        self.health = status.health
        ourMap = self.ourMap
        players = {}
        for x in range(ourMap.width):
            for y in range(ourMap.height):
                tile = status.map[x, y]
                if tile != TileStatus.Unknown:
                    ourMap[x, y].status = tile.status
                    obj = tile.obj
                    if obj is not None:
                        if obj.is_gold():
                            continue
                        else:
                            if obj.is_player(status.player):
                                continue
                            else:
                                other_player_id = obj.as_player()
                                players[other_player_id] = (x,y)
        self.ourMap = ourMap
        pot = status.goldPots
        print(status.goldPots)
        pot_x, pot_y = next(iter(pot))[0], next(iter(pot))[1]
        x,y = status.x, status.y
        # numMoves = random.randint(1, 10)
        numMoves = self.calculate_actions(self.gold*0.1)
        moves = []
        paths = AllShortestPaths((pot_x, pot_y), ourMap)

        if players:
            paths_players = []
            for play_x, play_y in players.values():
                path = paths.shortestPathFrom((play_x, play_y))
                maxima = min(len(path), 5)
                try:
                    paths_players.append(paths.shortestPathFrom((play_x, play_y)[0:maxima]))
                except:
                    pass

        for i in range(1, numMoves):
            neigh = [n for n in paths.nonWallNeighborsIter((x, y))]
            cur_short_path = paths.shortestPathFrom((x, y))
            if (pot_x, pot_y) in neigh:
                dir_x, dir_y = pot_x - x, pot_y - y
                moves.append(coor_to_dir(dir_x, dir_y))
                return moves
            elif cur_short_path[1] in neigh and self.ourMap[cur_short_path[1]].status == TileStatus.Empty:
                #if
                dir_x, dir_y = cur_short_path[1][0]-x, cur_short_path[1][1]-y
                if dir_x != 0 or dir_y != 0:
                    move = coor_to_dir(dir_x, dir_y)
                    if players:
                        if not self.is_element_in_lists(move, paths_players):
                            x, y = cur_short_path[1][0], cur_short_path[1][1]
                            moves.append(move)
                        else:
                            new_neig = neigh.copy()
                            new_neig.remove(cur_short_path[1])
                            move = random.choice(new_neig)
                            x, y = cur_short_path[1][0], cur_short_path[1][1]
                            moves.append(move)
                    else:
                        x, y = cur_short_path[1][0], cur_short_path[1][1]
                        moves.append(move)
            else:
                return moves
        return moves

    def calculate_actions(self, gold, max_action_cost = 70):
        k = 0
        total_cost = 0
        while total_cost <= gold:  #and total_cost <= max_action_cost
            k += 1
            total_cost += k
        return k - 1

    def is_element_in_lists(self, element, list_of_lists):
        for sublist in list_of_lists:
            if element in sublist:
                return True
        return False



def coor_to_dir(x,y):
    d = {
        D.up: (0, 1),
        D.down: (0, -1),
        D.left: (-1, 0),
        D.right: (1, 0),
        D.up_left: (-1, 1),
        D.up_right: (1, 1),
        D.down_left: (-1, -1),
        D.down_right: (1, -1),
    }
    d_swap = {v: k for k, v in d.items()}
    return d_swap[(x,y)]


players = [MyDumbPlayer(), MyNotSoDumbPlayer()]