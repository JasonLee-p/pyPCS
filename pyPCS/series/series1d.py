from __future__ import annotations
from typing import List
import numpy as _np

import pyPCS.series.series2d as s2  # 避免循环调用错误，不使用from语法
from ..chorder import c_span, c_k_colour, semitone_num, root_note_PH
from .funcs import chord_type, to_pc_group, pc_to_circle_of_fifth_ns
from .tree import SeriesTree, RhymeTree
from .._basicData import note_value


class PitchSeries:
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

    def __init__(self, series: List[int], new_tree=True, name=False, parent=None, __style=None):
        """
        The first element of variable 'rhyme' is a pitch list while the second element is a duration list.
        You are not supposed to use attributes start with "__" !
        :param series: Segment.
        :param new_tree: If you want to set a new tree of segments and set this one as the parent, set it as True
        """

        # 判断输入值是否合法
        judging = [True
                   if (type(int(ii)) is not int) else 0
                   for ii in series]
        if True in judging:
            raise ValueError("Invalid note format.")

        if new_tree is True and name is True:
            raise ValueError("You shouldn't change '__name' default value.")
        elif new_tree is False and name is False:
            raise ValueError("You haven't set '__name', which is necessary when 'new_tree' is False.")
        elif new_tree is True:
            self.parent = None
            self.name = input("Enter the name of the series tree:\n")
            self.tree = SeriesTree(self)
        elif type(name) is str:  # 这时传入的tree_name应当是转换方法，也就是每一次变换之后返回的第三个值。
            self.parent = parent
            self.name = f'{self.parent.name}: {name}'
            self.tree = SeriesTree.check_tree(parent)
            self.tree.append_(parent, self)
        else:
            raise ValueError("Invalid tree_name")

        self.style = __style
        self.series = series  # 音高
        self.length = len(series)  # 获取音高列表的长度
        self.average = _np.mean(series)  # 计算平均音高
        segment_result = tendentiousness([[series], ['1'] * self.length])  # 音高和密度的趋向性
        self.pitch_tend = segment_result[0]  # 音高趋向性

    def __hash__(self):
        return hash(self.series)

    def __eq__(self, other):
        return self.series == other.compared_segment

    def __len__(self):
        return len(self.series)

    def __iter__(self):
        return self.series

    def __add__(self, add_pitch: int):
        new_series = [new_pitch + add_pitch for new_pitch in self.series]
        return PitchSeries(new_series,
                           new_tree=False, parent=self, name=f"Transposition{add_pitch}")

    def __sub__(self, sub_pitch: int):
        new_series = [new_pitch - sub_pitch for new_pitch in self.series]
        return PitchSeries(new_series,
                           new_tree=False, parent=self, name=f"Transposition{12 - sub_pitch}")

    def __mod__(self, number: int):
        pass

    def __getitem__(self, item):
        return self.series[int(item)]

    def __setitem__(self, key, value):
        """
        Variable *keys includes two element.
        Variable "values" is two-element list.
        """
        new_pitch_set = self.series
        new_pitch_set[key] = value
        return PitchSeries(new_pitch_set,
                           new_tree=self, parent=self, name=f"Reset pitch[{key}]{note_value[value]}")

    def __reversed__(self):
        new_series = reversed(self.series)
        return PitchSeries(list(new_series)[:],
                           new_tree=self, parent=self, name="Retrograde (with rhyme)")

    # def get_pc_segment(self) -> Tuple[PitchClassSegment, PitchSegment, str]:
    #     pitch_class_set = to_pc_group(self.series[:], ordered=True)
    #     return PitchClassSegment([pitch_class_set], self.rhyme[:]), self, "Pitch class series"

    def get_average(self) -> float:
        return self.average

    def get_pitch_tend(self) -> float:
        return self.pitch_tend

    def Transposition(self, add_pitch: int) -> PitchSeries:
        """
        This function creates a Transposition transformation of self.
        :param add_pitch: Transposition num.
        :return:
        Transposed pitch_segment,
        Original pitch_segment,
        A string indicating that a Transposition has been made.
        """
        new_series = [new_pitch + int(add_pitch) for new_pitch in self.series]
        return PitchSeries(new_series,
                           new_tree=self, parent=self, name=f"Transposition{add_pitch}")

    def Retrograde(self, add_pitch: int = 0) -> PitchSeries:
        """
        This function creates a Retrograde transformation of self without changing the rhythm.
        :param add_pitch: Transposition num.
        :return: Retrograded pitch_segment, Original pitch_segment, A string indicating that a Retrograde has been made.
        """
        new_series = list(reversed(self.series))[:]
        if add_pitch == 0:
            return s2.PitchSegment(new_series,
                                   new_tree=self, parent=self, name="Retrograde without rhyme")
        new_series = [new_pitch + int(add_pitch) for new_pitch in new_series]
        return s2.PitchSegment(new_series,
                               new_tree=self, parent=self, name=f"Retrograde{add_pitch}")

    def Inversion(self, axes: int) -> PitchSeries:
        """
        This function creates an Inversion transformation of self without changing the rhythm.
        :param axes: An int to invert each pitch in the set.
        :return: Inverted pitch_segment, Original pitch_segment, A string indicating that an Inversion has been made.
        """
        new_series = [2 * axes - pitch for pitch in self.series]
        return PitchSeries(new_series,
                           new_tree=self, parent=self, name=f"Inversion{axes}")

    def RetrogradeInversion(self, axes: int) -> PitchSeries:
        """
        This function creates a Retrograde then Inversion transformation of self with changed rhythm.
        :param axes: An int to invert each pitch in the set.
        :return: Retrograde then Inversion pitch_segment, Original pitch_segment,
        A string indicating that a RetrogradeInversion has been made.
        """
        new_series = reversed([2 * axes - pitch for pitch in self.series])
        return PitchSeries(new_series,
                           new_tree=self, parent=self, name=f"RetrogradeInversion{axes} (with rhyme)")

    def Rotation(self, num: int, add_pitch: int = 0) -> PitchSeries:
        """
        This function creates a Rotation transformation of self without changing the rhythm.
        :param num: Rotation num
        :param add_pitch: Transposition num.
        :return: Retrograded pitch_segment, Original pitch_segment, A string indicating that a Rotation has been made.
        """
        if not 0 <= num < self.length:
            raise ValueError("The attribute 'num' should be smaller than length of the series.")
        new_series = [self.series[(ii + num) % self.length] for ii in range(self.length)]
        if add_pitch == 0:
            return PitchSeries(new_series[:],
                               new_tree=self, parent=self, name=f"Rotation{num}")
        new_series = [new_pitch + int(add_pitch) for new_pitch in new_series]
        return PitchSeries(new_series[:],
                           new_tree=self, parent=self, name=f"Rotation{num},T{add_pitch}")

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
        play_pitch_segment(pg_player, [self, ['1'] * self.length], instrument=instrument, bpm=bpm)
        del play_pitch_segment


class Rhyme:
    def __init__(self, rhyme: List[str], new_tree=True, name=False, parent=None, __style=None):
        """
        The first element of variable 'series' is a pitch list while the second element is a duration list.
        You are not supposed to use attributes start with "__" !
        :param rhyme: Segment.
        :param new_tree: If you want to set a new tree of segments and set this one as the parent, set it as True
        """

        # 判断输入值是否合法
        judging = [True
                   if (type(ii) is not str and ('/' not in ii, len(ii) != 1)) else 0
                   for ii in rhyme]
        if True in judging:
            raise ValueError("Invalid duration format.")

        if new_tree is True and name is True:
            raise ValueError("You shouldn't change '__name' default value.")
        elif new_tree is False and name is False:
            raise ValueError("You haven't set '__name', which is necessary when 'new_tree' is False.")
        elif new_tree is True:
            self.parent = None
            self.name = input("Enter the name of the series tree:\n")
            self.tree = RhymeTree(self)
        elif type(name) is str:  # 这时传入的tree_name应当是转换方法，也就是每一次变换之后返回的第三个值。
            self.parent = parent
            self.name = f'{self.parent.name}: {name}'
            self.tree = RhymeTree.check_tree(parent)
            self.tree.append_(parent, self)
        else:
            raise ValueError("Invalid tree_name")

        self.style = __style
        self.rhyme = rhyme  # 时值
        self.length = len(rhyme)  # 获取音高列表的长度
        self.total_duration = _np.sum([float(eval(d)) for d in rhyme])  # 获取总时值
        segment_result = tendentiousness([[60] * self.length, rhyme])  # 音高和密度的趋向性
        self.rhythm_intensity_tend = segment_result[1]  # 密度趋向性

    def __hash__(self):
        return hash(self.rhyme)

    def __eq__(self, other):
        if type(other) is Rhyme:
            return self.rhyme == other.rhyme
        if type(other) is list[str]:
            return self.rhyme == other

    def __len__(self):
        return len(self.rhyme)

    def __iter__(self):
        return self.rhyme

    def __add__(self, add_beat: int):
        pass

    def __sub__(self, sub_beat: int):
        pass

    def __mod__(self, number: int):
        pass

    def __getitem__(self, item):
        return self.rhyme[int(item)]

    def __setitem__(self, key, value):
        """
        Variable *keys includes two element.
        Variable "values" is two-element list.
        """
        new_rhyme = self.rhyme
        new_rhyme[key] = value
        return Rhyme(new_rhyme,
                     new_tree=True, parent=self, name=f"Reset rhyme[{key}]{note_value[value]}")

    def __reversed__(self):
        new_duration_set = reversed(self.rhyme)
        return Rhyme(list(new_duration_set)[:],
                     new_tree=self, parent=self, name="Retrograde (with rhyme)")

    def get_rhythm_intensity_tend(self) -> float:
        return self.rhythm_intensity_tend

    def Retrograde(self) -> Rhyme:
        """
        This function creates a Retrograde transformation of self with changed rhythm.
        :return: Retrograded pitch_segment, Original pitch_segment, A string indicating that a Retrograde has been made.
        """
        new_rhyme = list(reversed(self.rhyme))[:]
        return Rhyme(new_rhyme,
                     new_tree=self, parent=self, name=f"Retrograde")

    def Rotation(self, num: int) -> Rhyme:
        """
        This function creates a Rotation transformation of self with changed rhythm.
        :param num: Rotation num
        :return: Retrograded pitch_segment, Original pitch_segment, A string indicating that a Rotation has been made.
        """
        if not 0 <= num < self.length:
            raise ValueError("The attribute 'num' should be smaller than length of the series.")
        new_duration_set = [self.rhyme[(ii + num) % self.length] for ii in range(self.length)]
        return s2.PitchSegment(new_duration_set[:],
                               new_tree=self, parent=self, name=f"Rotation{num}")

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
        play_pitch_segment(pg_player, [[69] * self.length, self.rhyme], instrument=instrument, bpm=bpm)
        del play_pitch_segment


class Chord:
    def __init__(self, pitch_group):
        self.pitch_group = pitch_group
        self.chord_type = chord_type(pitch_group)
        self.pitch_class_group = to_pc_group(pitch_group)
        self.span = c_span(to_pc_group(pitch_group))
        self.k_colour = c_k_colour(to_pc_group(pitch_group))
        self.semitone_num = semitone_num(to_pc_group(pitch_group))
        self.root_note = root_note_PH(pitch_group)

    def pitch_group(self):
        return self.pitch_group

    def get_chord_type(self):
        return self.chord_type

    def get_pc_group(self):
        return PitchClassSeries(self.pitch_class_group)[:], self, "Pitch set group"

    def __sub__(self, other):
        return _np.mean(self.pitch_group) - _np.mean(other.pitch_group)

    def __gt__(self, other):
        if _np.mean(self.pitch_group) > _np.mean(other.pitch_group):
            return True

    def __lt__(self, other):
        if _np.mean(self.pitch_group) < _np.mean(other.pitch_group):
            return True

    def __eq__(self, other):
        if _np.mean(self.pitch_group) == _np.mean(other.pitch_group):
            return self == other


# 音级集合
class PitchClassSeries:
    # TODO: unfinished
    def __init__(self, pitch_class_set):
        # 为了防止每调用一次都计算函数，先把结果存进变量
        cns = pc_to_circle_of_fifth_ns(pitch_class_set)
        dcns = pc_to_circle_of_fifth_ns(pitch_class_set)[1]
        self.pitch_class_set = pitch_class_set  # unordered
        self.pitch_class_group = sorted(list(set(pitch_class_set)))  # sorted, without repeating.
        self.cof_note_set = cns
        self.default_cof_note_set = dcns

    def __add__(self, cal_set):
        """
        :param cal_set: The set that you want to add to note set. It has to be as long as the note set.
        """
        result = []
        if len(self.pitch_class_set) != len(cal_set):
            raise RuntimeError("The cal_set'pypcs length should be equal to note set'pypcs length.")
        else:
            for ns in range(len(cal_set)):
                result.append((self.pitch_class_set[ns] + cal_set[ns]) % 12)
            return result

    # 比较向位集，向位集的元素数量必须相等
    def compare_cal_set(self, c_set1, c_set2):
        result1 = []
        result2 = []
        if len(c_set1) == len(c_set2):
            for ns in range(len(c_set1)):
                result1.append((self.pitch_class_set[ns] + c_set1[ns]) % 12)
            for ns in range(len(c_set2)):
                result2.append((self.pitch_class_set[ns] + c_set2[ns]) % 12)
            if result1 == result2:
                return True
        else:
            raise RuntimeError("The compared two c_sets' length should be the same.")
