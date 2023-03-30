"""
This module defines functions in Pitches-class Set Theory.

"""
from __future__ import annotations

import numpy as _np
from typing import List, Tuple

from .. import series  # 避免循环调用错误，不使用from语法
from .. import basicGenerator
from ..classmethod_dec import once_per_arg
from .tree import SegmentTree, SeriesTree, RhymeTree
from .funcs import *


# 有序的音集（截段）
class PitchSegment:
    """
    Any function that change the series list return a new object of a class (may not be PitchSegment):

    Pitch series contains a pitch set and a rhyme, various attributes and transformations are included in the class:
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
        self.pitch_set = segment[0]  # 音高
        self.duration_set = segment[1]  # 时值
        self.length = len(self.pitch_set)  # 获取音高列表的长度
        self.total_duration = _np.sum([float(eval(d)) for d in self.duration_set])  # 获取总时值
        self.w_average = pitches_weighed_average(segment)  # 计算加权（时值权重）平均音高
        segment_result = tendentiousness(segment)  # 音高和密度的趋向性
        self.pitch_tend = segment_result[0]  # 音高趋向性
        self.rhythm_intensity_tend = segment_result[1]  # 密度趋向性
        # 对时值表进行小数化，用于hash
        ds = [round(eval(duration), 2) for duration in self.duration_set]
        self.compared_segment = [self.pitch_set, ds[:]]

    def __hash__(self):
        return hash(self.compared_segment)

    def __eq__(self, other):
        return self.compared_segment == other.compared_segment

    def __len__(self):
        return len(self.duration_set)

    def __iter__(self):
        return iter(zip(self.pitch_set, self.duration_set))

    @once_per_arg
    def __add__(self, add_pitch: int) -> PitchSegment:
        new_pitch_set = [new_pitch + add_pitch for new_pitch in self.pitch_set]
        return series.PitchSegment([new_pitch_set, self.duration_set][:],
                                   new_tree=False, parent=self, name=f"Transposition{add_pitch}")

    @once_per_arg
    def __sub__(self, sub_pitch: int) -> PitchSegment:
        new_pitch_set = [new_pitch - sub_pitch for new_pitch in self.pitch_set]
        return series.PitchSegment([new_pitch_set, self.duration_set][:],
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
        return series.PitchSegment([new_pitch_set, self.duration_set[:]],
                                   new_tree=self, parent=self, name=f"Reset pitch[{key}]{note_value[value]}")

    @once_per_arg
    def __reversed__(self) -> PitchSegment:
        new_pitch_set = reversed(self.pitch_set)
        new_duration_set = reversed(self.duration_set)
        return series.PitchSegment([list(new_pitch_set)[:], list(new_duration_set)[:]],
                                   new_tree=self, parent=self, name="Retrograde (with rhyme)")

    @once_per_arg
    def get_pc_segment(self) -> Tuple[object, PitchSegment, str]:
        pitch_class_set = to_pc_group(self.pitch_set[:], ordered=True)
        return series.PitchClassSegment([pitch_class_set], self.duration_set[:]), self, "Pitch class series"

    @once_per_arg
    def change_rhyme(self, total_duration: float, new_style: str) -> PitchSegment:
        """ To overwrite a new rhyme to the pitch set.   """
        self.style = new_style
        _segment = [self.pitch_set, basicGenerator.randomRhythm(self.length, total_duration, new_style)]
        return series.PitchSegment(_segment,
                                   new_tree=self, parent=self, __style=new_style, name="Different rhyme")

    def get_counterpoint(self) -> PitchSegment:
        """ Get a two voice series using counterpoint. """
        # TODO:unfinished
        print("get_counterpoint unfinished")
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
        :return: Transposed new PitchSegment object.
        """
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in self.pitch_set]
        return series.PitchSegment([new_pitch_set, self.duration_set][:],
                                   new_tree=self, parent=self, name=f"Transposition{add_pitch}")

    @once_per_arg
    def Retrograde_with_rhyme(self, add_pitch: int = 0) -> PitchSegment:
        """
        This function creates a Retrograde transformation of self with changed rhythm.
        :param add_pitch: Transposition num.
        :return: Retrograded new PitchSegment object.
        """
        new_pitch_set = list(reversed(self.pitch_set))[:]
        new_duration_set = list(reversed(self.duration_set))[:]
        if add_pitch == 0:
            return series.PitchSegment([new_pitch_set, new_duration_set],
                                       new_tree=self, parent=self, name="Retrograde (with rhyme)")
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in new_pitch_set]
        return series.PitchSegment([new_pitch_set, new_duration_set],
                                   new_tree=self, parent=self, name=f"Retrograde{add_pitch}")

    @once_per_arg
    def Retrograde_without_rhyme(self, add_pitch: int = 0) -> PitchSegment:
        """
        This function creates a Retrograde transformation of self without changing the rhythm.
        :param add_pitch: Transposition num.
        :return: Retrograded new PitchSegment object.
        """
        new_pitch_set = list(reversed(self.pitch_set))[:]
        if add_pitch == 0:
            return series.PitchSegment([new_pitch_set, self.duration_set[:]],
                                       new_tree=self, parent=self, name="Retrograde without rhyme")
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in new_pitch_set]
        return series.PitchSegment([new_pitch_set, self.duration_set[:]],
                                   new_tree=self, parent=self, name=f"Retrograde{add_pitch}")

    @once_per_arg
    def Inversion(self, axes: int) -> PitchSegment:
        """
        This function creates an Inversion transformation of self without changing the rhythm.
        :param axes: An int to invert each pitch in the set.
        :return: Inverted new PitchSegment object.
        """
        new_pitch_set = [2 * axes - pitch for pitch in self.pitch_set]
        return series.PitchSegment([new_pitch_set, self.duration_set[:]],
                                   new_tree=self, parent=self, name=f"Inversion{axes}")

    @once_per_arg
    def RetrogradeInversion(self, axes: int) -> PitchSegment:
        """
        This function creates a Retrograde then Inversion transformation of self with changed rhythm.
        :param axes: An int to invert each pitch in the set.
        :return: Retrograde then Inversion new PitchSegment object.
        """
        new_pitch_set = reversed([2 * axes - pitch for pitch in self.pitch_set])
        new_duration_set = reversed(self.duration_set)
        return series.PitchSegment([new_pitch_set, new_duration_set],
                                   new_tree=self, parent=self, name=f"RetrogradeInversion{axes} (with rhyme)")

    @once_per_arg
    def Rotation_without_rhyme(self, num: int, add_pitch: int = 0) -> PitchSegment:
        """
        This function creates a Rotation transformation of self without changing the rhythm.
        :param num: Rotation num
        :param add_pitch: Transposition num.
        :return: Roted new PitchSegment object.
        """
        if not 0 <= num < self.length:
            raise ValueError("The attribute 'num' should be smaller than length of the series.")
        new_pitch_set = [self.pitch_set[(ii + num) % self.length] for ii in range(self.length)]
        if add_pitch == 0:
            return series.PitchSegment([new_pitch_set[:], self.duration_set[:]],
                                       new_tree=self, parent=self, name=f"Rotation{num} (without rhyme)")
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in new_pitch_set]
        return series.PitchSegment([new_pitch_set[:], self.duration_set[:]],
                                   new_tree=self, parent=self, name=f"Rotation{num} (without rhyme),T{add_pitch}")

    @once_per_arg
    def Rotation_with_rhyme(self, num: int, add_pitch: int = 0) -> PitchSegment:
        """
        This function creates a Rotation transformation of self with changed rhythm.
        :param num: Rotation num
        :param add_pitch: Transposition num.
        :return: Retrograded new PitchSegment object.
        """
        if not 0 <= num < self.length:
            raise ValueError("The attribute 'num' should be smaller than length of the series.")
        new_pitch_set = [self.pitch_set[(ii + num) % self.length] for ii in range(self.length)]
        new_duration_set = [self.duration_set[(ii + num) % self.length] for ii in range(self.length)]
        if add_pitch == 0:
            return series.PitchSegment([new_pitch_set[:], new_duration_set[:]],
                                       new_tree=self, parent=self, name=f"Rotation{num} (with rhyme)")
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in new_pitch_set]
        return series.PitchSegment([new_pitch_set[:], new_duration_set[:]],
                                   new_tree=self, parent=self, name=f"Rotation{num} (with rhyme),T{add_pitch}")

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


class PitchClassSegment(PitchSegment):
    def __init__(self, segment, __style=None):
        """ Variable 'series' should be a list of two lists.   """
        super().__init__(segment, __style=None)
        self.pitch_class_set = self.pitch_set
        self.pitch_tend = None
        self.rhythm_intensity_tend = None

    def __hash__(self):
        return hash(self.segment)

    def __eq__(self, other):
        return self.segment == other.segment

    def __iter__(self):
        return iter(zip(self.pitch_class_set, self.duration_set))

    def __add__(self, add_pitch):
        new_pitch_class_set = [new_pitch + int(add_pitch) for new_pitch in self.pitch_class_set]
        return PitchClassSegment([new_pitch_class_set, self.duration_set][:]), self, f"Transposition{add_pitch}"

    def __sub__(self, sub_pitch):
        new_pitch_class_set = [new_pitch - int(sub_pitch) for new_pitch in self.pitch_class_set]
        return PitchClassSegment([new_pitch_class_set, self.duration_set][:]), self, f"Transposition{12 - sub_pitch}"

    def __mod__(self, number):
        raise RuntimeError("")

    def __getitem__(self, item):
        return self.pitch_class_set[int(item)], self.duration_set[int(item)]

    def __setitem__(self, key, value):
        """
        Variable *keys includes two element.
        Variable "values" is two-element list.
        """
        new_pc_set = self.pitch_set
        new_pc_set[key] = value
        return PitchClassSegment(
            [new_pc_set, self.duration_set[:]]), self, f"Reset pitch set[{key}]{note_value[value]}"

    @once_per_arg
    def __reversed__(self):
        new_pc_set = reversed(self.pitch_set)[:]
        new_duration_set = reversed(self.duration_set)[:]
        return PitchClassSegment([new_pc_set, new_duration_set]), self, "Retrograde (with rhyme)"

    @once_per_arg
    def new_segment(self, note_num, total_duration, first_note, note_scale, style):
        """ To generate a new series while original series is empty.  """
        if self.segment:
            raise RuntimeError("The function 'new_segment' is only used for empty pitch series.")
        _segment = basicGenerator.randomSegment(note_num, total_duration, first_note, note_scale, style)
        self.__init__(_segment, __style=style)

    @once_per_arg
    def change_rhyme(self, total_duration, new_style):
        """ To overwrite a new rhyme to the pitch set.   """
        self.style = new_style
        _segment = [self.pitch_set, basicGenerator.randomRhythm(self.length, total_duration, new_style)]
        return PitchClassSegment(_segment), self, "Different rhyme"

    def get_average(self):
        return self.w_average

    def get_pitch_tend(self):
        return self.pitch_tend

    def get_rhythm_intensity_tend(self):
        return self.rhythm_intensity_tend

    @once_per_arg
    def Transposition(self, add_pitch):
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in self.pitch_set]
        return PitchClassSegment([new_pitch_set, self.duration_set][:]), self, f"Transposition{add_pitch}"

    @once_per_arg
    def Retrograde_with_rhyme(self, add_pitch=0):
        new_pitch_set = reversed(self.pitch_set)[:]
        new_duration_set = reversed(self.duration_set)[:]
        if add_pitch == 0:
            return PitchClassSegment([new_pitch_set, new_duration_set]), self, "Retrograde with rhyme"
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in new_pitch_set]
        return PitchClassSegment([new_pitch_set, new_duration_set]), self, f"Retrograde{add_pitch}"

    @once_per_arg
    def Retrograde_without_rhyme(self, add_pitch=0):
        new_pitch_set = reversed(self.pitch_set)[:]
        if add_pitch == 0:
            return PitchClassSegment([new_pitch_set, self.duration_set[:]]), self, "Retrograde without rhyme"
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in new_pitch_set]
        return PitchClassSegment([new_pitch_set, self.duration_set[:]]), self, "Retrograde" + str(add_pitch)

    @once_per_arg
    def Inversion(self, axes):
        new_pitch_set = [2 * int(axes) - pitch for pitch in self.pitch_set]
        return PitchClassSegment([new_pitch_set, self.duration_set[:]]), self, "Inversion" + str(axes)

    @once_per_arg
    def RetrogradeInversion(self, axes):
        new_pitch_set = reversed([2 * int(axes) - pitch for pitch in self.pitch_set])
        new_duration_set = reversed(self.duration_set)
        return PitchClassSegment([new_pitch_set, new_duration_set]), self, "Retrograde Inversion" + str(axes)

    @once_per_arg
    def Rotation_without_rhyme(self, num, add_pitch=0):
        if not 0 <= num < self.length:
            raise ValueError("The attribute 'num' should be smaller than length of the series.")
        new_pitch_set = [self.pitch_set[(ii + num) % self.length] for ii in range(self.length)]
        if add_pitch == 0:
            return PitchClassSegment([new_pitch_set[:], self.duration_set[:]]
                                     ), self, f"Rotation{num} (without rhyme)"
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in new_pitch_set]
        return PitchClassSegment([new_pitch_set[:], self.duration_set[:]]
                                 ), self, f"Rotation{num} (without rhyme),T{add_pitch}"

    @once_per_arg
    def Rotation_with_rhyme(self, num, add_pitch=0):
        if not 0 <= num < self.length:
            raise ValueError("The attribute 'num' should be smaller than length of the series.")
        new_pitch_set = [self.pitch_set[(ii + num) % self.length] for ii in range(self.length)]
        new_duration_set = [self.duration_set[(ii + num) % self.length] for ii in range(self.length)]
        if add_pitch == 0:
            return PitchClassSegment(
                [new_pitch_set[:], new_duration_set[:]]), self, f"Rotation{num} (with rhyme)"
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in new_pitch_set]
        return PitchClassSegment(
            [new_pitch_set[:], new_duration_set[:]]), self, f"Rotation{num} (with rhyme),T{add_pitch}"


# TODO: 轮廓截段
class ContourSegment:
    def __init__(self, segment):
        self.pitch_set = segment[0]
