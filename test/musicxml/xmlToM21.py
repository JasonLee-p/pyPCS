# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         musicxml/xmlToM21.py
# Purpose:      Conversion from MusicXML to Music21
#
# Authors:      Michael Scott Asato Cuthbert
#               Christopher Ariza
#               Jacob Tyler Walls
#
# Copyright:    Copyright © 2009-2022 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
import copy
import fractions
import io
# import pprint
import re
# import sys
# import traceback
import warnings

from math import isclose
import typing as t

import xml.etree.ElementTree as ET

from music21 import common
from music21 import exceptions21
from music21.musicxml import xmlObjects
from music21.musicxml.xmlObjects import MusicXMLImportException, MusicXMLWarning

from music21 import articulations
from music21 import bar
from music21 import base  # for typing
from music21 import beam
from music21 import chord
from music21 import clef
from music21 import defaults
from music21 import duration
from music21 import dynamics
from music21 import editorial
from music21 import expressions
from music21 import harmony  # for chord symbols
from music21 import instrument
from music21 import interval  # for transposing instruments
from music21 import key
from music21 import layout
from music21 import metadata
from music21.midi.percussion import MIDIPercussionException, PercussionMapper
from music21 import note
from music21 import meter
from music21 import percussion
from music21 import pitch
from music21 import repeat
from music21 import spanner
from music21 import stream
from music21 import style
from music21 import tablature
from music21 import tempo
from music21 import text  # for text boxes
from music21 import tie

from music21 import environment


if __name__ == '__main__':
    import music21
    music21.mainTest()  # doctests only
