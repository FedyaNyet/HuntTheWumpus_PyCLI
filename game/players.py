from board import Board, Tile
from game import ACTION_SHOOT, ACTION_MOVE, DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT

class AgentTile(Tile):

	isVisited = False
	isPit_guess_count = 0
	isWumpas_guess_count = 0


class Player:

	# this contains the tiles as the agent sees them.
	_board = None

	_bread_crumbs = []

	_points = 0
	_coordinates = (None, None)
	_has_gold = False
	_has_arrow = True
	_is_alive = True

	def __init__(self, board_height, board_width, coordinates):
		self._coordinates = coordinates
		self._board = Board()
		for row in range(board_height):
			self._board.append([])
			for col in range(board_width):
				self._board[row].append(AgentTile(row, col))

	def get_next_action(self):
		action = ACTION_MOVE
		return action

	def get_direction_of_closest_new_square(self):
		direction = DIRECTION_RIGHT
		return direction

	def get_next_move(self):
		"""
		Return a tuple of (ACTION_SHOOT|ACTION_MOVE, DIRECTION_UP|DIRECTION_DOWN|DIRECTION_LEFT|DIRECTION_RIGHT).
		"""
		## use shortest path algorth if self._has_gold
		theMove = (ACTION_MOVE, DIRECTION_RIGHT)
		if theMove[0] == ACTION_SHOOT: 
			#Assume the wumpus was killed.
			guestPitTile = self._board.get_tile_in_direction_of_coordinates((row,col), direction)
			self.update_knowledge_base()
		else:
			self._bread_crumbs.append(theMove)

		return theMove

	def update_knowledge_base(self):
		## on every move update the counter to +/- 1 if safe or not.
		## don't update counters of visited squares...
		## if wamups was shot, set all isWumpus_guess_counts to -1000
		directions = [DIRECTION_UP,DIRECTION_RIGHT,DIRECTION_DOWN, DIRECTION_LEFT]
		updated = False
		for row in range(self._board._height):
			for col in range(self._board._width):
				agentTile = self._board[row][col]
				if agentTile.isBreezy:
					for direction in directions:
						guessTile = self._board.get_tile_in_direction_of_coordinates(self._coordinates, direction)
						if not guestTile: continue
						guessTile.isWumpas_guess_count += 1
						updated = True
				if agentTile.isSmelly:
					for direction in directions:
						guessTile = self._board.get_tile_in_direction_of_coordinates(self._coordinates, direction)
						if not guestTile: continue
						self._board.get_tile_in_direction_of_coordinates(self._coordinates, direction).isWumpus_guess_count += 1
						updated = True
				if agentTile.isPit_guess_count > 1:
					agentTile.isPit = True
					updated = True
				if agentTile.isWumpus_guess_count > 1:
					agentTile.isWumpas = True
					updated = True
		if updated:
			self.update_knowledge_base()

	def reveal_tile(self, tile):
		if tile.coordinates != self._coordinates:
			print "You gave me the wrong tile. YOU BASTARD!"
			return
		if tile.isShiny:
			self._has_gold = True
		if tile.isPit or tile.isWumpas:
			self._is_alive = False
		if tile.isSmelly or tile.isBreezy:
			self.update_knowledge_base()