"""
Basic functions:
"""
import copy
import math
from fractions import Fraction
from typing import List

import numpy as _np
from .._basicData import note_value, chords_chroma_vector, note_cof_value, interval_dissonance


# 音集（有序或无序）的键位音级集（若不含重复，即repeat = False，可算作无序；反之可算作有序）
def to_pc_set(pitch_group, ordered=False):
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
    pc_group = to_pc_set(pitch_group)
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
    When you use this function, the series shouldn't be too short.

    If too short, it's pitch tend might be meaningless.

    :param pitch_segment:
        A list with two lists: note group(type = int) and its duration(beat, type = float)
        or class 'PitchSegment's attribute 'pitch_class_series'.
    :return: Pitch Tendentiousness and Rhythm Intensity Tendentiousness (type = list).
    """
    # 确保传入的参数是含两个相同长度列表的列表，并且长度大于等于3，否则报错
    if len(pitch_segment[0]) != len(pitch_segment[1]):
        raise RuntimeError("Segment's two lists' length should be the same.")
    if len(pitch_segment[0]) < 3:
        raise RuntimeError("The series should contain at least 3 notes")
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
        flag_dict[_i] = abs(_np.sum(_duration_list) - _np.sum(_duration_list))
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
    result.append(1 / _np.mean(t2) - 1 / _np.mean(t1))
    return result


def get_intensity(pitch_segment):
    return pitch_segment


# TODO: Unfinished 截段的分割（position只属于后面一段）
def cut(pitch_segment, position):
    if len(pitch_segment[0]) < 4:
        raise RuntimeError("The minimum of pitch_segment'pypcs length is 4.")
    if int(position) >= len(pitch_segment[0]) - 2 or position < 2:
        raise RuntimeError(
            "The 'position' attribute should cut the pitch_segment into two parts that contains at least two notes.")
    return


def get_subsegment(pitch_segment: List[List],
                   start_beat: str,
                   end_beat=None
                   ) -> List[List]:
    """
    :param pitch_segment: Pitch series, which should be a list of two lists.
    :param start_beat:Start beat
    :param end_beat:End beat
    :return:
    If start time is equal to finish time or finish time is None, it returns a pitch'pyPCS value(int),
        else, it returns a new pitch series(list with two lists inside).
    """
    pitch_s, r = pitch_segment
    total_duration = sum([Fraction(d) for d in r])
    all_nodes = [Fraction(0)]
    cou = Fraction(0)
    for i in r:
        cou += Fraction(i)
        all_nodes.append(copy.deepcopy(cou))

    # 确定start_index，初始化start_duration
    start_index = None
    start_beat = Fraction(start_beat)
    if start_beat > total_duration:  # ValueError
        raise ValueError("The start_beat should be larger than total duration of the series.")
    if start_beat == total_duration and end_beat is None:  # 当求的是最后时刻的音高：
        return [[pitch_s[-1]], ['0']]
    for node in reversed(all_nodes):
        if start_beat >= node:
            start_index = all_nodes.index(node)
            break
    start_duration = all_nodes[start_index + 1] - start_beat

    if end_beat is None:
        return [pitch_s[start_index], ['0']]
    else:
        if end_beat > total_duration:  # ValueError
            raise ValueError("The end_beat should be larger than total duration of the series.")
        end_beat = Fraction(end_beat)

    # 确定end_index，初始化end_duration
    end_index = None
    if total_duration - Fraction(r[-1]) < end_beat <= total_duration:
        end_index = len(r) - 1
    else:
        for node in reversed(all_nodes):
            if end_beat > node:
                end_index = all_nodes.index(node)
                break
    end_duration = end_beat - all_nodes[end_index]
    # print(all_nodes[end_index])

    # 计算最终结果：
    sub_ps = pitch_s[start_index:end_index + 1]  # 最后一个索引会丢失，所以+1
    sub_r = r[start_index:end_index + 1]  # 最后一个索引会丢失，所以+1
    if start_beat in all_nodes and end_beat in all_nodes:  # 如果没有音符被start_index和end_index截断
        pass
    else:  # 如果有音符被start_beat和end_beat截断：
        if end_index != start_index:  # 如果结果有多个音符：
            sub_r[0] = str(start_duration)
            sub_r[-1] = str(end_duration)
        else:  # 如果结果只有一个音符：
            # 三种截取点状态（是否在传入的segment的节点上）
            if start_beat not in all_nodes and end_beat not in all_nodes:  # start和end都不在
                sub_r = [str(end_duration + start_duration - Fraction(r[start_index]))]
            elif start_beat in all_nodes and end_beat not in all_nodes:  # start在而end不在
                sub_r = [str(end_duration)]
            else:  # start不在而end在
                sub_r = [str(start_duration)]
    return [sub_ps, sub_r]


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


def chord_dissonance(chord: List[int]):
    # dissonance_group = _np.zeros(len(chord) - 1)
    # for i in range(len(chord) - 1, 0, -1):
    #     avr = []
    #     for j in range(i):
    #         avr.append(interval_dissonance[chord[i] - chord[j]])
    #     # print(avr)
    #     dissonance_group[i - 1] = _np.mean(avr)

    dissonance_group = _np.zeros(math.factorial(len(chord))//(2 * math.factorial(len(chord)-2)))
    counter = 0
    for root_i in range(len(chord)-1):
        for interval_i in range(root_i+1, len(chord)):
            dissonance_group[counter] = interval_dissonance[chord[interval_i]-chord[root_i]]
            counter += 1
    return _np.mean(dissonance_group)


def chord_functionality(tonality, chord: List[int]):
    cof_relation = _np.zeros(len(chord))
    for i in len(chord):
        cof_relation[i] = note_cof_value[(chord[i] - tonality) % 12]
    return
