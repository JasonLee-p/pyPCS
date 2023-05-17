import unittest
from pyPCS import PitchSeries, Rhythm, PitchSegment


class TestPitchSegment(unittest.TestCase):
    r0 = Rhythm(['1/2', '3/2', '1', '1', '2', '2'])
    pSeries0 = PitchSeries([60, 61, 62, 63, 64, 65])
    pSeg = PitchSegment([pSeries0, r0])

    def test_equal(self):
        self.assertEqual(TestPitchSegment.pSeg, [[60, 61, 62, 63, 64, 65], ['1/2', '3/2', '1', '1', '2', '2']])
        self.assertEqual(TestPitchSegment.pSeg.segment, [[60, 61, 62, 63, 64, 65], ['1/2', '3/2', '1', '1', '2', '2']])
        # 测试PitchSegment
        self.assertEqual(TestPitchSegment.pSeg.pitchSeries, [60, 61, 62, 63, 64, 65])
        self.assertEqual(TestPitchSegment.pSeg.pitchSeries, TestPitchSegment.pSeries0)
        self.assertEqual(TestPitchSegment.pSeg.pitchSeries.series, [60, 61, 62, 63, 64, 65])
        self.assertEqual(TestPitchSegment.pSeg.pitchSeries.series, TestPitchSegment.pSeries0)
        # 测试Rhythm
        self.assertEqual(TestPitchSegment.pSeg.rhythm, ['1/2', '3/2', '1', '1', '2', '2'])
        self.assertEqual(TestPitchSegment.pSeg.rhythm, TestPitchSegment.r0)
        self.assertEqual(TestPitchSegment.pSeg.rhythm.rhythm, ['1/2', '3/2', '1', '1', '2', '2'])
        self.assertEqual(TestPitchSegment.pSeg.rhythm.rhythm, TestPitchSegment.r0)

    def test_T(self):
        self.assertEqual(
            TestPitchSegment.pSeg.Transposition(1),
            [[61, 62, 63, 64, 65, 66], ['1/2', '3/2', '1', '1', '2', '2']])
        self.assertEqual(
            TestPitchSegment.pSeg + 1,
            [[61, 62, 63, 64, 65, 66], ['1/2', '3/2', '1', '1', '2', '2']])

    def test_Retrograde(self):
        self.assertEqual(
            TestPitchSegment.pSeg.Retrograde_without_rhythm(),
            [[65, 64, 63, 62, 61, 60], ['1/2', '3/2', '1', '1', '2', '2']])
        self.assertEqual(
            TestPitchSegment.pSeg.Retrograde_with_rhythm(),
            [[65, 64, 63, 62, 61, 60], ['2', '2', '1', '1', '3/2', '1/2']])

