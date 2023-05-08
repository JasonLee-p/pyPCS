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

from .series1d import PitchSeries, Rhyme, Chord, PitchClassSeries
from .series2d import PitchSegment, PitchClassSegment, ContourSegment

__all__ = {
    "PitchSeries", "Rhyme", "Chord", "PitchClassSeries",
    "PitchSegment", "PitchClassSegment", "ContourSegment",
}
