#!/usr/bin/env python3

import heapq
import random
from game_utils import Direction as D, TileStatus, Map
from player_base import Player

class AStarNode:
    """
    A class representing a node in the A* search algorithm.
    """
    def __init__(self, position, parent=None, g=0, h=0):
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
    def reset(self, player_id, max_players, width, height, rules=None):
        self.player_name = "AStarScout"
        self.ourMap = Map(width, height)
        self.rules = rules


    def round_begin(self, r):
        pass

    def _as_direction(self, curpos, nextpos):
        """
        Calculate the direction from the current position to the next position.
        """
        for d in D:
            diff = d.as_xy()
            if (curpos[0] + diff[0], curpos[1] + diff[1]) == nextpos:
                return d
        return None

    def random_valid_direction(curpos, our_map):
        """
        Return a random valid direction from the current position.
        """
        possible_directions = []
        for direction in D:
            next_x, next_y = curpos[0] + direction.as_xy()[0], curpos[1] + direction.as_xy()[1]
            if (0 <= next_x < our_map.width) and (0 <= next_y < our_map.height) and our_map[next_x, next_y].status != TileStatus.Wall:
                possible_directions.append(direction)
        return random.choice(possible_directions)

    def move(self, status):
        our_map = status.map
        curpos = (status.x, status.y)
        assert len(status.goldPots) > 0
        g_loc = next(iter(status.goldPots))
        # Compute A*-search to find the best path to the gold pot
        path = a_star_search(curpos, g_loc, our_map)
        # If no path is found, move randomly
        if not path:
            return [random_valid_direction(curpos, our_map)]
        # Reduce the path to the next steps
        num_moves = min(1, len(path) - 1)
        path = path[:num_moves + 1]
        # Calculate the directions the robot should go
        directions = [self._as_direction(cur, next) for cur, next in zip(path, path[1:])]

        # Check if the trap method exists and if the player has enough gold to set a trap
        if hasattr(self.rules, 'trap') and self.rules.gold[self.player] >= 20:
            self.rules.trap(self.player)

        return directions

players = [MyAStarPlayer()]


players = [MyAStarPlayer()]
