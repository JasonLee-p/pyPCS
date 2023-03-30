"""
basicGenerator
==============
This package describes how to generate basic elements of music.
"""

from .basic_generator import get_segments_subsegment, random_relative_pitch_set, counterpoint
from .basic_generator import randomChord, randomRhythm, randomSegment

__all__ = [
    "get_segments_subsegment", "random_relative_pitch_set", "counterpoint",
    "randomChord", "randomRhythm", "randomSegment"
]
