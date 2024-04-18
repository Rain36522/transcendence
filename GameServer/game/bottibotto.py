import math
import random
import time
import asyncio
import copy
from sys import stderr



# bot routine
class BottiBotto:
	def __init__(self, game_logic, game_settings):
		self.game_logic = game_logic
		self.game_settings = game_settings

		self.ball = ball(
			self.game_settings["ball_diameter"],
			self.game_settings["ball_speed"],
			self.game_settings["ball_acceleration"],
		)
		self.ball.dir = self.game_settings["ball_dir"]
		self.paddle = paddle(
			self.game_settings["paddle_length"], self.game_settings["paddle_speed"]
		)
		self.up = False
		self.down = False

	# bottibotto_vit_sa_vie


	# main bot routine
	async def bottibotto_vit_sa_vie(self):
		time_to_hit = 0
		while True:
			game_state = await self.game_logic.get_game_state()
			if game_state["game_over"]:  # terminate bot routine, game over
				break
			self.ball.pos = game_state["ball_pos"]
			self.ball.dir = game_state["ball_dir"]
			self.ball.speed = game_state["ball_speed"]
			self.paddle.pos.y = game_state["paddle_pos"].y
			# print(
			# 	f"""
			# O[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]O
			# H
		 	# H							GAME UPDATE
			# H		BALL:
			# H				position: [{round(self.ball.pos.x, 3)}, {round(self.ball.pos.y, 3)}]
			# H				direction: [{round(self.ball.dir.x, 3)}, {round(self.ball.dir.y, 3)}]
			# H				speed: {round(self.ball.speed, 3)}
			# H   
			# H		PADDLE: 
			# H				pos: [{round(self.paddle.pos.x, 3)}, {round(self.paddle.pos.y, 3)}]
			# H
			# O[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]O
			# """,
			# 	file=stderr,
			# )
			time_to_hit = await self.calculate_next_y_extremum_hit(
				self.ball, self.paddle
			)
			# print(
			# 	f"""
			# /~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\\
		 	# L
		 	# L	sleep time: {round(time_to_hit if time_to_hit >= 1 else 1, 3)}
			# """,
			# 	file=stderr,
			# )
			timestamp = time.perf_counter()
			if time_to_hit < 1:
				time_to_hit = 1
			await asyncio.sleep(
				time_to_hit
			)  # wait for the next hit + delay to make sure the ball already bounced
			# print(
			# 	f"""
			# L	real time slept: {round(time.perf_counter() - timestamp, 3)}
			# L
			# \\~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/
			# """,
			# 	file=stderr,
			# )

	# bottibotto_vit_sa_vie end


	# this functions returns time to next hit (cumulates every hit until y=0.5 or y=-0.5) and the x position of the next hit
	async def calculate_next_y_extremum_hit(self, ball, paddle):
		cumulated_time = 0
		max_loop_repeat = 30
		# bounced_right = False
		delay_start = time.perf_counter()

		while max_loop_repeat:
			max_loop_repeat -= 1
	
			new_pos = find_collision_pos(ball.pos, ball.dir, ball.diameter)

			time_to_hit = time_to_travel(ball.pos, new_pos, ball.speed)
			cumulated_time += time_to_hit
			# old_pos = ball.pos
			ball.pos = new_pos

			if ball.speed < 1.8:
				ball.speed += ball.acceleration
			if ball.speed > 1.8:
				ball.speed = 1.8

			# collisoin_side = "LEFT" if new_pos.x == -0.49 + ball.diameter / 4 else ("RIGHT" if new_pos.x == 0.49 - ball.diameter / 4 else ("UP" if new_pos.y == -0.5 + ball.diameter / 2 else ("DOWN" if new_pos.y == 0.5 - ball.diameter / 2 else "NONE")))
			
			if new_pos.x == 0.49 - ball.diameter / 4: # Collision right
				ball.dir.x = -abs(ball.dir.x)
		
				paddle.next_pos.y = random.uniform(ball.pos.y + paddle.length / 2, ball.pos.y - paddle.length / 2)
				paddle_travel_time = cumulated_time - (time.perf_counter() - delay_start)
				if time_to_travel(paddle.pos, paddle.next_pos, paddle.speed) > paddle_travel_time:
					if paddle.next_pos.y - paddle.pos.y > 0:
						paddle.next_pos.y -= paddle_travel_time * paddle.speed
					else:
						paddle.next_pos.y += paddle_travel_time * paddle.speed
				else:
					paddle_travel_time = time_to_travel(paddle.pos, paddle.next_pos, paddle.speed)

				ball.dir = paddle.collide(ball)  # Collision à droite
				# print(
				# 	f"""
				# /--------------------------------------------------------------------\\
				# |
				# |   moving paddle from [{round(paddle.pos.x, 3)}, {round(paddle.pos.y, 3)}] to [{round(paddle.next_pos.x, 3)}, {round(paddle.next_pos.y, 3)}]
				# |	operation set to take {round(paddle_travel_time, 3)} seconds
				# |
				# |   remaining time to hit after operation: {round(cumulated_time - (time.perf_counter() - delay_start) - paddle_travel_time, 3)} seconds
				# |
				# \\--------------------------------------------------------------------/
				# """,
				# 	file=stderr,
				# )
				await self.move_paddle_to_pos(copy.deepcopy(paddle.pos), copy.deepcopy(paddle.next_pos),  copy.deepcopy(paddle.speed), copy.deepcopy(paddle_travel_time))
				paddle.pos.y = paddle.next_pos.y

			if new_pos.y == -0.5 + ball.diameter / 2 or new_pos.y == 0.5 - ball.diameter / 2:
				ball.dir.y = -ball.dir.y  # Collision down
			# print(
			# 	f"""
			# O--------------------------------------------------------------------O
			# |
			# |   COLLISION: {collisoin_side}
			# |
			# |   from [{round(old_pos.x, 3)}, {round(old_pos.y, 3)}] to [{round(new_pos.x, 3)},{round(new_pos.y, 3)}]
			# |
			# |   estimated travel time: {round(time_to_hit, 3)} seconds to travel distance {round(find_distance(old_pos, new_pos), 3)}
			# |
			# |   cumulated time: {round(cumulated_time, 3)} seconds
			# |
			# O--------------------------------------------------------------------O
			# """,
			# 	file=stderr,
			# )
			if new_pos.x <= -0.49 + ball.diameter / 4: #ball went fully 
				break
		#loop end
		# paddle.next_pos.y = 0
		# center_move_time =  time.perf_counter() - delay_start
		# if center_move_time > time_to_travel(paddle.pos, paddle.next_pos, paddle.speed):
		# 	center_move_time = time_to_travel(paddle.pos, paddle.next_pos, paddle.speed)
		# 	if paddle.next_pos.y - paddle.pos.y > 0:
		# 		paddle.next_pos.y -= center_move_time * paddle.speed
		# 	else:
		# 		paddle.next_pos.y += center_move_time * paddle.speed
		# print(
		# 	f"""
		# /--------------------------------------------------------------------\\
		# |
		# |   moving paddle from [{round(paddle.pos.x, 3)}, {round(paddle.pos.y, 3)}] to [{round(paddle.next_pos.x, 3)}, {round(paddle.next_pos.y, 3)}]
		# |	operation set to take {round(center_move_time, 3)} seconds
		# |
		# |   remaining time to hit after operation: {round(cumulated_time - (time.perf_counter() - delay_start) - center_move_time, 3)} seconds
		# |
		# \\--------------------------------------------------------------------/
		# """,
		# 	file=stderr,
		# )
		# await self.move_paddle_to_pos(copy.deepcopy(paddle.pos), copy.deepcopy(paddle.next_pos),  copy.deepcopy(paddle.speed), center_move_time)

		if cumulated_time - (time.perf_counter() - delay_start) >= 1:
			return cumulated_time - (time.perf_counter() - delay_start) + 0.05
		else:
			return 1 - (time.perf_counter() - delay_start) + 0.05
	# calculate_next_y_extremum_hit end


	# move paddle to next position to intercept the ball then move it back to the center
	async def move_paddle_to_pos(self, paddle_pos, next_pos, paddle_speed, total_time):
		delta_pos = next_pos.y - paddle_pos.y
		time_required = time_to_travel(paddle_pos, next_pos, paddle_speed)
		if time_required > total_time:
			time_required = total_time
		if delta_pos > 0:
			self.up = True
			await asyncio.sleep(time_required)
			self.up = False
		else:
			self.down = True
			await asyncio.sleep(time_required)
			self.down = False
		return time_required
	# move_paddle_to_pos end


	# get the paddle's movement status
	async def get_paddle_movement(self):
		return self.up, self.down
	# get_paddle_movement end
# BottiBotto end



# returns the first collision position with a border in the box{x{-0.5, 0.5}, y{-0.5, 0.5}}
def find_collision_pos(pos, dir, ball_diameter):
	radius = ball_diameter / 2
	slope = float("inf") if dir.x == 0 else dir.y / dir.x
	origin = pos.y - slope * pos.x
	# Calculate the collision position with the x border
	if dir.x != 0:
		x_edge = 0.49 - (radius / 2) if dir.x > 0 else -0.49 + (radius / 2)
		collide_x = Vec2(x_edge, slope * x_edge + origin)
		dist_x = find_distance(pos, collide_x)
	else:
		dist_x = float("inf")  # No collision with vertical borders if no horizontal movement
	# Calculate the collision position with the y border
	if dir.y != 0:
		y_edge = 0.5 - radius if dir.y > 0 else -0.5 + radius
		x_collide_y = (y_edge - origin) / slope if slope != float("inf") else pos.x
		collide_y = Vec2(x_collide_y, y_edge)
		dist_y = find_distance(pos, collide_y)
	else:
		dist_y = float("inf")  # No collision with horizontal borders if no vertical movement
	# Return the closest collision position
	if dist_x < dist_y:
		return collide_x
	elif dist_y < float("inf"):
		return collide_y
# find_collision_pos end



# returns distance between a and b
def find_distance(a, b):
	return math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)
# find_distance end



# returns the time required to travel between a and b
def time_to_travel(a, b, speed):
	return find_distance(a, b) / speed
# time_to_travel end



# contains every information related to the ball
class ball:
	def __init__(self, diameter, speed, acceleration):
		self.diameter = diameter
		self.speed = speed
		self.acceleration = acceleration
		self.pos = Vec2(0, 0)
		self.dir = Vec2(0, 0)
# ball end



# contains every information related do the paddle
class paddle:
	def __init__(self, length, speed):
		self.speed = speed
		self.length = length
		self.pos = Vec2(0.49, 0)
		self.next_pos = Vec2(0.49, 0)
		self.dir = Vec2(0, 0)
	# collide with the ball
	def collide(self, ball):
		max_collide = self.length / 2 + ball.diameter / 4
		angle = 180 + (70 * (self.next_pos.y - ball.pos.y) / max_collide)
		return angle_to_Vec2(angle)
# paddle end



# get direction vector from angle
def angle_to_Vec2(angle):
	return Vec2(math.cos(math.radians(angle)), math.sin(math.radians(angle)))
# dir_angle end



# class used for points and directions (2D vector)
class Vec2:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def normalize(self):
		mag = math.sqrt(self.x**2 + self.y**2)
		self.x /= mag
		self.y /= mag
		return self
# Vec2 end



# et voila on l'a bien baisé le noob d'adversaire