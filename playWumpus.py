	#!/usr/bin/env python
from cli.app import CommandLineApp
from game.engine import Engine

class HuntTheWumpusApp(CommandLineApp):

	name = "HuntTheWumpus"

	def setup(self):
		super(TicTacToeApp,self).setup()
		self.add_param("-f", "--file", help="Define the game file to play against.", 
			default="game.txt", action="store_true")
		
	# This is called after run() completes setup()
	def main(self):
		Engine(filename=self.params.file).play()


if __name__ == "__main__":
	HuntTheWumpusApp().run()
