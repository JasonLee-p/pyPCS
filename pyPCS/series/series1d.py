from __future__ import annotations
from typing import List
import numpy as _np

import pyPCS.series.series2d as s2  # 避免循环调用错误，不使用from语法
from .._player import play_chord
from ..chorder import c_span, chord_colour_k, semitone_num, root_note_PH
from .funcs import chord_type, to_pc_set, pc_to_circle_of_fifth_ns, tendentiousness, chord_dissonance,\
    chord_colour_hua, chord_consonance_tian
from .tree import SeriesTree, RhythmTree, PitchClassSeriesTree
from .._basicData import note_value
# from ..classmethod_dec import once_per_arg


class PitchSeries:
    """
        Any function that change the series list return a new object_ of a class (may not be PitchSegment):

        Pitch series contains a pitch set, various attributes and transformations are included in the class:
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
        The first element of variable 'pitch_class_series' is a pitch list while the second element is a duration list.
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

        self.series = series  # 音高

        if new_tree is True and name is True:
            raise ValueError("You shouldn't change '__name' default value.")
        elif new_tree is False and name is False:
            raise ValueError("You haven't set '__name', which is necessary when 'new_tree' is False.")
        if new_tree:
            self.parent = None
            self.name = input(f"Enter the name of the PitchSeries{self.series} tree:\n")
            self.tree = SeriesTree(self)
        elif type(name) is str:  # 这时传入的tree_name应当是转换方法，也就是每一次变换之后返回的第三个值。
            self.parent = parent
            self.name = f'{self.parent.name}: {name}'
            self.tree = parent.tree
            self.tree.append_(self.parent, self)
        else:
            raise ValueError("Invalid tree_name")

        self.style = __style
        self.length = len(series)  # 获取音高列表的长度
        self.average = _np.mean(series)  # 计算平均音高
        segment_result = tendentiousness([series, ['1'] * self.length])  # 音高和密度的趋向性
        self.pitch_tend = segment_result[0]  # 音高趋向性

    def show(self):
        print(self.series)

    def Transposition(self, add_pitch: int) -> PitchSeries:
        """
        This function creates a new obj.

        :param add_pitch: Transposition num.
        :return: Transposed new PitchSeries obj.
        """
        new_series = [new_pitch + int(add_pitch) for new_pitch in self.series]
        return PitchSeries(new_series,
                           new_tree=False, parent=self, name=f"Transposition{add_pitch}")

    def Retrograde(self, add_pitch: int = 0) -> PitchSeries:
        """
        This function creates a new obj.

        :param add_pitch: Transposition num.
        :return: Retrograded new PitchSeries obj.
        """
        new_series = reversed(self.series)
        if add_pitch == 0:
            return s2.PitchSegment(new_series,
                                   new_tree=False, parent=self, name="Retrograde")
        new_series = [new_pitch + int(add_pitch) for new_pitch in new_series]
        return s2.PitchSegment(new_series,
                               new_tree=False, parent=self, name=f"Retrograde{add_pitch}")

    def Inversion(self, axes: int) -> PitchSeries:
        """
        This function creates a new obj.

        :param axes: An int to invert each pitch in the set.
        :return: Inverted new PitchSeries obj.
        """
        new_series = [2 * axes - pitch for pitch in self.series]
        return PitchSeries(new_series,
                           new_tree=False, parent=self, name=f"Inversion{axes}")

    def RetrogradeInversion(self, axes: int) -> PitchSeries:
        """
        This function creates a new obj.

        :param axes: An int to invert each pitch in the set.
        :return: Retrograde new PitchSeries obj.
        """
        new_series = reversed([2 * axes - pitch for pitch in self.series])
        return PitchSeries(new_series,
                           new_tree=False, parent=self, name=f"RetrogradeInversion{axes}")

    def Rotation(self, num: int, add_pitch: int = 0) -> PitchSeries:
        """
        This function creates a new obj.

        :param num: Rotation num
        :param add_pitch: Transposition num.
        :return: Retrograded new PitchSeries obj.
        """
        if not 0 <= num < self.length:
            raise ValueError("The attribute 'num' should be smaller than length of the series.")
        new_series = [self.series[(ii + num) % self.length] for ii in range(self.length)]
        if add_pitch == 0:
            return PitchSeries(new_series[:],
                               new_tree=False, parent=self, name=f"Rotation{num}")
        new_series = [new_pitch + int(add_pitch) for new_pitch in new_series]
        return PitchSeries(new_series[:],
                           new_tree=False, parent=self, name=f"Rotation{num},T{add_pitch}")

    def play(self, pg_player=None, bpm=80, instrument='piano'):
        """
        :param pg_player: Pygame.midi.Output(int). If you haven't set it, keep it None.
            eg:
            player = pygame.midi.output(0)
            ps.play(pg_player=player)
        :param bpm: Beats per minutes.
        :param instrument: instrument.
        """
        from .._player import play_pitch_segment
        play_pitch_segment(pg_player, [self, ['1'] * self.length], instrument=instrument, bpm=bpm)
        del play_pitch_segment

    def __hash__(self):
        return hash(self.series)

    def __eq__(self, other):
        return self.series == other.compared_segment

    def __len__(self):
        return len(self.series)

    def __iter__(self):
        return self.series

    def __add__(self, add_pitch: int):
        new_series = [(new_pitch + add_pitch) % 12 for new_pitch in self.series]
        return PitchSeries(new_series,
                           new_tree=False, parent=self, name=f"Transposition{add_pitch}")

    def __sub__(self, sub_pitch: int):
        new_series = [(new_pitch - sub_pitch) % 12 for new_pitch in self.series]
        return PitchSeries(new_series,
                           new_tree=False, parent=self, name=f"Transposition{12 - sub_pitch}")

    def __mod__(self, number: int):
        pass

    def __getitem__(self, item):
        return self.series[int(item)]

    def __setitem__(self, key, value):
        new_pitch_set = self.series
        new_pitch_set[key] = value
        return PitchSeries(new_pitch_set,
                           new_tree=False, parent=self, name=f"Reset pitch[{key}]{note_value[value]}")

    def __reversed__(self):
        new_series = reversed(self.series)
        return PitchSeries(list(new_series)[:],
                           new_tree=False, parent=self, name="Retrograde")


class Rhythm:
    def __init__(self, rhythm: List[str], new_tree=True, name=False, parent=None, __style=None):
        """
        :param rhythm: beat list.
        :param new_tree: If you want to set a new tree of segments and set this one as the parent, set it as True
        """

        # 判断输入值是否合法
        judging = [True
                   if (type(ii) is not str and ('/' not in ii, len(ii) != 1)) else 0
                   for ii in rhythm]
        if True in judging:
            raise ValueError("Invalid duration format.")

        self.rhythm = rhythm  # 时值

        if new_tree is True and name is True:
            raise ValueError("You shouldn't change '__name' default value.")
        elif new_tree is False and name is False:
            raise ValueError("You haven't set '__name', which is necessary when 'new_tree' is False.")
        elif new_tree is True:
            self.parent = None
            self.name = input(f"Enter the name of the Rhythm{self.rhythm} tree:\n")
            self.tree = RhythmTree(self)
        elif type(name) is str:  # 这时传入的tree_name应当是转换方法，也就是每一次变换之后返回的第三个值。
            self.parent = parent
            self.name = f'{self.parent.name}: {name}'
            self.tree = parent.tree
            self.tree.append_(parent, self)
        else:
            raise ValueError("Invalid tree_name")

        self.style = __style
        self.length = len(rhythm)  # 获取音高列表的长度
        self.total_duration = _np.sum([float(eval(d)) for d in rhythm])  # 获取总时值
        segment_result = tendentiousness([[60] * self.length, rhythm])  # 音高和密度的趋向性
        self.rhythm_intensity_tend = segment_result[1]  # 密度趋向性

    def show(self):
        print(self.rhythm)

    def Retrograde(self) -> Rhythm:
        """
        This function creates a new obj.

        :return: New retrograded Rhythm obj.
        """
        new_rhyme = list(reversed(self.rhythm))[:]
        return Rhythm(new_rhyme,
                      new_tree=False, parent=self, name=f"Retrograde")

    def Rotation(self, num: int) -> Rhythm:
        """
        This function creates a new obj.

        :param num: Rotation num
        :return: New rotated Rhythm obj.
        """
        if not 0 <= num < self.length:
            raise ValueError("The attribute 'num' should be smaller than length of the series.")
        new_duration_set = [self.rhythm[(ii + num) % self.length] for ii in range(self.length)]
        return s2.PitchSegment(new_duration_set[:],
                               new_tree=False, parent=self, name=f"Rotation{num}")

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
        play_pitch_segment(pg_player, [[69] * self.length, self.rhythm], instrument=instrument, bpm=bpm)
        del play_pitch_segment

    def __hash__(self):
        return hash(self.rhythm)

    def __eq__(self, other):
        if type(other) is Rhythm:
            return self.rhythm == other.rhythm
        if type(other) is list[str]:
            return self.rhythm == other

    def __len__(self):
        return len(self.rhythm)

    def __iter__(self):
        return self.rhythm

    def __mod__(self, number: int):
        pass

    def __getitem__(self, item):
        return self.rhythm[int(item)]

    def __setitem__(self, key, value):
        """
        """
        new_rhyme = self.rhythm
        new_rhyme[key] = value
        return Rhythm(new_rhyme,
                      new_tree=True, parent=self, name=f"Reset pitch_class_series[{key}]{note_value[value]}")

    def __reversed__(self):
        new_duration_set = reversed(self.rhythm)
        return Rhythm(list(new_duration_set)[:],
                      new_tree=False, parent=self, name="Retrograde")


class Chord:
    def __init__(self, pitch_group):
        pitch_group = sorted(pitch_group)
        self.length = len(pitch_group)  # 获取音高列表的长度
        self.pitch_group = pitch_group
        self.pitch_class_group = to_pc_set(pitch_group)  # 会剔除重复的对象
        self.type = chord_type(pitch_group)
        self.cof_span = c_span(to_pc_set(pitch_group))
        self.semitone_num = semitone_num(to_pc_set(pitch_group))
        self.root_note = root_note_PH(pitch_group)
        self.colour_k = chord_colour_k(to_pc_set(pitch_group))
        self.colour_hua = chord_colour_hua(pitch_group)
        self.consonance_tian = chord_consonance_tian(pitch_group, self.type)
        self.dissonance = chord_dissonance(pitch_group)
        self.colour_tian = self.consonance_tian, self.colour_hua
        # if self.type == "Unable to recognize":
        #     return
        # if _len := len(str(self.dissonance)) == 4:
        #     print(f"{self.type}:\ndissonance= {self.dissonance}, colour= {self.colour_hua}")
        # elif _len == 3:
        #     print(f"{self.type}:\ndissonance= {self.dissonance} , colour= {self.colour_hua}")
        # elif _len == 1:
        #     print(f"{self.type}:\ndissonance= {self.dissonance}   , colour= {self.colour_hua}")

    def get_pc_group(self):
        return PitchClassSeries(self.pitch_class_group)[:], self, "Pitch set group"

    def play(self, player):
        play_chord(player, self.pitch_group)

    def __len__(self):
        return len(self.pitch_group)

    def __sub__(self, other):
        return _np.mean(self.pitch_group) - _np.mean(other.pitch_group)

    def __gt__(self, other):
        if _np.mean(self.pitch_group) > _np.mean(other.pitch_group):
            return True

    def __lt__(self, other):
        if _np.mean(self.pitch_group) < _np.mean(other.pitch_group):
            return True

    def __iter__(self):
        return self.pitch_group

    def __hash__(self):
        return hash(self.pitch_group)

    def __eq__(self, other):
        if _np.mean(self.pitch_group) == _np.mean(other.pitch_group):
            return self == other


# 音级集合
class PitchClassSeries:
    def __init__(
            self, series: List[int],
            new_tree=True, name=False, parent=None):
        """
        :param series: Series.
        :param new_tree: If you want to set a new tree of segments and set this one as the parent, set it as True
        """

        if new_tree is True and name is True:
            raise ValueError("You shouldn't change '__name' default value.")
        elif new_tree is False and name is False:
            raise ValueError("You haven't set '__name', which is necessary when 'new_tree' is False.")
        elif new_tree is True:
            self.parent = None
            self.name = input("Enter the name of the PitchSegment tree:\n")
            self.tree = PitchClassSeriesTree(self)
        elif type(name) is str:  # 这时传入的tree_name应当是转换方法，也就是每一次变换之后返回的第三个值。
            self.parent = parent
            self.name = f'{self.parent.name}: {name}'
            self.tree = parent.tree
            self.tree.append_(parent, self)
        else:
            raise ValueError("Invalid tree_name")
        # TODO: 检查节奏和音集长度是否相等
        self.series = series
        self.length = len(self.series)  # 获取音高列表的长度

    def show(self):
        print(self.series)

    def Transposition(self, add_pitch: int) -> PitchClassSeries:
        """
        This function creates a new obj.

        :param add_pitch: Transposition num.
        :return: Transposed new PitchClassSeries obj.
        """
        new_series = [(new_pitch + add_pitch) % 12 for new_pitch in self.series]
        return PitchClassSeries(new_series,
                                new_tree=False, parent=self, name=f"Transposition{add_pitch}")

    def Retrograde(self, add_pitch: int = 0) -> PitchClassSeries:
        """
        This function creates a new obj.

        :param add_pitch: Transposition num.
        :return: Retrograded new PitchClassSeries obj.
        """
        new_series = reversed(self.series)
        if add_pitch == 0:
            return PitchClassSeries(new_series,
                                    new_tree=False, parent=self, name="Retrograde")
        new_series = [(new_pitch + int(add_pitch)) % 12 for new_pitch in new_series]
        return PitchClassSeries(new_series,
                                new_tree=False, parent=self, name=f"Retrograde{add_pitch}")

    def Inversion(self, add: int) -> PitchClassSeries:
        """
        This function creates a new obj.

        :param add: An int to invert each pitch in the set.
        :return: Inverted new PitchClassSeries obj.
        """
        new_series = [(12 - pitch if pitch else 0) for pitch in self.series]
        new_series = [(new_pitch + int(add)) % 12 for new_pitch in new_series]
        return PitchClassSeries(new_series,
                                new_tree=False, parent=self, name=f"T{add}Inversion")

    def RetrogradeInversion(self, axes: int) -> PitchClassSeries:
        """
        This function creates a new obj.

        :param axes: An int to invert each pitch in the set.
        :return: Retrograde then Inversion new PitchClassSeries obj.
        """
        new_series = reversed([2 * axes - pitch for pitch in self.series])
        return PitchClassSeries(
            new_series, new_tree=False, parent=self, name=f"RetrogradeInversion{axes} (with pitch_class_series)")

    def Rotation(self, num: int) -> PitchClassSeries:
        """
        This function creates a new obj.

        :param num: Rotation num
        :return: Retrograded new PitchClassSeries obj.
        """
        if not 0 <= num < self.length:
            raise ValueError("The attribute 'num' should be smaller than length of the series.")
        new_series = [self.series[(ii + num) % self.length] for ii in range(self.length)]
        return PitchClassSeries(new_series[:],
                                new_tree=False, parent=self, name=f"Rotation{num}")

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
        return PitchClassSeries(new_series,
                                new_tree=False, parent=self, name=f"Transposition{add_pitch}")

    def __sub__(self, sub_pitch: int):
        new_series = [new_pitch - sub_pitch for new_pitch in self.series]
        return PitchClassSeries(new_series,
                                new_tree=False, parent=self, name=f"Transposition{12 - sub_pitch}")

    def __mod__(self, number: int):
        pass

    def __getitem__(self, item):
        return self.series[int(item)]

    def __setitem__(self, key, value):
        new_pitch_set = self.series
        new_pitch_set[key] = value
        return PitchClassSeries(new_pitch_set,
                                new_tree=False, parent=self, name=f"Reset pitch[{key}]{note_value[value]}")

    def __reversed__(self):
        new_series = reversed(self.series)
        return PitchClassSeries(list(new_series)[:],
                                new_tree=False, parent=self, name="Retrograde (with pitch_class_series)")
