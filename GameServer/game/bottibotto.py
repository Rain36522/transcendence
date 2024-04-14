import math
import random
import time
import asyncio


# bot routine
class BottiBotto:
	def __init__(self, game_logic, game_settings):
		self.game_logic = game_logic
		self.game_settings = game_settings 

		self.ball = ball(self.game_settings["ball_diameter"], self.game_settings["ball_speed"], self.game_settings["ball_acceleration"])
		self.ball.dir = self.game_settings["ball_dir"]
		self.paddle = paddle(self.game_settings["paddle_length"], self.game_settings["paddle_speed"])
		self.up = False
		self.down = False
	# bottibotto_vit_sa_vie

	# main bot routine
	async def bottibotto_vit_sa_vie(self):
		time_to_hit = 0
		while True:
			print("======================================")
			print("==========getting game state==========")
			print("======================================")
			game_state = await self.game_logic.get_game_state()
			if game_state["game_over"]: # terminate bot routine, game over
				break

			self.ball.pos = game_state["ball_pos"]
			self.ball.dir = game_state["ball_dir"]
			self.ball.speed = game_state["ball_speed"]
			self.paddle.pos = game_state["paddle_pos"]
			print("ball pos: ", self.ball.pos.x, self.ball.pos.y)
			print("ball dir: ", self.ball.dir.x, self.ball.dir.y)
			print("ball speed: ", self.ball.speed)
			print("paddle pos: ", self.paddle.pos.x, self.paddle.pos.y)
			print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
			print("OOOOOOOOOcalculating next hitOOOOOOOOO")
			print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
			time_to_hit = await self.calculate_next_y_extremum_hit(self.ball, self.paddle)
			if time_to_hit >= 1:
				asyncio.sleep(time_to_hit + time_to_hit / 10) # wait for the next hit + delay to make sure the ball already bounced
			else:
				asyncio.sleep(1) # next hit in enemy side is in les than a second, we are fucked
	#bottibotto_vit_sa_vie end
 
	# this functions returns time to next hit (cumulates every hit until y=0.5 or y=-0.5) and the x position of the next hit
	async def calculate_next_y_extremum_hit(self, ball, paddle):
		cumulated_time = 0
		y = 30
		while y:
			y -= 1
			new_pos = find_collision_pos(ball.pos, ball.dir, ball.diameter)
			time_to_hit = time_to_travel(ball.pos, new_pos, ball.speed)
			cumulated_time += time_to_hit

			ball.pos = new_pos
			ball.speed *= 1.1 if ball.speed < 2 else 1  # Incrémenter la vitesse à un maximum de 2

			# Mise à jour de la direction après collision
			if new_pos.x == -0.5 + ball.diameter / 2:
				print("collision on ennemy side")
				ball.dir.x = abs(ball.dir.x)  # Collision à gauche
			elif new_pos.x == 0.5 - ball.diameter / 2:
				ball.pos.x -= 0.01
				print("collision on our side")
				ball.dir = paddle.collide(ball)  # Collision à droite
				ball.dir.x = -abs(ball.dir.x)
				paddle.next_pos = Vec2(-0.5, random.uniform(ball.pos.y + paddle.length / 2, ball.pos.y - paddle.length / 2))
				self.move_paddle_to_pos(paddle.pos.y, paddle.next_pos.y, paddle.speed, time_to_hit)

			if new_pos.y == -0.5 + ball.diameter / 2:
				ball.pos.y += 0.01
				ball.dir.y = abs(ball.dir.y)  # Collision en bas
			elif new_pos.y == 0.5 - ball.diameter / 2:
				ball.pos.y -= 0.01
				ball.dir.y = -abs(ball.dir.y)  # Collision en haut

			# Si la balle atteint le bord opposé (x = -0.5), arrêter la simulation
			if new_pos.x <= -0.5 + ball.diameter / 2:
				break
		print("cumulated time: ", cumulated_time)
		return cumulated_time
	#calculate_next_y_extremum_hit end

	# move paddle to next position to intercept the ball then move it back to the center
	async def move_paddle_to_pos(self, paddle_pos, next_pos, paddle_speed, time):
		print("Moving paddle from", paddle_pos, "to", next_pos)
		delta_pos = next_pos - paddle_pos
		time_required = time_to_travel(paddle_pos, next_pos, paddle_speed)
		current_time = time.perf_counter()
		# move paddle to next position
		if delta_pos > 0:
			self.down = True
			asyncio.sleep(time_required)
			self.down = False
		else:
			self.up = True
			asyncio.sleep(time_required)
			self.up = False
		# move back paddle to center
		asyncio.sleep(time - (time.perf_counter() - current_time))
		time_required = time_to_travel(next_pos, 0, paddle_speed)
		if delta_pos > 0:
			self.down = True
			asyncio.sleep(time_required)
			self.down = False
		else:
			self.up = True
			asyncio.sleep(time_required)
			self.up = False
	#move_paddle_to_pos end
 
	# get the paddle's movement status
	async def get_paddle_movement(self):
		return self.up, self.down
	#get_paddle_movement end
#BottiBotto end


# returns the first collision position with a border in the box{x{-0.5, 0.5}, y{-0.5, 0.5}}
def find_collision_pos(pos, dir, ball_diameter):
	radius = ball_diameter / 2
	slope = float('inf') if dir.x == 0 else dir.y / dir.x
	origin = pos.y - slope * pos.x

	# Calculate the collision position with the x border
	if dir.x != 0:
		x_edge = 0.5 - radius if dir.x > 0 else -0.5 + radius
		collide_x = Vec2(x_edge, slope * x_edge + origin)
		dist_x = find_distance(pos, collide_x)
	else:
		dist_x = float('inf')  # No collision with vertical borders if no horizontal movement
	# Calculate the collision position with the y border
	if dir.y != 0:
		y_edge = 0.5 - radius if dir.y > 0 else -0.5 + radius
		x_collide_y = (y_edge - origin) / slope if slope != float('inf') else pos.x
		collide_y = Vec2(x_collide_y, y_edge)
		dist_y = find_distance(pos, collide_y)
	else:
		dist_y = float('inf')  # No collision with horizontal borders if no vertical movement
	# Return the closest collision position
	if dist_x < dist_y:
		print("Collision with x border at x:", collide_x.x, "y:", collide_x.y)
		return collide_x
	elif dist_y < float('inf'):
		return collide_y
	else:
		# No collision expected
		return None
#find_collision_pos end


# returns distance between a and b
def find_distance(a, b):
	return math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)
#find_distance end
	
# returns the time required to travel between a and b
def time_to_travel(a, b, speed):
	return find_distance(a, b) / speed
#time_to_travel end


# contains every information related to the ball
class ball:
	def __init__(self, diameter, speed, acceleration):
		self.diameter = diameter
		self.speed = speed
		self.acceleration = acceleration
		self.pos = Vec2(0, 0)
		self.dir = Vec2(0, 0)
#ball end


# contains every information related do the paddle
class paddle:
	def __init__(self, length, speed):
		self.speed = speed
		self.length = length
		self.pos = Vec2(0, 0)
		self.next_pos = Vec2(0, 0)
		self.dir = Vec2(0, 0)

	# collide with the ball
	def collide(self, ball):
		angle = 180 + (80 * (self.next_pos.y - ball.pos.y) / self.length)
		return Vec2(math.cos(angle), math.sin(angle))
#paddle end


# class used for points and directions (2D vector)
class Vec2:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def normalize(self):
		mag = math.sqrt(self.x ** 2 + self.y ** 2)
		self.x /= mag
		self.y /= mag
		return self
#Vec2 end
	
#et voila on l'a bien baisé le noob d'adversaire