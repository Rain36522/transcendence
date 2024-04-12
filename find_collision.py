import matplotlib.pyplot as plt
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
		return self

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
		angle = math.radians(180 + 70 * (self.next_pos.y - ball.pos.y) / (self.length / 2))
		
		# Calcul du nouveau vecteur directionnel basé sur l'angle
		new_dir_x = math.cos(angle)
		new_dir_y = math.sin(angle)
		
		return Vec2(new_dir_x, new_dir_y)

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

# Définitions de Vec2, ball, et paddle inchangées

def calculate_trajectory(ball, paddle):
	trajectory = [(ball.pos.x, ball.pos.y, 0)]  # Initiale: position et temps
	cumulated_time = 0

	while True:
		new_pos = find_collision_pos(ball.pos, ball.dir, ball.diameter)
		time_to_hit = time_to_travel(ball.pos, new_pos, ball.speed)
		cumulated_time += time_to_hit
		trajectory.append((new_pos.x, new_pos.y, cumulated_time))

		# Mise à jour de la position et potentiellement de la vitesse
		ball.pos = new_pos
		if ball.speed < 2:
			ball.speed *= 1.2

		# Réflexion selon le bord touché
		if ball.pos.y == 0.5 - ball.diameter / 2 or ball.pos.y == -0.5 + ball.diameter / 2:
			ball.dir.y *= -1
		if ball.pos.x == 0.5 - ball.diameter / 2:
			paddle.next_pos = Vec2(-0.5, ball.pos.y + paddle.length / 2)  # Mettre à jour la position de la raquette pour la collision
			ball.dir = paddle.collide(ball).normalize()  # Ajuster la direction de la balle après collision

		# Arrêt si la balle atteint un bord vertical autre que le bord gauche
		if ball.pos.x == -0.5 + ball.diameter / 2:
			break

	return trajectory

def main():
	# Initialisation de la balle et de la raquette
	ball_dia = 0.05
	initial_pos = Vec2(-0.49, 0)  # Position initiale
	initial_dir = Vec2(1, 3).normalize()  # Direction initiale normalisée
	my_ball = ball(ball_dia, 0.1, 0.1)
	my_ball.pos = initial_pos
	my_ball.dir = initial_dir

	my_paddle = paddle(0.4, 0)  # Création de la raquette

	trajectory = calculate_trajectory(my_ball, my_paddle)

	# Configuration du graphique
	fig, ax = plt.subplots()
	ax.set_xlim(-0.6, 0.6)
	ax.set_ylim(-0.6, 0.6)
	rectangle = plt.Rectangle((-0.5, -0.5), 1, 1, linewidth=2, edgecolor='r', facecolor='none')
	ax.add_patch(rectangle)

	# Tracer la trajectoire
	x_values, y_values, times = zip(*trajectory)
	plt.plot(x_values, y_values, '-o', color='blue')

	# Annoter chaque point de collision avec le temps écoulé
	for x, y, time in trajectory:
		plt.text(x, y, f'{time:.2f}s', verticalalignment='bottom')

	plt.show()

if __name__ == "__main__":
	main()
