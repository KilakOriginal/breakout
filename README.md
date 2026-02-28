# Breakout
Breakout is a video game inspired by the 1976 Atari, Inc. action game of the same title for the Atari 2600.

<img src="breakout_gameplay.gif" style="display: block; margin-left: auto; margin-right: auto; height: 500px;"/>

# Gameplay
The goal of breakout is to break as many of the coloured blocks as possible, by hitting the ball into them with the paddle.

If you succeed and destroy all the blocks, you progress to the next level, increasing the difficulty. You lose one life each time the ball is dropped. If you run out of lives, you lose.

## Controls
You can play Breakout with a keyboard or with a joystick/controller.

**Keyboard:**
- `P`: Pause Game
- `R`: Restart Game
- `Right/Left Arrow`: Move Paddle to the Right/Left

**Joystick/Controller**
- `Main Axis`: Move Paddle to the Right/Left

## For Developers
Since the game logic is separate from the PyGame game loop, this can easily be adapted for a machine learning agent. You can also copy my environment from my [DQN Breakout Agent](https://github.com/KilakOriginal/breakout-agent) repository.