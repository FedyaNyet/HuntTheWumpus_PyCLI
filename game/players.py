from board import Board, Tile

class Player:

	_explored_board = []
	_current_pos
	_has_gold = False
	_is_alive = True

	__init__(self, board_size=4, start_pos=0):
		for i in range(0,board_size*board_size):
			_board.append()
		return

	def do_next_move(self):
		pass

	def isAlive(self):
		return self._is_alive
