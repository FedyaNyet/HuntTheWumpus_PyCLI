from math import sqrt
from game import DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT
import pdb

class Tile:

	isEntrance = False
	isSmelly = False
	isShiny = False
	isBreezy = False
	isPit = False
	isWumpas = False

	coordinates = (None, None) #(row, column)

	def __init__(self,row,col):
		self.coordinates = (row,col)
		#print "[board __init__] row: %d col: %d" % (row, col)
		#pdb.set_trace()

	def set_property(self,character):
		if character == "E":
			self.isEntrance = True
		if character == 'W':
			self.isWumpas = True
		if character == 'B':
			self.isBreezy = True
		if character == 'S':
			self.isSmelly = True
		if character == 'G':
			self.isShiny = True
		if character == 'P':
			self.isPit = True

	def __repr__(self):
		retString = list("------")
		if self.isEntrance:
			retString[0] = 'E'
		if self.isWumpas:
			retString[1] = 'W'
		if self.isBreezy:
			retString[2] = 'B'
		if self.isSmelly:
			retString[3] = 'S'
		if self.isShiny:
			retString[4] = 'G'
		if self.isPit:
			retString[5] = 'P'
		return "".join(retString)

	def is_clear_afik(self):
		is_clear = True
		if self.isBreezy or self.isSmelly or self.isPit or self.isWumpas:
			is_clear = False
		return is_clear

class Board:

	_height = 0
	_width = 0
	_entrance_tile = None
	_board = [[None]]

	def __init__(self, filename=None):
		if not filename: return
		self._board = self.parse_file(filename)
		# tile_1 = self[3][3]
		# tile_2 = self[4][1]
		# print str(tile_1.coordinates)+":"+str(tile_1) + " "+str(tile_2.coordinates)+":"+str(tile_2) + " dist:"+str(Board.get_distance(tile_1, tile_2))

	def __repr__(self):
		ret = ""
		for row in range(0,self._height):
			for col in range(0,self._width):
				ret += str(self._board[row][col])+"|"
				if col == self._width-1:
					ret+="\n"
		return ret

	def __getitem__(self, row):
		return self._board[row]

	def append(self, row):
		self._board.append(row)

	def parse_file(self, filename):
		#print "parse_file: "+ filename
		newBoard = []
		myFile = open( filename, "r" )
		for i,line in enumerate(myFile):
			if not i:
				dimensions = line.split("=")[1].strip().split(",")
				self._width = int(dimensions[0])
				#print "Board _width: %d" % self._width
				self._height = int(dimensions[1])
				#print "Board _height: %d" % self._height
				for row in range(self._height):
					newBoard.append([])
					for col in range(self._width):
						newBoard[row].append(Tile(row, col))
				continue
			lineInfo = line.rstrip().split(",")
			coordinates = lineInfo[0:2]
			tileProperties = lineInfo[2:]
			for tileProp in tileProperties:
				row = int(coordinates[0])
				col = int(coordinates[1])
				tile = newBoard[row][col]
				tile.set_property(tileProp)
				if tile.isEntrance:
					self._entrance_tile = tile
		myFile.close()
		return newBoard

	def get_tile_in_direction_of_coordinates(self, coordinates, direction):
		tile = None
		#pdb.set_trace()
		try:
			if direction == DIRECTION_DOWN:
				if coordinates[0] > 0:
					tile = self[coordinates[0]-1][coordinates[1]]
			elif direction == DIRECTION_UP:
				if coordinates[0] < (self._height-1):
					tile = self[coordinates[0]+1][coordinates[1]]
			elif direction == DIRECTION_LEFT:
				if coordinates[1] > 0:
					tile = self[coordinates[0]][coordinates[1]-1]
			elif direction == DIRECTION_RIGHT:
				if coordinates[1] < (self._width-1):
					tile = self[coordinates[0]][coordinates[1]+1]
			return tile
		except:
			return None

	@classmethod
	def get_distance(cls, tile1, tile2):
		return abs(tile1.coordinates[0] - tile2.coordinates[0]) + abs(tile1.coordinates[1] - tile2.coordinates[1])

