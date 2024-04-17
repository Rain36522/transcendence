import numpy as np
import matplotlib.pyplot as plt

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Ball:
    def __init__(self, pos, dir, speed, diameter):
        self.pos = pos
        self.dir = dir
        self.speed = speed
        self.diameter = diameter

class Paddle:
    def __init__(self, pos, length, speed):
        self.pos = pos
        self.length = length
        self.speed = speed

def find_collision_pos(pos, dir, ball_diameter):
    radius = ball_diameter / 2
    slope = float('inf') if dir.x == 0 else dir.y / dir.x
    origin = pos.y - (slope * pos.x if dir.x != 0 else 0)

    collide_x = Vec2(0.5 - radius if dir.x > 0 else -0.5 + radius, 
                     slope * (0.5 - radius if dir.x > 0 else -0.5 + radius) + origin if dir.x != 0 else pos.y)
    collide_y = Vec2(pos.x, 0.5 - radius if dir.y > 0 else -0.5 + radius)

    if dir.x == 0 or (collide_y.y == 0.5 - radius or collide_y.y == -0.5 + radius):
        return collide_y
    return collide_x

def find_distance(a, b):
    return np.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)

def calculate_trajectory(ball, paddle):
    positions = [ball.pos]
    times = [0]
    total_time = 0

    while True:
        new_pos = find_collision_pos(ball.pos, ball.dir, ball.diameter)
        print("Collision at x:", new_pos.x, "y:", new_pos.y)
        time_to_hit = find_distance(ball.pos, new_pos) / ball.speed
        total_time += time_to_hit

        # Update ball position
        ball.pos = new_pos
        positions.append(new_pos)
        times.append(total_time)

        # Reflect the ball's direction at borders
        if new_pos.x == 0.5 - ball.diameter/2 or new_pos.x == -0.5 + ball.diameter/2:
            ball.dir.x = -ball.dir.x
        if new_pos.y == 0.5 - ball.diameter/2 or new_pos.y == -0.5 + ball.diameter/2:
            ball.dir.y = -ball.dir.y

        # Check for game over condition
        if new_pos.x <= -0.5 + ball.diameter/2 or new_pos.x >= 0.5 - ball.diameter/2:
            break

    return positions, times

# Set up the initial conditions
ball = Ball(Vec2(0, 0), Vec2(3, 0), 0.02, 0.05)
paddle = Paddle(Vec2(0, 0.5), 0.1, 0.02)

# Calculate the trajectory
positions, times = calculate_trajectory(ball, paddle)

# Plot the results
x_vals = [p.x for p in positions]
y_vals = [p.y for p in positions]
plt.figure(figsize=(10, 5))
plt.plot(x_vals, y_vals, marker='o')
plt.grid(True)
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Ball Trajectory and Collisions')
plt.show()
