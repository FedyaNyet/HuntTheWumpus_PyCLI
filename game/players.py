from board import Board, Tile

class Player:

	_explored_board = []
	_current_pos = None
	_has_gold = False
	_is_alive = True
	_did_win = False

	def __init__(self, board_size=4, start_pos=0):
		for i in range(0,board_size*board_size):
			self._explored_board.append(Tile())
		self._current_pos = start_pos
		return

	def do_next_move(self):
		self._did_win = True
		pass

	def isAlive(self):
		return self._is_alive

	def didWin(self):
		return self._did_win