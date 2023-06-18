#!/usr/bin/env python3

import heapq
import random
from game_utils import Direction as D, TileStatus, Map
from player_base import Player
from collections import deque

class AStarNode:
    """
    A class representing a node in the A* search algorithm.
    """
    def __init__(self, position, parent=None, g=0, h=0):
        """
        Initialize a new node with the given position, parent node, cost to reach the node from the start node, and estimated cost to reach the goal node from the current node.
        """
        self.position = position
        self.parent = parent
        self.g = g  # The cost to reach the current node from the start node
        self.h = h  # The estimated cost to reach the goal node from the current node
        self.f = g + h  # The total estimated cost of the cheapest solution through the current node

    def __eq__(self, other):
        """
        Check if two nodes are equal based on their position. This is needed to check if a node is already in the open list.
        """
        return self.position == other.position

    def __lt__(self, other):
        """
        Compare two nodes based on their total estimated cost. This is needed to sort the open list.
        """
        return self.f < other.f

def heuristic(pos1, pos2):
    """
    Compute the heuristic distance between two positions using the Manhattan distance.
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def a_star_search(start, goal, our_map):
    """
    Perform A* search algorithm to find the shortest path from start to goal on the given map.
    """
    start_node = AStarNode(start, None, 0, heuristic(start, goal))
    open_list = [start_node]
    closed_list = []

    while open_list:
        current_node = heapq.heappop(open_list)

        # Check if we have reached the goal node
        if current_node.position == goal:
            path = []
            while current_node is not None:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        closed_list.append(current_node)

        # Check all neighbors of the current node and add them to the open list if they are not already there
        for direction in D:
            neighbor_pos = (current_node.position[0] + direction.as_xy()[0],
                            current_node.position[1] + direction.as_xy()[1])

            if (neighbor_pos[0] < 0 or neighbor_pos[0] >= our_map.width or
                    neighbor_pos[1] < 0 or neighbor_pos[1] >= our_map.height):
                continue

            neighbor_tile = our_map[neighbor_pos[0], neighbor_pos[1]]
            if neighbor_tile.status == TileStatus.Wall:
                continue

            neighbor_node = AStarNode(neighbor_pos, current_node,
                                      current_node.g + 1, heuristic(neighbor_pos, goal))

            if any(closed_node == neighbor_node for closed_node in closed_list):
                continue

            open_node = next((node for node in open_list if node == neighbor_node), None)
            if open_node is not None and open_node.g <= neighbor_node.g:
                continue

            heapq.heappush(open_list, neighbor_node)

    return []

class MyAStarPlayer(Player):
    """
    A custom player class implementing the A* search algorithm to find the shortest path to gold.
    """
    def __init__(self):
        super().__init__()
        self.player_name = "Another AStarScout" 
        self.ourMap = None
        self.visited = None

    def reset(self, player_id, max_players, width, height):
        """
        Reset the player's state at the beginning of a new game.
        """
        self.ourMap = Map(width, height)
        self.visited = [[0] * width for _ in range(height)]

    def round_begin(self, r):
        """
        This method is called at the beginning of each round.
        """
        pass

    def _update_map(self, status):
        """
        Update our map with the current status of the game map.
        """
        for x in range(self.ourMap.width):
            for y in range(self.ourMap.height):
                if status.map[x, y].status != TileStatus.Unknown:
                    self.ourMap[x, y].status = status.map[x, y].status

    def _as_direction(self, curpos, nextpos):
        """
        Calculate the direction from the current position to the next position.
        """
        for d in D:
            diff = d.as_xy()
            if (curpos[0] + diff[0], curpos[1] + diff[1]) == nextpos:
                return d
        return None

    def _get_path_to_gold(self, status):
        """
        Use the A* search algorithm to find the shortest path to the gold pot with the most gold.
        """
        gLoc = max(status.goldPots, key=status.goldPots.get)
        return a_star_search((status.x, status.y), gLoc, self.ourMap)

    def move(self, status):
        """
        Determine the player's move based on the current status.
        """
        self._update_map(status)
        if not status.goldPots: return []
        path = self._get_path_to_gold(status)
        if not path: return []
        directions = [self._as_direction(cur, next) for cur, next in zip(path, path[1:])]
        num_moves = round((len(directions) / len(path)) * 5)
        if num_moves > 0 and len(path) / num_moves > status.goldPotRemainingRounds:
            num_moves = 0
        return directions[:num_moves]

    def set_mines(self, status):
        """
        #Set mines on the path to the gold pot if an enemy player is near.
        """
        if hasattr(self.rules, 'set_mine') and self.rules.gold[self.player] >= 20:
            path = self._get_path_to_gold(status)
            if not path: return []
            for enemy in status.players:
                if any(heuristic(enemy, pos) <= 2 for pos in path):
                    self.rules.set_mine(self.player, pos)
                    return [pos]
        return []

    def fight_target_player(self, status):
        """
        Determine the target player to fight based on the current status.
        """
        if not status.others: return None
        # Filter out None values from status.others
        valid_others = [player for player in status.others if player is not None]
        if not valid_others: return None  # Return None if valid_others is empty
        weakest_player = min(valid_others, key=lambda p: p.health)
        if status.health > weakest_player.health:
            return weakest_player.player
        return None

    def possible_moves(self, status):
        """
        Determine the best possible move based on the current status.
        """
        neighbours = [((d, coord), abs(gLoc[0] - dir[0]) + abs(gLoc[1] - dir[1])) for d in D for coord in [(status.x + diff[0], status.y + diff[1])] if 0 <= coord[0] < status.map.width and 0 <= coord[1] < status.map.height and self.ourMap[coord].status != TileStatus.Wall and self.visited[coord[0]][coord[1]] == 0]
        assert neighbours, "No possible moves"
        gLoc = next(iter(status.goldPots))
        best_move = min(neighbours, key=lambda x: x[1])[0][0]
        return best_move

players = [MyAStarPlayer()]