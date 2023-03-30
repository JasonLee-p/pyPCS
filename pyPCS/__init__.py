"""
A professional post tonal music analyzer (unfinished).
We will try to put all the concepts about post tonal theory in the package.
"""

from .pitchSegment import PitchSegment, PitchClassSeries

from ._player import *

from .basicGenerator import get_segments_subsegment, counterpoint, \
    randomChord, randomSegment, randomRhythm, random_relative_pitch_set

from .chorder import root_note_PH, mod12

__all__ = [
    "PitchSegment", "PitchClassSeries",  # basicGenerator
    "play_note", "play_chord", "play_chord_set", "play_pitch_segment",  # _player
    "get_segments_subsegment", "counterpoint",  # basicGenerator
    "randomChord", "randomSegment", "randomRhythm", "random_relative_pitch_set",  # basicGenerator
    "root_note_PH", "mod12"  # chorder
]
