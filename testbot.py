import math
import random

#class used for points and directions (2D vector)
class Vec2:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def normalize(self):
		mag = math.sqrt(self.x ** 2 + self.y ** 2)
		self.x /= mag
		self.y /= mag

#contains every information related to the ball
class ball:
	def __init__(self, diameter, speed, acceleration):
		self.diameter = diameter
		self.speed = speed
		self.acceleration = acceleration
		self.pos = Vec2(0, 0)
		self.dir = Vec2(0, 0)

#contains every information related do the paddle
class paddle:
	def __init__(self, length, speed):
		self.speed = speed
		self.length = length
		self.pos = Vec2(0, 0)
		self.dir = Vec2(0, 0)

	#collide with the ball
	def collide(self, ball):
		angle = 180 + (80 * (self.next_pos.y - ball.pos.y) / self.length)
		return Vec2(math.cos(angle), math.sin(angle))


#returns distance between a and b
def find_distance(a, b):
	return math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)
	
#returns the time required to travel between a and b
def time_to_travel(a, b, speed):
	return find_distance(a, b) / speed


#returns the first collision position with a border in the box{x{-0.5, 0.5}, y{-0.5, 0.5}}
def find_collision_pos(pos, dir, diameter):
	radius = diameter / 2
	
	slope = dir.y / dir.x if dir.x != 0 else float('inf')
	origin = pos.y - (slope * pos.x if dir.x != 0 else 0)
	# Calculate collision with extremums
	collide_x = Vec2(0.5 - radius if dir.x > 0 else -0.5 + radius, slope * (0.5 - radius if dir.x > 0 else -0.5 + radius) + origin if dir.x != 0 else pos.y)
	collide_y = Vec2(((0.5 - radius if dir.y > 0 else -0.5 + radius) - origin) / slope if slope != float('inf') else pos.x, 0.5 - radius if dir.y > 0 else -0.5 + radius)
	# Calculate distances
	dist_x = find_distance(pos, collide_x)
	dist_y = find_distance(pos, collide_y)
	if dir.x == 0:
		return collide_y
	elif dir.y == 0:
		return collide_x
	else:
		return collide_x if dist_x < dist_y else collide_y



#this functions returns time to next hit (cumulates every hit until y=0.5 or y=-0.5) and the x position of the next hit
def calculate_next_y_extremum_hit(ball, paddle):
	# extend direction vector until it reaches one extremum of the plank (defined by x{-0.5, 0.5} y{-0.5, 0.5})

	new_pos = find_collision_pos(ball.pos, ball.dir)
	time_to_hit = time_to_travel(ball.pos, new_pos, ball.speed)
	ball.pos = new_pos
	if ball.speed < 2:
		ball.speed *= 1.2
	# if it reaches y=-0.5 or y=0.5 before an x extremum
	if new_pos.x != 0.5:
		if new_pos.y == 0.5 or new_pos.y == -0.5:
			ball.dir.y = -ball.dir.y
		if new_pos.x == -0.5:
			paddle.next_pos = Vec2(-0.5, random.uniform(ball.pos.y + paddle.length / 2, ball.pos.y - paddle.length / 2))
			ball.dir = paddle.collide(ball)
		cumulated_time, hit_pos = calculate_next_y_extremum_hit(ball)
		cumulated_time += time_to_hit
	# else (it reaches x=-0.5 or x=0.5)
	else:
		cumulated_time = time_to_hit
	return cumulated_time, ball.pos.y






# ATTENTION JAI FINIT CETTE FONCTION TRES FATIGUE ELLE EST APPROXIMATIVE PEUTETRE
def move_paddle_to_pos(paddle.pos, pos, time):
	delta = pos - paddle.pos
	if delta > 0:
		send le message "2u-on"
		while le temps qui passe < time:
			on attend
		send le message "2u-off"
	else:
		send le message "2d-on"
		while le temps qui passe < time:
			on attend
		send le message "2d-off"
	et voila le travail bebou





def bottibotto_vit_sa_vie():
	ball la_balle
	
	while la vie est belle: #FF si il pleut
		function_to_interrogate_the_gameLogic()
		paddle_pos = 0
		pos, time = calculate_next_y_extremum_hit(ball)
		if ball.direction[0] > 0:
			#faut mettre la fonction en async
			move_paddle_to_pos(paddle_pos, pos, time) #we put the ball to target point to intercept it because it is going toward us
		else:
			#faut mettre la fonction en async
			move_paddle_to_pos(paddle_pos, 0, time) #we put the ball to the center of the plank to intercept it because it is going away from us so we get higher probability to be close enough to the ball next time
		#en meme temps on fait un wait de duree time pour recup le sprochaines info juste apres le hit avec l ejoueeur
		if time > 1seconde:
			wait en async time
		else:
			wait en async 1 seconde
	
	#et voila on l'a bien baisé le noob d'adversaire