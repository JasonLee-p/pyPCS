"""
series
======
(unfinished)

Provides
  1. Various class object_ of post-tonal music items
  2. Easy transpositions over post-tonal music items

Available packages:
-------------------
1d series:
    PitchSeries, Rhythm, Chord, PitchClassSeries
2d series(pitch_class_series):
    PitchSegment, PitchClassSeries, ContourSegment
"""

from .series1d import PitchSeries, Rhythm, Chord, PitchClassSeries
from .series2d import PitchSegment, ContourSegment
from .tree import MainTree

__all__ = {
    "PitchSeries", "Rhythm", "Chord", "PitchClassSeries",
    "PitchSegment", "PitchClassSeries", "ContourSegment",
    "MainTree",
}
