"""
    This module defines how to play various music elements (in midi file).
"""
from __future__ import annotations
import pygame.midi as pm
import pygame.time

pm.init()  # init midi _player
BPM = 80


if __name__ == "__main__":
    player = pm.Output(0)
