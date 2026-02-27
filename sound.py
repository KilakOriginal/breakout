from constants import *

import math
import numpy as np
import pygame

def noise(amplitude: float, frequency: float, time: float, phase: float = 0.0) -> float:
    return amplitude * np.random.uniform(-1, 1)

def sine(amplitude: float, frequency: float, time: float, phase: float = 0.0) -> float:
    return amplitude * math.sin(2 * math.pi * frequency * time + phase)

def sawtooth(amplitude: float, frequency: float, time: float, phase: float = 0.0) -> float:
    return amplitude * (2 * (time * frequency - math.floor(time * frequency + 0.5 + phase / (2 * math.pi))) - 0.5)

def square(amplitude: float, frequency: float, time: float, phase: float = 0.0) -> float:
    return amplitude * (1 if math.sin(2 * math.pi * frequency * time + phase) >= 0 else -1)

def triangle(amplitude: float, frequency: float, time: float, phase: float = 0.0) -> float:
    return amplitude * (2 * abs(2 * (time * frequency - math.floor(time * frequency + 0.5 + phase / (2 * math.pi))) - 0.5) - 1)


class Sound:
    def __init__(self, frequency: float, duration_seconds: float, sound_wave_generator: callable = sine):
        self.frequency = frequency
        self.duration = duration_seconds
        self.sound_wave_generator = sound_wave_generator

    def generate(self) -> pygame.mixer.Sound:
        num_samples = int(AUDIO_SAMPLE_RATE * self.duration)
        amplitude = 2 ** (AUDIO_BIT_DEPTH - 1) - 1

        samples = np.array([self.sound_wave_generator(amplitude, self.frequency, i / AUDIO_SAMPLE_RATE) for i in range(num_samples)], dtype=np.int16)
        if AUDIO_CHANNELS > 1:
            samples = np.repeat(samples[:, np.newaxis], AUDIO_CHANNELS, axis=1)

        return pygame.sndarray.make_sound(samples)
    

def play_sounds(sounds: list[pygame.mixer.Sound]):
    for sound in sounds:
        sound.play()