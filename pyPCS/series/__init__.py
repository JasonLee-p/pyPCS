"""
series
======
(unfinished)

Provides
  1. Various class object of post-tonal music items
  2. Easy transpositions over post-tonal music items

Available packages:
-------------------
1d series:
    PitchSeries, Rhyme, Chord, PitchClassSeries
2d series(segment):
    PitchSegment, PitchClassSegment, ContourSegment
"""

from .series1d import PitchSeries, Rhyme, Chord, PitchClassSeries
from .series2d import PitchSegment, PitchClassSegment, ContourSegment

__all__ = {
    "PitchSeries", "Rhyme", "Chord", "PitchClassSeries",
    "PitchSegment", "PitchClassSegment", "ContourSegment",
}