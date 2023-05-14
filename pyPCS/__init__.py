"""
pyPCS
=====
(unfinished)

Provides
  1. Various class object_ of post-tonal music items
  2. Easy transpositions over post-tonal music items
  3. Random chord, series, pitch_class_series generation

    We are trying to make a powerful and professional post tonal music analyzing tool.

    As midi file regard C4 as 60, so in pypcs, we consider C4'pypcs pitch space as 60 instead of 0.

How to use the documentation
----------------------------
Documentation is available in two forms: docstrings provided
with the code, and a loose standing reference guide, available from
`github <https://github.com/JasonLee-p/pyPCS>`_.
(might be uncompleted somewhere as it is unfinished)

To import `pyPCS`::

  >>> import pyPCS

Code snippets are indicated by three greater-than signs::

  >>> x = 69
  >>> x = x % 12

Use the built-in ``help`` function to view a function'pypcs docstring::

  >>> # unfinished
  >>> help(pyPCS.PitchSegment)
  ... # doctest: +SKIP

For some objects, ``np.info(obj)`` may provide additional help.  This is
particularly true if you see the line "Help on ufunc object_:" at the top
of the help() page.  Ufuncs are implemented in C, not Python, for speed.
The native Python help() does not know how to view their help, but our
np.info() function does.

To search for documents containing a keyword, do::

  >>> # unfinished
  >>> pyPCS.lookfor('keyword')
  ... # doctest: +SKIP

General-purpose documents like a glossary and help on the basic concepts
of numpy are available under the ``doc`` sub-module::

  >>> # unfinished
  >>> from pyPCS import PitchSegment
  >>> help(PitchSegment)
  ... # doctest: +SKIP

Available subpackages
---------------------
basicGenerator
    Basic functions used in generating small music elements like a pitch set.
chorder
    Basic functions used in chord analysing.
piecesGenerator
    Functions used in generating some tiny piano pieces.
pitchSegment
    Class objects of several post-tonal music items, and several related funtions.
testing  # unfinished
    pypcs testing tools


Some naming regulations:
------------------------
If an attribute end up with "group",
    it means that it'pypcs order is not in consideration.

If an attribute end up with "pitch_class_series",
    it means that it'pypcs ordered and contains pitch_class_series set.

If an attribute end up with "series",
    it means that it'pypcs ordered and contains pitches' or pitch sets' duration.
"""

from .series import PitchSegment, PitchClassSeries

from ._player import *

from .chorder import root_note_PH, mod12

__all__ = [
    "play_note", "play_chord", "play_chord_set", "play_pitch_segment",  # _player
    "root_note_PH", "mod12"  # chorder
]
from .series.series1d import PitchSeries, Rhythm, Chord, PitchClassSeries
from .series.series2d import PitchSegment, ContourSegment
from .basicGenerator import get_segments_subsegment, counterpoint, \
    randomChord, randomSegment, randomRhythm
from .piecesGenerator import *

__all__.extend(series.__all__)
__all__.extend(basicGenerator.__all__)
__all__.extend(piecesGenerator.__all__)


def __dir__():
    public_symbols = globals().keys() | {'Tester', 'testing'}  # TODO: unfinished
    public_symbols -= {
        "pm",
    }
    return list(public_symbols)
