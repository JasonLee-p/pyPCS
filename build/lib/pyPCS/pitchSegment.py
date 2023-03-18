"""
    This module defines functions in Pitches-class Set Theory.

    Attention:
        As mido module consider C4 as 60, in this module, we consider C4's pitch space as 60 instead of 0.
        If an attribute's end is "group", it means that it's order is not in consideration.
        If an attribute's end is "segment", it means that it's ordered and contains pitches' or pitch sets' duration.
"""
import numpy as np
from pyPCS import basicGenerator
from pyPCS._basicData import note_value, chords_chroma_vector, note_cof_value
from pyPCS.chorder import c_span, semitone_num, c_k_colour
from pyPCS.chorder import root_note_PH


# 音集（有序或无序）的键位音级集（若不含重复，即repeat = False，可算作无序；反之可算作有序）
def to_pc_group(pitch_group, ordered=False):
    cns = []
    if ordered is False:
        for pitch in pitch_group:
            pitch_set = pitch % 12
            if pitch_set in cns:
                continue
            else:
                cns.append(pitch_set)
        return cns
    else:
        result = list([pitch % 12 for pitch in pitch_group])
        return result


# 通过色度向量计算出和弦类型
def chord_type(pitch_group):
    pc_group = to_pc_group(pitch_group)
    self_template = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for _i in pc_group:
        self_template[_i] = 1
    for template in chords_chroma_vector.values():
        if template == self_template:
            # 在此可以添加特殊情况
            # if:
            #     return
            return list(chords_chroma_vector.keys())[list(chords_chroma_vector.values()).index(self_template)]
    return "Unable to recognize"


# 通过和弦名给出根音
def _get_root_note(chord_name):
    _l = ["C", "D", "E", "F", "G", "A", "B"]
    if chord_name == "Unable to recognize":
        return None
    if chord_name[0] == "b":
        if chord_name[1] == "A":
            return "#G"
        if chord_name[1] == "B":
            return "#A"
        if chord_name[1] == "D":
            return "#C"
        if chord_name[1] == "E":
            return "#D"
        if chord_name[1] == "G":
            return "#F"
    elif chord_name[0] == "#":
        return chord_name[0] + chord_name[1]
    elif chord_name[0] in ["C", "D", "E", "F", "G", "A", "B"]:
        return chord_name[0]


# 音集（有序或无序）的五度圈音级集（有序）
def circle_of_fifth_n_s(pitch_group):
    c_o_f_n_s = []
    cofns12 = []
    cofns_12 = []
    for n in pitch_group:
        cof_value = note_cof_value[n % 12]
        c_o_f_n_s.append(cof_value)
        cofns12.append(cof_value + 12)
        cofns_12.append(cof_value - 12)
    return [c_o_f_n_s, cofns12, cofns_12]


# 键位音级集的五度圈音级集
def pc_to_circle_of_fifth_ns(pitch_class_set):
    _ = [note_cof_value[pc_set] for pc_set in pitch_class_set]
    return _, [_i + 12 for _i in _], [_i - 12 for _i in _]


# 音集截段的加权平均音高
def pitches_weighed_average(pitch_segment):
    # 从segment获取音符集合
    pitches = pitch_segment[0]
    # 从segment获取时值集合
    duration_list = [eval(d) for d in pitch_segment[1]]
    result_list = []
    for _i in range(len(pitches)):
        result_list.append(pitches[_i] * float(duration_list[_i]) / sum(duration_list))
    return sum(result_list)


# 音集（有序无时值）的轮廓截段
def pitches_counter(pitch_series):
    pitch_set = pitch_series[0]
    result = []
    for pitch in pitch_set:
        cal = 0
        for compared_pitch in pitch_set:
            if pitch > compared_pitch:
                cal += 1
        result.append(cal)
    return result


# 音集截段的倾向性（音高，音符密集度）
def tendentiousness(pitch_segment):
    """
    When you use this function, the segment shouldn't be too short. If too short, it's pitch tend might be meaningless.

    :param pitch_segment: A list with two lists: note group(type = int) and its duration(beat, type = float)
    :return: Pitch Tendentiousness and Rhythm Intensity Tendentiousness (type = list).
    """
    # 确保传入的参数是含两个相同长度列表的列表，并且长度大于等于3，否则报错
    if len(pitch_segment[0]) != len(pitch_segment[1]):
        raise RuntimeError("Segment's two lists' length should be the same.")
    if len(pitch_segment[0]) < 3:
        raise RuntimeError("The segment should contain at least 3 notes")
    # 从segment获取音符集合
    pitches = pitch_segment[0]
    # 从segment获取时值集合
    duration_list = pitch_segment[1]
    _duration_list = [eval(d) for d in duration_list]
    # 通过时值把segment分成最平均的两半：
    # 先获取分割线split：
    group1 = [_duration_list[0]]
    group2 = [_duration_list[-1]]
    flag_dict = {}
    for _i in range(1, len(_duration_list)):
        for i1 in range(0, _i + 1):
            group1.append(_duration_list[i1])
        for i2 in range(_i + 1, len(_duration_list)):
            group2.append(_duration_list[i2])
        flag_dict[_i] = abs(np.sum(_duration_list) - np.sum(_duration_list))
    # 暂时先把最小差值赋给split
    split = min(flag_dict.values())
    # 遍历键，若值等于最小值就返回键
    for n in flag_dict.keys():
        if list(flag_dict.values())[n - 1] == split:
            # 给split正式赋值为分割点
            split = n
            break
    """     Pitch Tendentiousness
            获取完了分割线之后，开始计算分割线前后的音符平均值   """
    pitches1 = []
    pitches2 = []
    durations1 = []
    durations2 = []
    for _i in range(split):
        pitches1.append(pitches[_i])
        durations1.append(duration_list[_i])
    for _i in range(split, len(pitches)):
        pitches2.append(pitches[_i])
        durations2.append(duration_list[_i])
    wa1 = pitches_weighed_average([pitches1, durations1])
    wa2 = pitches_weighed_average([pitches2, durations2])
    # 取加权平均值的差，得到结果
    result = [wa2 - wa1]
    """     Rhythm Intensity Tendentiousness:
            开始计算密集度倾向值：                         """
    t1 = []
    t2 = []
    for _i in range(split):
        t1.append(_duration_list[_i])
    for _i in range(split, len(_duration_list)):
        t2.append(_duration_list[_i])
    # 取平均值倒数的差，即每拍的音符数量之差，得到结果
    result.append(1 / np.mean(t2) - 1 / np.mean(t1))
    return result



def get_intensity(pitch_segment):
    return


# TODO: Unfinished 截段的分割（position只属于后面一段）
def cut(pitch_segment, position):
    if len(pitch_segment[0]) < 4:
        raise RuntimeError("The minimum of pitch_segment's length is 4.")
    if int(position) >= len(pitch_segment[0]) - 2 or position < 2:
        raise RuntimeError(
            "The 'position' attribute should cut the pitch_segment into two parts that contains at least two notes.")
    return


def get_segments_subsegment(ps, start_time, finish_time=None):
    """
    :param ps: Pitch segment
    :param start_time:Start time
    :param finish_time:Finish time
    :return: If start time is equal to finish time or finish time is None, it returns a pitch's value(int),
    else, it returns a new pitch segment(list with two lists inside).
    """
    total_duration = sum([float(ii) for ii in ps[1]])
    if finish_time < start_time:
        raise ValueError("Finish time should be larger than start time.")
    if float(start_time) == total_duration:
        raise ValueError("Start time should be smaller than total duration.")
    if finish_time > total_duration:
        # print(sum([float(i) for i in ps[1]]))
        raise ValueError("Finish time should be smaller than the total duration of the pitch segment.")
    duration_set = ps[1]
    result_ps = [[], []]
    start_index = 0
    finish_index = 0
    first_d = 0
    last_d = 0
    t = 0
    start_cal = True
    for ii in range(len(duration_set)):
        t += duration_set[ii]
        if t > finish_time:
            if start_time == finish_time or finish_time is None:
                return ps[0][ii]
            finish_index = ii
            last_d = t - finish_time
            break
        if t == finish_time:
            if start_time == finish_time or finish_time is None:
                return ps[0][ii + 1]
            finish_index = ii
            last_d = t - start_time
            break
        if t > start_time and start_cal:
            start_index = ii
            first_d = t - start_time
            start_cal = 0
    if not start_index:
        return [[ps[0][finish_index]], [str(last_d)]]
    for ii in range(start_index, finish_index + 1):
        result_ps[0].append(ps[0][ii])
        if ii == start_index:
            result_ps[1].append(str(first_d))
        elif ii == finish_index:
            result_ps[1].append((str(last_d)))
        else:
            result_ps[1].append(str(duration_set[ii]))
    return result_ps


""" Basic operation on Pitch-class Segment:
    音级截段的四种基本操作：                        """


# Transposition（移位）音级集（有序或无序均可）
def transport(pitch_class_group, num):
    result = []
    for pitch_set in pitch_class_group:
        return_set = (pitch_set + num) % 12
        result.append(return_set)
    return result


# Retrograde（逆行）音集截段（有序有时值）
def retrograde(pitch_class_segment, num):
    pitch_class_group = list(reversed(pitch_class_segment[0]))
    duration_group = list(reversed(pitch_class_segment[1]))
    new_pitch_class_group = []
    for pitch_class in pitch_class_group:
        new_pitch_class_group.append((pitch_class + num) % 12)
    return [new_pitch_class_group, duration_group]


# Inversion（倒影）音级集（有序或无序均可）,num是倒影后加的数字
def inversion(pitch_class_group, num):
    result_g = []
    for pitch_class in pitch_class_group:
        result = 12 - pitch_class + num
        result_g.append(result)
    return result_g


# Retrograde-Inversion（逆行倒影）音集截段（有序有时值）
def retrograde_inversion(pitch_class_segment, num):
    pitch_class_group = list(reversed(pitch_class_segment[0]))
    duration_group = list(reversed(pitch_class_segment[1]))
    new_pitch_class_group = []
    for pitch_class in pitch_class_group:
        new_pitch_class_group.append((12 - pitch_class + num) % 12)
    return [new_pitch_class_group, duration_group]


# 三种乘法
# TODO: Multiplication（乘法）音集截段（有序有时值）
def multiplication_seg(pitch_segment, num):
    result = []
    for pitch in pitch_segment:
        result.append(((pitch - 60) * num) + 60)
    return result


# Multiplication（乘法）音级集（有序或无序均可）
def multiplication_set(pitch_class_series, num):
    result = []
    for pitch_class in pitch_class_series:
        result.append((pitch_class * num) % 12)
    return result


# Multiplication（乘法）轮廓截段（有序无时值）
def multiplication_cou(pitches_cou, num):
    result = []
    for counter in pitches_cou:
        result.append((counter * num) % 12)
    return result


# Rotation（轮转）操作：
# Pitch-class cycles（轮转）音级集（有序无时值）
def pitch_class_cycles(pitch_class_series, num=0):
    num_of_pitch_class = len(pitch_class_series)
    if not 0 <= num < num_of_pitch_class:
        raise RuntimeError("The attribute 'num' should be smaller than length of the series.")
    for _i in range(num):
        first = pitch_class_series[0]
        del pitch_class_series[0]
        pitch_class_series.append(first)
    return pitch_class_series


""" 函数写完后，开始创建类"""


# 有序的音集（截段）
class PitchSegment:
    """
    Except func 'new_segment', no attribute change the original segment of the class object!
    Any function that change the segment list return three variables:
        Newly generated PitchSegment object -------------------(class)
        Original PitchSegment object (this one) ---------------(class)
        Transformation type and argument ------------------------(str)

    Pitch segment contains a pitch set and a rhyme, various attributes and transformations are included in the class:
    Attributes:
        number of notes:
        duration:
        average pitch:
        tendentiousness:

    Transformations:
        transposition:
        retrograde:
        inversion:
        retrograde inversion:
        multiplication:
        rotation:
    """

    def __init__(self, segment, __style=None):
        """ Variable 'segment' should be a list of two lists.   """
        self.segment = segment
        if not segment:
            return
        self.style = __style
        # self.segment = segment
        self.pitch_set = segment[0]
        self.duration_set = segment[1]
        self.length = len(self.pitch_set)
        self.total_duration = np.sum([float(eval(d)) for d in self.duration_set])
        self.w_average = pitches_weighed_average(segment)
        segment_result = tendentiousness(segment)
        self.pitch_tend = segment_result[0]
        self.rhythm_intensity_tend = segment_result[1]

    def __len__(self):
        return len(self.duration_set)

    def __iter__(self):
        return iter(zip(self.pitch_set, self.duration_set))

    def __add__(self, add_pitch):
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in self.pitch_set]
        return PitchSegment([new_pitch_set, self.duration_set][:]), self, "Transposition" + str(add_pitch)

    def __mod__(self, number):
        pass

    def __getitem__(self, item):
        return self.pitch_set[int(item)], self.duration_set[int(item)]

    def __setitem__(self, key, value):
        """
        Variable *keys includes two element.
        Variable "values" is two-element list.
        """
        new_pitch_set = self.pitch_set
        new_pitch_set[key] = value
        return PitchSegment(
            [new_pitch_set, self.duration_set[:]]), self, "Reset pitch[" + str(key) + "]" + note_value[value]

    def __reversed__(self):
        new_pitch_set = reversed(self.pitch_set)
        new_duration_set = reversed(self.duration_set)
        return PitchSegment([list(new_pitch_set)[:], list(new_duration_set)[:]]), self, "Retrograde with rhyme"

    def new_segment(self, note_num, total_duration, first_note, note_scale, style):
        """ To generate a new segment while original segment is empty.  """
        if self.segment:
            raise RuntimeError("The function 'new_segment' is only used for empty pitch segment.")
        _segment = basicGenerator.randomSegment(note_num, total_duration, first_note, note_scale, style)
        print(_segment)
        self.__init__(_segment, style)

    def get_pc_segment(self):
        pitch_class_set = to_pc_group(self.pitch_set[:], ordered=True)
        return PitchClassSeries([pitch_class_set], self.duration_set[:]), self, "Pitch class segment"

    def change_rhyme(self, total_duration, new_style):
        """ To overwrite a new rhyme to the pitch set.   """
        self.style = new_style
        _segment = [self.pitch_set, basicGenerator.randomRhythm(self.length, total_duration, new_style)]
        return PitchSegment(_segment), self, "Different rhyme"

    def get_counterpoint(self):
        """ Get a two voice segment using counterpoint. """
        # TODO:unfinished
        print("get_counterpoint unfinished")

    def get_average(self):
        return self.w_average

    def get_pitch_tend(self):
        return self.pitch_tend

    def get_rhythm_intensity_tend(self):
        return self.rhythm_intensity_tend

    def _transposition(self, add_pitch):
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in self.pitch_set]
        return PitchSegment([new_pitch_set, self.duration_set][:]), self, "Transposition" + str(add_pitch)

    def _retrograde_with_rhyme(self, add_pitch=0):
        new_pitch_set = list(reversed(self.pitch_set))[:]
        new_duration_set = list(reversed(self.duration_set))[:]
        if add_pitch == 0:
            return PitchSegment([new_pitch_set, new_duration_set]), self, "Retrograde with rhyme"
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in new_pitch_set]
        return PitchSegment([new_pitch_set, new_duration_set]), self, "Retrograde" + str(add_pitch)

    def _retrograde_without_rhyme(self, add_pitch=0):
        new_pitch_set = list(reversed(self.pitch_set))[:]
        if add_pitch == 0:
            return PitchSegment([new_pitch_set, self.duration_set[:]]), self, "Retrograde without rhyme"
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in new_pitch_set]
        return PitchSegment([new_pitch_set, self.duration_set[:]]), self, "Retrograde" + str(add_pitch)

    def _inversion(self, axes):
        new_pitch_set = [2 * int(axes) - pitch for pitch in self.pitch_set]
        return PitchSegment([new_pitch_set, self.duration_set[:]]), self, "Inversion" + str(axes)

    def _retrograde_inversion(self, axes):
        new_pitch_set = reversed([2 * int(axes) - pitch for pitch in self.pitch_set])
        new_duration_set = reversed(self.duration_set)
        return PitchSegment([new_pitch_set, new_duration_set]), self, "Retrograde Inversion" + str(axes)

    def _rotation_without_rhyme(self, num, add_pitch=0):
        if not 0 <= num < self.length:
            raise ValueError("The attribute 'num' should be smaller than length of the series.")
        new_pitch_set = self.pitch_set
        for _i in range(num):
            first = new_pitch_set[0]
            del new_pitch_set[0]
            new_pitch_set.append(first)
        if add_pitch == 0:
            return PitchSegment(
                [new_pitch_set, self.duration_set[:]]), self, "Rotation (without rhyme)" + str(num)
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in new_pitch_set]
        return PitchSegment(
            [new_pitch_set, self.duration_set[:]]), self, "Rotation (without rhyme)" + str(num) + ',T' + str(add_pitch)

    def _rotation_with_rhyme(self, num, add_pitch=0):
        if not 0 <= num < self.length:
            raise ValueError("The attribute 'num' should be smaller than length of the series.")
        new_pitch_set = self.pitch_set
        new_duration_set = self.duration_set
        for _i in range(num):
            first = new_pitch_set[0]
            first_duration = new_duration_set[0]
            del new_pitch_set[0]
            del new_duration_set[0]
            new_pitch_set.append(first)
            new_duration_set.append(first_duration)
        if add_pitch == 0:
            return PitchSegment(
                [new_pitch_set, new_duration_set]), self, "Rotation (with rhyme)" + str(num)
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in new_pitch_set]
        return PitchSegment(
            [new_pitch_set, new_duration_set]), self, "Rotation (with rhyme)" + str(num) + ',T' + str(add_pitch)


# 音集集合
class PitchClassSeries(PitchSegment):
    def __init__(self, segment, __style=None):
        """ Variable 'segment' should be a list of two lists.   """
        super().__init__(segment, __style=None)
        self.pitch_class_set = self.pitch_set
        self.pitch_tend = None
        self.rhythm_intensity_tend = None

    def __iter__(self):
        return iter(zip(self.pitch_class_set, self.duration_set))

    def __add__(self, add_pitch):
        new_pitch_class_set = [new_pitch + int(add_pitch) for new_pitch in self.pitch_class_set]
        return PitchClassSeries([new_pitch_class_set, self.duration_set][:]), self, "Transposition" + str(add_pitch)

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
        return PitchSegment(
            [new_pc_set, self.duration_set[:]]), self, "Reset pitch set[" + str(key) + "]" + note_value[value]

    def __reversed__(self):
        new_pc_set = reversed(self.pitch_set)[:]
        new_duration_set = reversed(self.duration_set)[:]
        return PitchSegment([new_pc_set, new_duration_set]), self, "Retrograde with rhyme"

    def new_segment(self, note_num, total_duration, first_note, note_scale, style):
        """ To generate a new segment while original segment is empty.  """
        if self.segment:
            raise RuntimeError("The function 'new_segment' is only used for empty pitch segment.")
        _segment = basicGenerator.randomSegment(note_num, total_duration, first_note, note_scale, style)
        self.__init__(_segment, __style=style)

    def change_rhyme(self, total_duration, new_style):
        """ To overwrite a new rhyme to the pitch set.   """
        self.style = new_style
        _segment = [self.pitch_set, basicGenerator.randomRhythm(self.length, total_duration, new_style)]
        return PitchClassSeries(_segment), self, "Different rhyme"

    def get_average(self):
        return self.w_average

    def get_pitch_tend(self):
        return self.pitch_tend

    def get_rhythm_intensity_tend(self):
        return self.rhythm_intensity_tend

    def _transposition(self, add_pitch):
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in self.pitch_set]
        return PitchSegment([new_pitch_set, self.duration_set][:]), self, "Transposition" + str(add_pitch)

    def _retrograde_with_rhyme(self, add_pitch=0):
        new_pitch_set = reversed(self.pitch_set)[:]
        new_duration_set = reversed(self.duration_set)[:]
        if add_pitch == 0:
            return PitchClassSeries([new_pitch_set, new_duration_set]), self, "Retrograde with rhyme"
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in new_pitch_set]
        return PitchClassSeries([new_pitch_set, new_duration_set]), self, "Retrograde" + str(add_pitch)

    def _retrograde_without_rhyme(self, add_pitch=0):
        new_pitch_set = reversed(self.pitch_set)[:]
        if add_pitch == 0:
            return PitchClassSeries([new_pitch_set, self.duration_set[:]]), self, "Retrograde without rhyme"
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in new_pitch_set]
        return PitchClassSeries([new_pitch_set, self.duration_set[:]]), self, "Retrograde" + str(add_pitch)

    def _inversion(self, axes):
        new_pitch_set = [2 * int(axes) - pitch for pitch in self.pitch_set]
        return PitchClassSeries([new_pitch_set, self.duration_set[:]]), self, "Inversion" + str(axes)

    def _retrograde_inversion(self, axes):
        new_pitch_set = reversed([2 * int(axes) - pitch for pitch in self.pitch_set])
        new_duration_set = reversed(self.duration_set)
        return PitchClassSeries([new_pitch_set, new_duration_set]), self, "Retrograde Inversion" + str(axes)

    def _rotation_without_rhyme(self, num, add_pitch=0):
        if not 0 <= num < self.length:
            raise ValueError("The attribute 'num' should be smaller than length of the series.")
        new_pitch_set = self.pitch_set
        for _i in range(num):
            first = new_pitch_set[0]
            del new_pitch_set[0]
            new_pitch_set.append(first)
        if add_pitch == 0:
            return PitchClassSeries(
                [new_pitch_set, self.duration_set[:]]), self, "Rotation (without rhyme)" + str(num)
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in new_pitch_set]
        return PitchClassSeries(
            [new_pitch_set, self.duration_set[:]]), self, "Rotation (without rhyme)" + str(num) + ',T' + str(add_pitch)

    def _rotation_with_rhyme(self, num, add_pitch=0):
        if not 0 <= num < self.length:
            raise ValueError("The attribute 'num' should be smaller than length of the series.")
        new_pitch_set = self.pitch_set
        new_duration_set = self.duration_set
        for _i in range(num):
            first = new_pitch_set[0]
            first_duration = new_duration_set[0]
            del new_pitch_set[0]
            del new_duration_set[0]
            new_pitch_set.append(first)
            new_duration_set.append(first_duration)
        if add_pitch == 0:
            return PitchClassSeries(
                [new_pitch_set, new_duration_set]), self, "Rotation (with rhyme)" + str(num)
        new_pitch_set = [new_pitch + int(add_pitch) for new_pitch in new_pitch_set]
        return PitchClassSeries(
            [new_pitch_set, new_duration_set]), self, "Rotation (with rhyme)" + str(num) + ',T' + str(add_pitch)


# TODO: 除了五度圈跨度 (self.span) 之外，为了保证增三和弦能被加入 CPG 和 GCPG 的产物，应当对其 span_tolerance 的算法进行优化，取加权平均数。
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
        return PitchClassSet(self.pitch_class_group)[:], self, "Pitch set group"

    def __sub__(self, other):
        return np.mean(self.pitch_group) - np.mean(other.pitch_group)

    def __gt__(self, other):
        if np.mean(self.pitch_group) > np.mean(other.pitch_group):
            return True

    def __lt__(self, other):
        if np.mean(self.pitch_group) < np.mean(other.pitch_group):
            return True

    def __eq__(self, other):
        if np.mean(self.pitch_group) == np.mean(other.pitch_group):
            return self == other


# TODO: 轮廓截段
class ContourSegment:
    def __init__(self, segment):
        self.pitch_set = segment[0]


# 音级集合
class PitchClassSet:
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
            raise RuntimeError("The cal_set's length should be equal to note set's length.")
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


if __name__ == '__main__':
    # segment1 = PitchSegment([[60, 64, 67, 59, 60, 62, 60], [2, 1, 1, 1.5, 0.25, 0.25, 2]])
    # segment2 = PitchSegment([[60, 64, 67], [2, 1, 1]])
    # a1 = segment1.get_average()
    # a2 = segment2.get_average()
    # pt1 = segment1.get_pitch_tend()
    # pt2 = segment2.get_pitch_tend()
    # rit1 = segment1.get_rhythm_intensity_tend()
    # rit2 = segment2.get_rhythm_intensity_tend()
    # print(a1)
    # print(pt1)
    # print(rit1)
    # print(a2)
    # print(pt2)
    # print(rit2)
    # print(pitch_class_cycles([1, 2, 3, 5, 6], 4))
    import pygame.midi
    import _player

    player = pygame.midi.Output(0)
    player.set_instrument(0)
    for i in range(16):
        while True:
            ng = basicGenerator.randomChord(6, 4, loc=64)
            if chord_type(ng) != "Unable to recognize":
                print("Chord:" + str(sorted(ng)))
                print("Type: " + chord_type(ng))
                break
        # 计算根音
        r_note = _get_root_note(chord_type(ng))
        if r_note is None:
            r_note = root_note_PH(ng)
        else:
            r_note = note_value[r_note] - 12
        print("Root: " + str(r_note))
        # 播放
        if type(r_note) == int:
            _player.play_chord(player, ng, 3)
            _player.play_note(player, r_note, 1)
        else:
            _player.play_chord(player, ng, 4)
