from __future__ import annotations
import unittest
from pyPCS import Chord
from typing import List


class TestChord(unittest.TestCase):
    C = Chord([60, 64, 67])
    Cm = Chord([60, 63, 67])
    C7 = Chord([60, 64, 67, 70])
    C6 = Chord([48, 60, 64, 67, 69])

    def test_colour_tian(self):
        self.assertEqual(TestChord.C.colour_tian_CentralOnC, (10, 35.0))
        self.assertEqual(TestChord.Cm.colour_tian_CentralOnC, (10, -35.0))
        self.assertEqual(TestChord.C7.colour_tian_CentralOnC, (9, 7.5))
        self.assertEqual(TestChord.C6.colour_tian_CentralOnC, (10, 33.0))

