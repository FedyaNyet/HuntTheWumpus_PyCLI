from board import Board, Tile
from game import ACTION_SHOOT, ACTION_MOVE, DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT

class AgentTile(Tile):

	isVisited = False
	isPit_guess_count = 0
	isWumpas_guess_count = 0


class Player:

	# this contains the tiles as the agent sees them.
	_board = None

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

	def get_next_move(self):
		"""
		Return a tuple of (ACTION_SHOOT|ACTION_MOVE, DIRECTION_UP|DIRECTION_DOWN|DIRECTION_LEFT|DIRECTION_RIGHT).
		"""
		action = ACTION_MOVE
		direction = DIRECTION_RIGHT

		if action == ACTION_SHOOT: 
			#Assume the wumpus was killed.
			self._board.get_tile_in_direction_of_coordinates(self._coordinates, direction).isWumpas = False
			self.update_knowledge_base()
		return (action, direction)

	def update_knowledge_base(self):
		#this should be a recursive function that updates the agent board tiles, until there's nothing left to update. 
		pass

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