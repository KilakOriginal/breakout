from constants import *
from sound.waves import *

import numpy as np
import pygame


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