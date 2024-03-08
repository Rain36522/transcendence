from PutInShell import PutInShell
import curses
from time import sleep

# Initialisation de curses
stdscr = curses.initscr()
curses.curs_set(0)  # Masquer le curseur
stdscr.nodelay(1)   # Mode non-bloquant pour la saisie

raqA = 25
raqB = 25
raqSize = 10

try:
	while True:
		key = stdscr.getch()
		if key != -1:
			if key == curses.KEY_UP and raqA - raqSize / 2 > 0:
				raqA -= 1
			elif key == curses.KEY_DOWN and raqA + raqSize / 2 < 50:
				raqA += 1
			elif key == ord('q'):
				break  # Quitter si la touche 'q' est pressée
		sleep(0.1)
		PutInShell(10, 10, raqA, raqB, raqSize, stdscr)

finally:
	curses.echo()
	curses.nocbreak()
	stdscr.keypad(False)
	curses.endwin()

