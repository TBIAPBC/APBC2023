import math
import random
import copy
from decimal import *

from matplotlib import pyplot as plt
from pathfinding.core.grid import Grid
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.finder.breadth_first import BreadthFirstFinder

from game_utils import Direction, TileStatus
from player_base import Player

sharpness_factor = 1 / 10  # should be < 1
view_range = 7


def move_length_to_costs(length):
	return sum(list(range(1, length + 1)))


def move_costs_to_length(costs):
	length = 0
	for L in range(1, costs + 1):
		costs -= L
		if costs >= 0:
			length += 1
		else:
			break
	return length


def euclidian_distance_heuristic(position, target):
	return math.sqrt((position[0] - target[0]) ** 2 + (position[1] - target[1]) ** 2)


def convert_move(current_coordinates, move_coordinates):
	relative_coordinates = (
		move_coordinates[0] - current_coordinates[0], move_coordinates[1] - current_coordinates[1]
	)
	match relative_coordinates:
		case (-1, 1):
			return Direction.up_left
		case (-1, 0):
			return Direction.left
		case (-1, -1):
			return Direction.down_left
		case (0, 1):
			return Direction.up
		case (0, -1):
			return Direction.down
		case (1, 1):
			return Direction.up_right
		case (1, 0):
			return Direction.right
		case (1, -1):
			return Direction.down_right
		case _:
			raise RuntimeError('This should be impossible?')


def chose_candidate(candidates, sharpness=None):
	if not sharpness:
		sharpness = max(1., len(candidates) * sharpness_factor)
	distances = list(candidate[1] for candidate in candidates)

	# negate distances
	max_distance = distances[-1]
	probabilities_raw = list()
	for i in range(len(distances)):
		probabilities_raw.append(1 + max_distance - distances[i])
	# scale distances
	probabilities_sum = sum(probabilities_raw)
	probabilities_normalized = list()
	for i in range(len(probabilities_raw)):
		probability = probabilities_raw[i]
		probabilities_normalized.append(probability / probabilities_sum)

	# harden probabilities
	probabilities_hardened = [Decimal(probability) ** Decimal(sharpness) for probability in probabilities_normalized]
	probabilities_sum = sum(probabilities_hardened)
	# renormalize probabilities
	probabilities_hardened_renormalized = \
		[float(probability / probabilities_sum) for probability in probabilities_hardened]

	# optionally print out sharpness curve
	print_curves = False
	if print_curves:
		ys = list(reversed(probabilities_hardened_renormalized))
		xs = range(len(ys))
		plt.plot(xs, ys)
		plt.savefig('./sharpness_curves.png')

	# chose
	random_value = random.random()
	chosen_candidate = [[], 0, 0]
	lower_bound = 0
	for i in range(len(probabilities_hardened_renormalized)):
		upper_bound = lower_bound + probabilities_hardened_renormalized[i]
		if lower_bound <= random_value <= upper_bound:
			chosen_candidate = candidates[i]
			break
		lower_bound = upper_bound

	return chosen_candidate


class IntelliBot(Player):
	def __init__(self):
		self.player_name = None
		self.path_finder = None
		self.path = None
		self.map = None
		self.last_position = None

	def reset(self, player_id, max_players, width, height):
		self.player_name = "YEEEEEEET"
		self.path_finder = BreadthFirstFinder(diagonal_movement=DiagonalMovement.always)
		self.path = list()
		self.map = list([-1 for _ in range(width)] for _ in range(height))  # 0: free, -1: unknown, -2: mine, -3: enemy

	def round_begin(self, current_round):
		self.path = list()

	def categorize_gold_pots(self, status):
		gold_pots_in_view_range = list()
		gold_pots_out_of_view_range = list()
		for gold_pot_position in status.goldPots.keys():
			i, j = gold_pot_position[1], gold_pot_position[0]
			if self.map[i][j] == -1:
				gold_pots_out_of_view_range.append(gold_pot_position)
			else:
				gold_pots_in_view_range.append(gold_pot_position)

		return gold_pots_in_view_range, gold_pots_out_of_view_range

	def map_to_string(self, status):
		# return '\n'.join(' '.join(str(tile) for tile in row) for row in reversed(self.map_grid)) + '\n'
		string_map = copy.deepcopy(self.map)
		for i in range(len(string_map)):
			for j in range(len(string_map[i])):
				if (status.x, status.y) == (j, i):
					string_map[i][j] = 'P'
				else:
					match string_map[i][j]:
						case 1: string_map[i][j] = '.'
						case -1: string_map[i][j] = '#'
						case -2: string_map[i][j] = 'x'
						case -3: string_map[i][j] = 'P'

		return '\n'.join(' '.join(tile for tile in row) for row in string_map) + '\n'

	def update_map(self, status):
		for x in range(max(0, status.x - view_range), min(status.x + view_range, status.map.width - 1) + 1):
			for y in range(max(0, status.y - view_range), min(status.y + view_range, status.map.height - 1) + 1):
				i, j = y, x

				# if it is the current position, it's free
				if (x, y) == (status.x, status.y):
					self.map[i][j] = 1
				else:
					# if it is a free position
					if status.map[x, y].status == TileStatus.Empty:
						# check whether someone else is on it
						if (x, y) in list((other.x, other.y) for other in status.others if other):
							self.map[i][j] = -3
						else:
							self.map[i][j] = 1
					# if it is a mine
					elif status.map[x, y].status == TileStatus.Mine:
						self.map[i][j] = -2

	def move(self, status):
		self.update_map(status)
		gold_pots_in_view_range, gold_pots_out_of_view_range = self.categorize_gold_pots(status)

		grid = Grid(matrix=self.map)
		start = grid.node(status.x, status.y)

		new_path = list()

		# try to find the path to the closest gold pot in view range
		current_path_length = math.inf
		for gold_pot_in_view_range in gold_pots_in_view_range:
			end = grid.node(*gold_pot_in_view_range)
			path, _ = self.path_finder.find_path(start, end, grid)
			grid.cleanup()

			if 0 < len(path) < current_path_length:
				current_path_length = len(path)
				new_path = path

		# if one found, determine how many tiles to move at once
		if current_path_length < math.inf:

			gold_amount = status.goldPots[new_path[-1]]
			move_length = len(new_path) - 1

			best_move_length = move_costs_to_length(status.gold // 4)
			for divisor in range(1, move_length):
				split_move_length = move_length // divisor + 1
				split_move_costs = divisor * move_length_to_costs(split_move_length)
				if status.gold >= split_move_costs and split_move_costs < gold_amount:
					best_move_length = split_move_length
					break
			new_path = new_path[0:best_move_length + 1]

		# if none reachable, do nothing
		elif len(gold_pots_in_view_range) > 0:
			return list()

		# if none found, find the path to a good position that's close to some gold pot
		else:
			'''chosen_path = list()
			chosen_total_distance = math.inf
			chosen_gold_pot_amount = -math.inf'''

			# sort all positions in view range by their distance to their closest gold pot
			candidates = list()
			for i in range(len(self.map)):
				for j in range(len(self.map[i])):
					x, y = j, i

					# if the candidate position is not the own AND is free
					if (x, y) != (status.x, status.y) and self.map[i][j] == 1:

						# get the distance to the gold pot that's closest to the candidate position
						closest_gold_pot = (-math.inf, math.inf)
						for gold_pot_position in gold_pots_out_of_view_range:
							distance_heuristic = euclidian_distance_heuristic((x, y), gold_pot_position)
							if distance_heuristic < closest_gold_pot[1]:
								closest_gold_pot = (distance_heuristic, status.goldPots[gold_pot_position])

						# get the path to the candidate position
						end = grid.node(x, y)
						path, _ = self.path_finder.find_path(start, end, grid)
						grid.cleanup()

						# get the minimum total distance: path length + distance to closest gold pot (A*)
						if len(path) > 0:
							total_distance = float(len(path)) * 0.99 + closest_gold_pot[0]
							candidates.append((path, total_distance, closest_gold_pot[1]))
							'''if total_distance < chosen_total_distance:
								chosen_path = path
								chosen_total_distance = total_distance
								chosen_gold_pot_amount = closest_gold_pot[1]'''
						else:
							# tile unreachable
							pass
					else:
						# tile not free
						pass

			# if still possible path found
			if len(candidates) == 0:  # this can only happen if every single tile in view range is occupied or unreachable
				return list()

			candidates.sort(key=lambda e: e[1], reverse=False)
			chosen_candidate = chose_candidate(candidates)
			chosen_path = chosen_candidate[0]
			chosen_total_distance = chosen_candidate[1]
			chosen_gold_pot_amount = chosen_candidate[2]

			new_path = chosen_path
			# if one found, determine how many tiles to move at once
			gold_amount = chosen_gold_pot_amount
			move_length = len(new_path) - 1
			full_move_length = move_length + math.ceil(chosen_total_distance - move_length)
			best_move_length = move_costs_to_length(status.gold // 4)
			for divisor in range(1, full_move_length):
				split_move_length = move_length // divisor + 1
				if split_move_length <= move_length:
					split_move_costs = divisor * move_length_to_costs(split_move_length)
					if status.gold >= split_move_costs and split_move_costs < gold_amount:
						best_move_length = split_move_length
						break
			new_path = new_path[0:best_move_length + 1]

		# convert path to moves (truncating the first value, as it is the current position)
		moves = list()
		for i in range(1, len(new_path)):
			relative_move = convert_move(new_path[i - 1], new_path[i])
			moves.append(relative_move)

		# if the gold pot spawns right on the player, the path length is 1 and therefore the move length is 0
		if len(moves) == 0:
			return list()

		# set variables for next round
		self.last_position = (status.x, status.y)

		# return
		return moves

	def set_mines(self, status):
		# TODO
		return list()


players = [IntelliBot()]
