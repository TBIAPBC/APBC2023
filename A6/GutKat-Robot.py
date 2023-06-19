#!/usr/bin/env python3
import math

import numpy as np

from game_utils import Direction as D
from game_utils import TileStatus
from game_utils import Map
from player_base import Player
import random
from shortestpaths import AllShortestPaths



class GutKat_player(Player):
    def reset(self, player_id, max_players, width, height):
        self.player_name = "GutKat"
        self.myMap = Map(width, height)
        self.moves = [D.up, D.left, D.down, D.right, D.up_left, D.down_left, D.down_right, D.up_right]
        self.gold = 100
        self.players = {}
        self.paths_players = []
        self.mines = {}
        self.last_moves = []
        self.round = 0
        self.stuck = 0
        self.mine_exp_time = 3
        self.position = (None, None)
        self.total_cost = 0
        self.k = 0
        self.path = None
        self.goldPotTimeOut = 0
        self.goldPosition = (None, None)
        self.gold_amount = None
        self.set_mine = None
        self.mode = {"map": "normal", "players": max_players}
        if width >= 40:
            self.mode["map"] = "big"



    def round_begin(self, r):
        self.round = r
        self.k = 0
        self.total_cost = 0

    def move(self, status):

        #get gold, health, gold location, robot location and and map
        self.gold = status.gold
        self.health = status.health
        myMap = self.myMap
        pot = status.goldPots

        #pot_money =
        pot_x, pot_y = next(iter(pot))[0], next(iter(pot))[1]
        rob_x, rob_y = status.x, status.y
        self.gold_amount = (pot[pot_x, pot_y])
        if self.goldPosition == (pot_x, pot_y):
            self.goldPotTimeOut += 1
        else:
            self.goldPotTimeOut = 0

        self.goldPosition = (pot_x, pot_y)

        #check if some of my mines are still valid
        self.check_mines()

        # reset players and paths - they (probably) moved in last round
        players = self.players
        paths_players = self.paths_players

        moves = []
        # euclidean distance to pot
        distance_pot = math.sqrt((rob_x - pot_x) ** 2 + (rob_y - pot_y) ** 2)
        # paths to the gold
        paths = AllShortestPaths((pot_x, pot_y), myMap)
        # calculate number of moves to gold
        numMoves = self.calculate_actions(self.gold, paths, (rob_x,rob_y), distance_pot)

        neighbour_near = False
        pls_move = False

        paths = AllShortestPaths((pot_x, pot_y), myMap)
        # if we are in same position as before - we did not move -> we could be stuck
        if (rob_x,rob_y) == self.position:
            self.stuck += 1
            neigh = [n for n in paths.nonWallNeighborsIter((rob_x, rob_y))]
            neighbours = []
            for n in neigh:
                neighbours.append([x for x in paths.nonWallNeighborsIter(n)])
            flat_neigh = [item for sublist in neighbours for item in sublist]
            for pos in players.values():
                if pos in flat_neigh:
                    neighbour_near = True

                    cur_short_path_me = paths.shortestPathFrom((rob_x, rob_y))
                    cur_short_path_enemy = paths.shortestPathFrom(pos)
                    try:
                        if cur_short_path_me[1] == cur_short_path_enemy[1]:
                            pls_move = True
                            self.set_mine = cur_short_path_enemy[1:3]
                    except:
                        pass


        # if not - we moved
        else:
            self.stuck = 0

        # update our position before moving
        self.position = (rob_x, rob_y)

        # if we are in same position for 2 rounds, we are probably stuck
        if self.stuck >= 1 and self.last_moves and neighbour_near or self.stuck >= 3 or pls_move:
            # if we are stuck, remember this position to be blocked (set to Wall)
            blocked_x, blocked_y = rob_x, rob_y
            myMap[blocked_x, blocked_y].status = TileStatus.Wall
            # neighbours of current position
            neigh = [n[1] for n in myMap.nonWallNeighbours((rob_x, rob_y))]
            # if we wanted to move last round, remove done step from neighbours
            try:
                move_x, move_y = self.last_moves[0].as_xy()
                move = (move_x + rob_x, move_y + rob_y)
                neigh.remove(move)
            except:
                pass

            if self.set_mine:
                try:
                    for mine in self.set_mine:
                        neigh.remove(mine)
                except:
                    pass

            # choose random from neighbours remaining
            if neigh:
                cor_x, cor_y = random.choice(neigh)
                # get direction
                dir_x, dir_y = cor_x - rob_x, cor_y - rob_y
                # get direction and append it
                move = coor_to_dir(dir_x, dir_y)
                moves.append(move)
                # remove done steps from total steps
                numMoves -= 1
                # reset stuck to 0
                self.stuck = 0
                # update our position and paths (blocked position)
                rob_x, rob_y = cor_x, cor_y
                paths = AllShortestPaths((pot_x, pot_y), myMap)



        # enumerate over our number of steps
        for i in range(0, numMoves):
            # get neighbors of current position
            neigh = [n for n in paths.nonWallNeighborsIter((rob_x, rob_y))]

            # get shortest path to gold
            cur_short_path = paths.shortestPathFrom((rob_x, rob_y))

            # if gold is in neighbour add this move to moves and return it
            if (pot_x, pot_y) in neigh:
                dir_x, dir_y = pot_x - rob_x, pot_y - rob_y
                moves.append(coor_to_dir(dir_x, dir_y))
                rob_x, rob_y = rob_x + dir_x, rob_y + dir_y
                self.last_moves = moves
                self.path = paths.shortestPathFrom((rob_x, rob_y))
                return moves

            # else check if our next best step is in neighbor and if the tile is empty and if the spot is save from mines
            elif cur_short_path[1] in neigh and self.myMap[cur_short_path[1]].status == TileStatus.Empty and self.save_spot(cur_short_path[1]):

                # if we found player iterate over them
                if players:
                    # only remember players which could interfere with us
                    danger_player = []
                    for player_path in paths_players:
                        # only intereseting in next 3 steps of player
                        maxima = min(len(player_path), 3)
                        if cur_short_path[1] in player_path[0:maxima]:
                            danger_player.append(player_path)

                    # if no dangerous player are found, proceed as normal
                    if not danger_player:
                        dir_x, dir_y = cur_short_path[1][0] - rob_x, cur_short_path[1][1] - rob_y
                        move = coor_to_dir(dir_x, dir_y)
                        rob_x, rob_y = cur_short_path[1][0], cur_short_path[1][1]
                        moves.append(move)

                    # if we found dangerous player
                    else:
                        danger = False
                        # check if they are closer or further away from gold than us
                        for player_path in danger_player:
                            if len(player_path) >= len(cur_short_path):
                                continue
                            # if they are closer to gold...
                            else:
                                # ...remove wanted step from possible next steps
                                neigh.remove(cur_short_path[1])
                                # if still some neighbour is remaining...
                                if neigh:
                                    # ...choose random one of neighbours
                                    n = random.choice(neigh)
                                    while not self.save_spot(n):
                                        n = random.choice(neigh)
                                    cor_x, cor_y = n
                                    dir_x, dir_y = cor_x - rob_x, cor_y - rob_y
                                    move = coor_to_dir(dir_x, dir_y)
                                    rob_x, rob_y = cor_x, cor_y
                                    moves.append(move)
                                    danger = True
                                    break
                                # if no neighbour are available, just return saved moves
                                else:
                                    self.last_moves = moves
                                    self.path = paths.shortestPathFrom((rob_x, rob_y))
                                    return moves
                        if not danger:
                            # if no dangerous player is closer to gold than us, just continue as normal
                            dir_x, dir_y = cur_short_path[1][0] - rob_x, cur_short_path[1][1] - rob_y
                            move = coor_to_dir(dir_x, dir_y)
                            rob_x, rob_y = cur_short_path[1][0], cur_short_path[1][1]
                            moves.append(move)

                # if we have no information about other players, continue as normal
                else:
                    dir_x, dir_y = cur_short_path[1][0] - rob_x, cur_short_path[1][1] - rob_y
                    move = coor_to_dir(dir_x, dir_y)
                    rob_x, rob_y = cur_short_path[1][0], cur_short_path[1][1]
                    moves.append(move)
            else:
                # else return saved moves
                self.last_moves = moves
                self.path = paths.shortestPathFrom((rob_x, rob_y))
                return moves
        self.last_moves = moves
        self.path = paths.shortestPathFrom((rob_x, rob_y))
        return moves


    def save_spot(self, position):
        #check if mine is set on this position
        if position in self.mines.values():
            return False
        return True

    def check_mines(self):
        # update mines
        new_mines = {}
        mines = self.mines
        for r in mines.keys():
            if r+self.mine_exp_time < self.round:
                new_mines[r] = mines[r]
        self.mines = new_mines


    def calculate_actions(self, gold, paths, position, gold_distance):
        '''
        mehr steps je näher ich beim pot bin!! change!!!
        '''
        x, y = position
        cur_short_path = paths.shortestPathFrom((x,y))
        steps_to_gold = len(cur_short_path)
        k = self.k
        total_cost = self.total_cost
        gold_amount = self.gold_amount

        gold = gold * 0.75
        if not gold_amount:
            gold_amount = 100

        paths_players = self.paths_players
        if paths_players:
            for player_path in paths_players:
                if self.myMap.width * (2/3) >= (steps_to_gold - len(player_path)):
                    return 1

        while total_cost <= gold and total_cost <= gold_amount:
            k += 1
            total_cost += k

        max_k = k - 1
        if gold >= 500:
            if max_k >= steps_to_gold:
                return max_k

        elif gold >= 300:
            return min(max_k, 4)

        else:
            if self.mode["map"] == "big":
                if steps_to_gold > (self.myMap.width * (1/2)):
                    self.stuck = 0
                    return 0
                if self.goldPotTimeOut >= 15:
                    self.stuck = 0
                    return 0

            #steps = round((steps_to_gold / gold_distance) * 4)
            steps = round((max_k / gold_distance) * 4)
            steps = max(1, steps) #maximal_step
            steps = min(steps, 3)
            return steps


    def is_element_in_lists(self, element, list_of_lists, path):
        if path:
            for sublist in list_of_lists:
                maxima = min(len(sublist), 2)
                if element in sublist[0:maxima]:
                    return True
            return False
        else:
            for sublist in list_of_lists:
                if element in sublist:
                    return True
            return False



    def set_mines(self, status):
        self.gold = status.gold
        self.health = status.health
        myMap = self.myMap
        pot = status.goldPots

        # pot_money =
        pot_x, pot_y = next(iter(pot))[0], next(iter(pot))[1]
        rob_x, rob_y = status.x, status.y
        self.gold_amount = (pot[pot_x, pot_y])
        self.goldPosition = (pot_x, pot_y)

        # reset players and paths - they (probably) moved in last round
        self.players = {}
        self.paths_players = []
        # check map
        players = {}
        for x in range(myMap.width):
            for y in range(myMap.height):
                tile = status.map[x, y]
                # if we know tile status - remember it
                if tile.status != TileStatus.Unknown:
                    myMap[x, y].status = tile.status
                    obj = tile.obj
                    if obj is not None:
                        if obj.is_gold():
                            continue
                        else:
                            # found myself
                            if obj.is_player(status.player):
                                continue
                            # found other player
                            else:
                                # remember other player in dictionary
                                other_player_id = obj.as_player()
                                players[other_player_id] = (x, y)

        paths = AllShortestPaths((pot_x, pot_y), myMap)
        # if we know where other players are calculate path to gold of players
        if players:
            paths_players = []
            for play_x, play_y in players.values():
                #path = paths.shortestPathFrom((play_x, play_y))
                try:
                    paths_players.append(paths.shortestPathFrom((play_x, play_y)))
                except:
                    pass
            # remember paths_player for next round (used for setting mines)
            self.paths_players = paths_players


        # update map
        self.myMap = myMap
        self.players = players

        mines = []
        k = self.k
        total_cost = self.total_cost
        if self.gold >= 100:
            if self.set_mine:
                for mine in self.set_mine:
                    mines.append(mine)
                    k += 1
                    total_cost += k
                self.set_mine = None

            if self.players and self.gold >= 150:
                path = paths.shortestPathFrom((rob_x, rob_y))

                for player_path in paths_players:
                    if len(player_path) < len(path) and len(player_path) < 8:
                        minima = min(1, len(player_path) - 1)
                        mine = player_path[minima]
                        mines.append(mine)
                        if random.random() > 1/16:
                            neigh = [n[1] for n in self.myMap.nonWallNeighbours(mine)]
                            second_mine = random.choice(neigh)
                            mines.append(second_mine)
                            k += 1
                            total_cost += k
                        k += 1
                        total_cost += k
            self.k = k
            self.total_cost = total_cost
            return mines
        else:
            return []


    def trap_random_player(self, status):
        if self.gold >= 200:
            if random.random() < (1/64):
                paths_players = self.paths_players
                path = self.path
                for player_path in paths_players:
                    if len(player_path) > len(path):
                        self.total_cost += 20
                        return True
            return False


    def fight_target_player(self, status):
        self.gold = status.gold
        self.health = status.health

        myMap = self.myMap
        rob_x, rob_y = status.x, status.y
        paths = AllShortestPaths((rob_x, rob_y), myMap)
        # calculate number of moves to gold

        if self.health >= 50 and self.players:
            near_enemy = None
            for iD in self.players:
                pos = self.players[iD]
                distance = len(paths.shortestPathFrom(pos))
                if distance == 1:
                    near_enemy = iD
                    break
            if near_enemy != None:
                return near_enemy
            return None






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


players = [GutKat_player()]
