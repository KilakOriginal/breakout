FPS: int = 60
COLUMS_ROWS: tuple[int, int] = (15, 6)
TITLE: str = "Breakout"
WINDOW_SIZE: tuple[int, int] = (1200, 1200)

FONT_PATH: str = "assets/fonts/roboto.ttf"
FONT_SIZE: int = 24

BOARD_SIZE: tuple[float, float] = (800, 1000)
BORDER_SIZE: float = 20.0

BASE_BALL_MAX_VELOCITY: float = 35.0
BASE_BALL_VELOCITY: float = 30.0
LEVEL_BALL_SPEED_MULTIPLIER: float = 1.3
PADDLE_ACCELERATION_FACTOR: float = 1.5
PADDLE_BASE_SPEED_MULTIPLIER: float = 0.02
PADDLE_MAX_SPEED_MULTIPLIER: float = 0.08

AUDIO_BIT_DEPTH: int = 16
AUDIO_SAMPLE_RATE: int = 44100
AUDIO_CHANNELS: int = 2 # Valid options are 2 and 3. Mono or higher values are not supported by pygame.
