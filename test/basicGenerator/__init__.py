"""
basicGenerator
==============
This package describes how to generate basic elements of music.
"""

from .basic_generator import get_segments_subsegment, random_atonal_pitch_space, counterpoint
from .basic_generator import randomChord, randomRhythm, randomSegment

__all__ = [
    "get_segments_subsegment", "random_atonal_pitch_space", "counterpoint",
    "randomChord", "randomRhythm", "randomSegment"
]
