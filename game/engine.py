from game.players import Computer, User
from board import Board

class Engine:

	_game_over = False
	_player = None
	_board = None

	def __init__(self, filename):
		"""
		Play Hunt The Wumpus. 
		"""
		self._board = Board(filename)
		self._player = Player()

	def play(self):
		while self._player.isAlive():
			self._player.do_next_move()