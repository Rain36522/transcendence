from PutInShell import PutInShell
from time import sleep

raqA = 25
raqB = 25
raqSize = 10

def detectMv():
	return ""


while True:
		if detectMv == "Up" and raqA - raqSize / 2 > 0:
			raqA -= 1
		elif detectMv == "Down" and raqA + raqSize / 2 < 50:
			raqA += 1
		elif detectMv == "Q":
			break  # Quitter si la touche 'q' est pressée
	PutInShell(10, 10, raqA, raqB, raqSize, stdscr)

