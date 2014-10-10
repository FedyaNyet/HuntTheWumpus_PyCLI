from math import sqrt

class Tile:

	isEntrance = False
	isSmelly = False
	isShiny = False
	isBreezy = False
	isPit = False
	isWumpas = False

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


class Board:

	_height = 0
	_width = 0
	_board = [[None]]

	def __init__(self, filename=None):
		if not filename: return
		self._board = self.parse_file(filename)

	def get(self, row, column):
		return self._board[col][row]

	def parse_file(self, filename):
		newBoard = []
		myFile = open( filename, "r" )
		for i,line in enumerate(myFile):
			if not i:
				dimensions = line.split("=")[1].strip().split(",")
				self._width = int(dimensions[0])
				self._height = int(dimensions[1])
				newBoard = [[Tile() for i in xrange(self._width)] for i in xrange(self._height)]
				continue
			lineInfo = line.rstrip().split(",")
			coordinates = lineInfo[0:2]
			tileProperties = lineInfo[2:]
			for tileProp in tileProperties:
				row = int(coordinates[0])
				col = int(coordinates[1])
				tile = newBoard[col][row]
				tile.set_property(tileProp)
		myFile.close()
		return newBoard


	def __repr__(self):
		ret = ""
		for col in range(0,self._width):
			for row in range(0,self._height):
				ret += str(self._board[row][col])+"|"
				if row == self._width-1:
					ret+="\n"
		return ret

