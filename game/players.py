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

	_wumpusTile = None

	_direction_map = [DIRECTION_RIGHT, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_UP]

	def __init__(self, board_height, board_width, coordinates):
		self._coordinates = coordinates
		self._board = Board()
		self._board._height = board_height
		self._board._width = board_width
		print "[__init__] board_height: %d" % board_height
		for row in range(board_height):
			self._board.append([])
			for col in range(board_width):
				print "[__init__] append to row: %d col: %d" % (row, col)
				tile = AgentTile(row, col)
				print "[__init__] tile created is visited: ", tile.isVisited
				self._board[row].append(tile)


	def get_next_action(self):
		action = ACTION_MOVE
		return action

	def get_direction_of_closest_new_square(self):
		print "[get_direction_of_closest_new_square]"
		tile = None
		unvistited_tiles = []
		for row in range(self._board._height):
			for col in range(self._board._width):
				tile = self._board[row][col]
				print "[get_direction_of_closest_new_square] tile coordinates: ", tile.coordinates
				print "[get_direction_of_closest_new_square] tile is visited: %r " % self._board[row][col].isVisited
				if tile.isVisited == False:
					#print "[get_direction_of_closest_new_square] add unvistied tile with coordinates: ", tile.coordinates
					unvistited_tiles.append(tile)

		min_distance_tile = None
		min_distance = 9223372036854775807

		for tile in unvistited_tiles:
			#calc distance and keep track of min
			if not self._coordinates == tile.coordinates:
				rowdistance = abs(self._coordinates[0] - tile.coordinates[0])
				coldistance = abs(self._coordinates[1] - tile.coordinates[1])
				distance = rowdistance + coldistance
				#print "[get_direction_of_closest_new_square] tile: ", tile
				if distance < min_distance:
					min_distance = distance
					min_distance_tile = tile

		#print "[get_direction_of_closest_new_square] min_distance_tile coordinates: ", min_distance_tile.coordinates
		vertical_direction = None
		horizontal_direction = None
		direction_to_go = DIRECTION_RIGHT
		if min_distance_tile:
			if min_distance_tile.coordinates[0] > self._coordinates[0]:
				vertical_direction = DIRECTION_UP
			elif min_distance_tile.coordinates[0] < self._coordinates[0]:
				vertical_direction = DIRECTION_DOWN

			if min_distance_tile.coordinates[1] > self._coordinates[1]:
				horizontal_direction = DIRECTION_RIGHT
			elif min_distance_tile.coordinates[1] < self._coordinates[1]:
				horizontal_direction = DIRECTION_LEFT

			if not vertical_direction:
				direction_to_go = horizontal_direction
			elif not horizontal_direction:
				direction_to_go = vertical_direction
			else:
				direction_to_go = vertical_direction

		print "[get_direction_of_closest_new_square] direction to go: ", direction_to_go
		return 	direction_to_go

	def get_reverse_move(self, move):
		print "[get_reverse_move] for move:", move
		direction = None
		if move[1] == DIRECTION_RIGHT:
			direction = DIRECTION_LEFT
		if move[1] == DIRECTION_DOWN:
			direction = DIRECTION_UP
		if move[1] == DIRECTION_LEFT:
			direction = DIRECTION_RIGHT
		if move[1] == DIRECTION_UP:
			direction = DIRECTION_DOWN
		reverseMove = (ACTION_MOVE, direction)
		print "[get_reverse_move] reverse move is: ", reverseMove
		return reverseMove

	def get_direction_of_wumpus_tile(self):
		direction = None
		if self._wumpusTile.coordinates[0] > self._coordinates[0]:
			direction = DIRECTION_DOWN
		elif self._wumpusTile.coordinates[0] < self._coordinates[0]:
			direction = DIRECTION_UP
		elif self._wumpusTile.coordinates[1] > self._coordinates[1]:
			direction = DIRECTION_RIGHT
		elif self._wumpusTile.coordinates[1] < self._coordinates[1]:
			direction = DIRECTION_LEFT
		return direction

	def get_next_move(self):
		"""
		Return a tuple of (ACTION_SHOOT|ACTION_MOVE, DIRECTION_UP|DIRECTION_DOWN|DIRECTION_LEFT|DIRECTION_RIGHT).
		"""
		self.update_knowledge_base()

		if self._has_gold:
			print "[get_next_move] found gold - let's get out of here"
			# follow bread crumb back to start
			theMove = self.get_reverse_move( self._bread_crumbs.pop() )
		else :
			myTile = self._board[self._coordinates[0]][self._coordinates[1]]
			print "[get_next_move] Tile I'm on is at row: %d column: %d" % (self._coordinates[0], self._coordinates[1])
			shouldReverseDirection = False
			if myTile:
				print "[get_next_move] I'm on a legit tile"
				if myTile.isBreezy:
					print "[get_next_move] Tile I'm on is breezy"
					shouldReverseDirection = True
				elif myTile.isSmelly:
					print "[get_next_move] Tile I'm on is smelly"
					# starter logic for whether or not to shoot:
					# 	if we've made more than 30 moves and we know where it is
					#	otherwise, back off
					shootTheWumpus = False
					if len(self._bread_crumbs) > 30:
						if self._wumpusTile:
							shootTheWumpus = True
					if shootTheWumpus:
						theMove = (ACTION_SHOOT, self.get_direction_of_wumpus_tile())
						#Assume the wumpus was killed.
						#guessTile = self._board.get_tile_in_direction_of_coordinates((row,col), direction)
						#self.update_knowledge_base()
					else:
						shouldReverseDirection = True

			if shouldReverseDirection:
				print "[get_next_move] I shouldReverseDirection"
				theMove = self.get_reverse_move( self._bread_crumbs.pop() )
			else:
				print "[get_next_move] I can make a move"
				theMove = ( ACTION_MOVE, self.get_direction_of_closest_new_square() )
				self._bread_crumbs.append(theMove)

		return theMove

	def update_knowledge_base(self):
		print "[update_knowledge_base]"
		## on every move update the counter to +/- 1 if safe or not.
		## don't update counters of visited squares...
		## if wamups was shot, set all isWumpus_guess_counts to -1000
		directions = [DIRECTION_UP,DIRECTION_RIGHT,DIRECTION_DOWN,DIRECTION_LEFT]
		updated = False
		#print "self._board._height: %d" % self._board._height
		#print "self._board._width: %d" % self._board._width
		for row in range(self._board._height):
			for col in range(self._board._width):
				#print "[update_knowledge_base] at row: %d column: %d" % (row, col)
				agentTile = self._board[row][col]
				#print "[update_knowledge_base] tile isBreezy: %r isSmelly: %r" % (agentTile.isBreezy, agentTile.isSmelly)
				if agentTile.isBreezy:
					for direction in directions:
						guessTile = self._board.get_tile_in_direction_of_coordinates(self._coordinates, direction)
						if not guessTile: continue
						if not guessTile.isVisited: continue
						guessTile.isPit_guess_count += 1
						updated = True
				if agentTile.isSmelly:
					for direction in directions:
						guessTile = self._board.get_tile_in_direction_of_coordinates(self._coordinates, direction)
						if not guessTile: continue
						if not guessTile.isVisited: continue
						guessTile.isWumpas_guess_count += 1
						updated = True
				if agentTile.isPit_guess_count > 1:
					agentTile.isPit = True
					updated = True
				if agentTile.isWumpas_guess_count > 1:
					agentTile.isWumpas = True
					self._wumpusTile = agentTile
					updated = True
		if updated:
			print "[update_knowledge_base] did update"
			#self.update_knowledge_base()

	def reveal_tile(self, tile):
		if tile.coordinates != self._coordinates:
			print "[reveal_tile] You gave me the wrong tile. YOU BASTARD!"
			return

		print "[reveal_tile] I moved to tile at row: %d column: %d" % (tile.coordinates[0], tile.coordinates[1])
		agentTile = self._board[tile.coordinates[0]][tile.coordinates[1]]
		if not agentTile:
			agentTile = AgentTile(tile.coordinates[0], tile.coordinates[1])
		print "[reveal_tile] the tile where I moved: ", agentTile
		agentTile.isVisited = True
		agentTile.isShiny = tile.isShiny
		agentTile.isSmelly = tile.isSmelly
		agentTile.isBreezy = tile.isBreezy
		agentTile.isPit = tile.isPit
		agentTile.isWumpas = tile.isWumpas
		agentTile.isEntrance = tile.isEntrance

		self._board[tile.coordinates[0]][tile.coordinates[1]] = agentTile
		print self._board[tile.coordinates[0]][tile.coordinates[1]].isVisited
		if tile.isShiny:
			self._has_gold = True
		if tile.isPit or tile.isWumpas:
			self._is_alive = False
		if tile.isEntrance:
			print "[reveal_tile] I moved to the entrance tile"
		if tile.isSmelly or tile.isBreezy:
			print "[reveal_tile] I moved to a tile that either is breezy or smelly"

		self.update_knowledge_base()