"""
    Show how to receive MIDI input by setting a callback function and send data to midi output .
"""

from __future__ import print_function

import logging
import sys
import time
import rtmidi
midiout = rtmidi.RtMidiOut()
available_ports = midiout.getPortCount()

if available_ports:
    midiout.openPort(0)
else:
    midiout.openVirtualPort("My virtual output")

log = logging.getLogger('midiin_callback')
logging.basicConfig(level=logging.DEBUG)

