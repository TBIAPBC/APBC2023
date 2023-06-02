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

class BasePlayer(Player):
    """
    A base player class that implements the Player interface. This class can be used as a base for other player classes.
    """
    def __init__(self, player_name):
        self.player_name = player_name
        self.ourMap = None
        self.rules = None

    def reset(self, player_id, max_players, width, height, rules=None):
        """
        Reset the player's state at the start of a new game.
        """
        self.ourMap = Map(width, height)
        self.rules = rules

    def round_begin(self, r):
        """
        This method is called at the beginning of each round.
        """
        pass

    def random_valid_direction(self, curpos, our_map):
        """
        Return a random valid direction from the current position.
        """
        possible_directions = []
        for direction in D:
            next_x, next_y = curpos[0] + direction.as_xy()[0], curpos[1] + direction.as_xy()[1]
            if (0 <= next_x < our_map.width) and (0 <= next_y < our_map.height) and our_map[next_x, next_y].status != TileStatus.Wall:
                possible_directions.append(direction)
        if possible_directions:
            return random.choice(possible_directions)
        else:
            return None
        

class naivePlayer(BasePlayer):
    """
    A naive player that moves in a random direction that isn't a wall.
    """
    def __init__(self):
        super().__init__("NaiveScout")

    def move(self, status):
        """
        Determines the moves for the player in the current turn.

        This player will simply try to move in a random direction that isn't a wall.
        If it can't move, it will stay in place.
        """
        our_map = status.map
        curpos = (status.x, status.y)
        return [self.random_valid_direction(curpos, our_map)]


class MyAStarPlayer(BasePlayer):
    """
    A custom player class implementing the A* search algorithm to find the shortest path to gold.
    """
    def __init__(self):
        super().__init__("AStarScout")
        self.enemy_locations = {}  # Keep track of enemy locations
        
    def _as_direction(self, curpos, nextpos):
        """
        Calculate the direction from the current position to the next position.
        """
        for d in D:
            diff = d.as_xy()
            if (curpos[0] + diff[0], curpos[1] + diff[1]) == nextpos:
                return d
        return None

    def set_mines(self, status):
        """
        Sets a mine on the path to the gold pot if an enemy player is near.
        """
        mines = []  # List to store the positions where mines will be set

        # Check if the mine setting method exists and if the player has enough gold to set a mine
        if hasattr(self.rules, 'set_mine') and self.rules.gold[self.player] >= 20:
            # Compute A*-search to find the best path to the gold pot
            path = a_star_search(self.curpos, self.g_loc, self.ourMap)
            # If no path is found, do nothing
            if not path:
                return mines

            # Convert the path to a set for faster lookup
            path_set = set(path)

            # Check each enemy player
            for enemy in status.players:
                # If an enemy is near the path, set a mine
                if any(heuristic(enemy, pos) <= 2 for pos in path_set):
                    # Before setting a mine, check if the position is near a gold pot or in a narrow passage
                    if self.is_near_gold(pos, status) or self.is_in_narrow_passage(pos, status):
                        self.rules.set_mine(self.player, pos)
                        mines.append(pos)  # Add the position to the list of mines
                        return mines  # Return the list of mines as soon as one is set

        return mines  # Return the list of mines (empty if no mines were set)

    def is_near_gold(self, pos, status):
        """
        Check if a position is near a gold pot.
        """
        for gold_pos in status.goldPots:
            if heuristic(pos, gold_pos) <= 2:
                return True
        return False

    def is_in_narrow_passage(self, pos, status):
        """
        Check if a position is in a narrow passage.
        """
        open_spaces = 0
        for direction in D:
            next_pos = (pos[0] + direction.as_xy()[0], pos[1] + direction.as_xy()[1])
            if status.map[next_pos].status != TileStatus.Wall:
                open_spaces += 1
        return open_spaces <= 2

    def fight_target_player(self, status):
        """
        Called to ask the player wants to fight an adjacent player
        @param self the Player itself
        @param status the status
        @returns player_id of the enemy
        Currently the odds of winning are 0.7. The winner gets 5% of the gold of the losing player
        If a player does not define the method, this step is skipped.
        """
        if self.enemy_locations:  # Check if self.enemy_locations is not empty
            closest_player = min(self.enemy_locations.keys(), key=lambda player: heuristic(self.curpos, self.enemy_locations[player]))
            return closest_player
        else:
            return None  # Return None if there are no enemies

    def explore_map(self, curpos, our_map):
        """
        Explore the map using a breadth-first search algorithm.
        """
        visited = set()
        queue = deque([curpos]) # Use a deque to store the positions to visit

        while queue:
            pos = queue.popleft()
            if pos not in visited:
                visited.add(pos)
                for direction in D:
                    next_pos = (pos[0] + direction.as_xy()[0], pos[1] + direction.as_xy()[1])
                    if (0 <= next_pos[0] < our_map.width and 0 <= next_pos[1] < our_map.height and
                            our_map[next_pos[0], next_pos[1]].status != TileStatus.Wall):
                        queue.append(next_pos)
                if pos != curpos:
                    return self._as_direction(curpos, pos)
        return None

    def move(self, status):
        our_map = status.map
        curpos = (status.x, status.y)

        if status.goldPots:
            # If there are multiple gold pots, move towards the farthest one
            if len(status.goldPots) > 1:
                g_loc = max(status.goldPots, key=lambda g: heuristic(curpos, g))
            else:
                g_loc = next(iter(status.goldPots))
            # Compute A*-search to find the best path to the gold pot
            path = a_star_search(curpos, g_loc, our_map)
            # If no path is found, move randomly
            if not path:
                return [self.random_valid_direction(curpos, our_map)]
            # Reduce the path to the next steps
            num_moves = min(1, len(path) - 1)
            path = path[:num_moves + 1]
            # Calculate the directions the robot should go
            directions = [self._as_direction(cur, next) for cur, next in zip(path, path[1:])]
        else:
            # If there are no gold pots, explore the map
            direction = self.explore_map(curpos, our_map)
            if direction is not None:
                directions = [direction]
            else:
                directions = [self.random_valid_direction(curpos, our_map)]

        # Check if the trap method exists and if the player has enough gold to set a trap
        if hasattr(self.rules, 'trap') and self.rules.gold[self.player] >= 20:
            # Check each enemy player
            for enemy in status.players:
                if enemy != self.player:
                    # Calculate the shortest path from the enemy to our current position
                    enemy_path = a_star_search(enemy, curpos, our_map)
                    # If the enemy can reach our current position in the next turn, set a trap
                    if enemy_path and len(enemy_path) <= 1:
                        self.rules.trap(self.player)
                        break

        # Call the set_mines method to set mines on the path to the gold pot if an enemy player is near
        self.set_mines(status)

        return directions

players = [naivePlayer(), MyAStarPlayer()]