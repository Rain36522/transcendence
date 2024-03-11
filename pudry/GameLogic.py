from PutInShell import PutInShell
import readchar
from time import sleep
import select
import sys

def is_data_available():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

raqA = 25
raqB = 25
raqSize = 10

while True:
	if is_data_available():
		key = readchar.readkey()
		if key == '\x1b[A' and raqA - raqSize / 2 > 0: # up
			raqA -= 1
		elif key == '\x1b[B' and raqA + raqSize / 2 < 50: # down
			raqA += 1
	PutInShell(10, 10, raqA, raqB, raqSize)
	sleep(0.1)
    #elif key == '\x1b[C': # right
    #elif key == '\x1b[D': # left
