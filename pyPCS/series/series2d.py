"""
This module defines functions in Pitches-class Set Theory.

"""
from __future__ import annotations

import numpy as _np
from typing import Tuple, Union
from fractions import Fraction

import pyPCS.series.series1d as ps  # 避免循环调用错误，不使用from语法
from .. import basicGenerator
from ..classmethod_dec import once_per_arg
from .tree import SegmentTree, SeriesTree, RhythmTree
from .funcs import *


# 有序的音集（截段）
class PitchSegment:
    """
    Any function that change the series list return a new object_ of a class (may not be PitchSegment):

    Pitch series contains a pitch set and a pitch_class_series, various attributes and transformations are included in the class:
    Attributes:
        number of notes:
        duration:
        average pitch:
        tendentiousness:

    Transformations:
        transposition:
        retrograde:
        Inversion:
        retrograde Inversion:
        multiplication:
        rotation:
    """

    def __init__(
            self, segment: Union[List[Union[ps.PitchSeries, ps.Rhythm]], List[List[int], list[str]]],
            new_tree=True, name=False, parent=None, __style=None):
        """
        The first element of variable 'series' is a PitchSeries object_ while the second element is a Rhythm object_.
        You are not supposed to use attributes start with "__" !
        :param segment: Segment.
        :param new_tree: If you want to set a new tree of segments and set this one as the parent, set it as True
        """

        if new_tree and name:
            raise ValueError("You shouldn't change '__name' default value.")
        elif new_tree is False and name is False:
            raise ValueError("You haven't set '__name', which is necessary when 'new_tree' is False.")
        elif new_tree:
            self.parent = None
            self.name = input("Enter the name of the PitchSegment tree:\n")
            self.tree = SegmentTree(self)
        elif type(name) is str:  # 这时传入的tree_name应当是转换方法，也就是每一次变换之后返回的第三个值。
            self.parent = parent
            self.name = f'{self.parent.name}: {name}'
            self.tree = parent.tree
            self.tree.append_(parent, self)
        else:
            raise ValueError("Invalid tree_name")
        # TODO: 检查节奏和音集长度是否相等
        self.pitchSeries = segment[0]  # 音集对象
        self.rhythm = segment[1]  # 节奏对象
        self.pitch_set = segment[0].series  # 音集列表
        self.duration_set = segment[1].rhythm  # 节奏列表
        self.segment = [self.pitch_set, self.duration_set]
        self.style = __style
        self.length = len(self.pitch_set)  # 获取音高列表的长度
        self.total_duration = _np.sum([float(eval(d)) for d in self.duration_set])  # 获取总时值
        self.w_average = pitches_weighed_average(self.segment)  # 计算加权（时值权重）平均音高
        segment_result = tendentiousness(self.segment)  # 音高和密度的趋向性
        self.pitch_tend = segment_result[0]  # 音高趋向性
        self.rhythm_intensity_tend = segment_result[1]  # 密度趋向性

    def show(self):
        print(self.segment)

    def show_sheet(self):
        import matplotlib.pyplot as plt
        # import matplotlib

        # 设置图像大小和边距
        fig = plt.figure(figsize=(8, 3), dpi=100)
        plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.2)

        # 绘制五条线
        x = [0, 10]
        for i in range(5):
            y = [i * 2 + 1, i * 2 + 1]
            plt.plot(x, y, 'k', linewidth=1)

        # 显示图像
        plt.axis('off')
        plt.show()

    @once_per_arg
    def get_pc_segment(self) -> Tuple[object, PitchSegment, str]:
        pitch_class_set = to_pc_set(self.pitch_set[:], ordered=True)
        return ps.PitchClassSeries([pitch_class_set], self.rhythm), self, "Pitch class series"

    def getSubsegment(self, start_beat, end_beat=None):
        """
        This attribute returns a pitch series list.

        :param start_beat:Start beat.
        :param end_beat:End beat.
        :return:New PitchSegment object which is the subsegment of the original one.
        """
        s = get_subsegment(self.segment, start_beat, end_beat)[:]
        return s

    def getCounterpoint(self) -> PitchSegment:
        """ Get a two voice series using counterpoint. """
        # TODO:unfinished
        print("getCounterpoint unfinished")
        return self

    def get_average(self) -> float:
        return self.w_average

    @once_per_arg
    def Transposition(self, add_pitch: int) -> PitchSegment:
        """
        This function creates a Transposition transformation of self.

        :param add_pitch: Transposition num.
        :return: Transposed new PitchSegment object_.
        """
        new_ps = self.pitchSeries.Transposition(add_pitch)
        return PitchSegment([new_ps, self.rhythm],
                            new_tree=False, parent=self, name=f"Transposition{add_pitch % 12}")

    @once_per_arg
    def Retrograde_with_rhythm(self, add_pitch: int = 0) -> PitchSegment:
        """
        This function creates a Retrograde transformation of self with changed pitch_class_series.

        :param add_pitch: Transposition num.
        :return: Retrograded new PitchSegment object_.
        """
        new_ps = reversed(self.pitchSeries)
        new_r = reversed(self.rhythm)
        if add_pitch == 0:
            return PitchSegment([new_ps, new_r],
                                new_tree=False, parent=self, name="Retrograde (with pitch_class_series)")
        new_ps_ = new_ps.Transposition(add_pitch)
        return PitchSegment([new_ps_, new_r],
                            new_tree=False, parent=self, name=f"Retrograde{add_pitch}")

    @once_per_arg
    def Retrograde_without_rhythm(self, add_pitch: int = 0) -> PitchSegment:
        """
        This function creates a Retrograde transformation of self without changing the pitch_class_series.
        :param add_pitch: Transposition num.
        :return: Retrograded new PitchSegment object_.
        """
        new_ps = reversed(self.pitchSeries)
        if add_pitch == 0:
            return PitchSegment([new_ps, self.rhythm],
                                new_tree=False, parent=self, name="Retrograde (without pitch_class_series)")
        new_ps_ = new_ps.Transposition(add_pitch)
        return PitchSegment([new_ps_, self.rhythm],
                            new_tree=False, parent=self, name=f"Retrograde{add_pitch} (without pitch_class_series)")

    @once_per_arg
    def Inversion(self, axes: int) -> PitchSegment:
        """
        This function creates an Inversion transformation of self without changing the pitch_class_series.
        :param axes: An int to invert each pitch in the set.
        :return: Inverted new PitchSegment object_.
        """
        new_ps = self.pitchSeries.Inversion(axes)
        return PitchSegment([new_ps, self.rhythm],
                            new_tree=False, parent=self, name=f"Inversion{axes}")

    @once_per_arg
    def RetrogradeInversion(self, axes: int) -> PitchSegment:
        """
        This function creates a Retrograde then Inversion transformation of self with changed pitch_class_series.
        :param axes: An int to invert each pitch in the set.
        :return: Retrograde then Inversion new PitchSegment object_.
        """
        new_ps_i = self.pitchSeries.Inversion(axes)
        new_ps_ir = new_ps_i.Retrograde()
        new_rhythm = reversed(self.rhythm)
        return PitchSegment([new_ps_ir, new_rhythm],
                            new_tree=False, parent=self, name=f"RetrogradeInversion{axes} (with pitch_class_series)")

    @once_per_arg
    def Rotation_without_rhythm(self, num: int, add_pitch: int = 0) -> PitchSegment:
        """
        This function creates a Rotation transformation of self without changing the pitch_class_series.
        :param num: Rotation num
        :param add_pitch: Transposition num.
        :return: Roted new PitchSegment object_.
        """
        if not 0 <= num < self.length:
            raise ValueError("The attribute 'num' should be smaller than length of the series.")
        new_ps = self.pitchSeries.Rotation(num=num, add_pitch=add_pitch)
        if add_pitch == 0:
            return PitchSegment([new_ps, self.rhythm],
                                new_tree=False, parent=self, name=f"Rotation{num} (without pitch_class_series)")
        new_ps_ = new_ps.Transposition(add_pitch)
        return PitchSegment([new_ps_, self.rhythm],
                            new_tree=False, parent=self, name=f"Rotation{num} (without pitch_class_series),T{add_pitch}")

    @once_per_arg
    def Rotation_with_rhythm(self, num: int, add_pitch: int = 0) -> PitchSegment:
        """
        This function creates a Rotation transformation of self with changed pitch_class_series.
        :param num: Rotation num
        :param add_pitch: Transposition num.
        :return: Retrograded new PitchSegment object_.
        """
        if not 0 <= num < self.length:
            raise ValueError("The attribute 'num' should be smaller than length of the series.")
        new_ps = self.pitchSeries.Rotation(num=num, add_pitch=add_pitch)
        new_r = self.rhythm.Rotation(num)
        if add_pitch == 0:
            return PitchSegment([new_ps, new_r],
                                new_tree=False, parent=self, name=f"Rotation{num} (with pitch_class_series)")
        new_ps_ = new_ps.Transposition(add_pitch)
        return PitchSegment([new_ps_, new_r],
                            new_tree=False, parent=self, name=f"Rotation{num} (with pitch_class_series),T{add_pitch}")

    def play(self, pg_player=None, bpm=80, instrument='piano'):
        """
        :param pg_player: Pygame.midi.Output(int) var. If you haven't set it, keep it None.
        eg:
        player = pygame.midi.output(0)
        ps1.play(pg_player=player)
        :param bpm: Beats per minutes.
        :param instrument: instrument.
        """
        from .._player import play_pitch_segment
        play_pitch_segment(pg_player, self.segment, instrument=instrument, bpm=bpm)
        del play_pitch_segment

    def __hash__(self):
        return hash(self.segment)

    def __eq__(self, other: Union[list, PitchSegment]):
        if type(other) == list:
            return self.segment == other
        return self.segment == other.segment

    def __len__(self):
        return self.length

    def __iter__(self):
        return iter(zip(self.pitch_set, self.duration_set))

    @once_per_arg
    def __add__(self, add_pitch: int) -> PitchSegment:
        new_ps = self.pitchSeries.Transposition(add_pitch)
        return PitchSegment([new_ps, self.rhythm],
                            new_tree=False, parent=self, name=f"Transposition{add_pitch}")

    @once_per_arg
    def __sub__(self, sub_pitch: int) -> PitchSegment:
        new_ps = self.pitchSeries.Transposition(sub_pitch)
        return PitchSegment([new_ps, self.rhythm],
                            new_tree=False, parent=self, name=f"Transposition{12 - sub_pitch}")

    def __mod__(self, number: int):
        pass

    def __getitem__(self, item):
        return self.pitch_set[int(item)], self.duration_set[int(item)]

    @once_per_arg
    def __setitem__(self, key, value) -> PitchSegment:
        """
        Variable *keys includes two element.
        Variable "values" is two-element list.
        """
        new_pitch_set = self.pitch_set
        new_pitch_set[key] = value
        new_pitch_series = ps.PitchSeries(
            new_pitch_set, new_tree=False, parent=self.pitchSeries, name=f"Reset pitch[{key}]{note_value[value]}")
        return PitchSegment(
            [new_pitch_series, self.rhythm],
            new_tree=False, parent=self, name=f"Reset pitch[{key}]{note_value[value]}")

    @once_per_arg
    def __reversed__(self) -> PitchSegment:
        new_ps = reversed(self.pitchSeries)
        new_r = reversed(self.rhythm)
        return PitchSegment([new_ps, new_r],
                            new_tree=False, parent=self, name="Retrograde (with pitch_class_series)")


# 有序的音集（截段），这个是一个不实例化节奏和音级集合的版本，暂时不用
class _PitchSegment:
    """
    Any function that change the series list return a new object_ of a class (may not be PitchSegment):

    Pitch series contains a pitch set and a pitch_class_series, various attributes and transformations are included in the class:
    Attributes:
        number of notes:
        duration:
        average pitch:
        tendentiousness:

    Transformations:
        transposition:
        retrograde:
        Inversion:
        retrograde Inversion:
        multiplication:
        rotation:
    """

    def __init__(self, segment: List[List[int], List[str]], new_tree=True, name=False, parent=None, __style=None):
        """
        The first element of variable 'series' is a pitch list while the second element is a duration list.
        You are not supposed to use attributes start with "__" !
        :param segment: Segment.
        :param new_tree: If you want to set a new tree of segments and set this one as the parent, set it as True
        """

        # 判断输入值是否合法
        judging0 = [True
                    if (type(int(ii)) is not int) else 0
                    for ii in segment[0]]
        judging1 = [True
                    if (type(ii) is not str and ('/' not in ii, len(ii) != 1)) else 0
                    for ii in segment[1]]
        if True in judging0:
            raise ValueError("Invalid note format.")
        if True in judging1:
            raise ValueError("Invalid duration format.")

        if new_tree is True and name is True:
            raise ValueError("You shouldn't change '__name' default value.")
        elif new_tree is False and name is False:
            raise ValueError("You haven't set '__name', which is necessary when 'new_tree' is False.")
        elif new_tree is True:
            self.parent = None
            self.name = input("Enter the name of the series tree:\n")
            self.tree = SegmentTree(self)
        elif type(name) is str:  # 这时传入的tree_name应当是转换方法，也就是每一次变换之后返回的第三个值。
            self.parent = parent
            self.name = f'{self.parent.name}: {name}'
            self.tree = SegmentTree.check_tree(parent)
            self.tree.append_(parent, self)
        else:
            raise ValueError("Invalid tree_name")

        self.segment = segment
        self.style = __style
        self.pitch_series = segment[0]  # 音高
        self.rhythm = segment[1]  # 时值
        self.length = len(self.pitch_series)  # 获取音高列表的长度
        self.total_duration = _np.sum([float(eval(d)) for d in self.rhythm])  # 获取总时值
        self.w_average = pitches_weighed_average(segment)  # 计算加权（时值权重）平均音高
        segment_result = tendentiousness(segment)  # 音高和密度的趋向性
        self.pitch_tend = segment_result[0]  # 音高趋向性
        self.rhythm_intensity_tend = segment_result[1]  # 密度趋向性

    def __hash__(self):
        return hash(self.segment)

    def __eq__(self, other):
        return self.segment == other.segment

    def __len__(self):
        return self.length

    def __iter__(self):
        return iter(zip(self.pitch_series, self.rhythm))

    @once_per_arg
    def __add__(self, add_pitch: int) -> PitchSegment:
        new_pitch_set = [new_pitch + add_pitch for new_pitch in self.pitch_series]
        return PitchSegment([new_pitch_set, self.rhythm][:],
                            new_tree=False, parent=self, name=f"Transposition{add_pitch}")

    @once_per_arg
    def __sub__(self, sub_pitch: int) -> PitchSegment:
        new_pitch_set = [new_pitch - sub_pitch for new_pitch in self.pitch_series]
        return PitchSegment([new_pitch_set, self.rhythm][:],
                            new_tree=False, parent=self, name=f"Transposition{12 - sub_pitch}")

    def __mod__(self, number: int):
        pass

    def __getitem__(self, item):
        return self.pitch_series[int(item)], self.rhythm[int(item)]

    @once_per_arg
    def __setitem__(self, key, value) -> PitchSegment:
        """
        Variable *keys includes two element.
        Variable "values" is two-element list.
        """
        new_pitch_set = self.pitch_series
        new_pitch_set[key] = value
        return PitchSegment([new_pitch_set, self.rhythm[:]],
                            new_tree=False, parent=self, name=f"Reset pitch[{key}]{note_value[value]}")

    @once_per_arg
    def __reversed__(self) -> PitchSegment:
        new_pitch_set = reversed(self.pitch_series)
        new_duration_set = reversed(self.rhythm)
        return PitchSegment([list(new_pitch_set)[:], list(new_duration_set)[:]],
                            new_tree=False, parent=self, name="Retrograde (with pitch_class_series)")

    @once_per_arg
    def get_pc_segment(self) -> Tuple[object, PitchSegment, str]:
        pitch_class_set = to_pc_set(self.pitch_series[:], ordered=True)
        import pyPCS.series.series1d as ps1
        return ps1.PitchClassSeries([pitch_class_set], self.rhythm[:]), self, "Pitch class series"

    @once_per_arg
    def change_rhyme(self, total_duration: float, new_style: str) -> PitchSegment:
        """ To overwrite a new pitch_class_series to the pitch set.   """
        self.style = new_style
        _segment = [self.pitch_series, basicGenerator.randomRhythm(self.length, total_duration, new_style)]
        return PitchSegment(_segment,
                            new_tree=False, parent=self, __style=new_style, name="Different pitch_class_series")

    def get_counterpoint(self) -> PitchSegment:
        """ Get a two voice series using counterpoint. """
        # TODO:unfinished
        print("getCounterpoint unfinished")
        return self

    def get_average(self) -> float:
        return self.w_average

    def get_pitch_tend(self) -> float:
        return self.pitch_tend

    def get_rhythm_intensity_tend(self) -> float:
        return self.rhythm_intensity_tend

    @once_per_arg
    def Transposition(self, add_pitch: int) -> PitchSegment:
        """
        This function creates a Transposition transformation of self.
        :param add_pitch: Transposition num.
        :return: Transposed new PitchSegment object_.
        """
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in self.pitch_series]
        return PitchSegment([new_pitch_set, self.rhythm][:],
                            new_tree=False, parent=self, name=f"Transposition{add_pitch % 12}")

    @once_per_arg
    def Retrograde_with_rhyme(self, add_pitch: int = 0) -> PitchSegment:
        """
        This function creates a Retrograde transformation of self with changed pitch_class_series.
        :param add_pitch: Transposition num.
        :return: Retrograded new PitchSegment object_.
        """
        new_pitch_set = list(reversed(self.pitch_series))[:]
        new_duration_set = list(reversed(self.rhythm))[:]
        if add_pitch == 0:
            return PitchSegment([new_pitch_set, new_duration_set],
                                new_tree=False, parent=self, name="Retrograde (with pitch_class_series)")
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in new_pitch_set]
        return PitchSegment([new_pitch_set, new_duration_set],
                            new_tree=False, parent=self, name=f"Retrograde{add_pitch}")

    @once_per_arg
    def Retrograde_without_rhyme(self, add_pitch: int = 0) -> PitchSegment:
        """
        This function creates a Retrograde transformation of self without changing the pitch_class_series.
        :param add_pitch: Transposition num.
        :return: Retrograded new PitchSegment object_.
        """
        new_pitch_set = list(reversed(self.pitch_series))[:]
        if add_pitch == 0:
            return PitchSegment([new_pitch_set, self.rhythm[:]],
                                new_tree=False, parent=self, name="Retrograde without pitch_class_series")
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in new_pitch_set]
        return PitchSegment([new_pitch_set, self.rhythm[:]],
                            new_tree=False, parent=self, name=f"Retrograde{add_pitch}")

    @once_per_arg
    def Inversion(self, axes: int) -> PitchSegment:
        """
        This function creates an Inversion transformation of self without changing the pitch_class_series.
        :param axes: An int to invert each pitch in the set.
        :return: Inverted new PitchSegment object_.
        """
        new_pitch_set = [2 * axes - pitch for pitch in self.pitch_series]
        return PitchSegment([new_pitch_set, self.rhythm[:]],
                            new_tree=False, parent=self, name=f"Inversion{axes}")

    @once_per_arg
    def RetrogradeInversion(self, axes: int) -> PitchSegment:
        """
        This function creates a Retrograde then Inversion transformation of self with changed pitch_class_series.
        :param axes: An int to invert each pitch in the set.
        :return: Retrograde then Inversion new PitchSegment object_.
        """
        new_pitch_set = reversed([2 * axes - pitch for pitch in self.pitch_series])
        new_duration_set = reversed(self.rhythm)
        return PitchSegment([new_pitch_set, new_duration_set],
                            new_tree=False, parent=self, name=f"RetrogradeInversion{axes} (with pitch_class_series)")

    @once_per_arg
    def Rotation_without_rhyme(self, num: int, add_pitch: int = 0) -> PitchSegment:
        """
        This function creates a Rotation transformation of self without changing the pitch_class_series.
        :param num: Rotation num
        :param add_pitch: Transposition num.
        :return: Roted new PitchSegment object_.
        """
        if not 0 <= num < self.length:
            raise ValueError("The attribute 'num' should be smaller than length of the series.")
        new_pitch_set = [self.pitch_series[(ii + num) % self.length] for ii in range(self.length)]
        if add_pitch == 0:
            return PitchSegment([new_pitch_set[:], self.rhythm[:]],
                                new_tree=False, parent=self, name=f"Rotation{num} (without pitch_class_series)")
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in new_pitch_set]
        return PitchSegment([new_pitch_set[:], self.rhythm[:]],
                            new_tree=False, parent=self, name=f"Rotation{num} (without pitch_class_series),T{add_pitch}")

    @once_per_arg
    def Rotation_with_rhyme(self, num: int, add_pitch: int = 0) -> PitchSegment:
        """
        This function creates a Rotation transformation of self with changed pitch_class_series.
        :param num: Rotation num
        :param add_pitch: Transposition num.
        :return: Retrograded new PitchSegment object_.
        """
        if not 0 <= num < self.length:
            raise ValueError("The attribute 'num' should be smaller than length of the series.")
        new_pitch_set = [self.pitch_series[(ii + num) % self.length] for ii in range(self.length)]
        new_duration_set = [self.rhythm[(ii + num) % self.length] for ii in range(self.length)]
        if add_pitch == 0:
            return PitchSegment([new_pitch_set[:], new_duration_set[:]],
                                new_tree=False, parent=self, name=f"Rotation{num} (with pitch_class_series)")
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in new_pitch_set]
        return PitchSegment([new_pitch_set[:], new_duration_set[:]],
                            new_tree=False, parent=self, name=f"Rotation{num} (with pitch_class_series),T{add_pitch}")

    def play(self, pg_player=None, bpm=80, instrument='piano'):
        """
        :param pg_player: Pygame.midi.Output(int) var. If you haven't set it, keep it None.
        eg:
        player = pygame.midi.output(0)
        ps1.play(pg_player=player)
        :param bpm: Beats per minutes.
        :param instrument: instrument.
        """
        from .._player import play_pitch_segment
        play_pitch_segment(pg_player, self, instrument=instrument, bpm=bpm)
        del play_pitch_segment


# TODO: 轮廓截段
class ContourSegment:
    def __init__(self, segment):
        self.pitch_set = segment[0]
