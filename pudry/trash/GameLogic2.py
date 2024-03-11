from PutInShell import PutInShell
from time import sleep

raqA = 25
raqB = 25
raqSize = 10

class GameLogic:
	def __init__(self, raqA, raqB, raqSize):
		self.InitBallMv()

	def InitBallMv(self):
		self.ballx = 50
		self.bally = 25
		

