import math
import random
from game_utils import Direction


class ProbablyGreedy:
	def __init__(self):
		self.player_name = None

	def convert_move(self, current_coordinates, move_coordinates):
		relative_coordiantes = (
			move_coordinates[0] - current_coordinates[0], move_coordinates[1] - current_coordinates[1])
		match relative_coordiantes:
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

	def non_wall_neighbours(self, status, x, y):
		free_neighbours = list()
		neighbour_coordinates = [
			(x - 1, y - 1),
			(x - 1, y),
			(x - 1, y + 1),
			(x, y - 1),
			(x, y + 1),
			(x + 1, y - 1),
			(x + 1, y),
			(x + 1, y + 1),
		]
		for coordinate in neighbour_coordinates:
			if 0 <= coordinate[0] < status.map.width \
					and 0 <= coordinate[1] < status.map.height \
					and not status.map[coordinate].is_blocked():
				free_neighbours.append(coordinate)
		return free_neighbours

	def post_process_probabilities(self, probabilities, hardness=5):
		# harden
		probabilities_hardened = [probability ** hardness for probability in probabilities]
		probabilities_sum = sum(probabilities_hardened)
		# rescale
		probabilities_hardened_rescaled = [probability / probabilities_sum for probability in probabilities_hardened]
		return probabilities_hardened_rescaled

	def goodness_to_probability(self, distance_candidates):
		# negate distances
		max_distance = distance_candidates[-1]
		probabilities_raw = list()
		for i in range(len(distance_candidates)):
			probabilities_raw.append(1 + max_distance - distance_candidates[i])
		# scale
		probability_sum = sum(probabilities_raw)
		probabilities_normalized = list()
		for i in range(len(probabilities_raw)):
			probability = probabilities_raw[i]
			probabilities_normalized.append(probability / probability_sum)

		return probabilities_normalized

	def heuristic(self, position, goal):
		return math.sqrt((position[0] - goal[0]) ** 2 + (position[1] - goal[1]) ** 2)  # euclidian distance

	def get_scored_moves(self, status):
		# todo: find best pot
		best_pot_position = next(iter(status.goldPots))

		neighbour_candidates = self.non_wall_neighbours(status, status.x, status.y)
		for i in range(len(neighbour_candidates)):
			neighbour_heuristic = self.heuristic(neighbour_candidates[i], best_pot_position)
			neighbour_candidates[i] = (neighbour_candidates[i], neighbour_heuristic)

		neighbour_candidates.sort(key=lambda x: x[1], reverse=False)
		return [neighbour_candidates[i][0] for i in range(len(neighbour_candidates))], \
			[neighbour_candidates[i][1] for i in range(len(neighbour_candidates))]

	def reset(self, player_id, max_players, width, height):
		self.player_name = "ProbablyGreedy"

	def round_begin(self, r):
		pass

	def move(self, status):
		move_candidates, distance_candidates = self.get_scored_moves(status)

		# chose a move with a probability based on its goodness
		probability_candidates = self.goodness_to_probability(distance_candidates)

		# optional post-processing
		probability_candidates_processed = self.post_process_probabilities(probability_candidates, hardness=5)

		# random.seed(42)
		random_value = random.random()
		chosen_move = None
		lower_bound = 0
		for i in range(len(probability_candidates_processed)):
			upper_bound = lower_bound + probability_candidates_processed[i]
			if lower_bound <= random_value <= upper_bound:
				chosen_move = move_candidates[i]
				break
			lower_bound = upper_bound

		relative_move = self.convert_move((status.x, status.y), chosen_move)
		# greedy_move = self.convert_move((status.x, status.y), move_candidates_with_probabilities[0][0])
		return [relative_move]

	def set_mines(self, status):
		return []


players = [ProbablyGreedy()]
