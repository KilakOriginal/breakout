from colours import *
from constants import *
from maths import Vector

import enum
import random


# Tweakable Gravitation
G: float = 6.67439e-11
M: float = 5.972e+24
r: float = 6.371e+6
g: float = G * (M / (r ** 2))
vector_g: Vector[float] = Vector(0.0, g)

class Block:
    colour: tuple[int, int, int]
    position: Vector[float]
    size: float

    def __init__(self, position: Vector[float], size: float, colour: tuple[int, int, int]):
        self.position = position # Top left
        self.size = size
        self.colour = colour


class Ball:
    position: Vector[float] # Center
    radius: float
    velocity: Vector[float]
    max_velocity: float
    
    def __init__(self, position: Vector[float], radius: float):
        self.position = position
        self.radius = radius
        self.velocity = Vector(random.choice([-5.0, 5.0]), -BASE_BALL_VELOCITY)
        self.max_velocity = BASE_BALL_MAX_VELOCITY

    def update(self, delta_time: float):
        # Constant velocity kinematics (No gravity)
        #self.position = self.position + self.velocity * delta_time + 0.5 * vector_g * (delta_time ** 2)
        #self.velocity = self.velocity + vector_g * delta_time
        self.position = self.position + self.velocity * delta_time

    def bounce_x(self):
        self.velocity = Vector(-min(self.max_velocity, abs(self.velocity[0])) * (1 if self.velocity[0] > 0 else -1), self.velocity[1])

    def bounce_y(self):
        self.velocity = Vector(self.velocity[0], -min(self.max_velocity, abs(self.velocity[1])) * (1 if self.velocity[1] > 0 else -1))


class Direction(enum.Enum):
    LEFT = -1
    RIGHT = 1
    STOP = 0

class Paddle:
    position: Vector[float] # Top left
    size: tuple[float, float]
    velocity: Vector[float]

    board_width: float
    
    max_speed: float
    base_speed: float
    acceleration_factor: float
    deceleration_factor: float

    def __init__(self, position: Vector[float], size: tuple[float, float], board_width: float):
        self.position = position
        self.size = size
        self.velocity = Vector(0.0, 0.0)
        
        self.board_width = board_width

        self.max_speed = PADDLE_MAX_SPEED_MULTIPLIER * board_width
        self.base_speed = PADDLE_BASE_SPEED_MULTIPLIER * board_width
        self.acceleration_factor = PADDLE_ACCELERATION_FACTOR
        self.deceleration_factor = self.acceleration_factor ** 1.5

    def update(self, direction: Direction, delta_time: float, speed_multiplier: float = 1.0):
        current_speed: float = abs(self.velocity[0])

        # === Deceleration ===
        if direction == Direction.STOP:
            if current_speed > 0:
                current_speed = max(current_speed - current_speed * self.deceleration_factor * delta_time, 0.0)
                self.velocity = Vector(current_speed * (1 if self.velocity[0] > 0 else -1), 0.0)
                self.position = Vector(min(max(self.position[0] + self.velocity[0] * delta_time, 0.0), self.board_width - self.size[0]), self.position[1])
            return
        
        # === Acceleration ===
        # Instant turn-around
        #if (self.velocity[0] > 0 and direction == Direction.LEFT) or (self.velocity[0] < 0 and direction == Direction.RIGHT):
        #    self.velocity = Vector(0.0, 0.0)
        
        
        if current_speed < self.base_speed:
            current_speed = self.base_speed

        # Exponential acceleration: v = v + (v * factor * dt)
        current_speed = min(current_speed + current_speed * self.acceleration_factor * delta_time, self.max_speed * speed_multiplier)

        self.velocity = Vector(current_speed * direction.value, 0.0)
        self.position = Vector(min(max(self.position[0] + self.velocity[0] * delta_time, 0.0), self.board_width - self.size[0]), self.position[1])


class Board:
    ball: Ball
    blocks: list[Block]
    paddle: Paddle
    
    bounds: tuple[float, float]
    original_bounds: tuple[float, float] # Add this
    number_blocks: tuple[int, int]
    block_colours: list[tuple[int, int, int]]
    block_area: float 
    block_percentage: float = 0.25 # Top 25% of board

    top_space: int = 2

    level: int
    score: int

    def __init__(self, bounds: tuple[float, float], number_blocks: tuple[int, int] = COLUMS_ROWS, block_colours: list[tuple[int, int, int]] = BLOCK_COLOURS, level: int = 1, score: int = 0):
        self.original_bounds = bounds
        block_size: float = bounds[0] / number_blocks[0]
        self.bounds = (bounds[0], max(bounds[1], ((number_blocks[1] - self.top_space) * block_size) * (1/self.block_percentage)))
        
        self.blocks = []
        self.number_blocks = number_blocks
        self.block_colours = block_colours
        for y in range(number_blocks[1]):
            for x in range(number_blocks[0]):
                self.blocks.append(Block(Vector(x * block_size, (y + self.top_space) * block_size), block_size, block_colours[y]))
        self.block_area = ((number_blocks[1] + self.top_space) * block_size) + block_size

        self.ball = Ball(Vector(self.original_bounds[0] / 2 - block_size / 2, self.original_bounds[1] * (1 - 0.1) + block_size / 2), block_size / 3) 

        paddle_size: tuple[float, float] = (block_size * 3, block_size / 2)
        self.paddle = Paddle(Vector(self.original_bounds[0] / 2 - paddle_size[0] / 2, self.original_bounds[1] * (1 - 0.05)), paddle_size, self.original_bounds[0]) 
        
        self.level = level
        self.score = score

    def update(self, paddle_direction: Direction, delta_time: float, paddle_speed_multiplier: float = 1.0) -> int:
        self.ball.update(delta_time)
        self.paddle.update(paddle_direction, delta_time, paddle_speed_multiplier)

        # Check Wall Collisions
        if self.ball.position[1] - self.ball.radius >= self.bounds[1]: # Bottom Wall
            return 0 # Game Over
        
        # Left/Right Walls
        if (self.ball.position[0] - self.ball.radius <= 0) or \
           (self.ball.position[0] + self.ball.radius >= self.bounds[0]):
            self.ball.bounce_x()
            # Push ball out of wall to prevent sticking
            if self.ball.velocity[0] > 0:
                self.ball.position = Vector(self.ball.radius, self.ball.position[1])
            else:
                self.ball.position = Vector(self.bounds[0] - self.ball.radius, self.ball.position[1])

        # Top Wall
        if (self.ball.position[1] - self.ball.radius <= 0):
            self.ball.bounce_y()
            self.ball.position = Vector(self.ball.position[0], self.ball.radius)

        # Check Paddle Collision
        if self.ball.position[1] + self.ball.radius >= self.paddle.position[1]: # Only if ball is at the height of the paddle

            if (self.ball.position[0] >= self.paddle.position[0]) and \
               (self.ball.position[0] <= self.paddle.position[0] + self.paddle.size[0]):
                
                # Calculate relative hit position (0 is left, 1 is right)
                relative_intersect = (self.ball.position[0] - self.paddle.position[0]) / self.paddle.size[0]

                # 0.5 is center. < 0.5 sends left, > 0.5 sends right.
                speed = (self.ball.velocity[0]**2 + self.ball.velocity[1]**2)**0.5
                
                # Map 0..1 to -1..1
                bounce_angle = (relative_intersect - 0.5) * 2.0 

                new_vx = speed * bounce_angle * 1.5
                new_vy = -(speed * (1 - abs(bounce_angle) * 0.5))
                
                self.ball.velocity = Vector(new_vx, new_vy)

                return 3


        # Check Block Collisions
        if self.ball.position[1] - self.ball.radius <= self.block_area: 
            for block in self.blocks:
                # AABB collision check. Not exact for a circle, but good enough and much faster than a circle-rectangle collision check.
                if (self.ball.position[0] + self.ball.radius >= block.position[0] and 
                    self.ball.position[0] - self.ball.radius <= block.position[0] + block.size and
                    self.ball.position[1] + self.ball.radius >= block.position[1] and 
                    self.ball.position[1] - self.ball.radius <= block.position[1] + block.size):
                    
                    self.blocks.remove(block)
                    self.ball.bounce_y()
                    self.score += 1
                    return 2
            if not self.blocks: # All blocks destroyed
                self.score += 10
                self.reset(level_up=True, score=self.score)
                return -1

        return 1

    def get_score(self) -> int:
        return self.score * 15 + self.level ** 3
    
    def reset(self, level_up: bool = False, score: int = 0):
        self.__init__(self.original_bounds, self.number_blocks, self.block_colours, self.level + 1 if level_up else 1, score)