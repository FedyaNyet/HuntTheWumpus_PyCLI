from game.players import Player
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
		print self._board

	def play(self):
		while self._player.isAlive() and not self._player.didWin():
			self._player.do_next_move()
		if self._player.didWin():
			print "You Escaped!!!"
			return
		print "Game Over"
