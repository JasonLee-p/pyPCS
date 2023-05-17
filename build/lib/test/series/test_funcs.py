"""
Basic functions:
"""
import unittest
import copy
import math
from fractions import Fraction
from typing import List

import numpy as np

import pyPCS
from pyPCS.series.funcs import *
from pyPCS import Chord


class TestFuncs(unittest.TestCase):
    # I1 = Chord([60, 63])
    # I2 = Chord([60, 64])
    # C_0 = Chord([48, 60, 64, 67])
    # C_1 = Chord([48, 55, 60, 64])
    # C_2 = Chord([48, 52, 55, 60])
    # C_3 = Chord([60, 64, 67])
    # C_4 = Chord([48, 55, 64, 67])
    # C_5 = Chord([48, 55, 64])
    # Caug = Chord([60, 64, 68, 72])
    # sFdim = Chord([60, 66, 69, 72])
    # Csus4 = Chord([60, 65, 67])
    # Csus2 = Chord([60, 62, 67])
    # Cq = Chord([60, 65, 70])
    # CM7_0 = Chord([48, 55, 59, 64])
    # CM7_1 = Chord([60, 64, 67, 71])
    # C7_0 = Chord([48, 55, 58, 64])
    # C7_1 = Chord([60, 64, 67, 70])
    # Cm7_0 = Chord([60, 63, 67, 70])
    # Cm7_1 = Chord([60, 67, 70, 75])
    # Cm75_0 = Chord([60, 63, 66, 70])
    # Cm75_1 = Chord([60, 66, 70, 75])

    def test_to_pc_set(self):
        self.assertEqual(to_pc_set([60, 61, 72, 65], True), [0, 1, 0, 5])
        self.assertEqual(to_pc_set([60, 61, 72, 65]), [0, 1, 5])
        self.assertEqual(to_pc_set([60, 60, 0, 0, 12, 75, 100], True), [0, 0, 0, 0, 0, 3, 4])
        self.assertEqual(to_pc_set([60, 60, 0, 0, 12, 75, 100]), [0, 3, 4])

    def test_get_sub_segment(self):
        test_segment = [[60, 61, 62, 63, 64, 65], ['1/2', '3/2', '1', '1', '2', '2']]
        self.assertEqual(get_subsegment(test_segment, 0, 8),
                         [[60, 61, 62, 63, 64, 65], ['1/2', '3/2', '1', '1', '2', '2']])
        self.assertEqual(get_subsegment(test_segment, 0, 4),
                         [[60, 61, 62, 63], ['1/2', '3/2', '1', '1']])
        self.assertEqual(get_subsegment(test_segment, 0, 1.5),
                         [[60, 61], ['1/2', '1']])
        self.assertEqual(get_subsegment(test_segment, 1.5, 8),
                         [[61, 62, 63, 64, 65], ['1/2', '1', '1', '2', '2']])
        self.assertEqual(get_subsegment(test_segment, 4, 8),
                         [[64, 65], ['2', '2']])
        self.assertEqual(get_subsegment(test_segment, 1, 4),
                         [[61, 62, 63], ['1', '1', '1']])
        self.assertEqual(get_subsegment(test_segment, 0.25, 1.5),
                         [[60, 61], ['1/4', '1']])
        self.assertEqual(get_subsegment(test_segment, 1, 1.5),
                         [[61], ['1/2']])

    def test_contains_Mm3_chord(self):
        self.assertTrue(contains_M_m_3chord([0, 4, 7]))

    def test_chord_consonance_tian(self):
        self.assertEqual(chord_consonance_tian([60, 64, 67], None), 10)
        self.assertEqual(chord_consonance_tian([60, 65, 67], None), 9.67)
        self.assertEqual(chord_consonance_tian([60, 61, 62, 75, 76], None), 1)
        for i in range(10000):
            print(i)
            chord = pyPCS.randomChord(3)
            self.assertNotEqual(chord_consonance_tian(sorted(chord), None), None)
            chord = pyPCS.randomChord(4)
            self.assertNotEqual(chord_consonance_tian(sorted(chord), None), None)
            chord = pyPCS.randomChord(5)
            self.assertNotEqual(chord_consonance_tian(sorted(chord), None), None)
            chord = pyPCS.randomChord(6)
            self.assertNotEqual(chord_consonance_tian(sorted(chord), None), None)
            chord = pyPCS.randomChord(7)
            self.assertNotEqual(chord_consonance_tian(sorted(chord), None), None)
            chord = pyPCS.randomChord(8)
            self.assertNotEqual(chord_consonance_tian(sorted(chord), None), None)
