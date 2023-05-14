"""
basicGenerator
==============
This package describes how to generate basic elements of music.
"""

from .basicGenerator import get_segments_subsegment, counterpoint
from .basicGenerator import randomChord, randomRhythm, randomSegment

__all__ = [
    "get_segments_subsegment", "counterpoint",
    "randomChord", "randomRhythm", "randomSegment"
]
