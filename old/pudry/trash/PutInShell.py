import os
from time import sleep
import curses

#This file put the game on terminal

# This function calcul the size of the game map depending on shell size.
def DefineMapSize():
	sheelSize = os.get_terminal_size()
	shellx = sheelSize.columns
	shelly = sheelSize.lines
	if (shellx / shelly > 4):
		x = shelly
		y = shelly // 4
	elif (shellx / shelly < 4):
		x = shellx
		y = shellx // 4
	else:
		return int(shellx), int(shelly - 1), 0

	while (x + 3 < shellx and y < shelly):
		x += 1
		y += 0.25
	start = 0
	if not x % 2:
		x -= 1
		y -= 0.25
	if (shellx - x > 0):
		start = (shellx - x) // 2
	return int(x), int(y - 1), int(start)



def PutLineExtern(x, stdscr):
	for i in range(x - 1):
		stdscr.addstr("1")
	stdscr.addstr("1\n")

def PutMiddelLine(x, ball, raquetA, raquetB, stdscr):
	stdscr.addstr("1")
	i = 1
	if raquetA:
		stdscr.addstr("A")
		i += 1
	if raquetB:
		i += 1
	while i < x - 1:
		if (ball and i + 1 == ball):
			stdscr.addstr("O")
		elif (i + 1) * 2 == x + 1 or (i + 1) * 2 == x:
			if raquetB:
				stdscr.addstr(" ")
				i += 1
			stdscr.addstr("1")
		else:
			stdscr.addstr(" ")
		i += 1
	if raquetB:
		stdscr.addstr("A")
	stdscr.addstr("1\n")
		
def	PutBegin(start, stdscr):
	if start:
		for i in range(start):
			stdscr.addstr(" ")

def	BallPose(ballx, bally, mapx, mapy):
	mapx -= 1
	mapy -= 2
	ballx = (ballx * mapx) // 100
	bally = (bally * mapy) // 50
	if ballx <= 0:
		ballx = 1
	return ballx + 1, bally

def RaquetPos(posy, size, mapy):
	mapy -= 2
	size = (size * mapy) // 50
	posy = (posy * mapy) // 50
	if size < 1:
		size = 1
	return posy - size // 2, size // 2 + posy

	


#this function put the map with the ball on the terminal
#the ball place is 
def PutInShell(ballx, bally, raqA, raqB, raqSize, stdscr):
	x, y, start, = DefineMapSize()
	# stdscr.addstr("Map size : ", x, y, start)
	ballx, bally = BallPose(ballx, bally, x, y)
	raqAUp, raqADwn = RaquetPos(raqA, raqSize, y)
	raqBUp, raqBDwn = RaquetPos(raqB, raqSize, y)	
	PutBegin(start, stdscr)
	PutLineExtern(x, stdscr)
	for i in range(y - 2):
		if i >= raqAUp and i <= raqADwn:
			raqA = True
		else:
			raqA = False
		if i >= raqBUp and i <= raqBDwn:
			raqB = True
		else:
			raqB = False
		PutBegin(start, stdscr)
		if i == bally - 1:
			PutMiddelLine(x, ballx, raqA, raqB, stdscr)
		else:
			PutMiddelLine(x, 0, raqA, raqB, stdscr)
	PutBegin(start, stdscr)
	PutLineExtern(x, stdscr)
		


# PutInShell(50, 20, 20, 30, 30)