class Tile:

	isSmelly = False
	isShiny = False
	isBreezy = False
	isPit = False
	isWumpas = False


class Board:

	_board = []

	def __init__(self, filename=None):
		if not filename: return
		self._board = self.parse_file(filename)

	def __setitem__(self,index,item):
		self._board[index] = item
		
	def __getitem__(self,index):
		return self._board[index]

	def parse_file(self, filename):
		newBoard = []
		for line in open( filename, "r" ):
			tile = Tile()
			tile.isSmelly = True
			newBoard.append(tile)
			# newBoard[idx] = tile
		return newBoard

	def print_board(self):
		pass

