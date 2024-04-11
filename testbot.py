class paddle:
	def __init__(self, length, speed):
		self.speed = speed
		self.length = length
		self.pos = [0, 0]
		self.movement = [0, 0]


class ball:
	def __init__(self, diameter, speed, acceleration):
		self.diameter = diameter
		self.speed = speed
		self.acceleration = acceleration
		self.position = [0, 0]
		self.movement = [0, 0]

		
