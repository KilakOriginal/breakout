import math
import numpy as np

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