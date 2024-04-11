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



# ATTENTION JAI FINIT CETTE FONCTION TRES FATIGUE ELLE EST APPROXIMATIVE PEUTETRE

#this functions returns time to next hit (cumulates every hit until y=0.5 or y=-0.5) and the x position of the next hit
func calculate_next_y_extremum_hit(ball):
	# extend direction vector until it reaches one extremum of the plank (defined by x{-0.5, 0.5} y{-0.5, 0.5})
 
	ball.position = #calculate the next collision position
   	time_to_hit = #calculate the time to next position
	if ball.speed < 2:
		ball.speed *= 1.2
	# if it reaches y=-0.5 or y=0.5 before an x extremum
	 	#update ball wth new speed and new direction vector (we apply a y axis reflection)
		cumulated_time, hit_pos = calculate_next_y_extremum_hit(ball)
		cumulated_time += time_to_hit
	# else (it reaches x=-0.5 or x=0.5)
		cumulated_time == time_to_hit
	return cumulated_time, ball.position[0]


# ATTENTION JAI FINIT CETTE FONCTION TRES FATIGUE ELLE EST APPROXIMATIVE PEUTETRE
func move_paddle_to_pos(paddle.pos, pos, time)
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


func bottibotto_vit_sa_vie():
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