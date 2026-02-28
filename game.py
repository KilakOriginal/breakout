from components import *
from constants import *
from maths import Vector
from pygame.locals import *
from sound import *

import pygame


class Game:
    def __init__(self):
        pygame.mixer.pre_init(AUDIO_SAMPLE_RATE, -AUDIO_BIT_DEPTH, AUDIO_CHANNELS)

        pygame.init()
        
        pygame.joystick.init()
        self.joystick = None
        self.joystick_deadzone = 0.1
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        
        pygame.font.init()
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)

        self.display = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(TITLE)

        self.fps = pygame.time.Clock()
        self.fps.tick(FPS)

        self.paused = False

        self.board = Board(BOARD_SIZE, COLUMS_ROWS)
        self.paddle_speed_multiplier = 1.0

        self.board_surface = pygame.Surface(BOARD_SIZE)
        self.board_position = ((WINDOW_SIZE[0] - BOARD_SIZE[0]) / 2, (WINDOW_SIZE[1] - BOARD_SIZE[1]) / 2)
        self.board_background = pygame.Surface((BOARD_SIZE[0] + BORDER_SIZE * 2, BOARD_SIZE[1] + BORDER_SIZE * 2))
        self.board_background_position = (self.board_position[0] - BORDER_SIZE, self.board_position[1] - BORDER_SIZE)

        self.block_hit_sound = Sound(1000, 0.1).generate()
        self.game_over_sound = [Sound(200, 0.5).generate(), Sound(150, 0.5).generate(), Sound(100, 0.5).generate()]
        self.clear_level_sound = [Sound(800, 0.5).generate(), Sound(5600, 0.5).generate(), Sound(10200, 0.5).generate()]
        self.paddle_hit_sound = Sound(500, 0.1).generate()

    def draw_board(self):
        self.board_background.fill(GREY)
        self.display.blit(self.board_background, self.board_background_position)

        self.board_surface.fill(BLACK)

        for block in self.board.blocks:
            x = int(round(block.position[0]))
            y = int(round(block.position[1]))
            next_x = int(round(block.position[0] + block.size))
            next_y = int(round(block.position[1] + block.size))

            width = next_x - x
            height = next_y - y
            
            pygame.draw.rect(self.board_surface, block.colour, (x, y, width, height))

        pygame.draw.circle(self.board_surface, WHITE, (int(self.board.ball.position[0]), int(self.board.ball.position[1])), int(self.board.ball.radius))

        pygame.draw.rect(self.board_surface, BROWN, (*self.board.paddle.position, *self.board.paddle.size))

        self.display.blit(self.board_surface, self.board_position)

    def draw_score(self):
        level_string = f"Level: {self.board.level}"
        score_string = f"Score: {self.board.get_score()}"
        lives_string = f"Lives: {self.board.lives}"

        level_text = self.font.render(level_string, True, WHITE)
        score_text = self.font.render(score_string, True, WHITE)
        lives_text = self.font.render(lives_string, True, WHITE)

        self.display.blit(level_text, (self.board_position[0] - BORDER_SIZE, self.board_position[1] - level_text.get_height() - BORDER_SIZE - 5))
        self.display.blit(score_text, (self.board_position[0] - BORDER_SIZE + level_text.get_width() + 10, self.board_position[1] - score_text.get_height() - BORDER_SIZE - 5))
        self.display.blit(lives_text, (self.board_position[0] - BORDER_SIZE + level_text.get_width() + score_text.get_width() + 20, self.board_position[1] - lives_text.get_height() - BORDER_SIZE - 5))

    def draw(self):
        self.display.fill(BLACK)
        self.draw_board()
        self.draw_score()

    def run(self) -> int:
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return 0
                if event.type == KEYDOWN:
                    if event.key == K_p:
                        self.paused = not self.paused
                    if event.key == K_r:
                        self.board.reset()

            if not self.paused:
                direction = Direction.STOP
                keys = pygame.key.get_pressed()
                if keys[K_LEFT] and not keys[K_RIGHT]:
                    direction = Direction.LEFT
                    self.paddle_speed_multiplier = 1.0
                elif keys[K_RIGHT] and not keys[K_LEFT]:
                    direction = Direction.RIGHT
                    self.paddle_speed_multiplier = 1.0

                # Joystick input overrides keyboard input
                if self.joystick is not None:
                    axis_value = self.joystick.get_axis(0)
                    if axis_value < -self.joystick_deadzone:
                        direction = Direction.LEFT
                        self.paddle_speed_multiplier = 0.1 + (abs(axis_value) * 0.9)
                    elif axis_value > self.joystick_deadzone:
                        direction = Direction.RIGHT
                        self.paddle_speed_multiplier = 0.1 + (abs(axis_value) * 0.9)

                game_state = self.board.update(direction, 1.0 / FPS, self.paddle_speed_multiplier)

                match game_state:
                    case 0:
                        play_sounds(self.game_over_sound)
                    case 1:
                        pass
                    case 2:
                        self.block_hit_sound.play()
                    case 3:
                        self.paddle_hit_sound.play()
                    case -1:
                        self.board.ball.max_velocity *= LEVEL_BALL_SPEED_MULTIPLIER
                        play_sounds(self.clear_level_sound)
                    case _:
                        raise ValueError(f"Invalid game state '{game_state}' returned from board update")

                self.draw()
            pygame.display.update()