
class Player(object):
	def reset(self, player_id, max_players, width, height):
		raise NotImplementedError("'reset' not implemented in '%s'." % self.__class__)

	def round_begin(self, r):
		raise NotImplementedError("'round_begin' not implemented in '%s'." % self.__class__)

	def move(self, status):
		raise NotImplementedError("'move' not implemented in '%s'." % self.__class__)

	def set_mines(self, status):
		"""
		Called to ask the player to set mines

		@param self the Player itself
		@param status the status
		@returns list of coordinates on the board

		The player answers with a list of positions, where mines
		should be set.

		Cost of setting mines:
		setting a mine in move distance k (as-the-eagle-flies, i.e.
		ignoring obstacles) to the player causes k actions.
		Actions are charged as usual.

		If a player does not define the method, this step is
		skipped.
		"""

		raise NotImplementedError("'setting mines' not implemented in '%s'." % self.__class__)

	def trap_random_player(self):
		"""
				Called to ask the player if they want to trap a random player by building walls around them for one round

				@param self the Player itself
				@returns boolean

				The player answers with a boolean indicating whether they want to randomly trap a player or not.

				Cost of trapping:
				20 Gold points (not set on that)

				The player that gets trapped will be chosen semi-randomly, there is a small chance
				one might be trapped themselves

				If a player does not define the method, this step is
				skipped.
				"""
		raise NotImplementedError("'strap_random_player' not implemented in '%s'." % self.__class__)
