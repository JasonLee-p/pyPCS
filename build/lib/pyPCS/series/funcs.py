"""
Basic functions:
"""
import copy
import json
import math
import os
from fractions import Fraction
from typing import List

import numpy as _np
from .._basicData import note_value, chords_chroma_vector, note_cof_value, interval_dissonance_t1, \
    interval_dissonance_t2, note_cof_angle


# 音集（有序或无序）的键位音级集（若不含重复，即repeat = False，可算作无序；反之可算作有序）
def to_pc_set(pitch_group, ordered=False):
    """
    注意，这个函数返回的 pitch segment 是无序的，如果如的音集含有重复音级的音，则会删除后面的，除非ordered参数为True

    :param pitch_group:
    :param ordered:
    :return:
    """
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


def chromaVector2pcSet(cv):
    pc_set = []
    for i in range(12):
        if cv[i]:
            pc_set.append(i)
    return pc_set


def contains_M_m_3chord(pc_group):
    Mm3chords = [
        [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
        # 小和弦
        [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
    ]
    self_template = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for _i in pc_group:
        self_template[_i] = 1
    for chroma_vector in Mm3chords:
        counter = 0
        judging = [self_template[i] == chroma_vector[i] == 1 for i in range(12)]
        # print(judging)
        for result in judging:
            if result:
                counter += 1
        if counter == 3:
            return True
    return False


def chroma_vector(pitch_class_group):
    vector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for _i in pitch_class_group:
        vector[_i] = 1
    return vector


# 通过色度向量计算出和弦类型
def chord_type(pitch_group):
    pc_group = to_pc_set(pitch_group)
    _chroma_vector = chroma_vector(pc_group)
    abs_dir = os.path.dirname(__file__)
    with open(os.path.join(os.path.dirname(abs_dir), 'ChordAttr.json'), 'r') as f:
        f = f.read()
        chordsAttr = json.loads(f)
    for chord_name in chordsAttr:
        if _chroma_vector == chordsAttr[chord_name][0]:
            # 在此可以添加特殊情况
            # if:
            #     return
            return chord_name
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
    # TODO:
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
    chord = sorted(chord)
    if len(chord) == 2:
        return interval_dissonance_t2[chord[1] - chord[0]]
    dissonance_group = _np.zeros(len(chord) - 1)
    for i in range(len(chord) - 1, 0, -1):
        avr = []
        for j in range(i):
            avr.append(interval_dissonance_t2[chord[i] - chord[j]])
        # print(avr)
        dissonance_group[i - 1] = _np.mean(avr)

    # dissonance_group = _np.zeros(math.factorial(len(chord))//(2 * math.factorial(len(chord)-2)))
    # counter = 0
    # for root_i in range(len(chord)-1):
    #     for interval_i in range(root_i+1, len(chord)):
    #         dissonance_group[counter] = interval_dissonance_t1[(chord[interval_i]-chord[root_i])]
    #         counter += 1

    return _np.mean(dissonance_group).round(2)


def chord_consonance_tian(chord: List[int]) -> float:
    # 得到音级集合pc_group
    pc_group = sorted(to_pc_set(chord))
    # 得到五度圈跨度fifth_span
    f_spans = []
    for n in pc_group:
        if note_cof_value[n] not in f_spans:
            f_spans.append(note_cof_value[n])
    _len = len(f_spans)
    span_g = []
    for i1 in range(_len):
        f_spans[0] = f_spans[0] + 12
        span = _np.max(f_spans) - _np.min(f_spans)
        f_spans.sort()
        span_g.append(span)
    fifth_span = _np.min(span_g)
    # print(f"fifth span:{fifth_span}")
    # 小二度，大二度数量
    semitone_num = 0
    major2 = 0
    if pc_group[-1] - pc_group[0] == 11:
        semitone_num += 1
    elif pc_group[-1] - pc_group[0] == 10:
        major2 += 1
    for ii in range(len(pc_group) - 1):
        if pc_group[ii + 1] - pc_group[ii] == 1:
            semitone_num += 1
        if pc_group[ii + 1] - pc_group[ii] == 2:
            major2 += 1
    # print(f"semitone_num:{semitone_num}")
    # print(f"major2:{major2}")
    # 是否有大三小三和弦：
    contain_M_m_3chord = contains_M_m_3chord(pc_group)
    # 开始判断：
    if 2 <= fifth_span <= 4:
        if major2 <= 1:
            if contain_M_m_3chord:
                return 10
            else:
                return 9.67
        elif 1 < major2 <= 3:
            return 9.33
    elif fifth_span == 5:
        if major2 <= 1 and contain_M_m_3chord:
            return 7
        elif major2 == 2 and contain_M_m_3chord:
            return 6.67
        else:
            return 6.33
    elif fifth_span == 6:
        if semitone_num == 0:
            if major2 <= 1:
                if contain_M_m_3chord:
                    return 9
                else:
                    return 8.67
            elif major2 == 3:
                return 8.33
        elif semitone_num == 1:
            if major2 == 1 and contain_M_m_3chord:
                return 6
            elif major2 == 2 and contain_M_m_3chord:
                return 5.67
            else:
                return 5.33
        elif semitone_num == 2:
            if major2 == 1 and contain_M_m_3chord:
                return 4
            else:
                return 3.5
    else:
        if semitone_num == 0:
            if fifth_span == 8 and major2 == 0:
                return 8
            elif fifth_span == 8 and major2 == 2:
                return 7.67
            else:
                return 7.33
        elif semitone_num == 1:
            if major2 == 0 and contain_M_m_3chord:
                return 5
            elif major2 <= 2 and contain_M_m_3chord:
                return 4.67
            else:
                return 4.33
        elif semitone_num == 2:
            if fifth_span != 7:
                if major2 <= 2 and contain_M_m_3chord:
                    return 3
                elif major2 > 2 or not contain_M_m_3chord:
                    return 2.75
            else:
                span_contains_7 = False
                for i in range(len(f_spans)):
                    for j in range(len(f_spans)):
                        if i - j == 7:
                            span_contains_7 = True
                            break
                    if span_contains_7:
                        break
                if not span_contains_7:
                    if major2 <= 2 and contain_M_m_3chord:
                        return 3
                    elif major2 > 2 or not contain_M_m_3chord:
                        return 2.75
                # 复杂和弦
                if major2 <= 3 and contain_M_m_3chord:
                    return 2.5
                elif major2 > 3 or not contain_M_m_3chord:
                    return 2.25
        else:
            series2semitone = 0
            series3semitone = 0
            if pc_group[-1] - pc_group[0] == 11:
                if pc_group[1] - pc_group[0] == 1 or pc_group[-1] - pc_group[-2] == 1:
                    series2semitone += 1
                    if pc_group[2] - pc_group[1] == pc_group[1] - pc_group[0] == 1 or \
                            pc_group[-1] - pc_group[-2] == pc_group[-2] - pc_group[-3] == 1:
                        series3semitone += 1
            ii = 0
            while ii < len(pc_group) - 2:
                if pc_group[ii + 2] - pc_group[ii + 1] == pc_group[ii + 1] - pc_group[ii] == 1:
                    series2semitone += 2
                    ii += 3
                ii += 1
            ii = 0
            while ii < len(pc_group) - 3:
                if pc_group[ii + 3] - pc_group[ii + 2] \
                        == pc_group[ii + 2] - pc_group[ii + 1] \
                        == pc_group[ii + 1] - pc_group[ii] == 1:
                    series3semitone += 1
                    ii += 4
                ii += 1
            if semitone_num == 3:
                if (not series2semitone) and (not series3semitone):
                    return 2
                elif series3semitone:
                    return 1.33
                elif series2semitone:
                    return 1.67
            elif semitone_num >= 4:
                if series2semitone == 2:
                    return 1
                elif series3semitone:
                    return 0.67
                else:
                    return 0.33
    txt = f'Failed to get consonance of the given chord {chord}'
    raise RuntimeError(txt)


def get_chordConsonanceTian_from_chromaVector(cv: List[int]) -> float:
    # 得到音级集合pc_group
    pc_group = chromaVector2pcSet(cv)
    # 得到五度圈跨度fifth_span
    f_spans = []
    for n in pc_group:
        if note_cof_value[n] not in f_spans:
            f_spans.append(note_cof_value[n])
    _len = len(f_spans)
    span_g = []
    for i1 in range(_len):
        f_spans[0] = f_spans[0] + 12
        span = _np.max(f_spans) - _np.min(f_spans)
        f_spans.sort()
        span_g.append(span)
    fifth_span = _np.min(span_g)
    # print(f"fifth span:{fifth_span}")
    # 小二度，大二度数量
    semitone_num = 0
    major2 = 0
    if pc_group[-1] - pc_group[0] == 11:
        semitone_num += 1
    elif pc_group[-1] - pc_group[0] == 10:
        major2 += 1
    for ii in range(len(pc_group) - 1):
        if pc_group[ii + 1] - pc_group[ii] == 1:
            semitone_num += 1
        if pc_group[ii + 1] - pc_group[ii] == 2:
            major2 += 1
    # print(f"semitone_num:{semitone_num}")
    # print(f"major2:{major2}")
    # 是否有大三小三和弦：
    contain_M_m_3chord = contains_M_m_3chord(pc_group)
    # 开始判断：
    if 2 <= fifth_span <= 4:
        if major2 <= 1:
            if contain_M_m_3chord:
                return 10
            else:
                return 9.67
        elif 1 < major2 <= 3:
            return 9.33
    elif fifth_span == 5:
        if major2 <= 1 and contain_M_m_3chord:
            return 7
        elif major2 == 2 and contain_M_m_3chord:
            return 6.67
        else:
            return 6.33
    elif fifth_span == 6:
        if semitone_num == 0:
            if major2 <= 1:
                if contain_M_m_3chord:
                    return 9
                else:
                    return 8.67
            elif major2 == 3:
                return 8.33
        elif semitone_num == 1:
            if major2 == 1 and contain_M_m_3chord:
                return 6
            elif major2 == 2 and contain_M_m_3chord:
                return 5.67
            else:
                return 5.33
        elif semitone_num == 2:
            if major2 == 1 and contain_M_m_3chord:
                return 4
            else:
                return 3.5
    else:
        if semitone_num == 0:
            if fifth_span == 8 and major2 == 0:
                return 8
            elif fifth_span == 8 and major2 == 2:
                return 7.67
            else:
                return 7.33
        elif semitone_num == 1:
            if major2 == 0 and contain_M_m_3chord:
                return 5
            elif major2 <= 2 and contain_M_m_3chord:
                return 4.67
            else:
                return 4.33
        elif semitone_num == 2:
            if fifth_span != 7:
                if major2 <= 2 and contain_M_m_3chord:
                    return 3
                elif major2 > 2 or not contain_M_m_3chord:
                    return 2.75
            else:
                span_contains_7 = False
                for i in range(len(f_spans)):
                    for j in range(len(f_spans)):
                        if i - j == 7:
                            span_contains_7 = True
                            break
                    if span_contains_7:
                        break
                if not span_contains_7:
                    if major2 <= 2 and contain_M_m_3chord:
                        return 3
                    elif major2 > 2 or not contain_M_m_3chord:
                        return 2.75
                # 复杂和弦
                if major2 <= 3 and contain_M_m_3chord:
                    return 2.5
                elif major2 > 3 or not contain_M_m_3chord:
                    return 2.25
        else:
            series2semitone = 0
            series3semitone = 0
            if pc_group[-1] - pc_group[0] == 11:
                if pc_group[1] - pc_group[0] == 1 or pc_group[-1] - pc_group[-2] == 1:
                    series2semitone += 1
                    if pc_group[2] - pc_group[1] == pc_group[1] - pc_group[0] == 1 or \
                            pc_group[-1] - pc_group[-2] == pc_group[-2] - pc_group[-3] == 1:
                        series3semitone += 1
            ii = 0
            while ii < len(pc_group) - 2:
                if pc_group[ii + 2] - pc_group[ii + 1] == pc_group[ii + 1] - pc_group[ii] == 1:
                    series2semitone += 2
                    ii += 3
                ii += 1
            ii = 0
            while ii < len(pc_group) - 3:
                if pc_group[ii + 3] - pc_group[ii + 2] \
                        == pc_group[ii + 2] - pc_group[ii + 1] \
                        == pc_group[ii + 1] - pc_group[ii] == 1:
                    series3semitone += 1
                    ii += 4
                ii += 1
            if semitone_num == 3:
                if (not series2semitone) and (not series3semitone):
                    return 2
                elif series3semitone:
                    return 1.33
                elif series2semitone:
                    return 1.67
            elif semitone_num >= 4:
                if series2semitone == 2:
                    return 1
                elif series3semitone:
                    return 0.67
                else:
                    return 0.33
    txt = f'Failed to get consonance of the given chroma vector {cv}'
    raise RuntimeError(txt)


def chord_colour_hua(chord: List[int]) -> float:
    _chord_colour_hua = []
    for note in chord:
        if (value := math.degrees(note_cof_angle[note % 12])) not in _chord_colour_hua:
            _chord_colour_hua.append(value)
    return round(float(_np.mean(_chord_colour_hua)), 1)


def chord_colour_hua_from_chromaVector(cv):
    _chord_colour_hua = []
    for pitchClass in chromaVector2pcSet(cv):
        if (value := math.degrees(note_cof_angle[pitchClass])) not in _chord_colour_hua:
            _chord_colour_hua.append(value)
    return round(float(_np.mean(_chord_colour_hua)), 1)


def chord_colour(chord: List[int], dynamics: List[int]) -> float:
    """
    :param chord: Chord's note group
    :param dynamics: Dynamics (0-1)
    :return:
    """
    _chord_colour_hua = [math.degrees(note_cof_angle[chord[i] % 12] * dynamics[i]) for i in range(len(chord))]
    return float(_np.mean(_chord_colour_hua))


def chord_functionality(tonality, chord: List[int]):
    cof_relation = _np.zeros(len(chord))
    for i in len(chord):
        cof_relation[i] = note_cof_value[(chord[i] - tonality) % 12]
    return


def conform_voice_leading(chord, last_chord):
    """

    :param chord:
    :param last_chord:
    :return: bool
    """
    chord = sorted(chord)
    if len(chord) < 3 or len(last_chord) < 3:
        raise ValueError("There should be more than 2 notes in a chord, especially when judging voice leading.")

    if len(chord) == len(last_chord):
        # 判断所有声部是否同向：
        # 定义计数器
        cou = 0
        for i in range(len(last_chord)):
            if last_chord[i] > chord[i]:
                cou += 1
            if last_chord[i] < chord[i]:
                cou -= 1
        if abs(cou) == len(chord):
            print(f"{last_chord}->{chord}: ")
            print("All voices" + "\033[0;31m same direction\033[0m" +
                  ".")
            return False
    elif len(chord) > len(last_chord):  # 声部扩张
        # 判断声部是否同向：
        cou_up = 0
        cou_dn = 0
        for i in range(-1, -len(last_chord) - 1, -1):
            if chord[i] < last_chord[i]:
                cou_dn += 1
        for i in range(len(last_chord)):
            if chord[i] > last_chord[i]:
                cou_up += 1
        if cou_up == len(last_chord) or cou_dn == len(last_chord):
            return False
    else:  # 声部减少
        # 判断声部是否同向：
        cou_up = 0
        cou_dn = 0
        for i in range(-1, -len(chord) - 1, -1):
            if chord[i] > last_chord[i]:
                cou_up += 1
        for i in range(len(chord)):
            if chord[i] < last_chord[i]:
                cou_dn += 1
        if cou_up == len(chord) or cou_dn == len(chord):
            return False
    return True
