from game.players import Player
from game import ACTION_SHOOT, ACTION_MOVE
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
		self._player = Player(board_height=self._board._height, board_width=self._board._width, coordinates=self._board._entrance_tile.coordinates)
		print self._board

	def agent_is_alive(self):
		return self._player._is_alive

	def agent_is_winner(self):
		return self._player._has_gold and self._player._coordinates == self._board._entrance_tile.coordinates

	def play(self):
		self._player.reveal_tile(self._board._entrance_tile)
		while self.agent_is_alive() and not self.agent_is_winner():
			next_move = self._player.get_next_move()
			next_action = next_move[0]
			next_tile = self._board.get_tile_in_direction_of_coordinates(self._player._coordinates, next_move[1])
			
			if ACTION_SHOOT == next_action:
				self._player._points -= 10
				# if next_tile.isWumpas:
					# self._player._points += 1000
				next_tile.isWumpas = False
			elif ACTION_MOVE == next_action:
				self._player._coordinates = next_tile.coordinates
				self._player._points -= 1
				self._player.reveal_tile(next_tile)
			print "Agent Points: "+str(self._player._points)
		if self.agent_is_winner():
			self._player._points += 1000
			print "The Agent Escaped!!! Points Total: "+str(self._player._points)
			return
		self._player._points -= 1000
		print "Game Over: Points Total: "+str(self._player._points)
