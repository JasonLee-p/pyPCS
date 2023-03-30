"""

"""
import math
from fractions import Fraction
# from .._player import play_pitch_segment
import time

import numpy as np
from .._basicData import _prt_func_time, _prt_funcs_time, _prt_func_run_num

style_group = ["smooth", "more doted notes", "triple"]


# 该函数在P_c_s_T文件中也有。
def get_segments_subsegment(ps, start_time, finish_time=None):
    """
    :param ps: Pitch series
    :param start_time:Start time
    :param finish_time:Finish time
    :return: If start time is equal to finish time or finish time is None, it returns a pitch'pypcs value(int),
        else, it returns a new pitch series(list with two lists inside).
    """
    start_time = float(start_time)
    finish_time = float(finish_time) if finish_time is not None else None
    # 判断传入变量是否合法：
    total_duration = sum([float(i) for i in ps[1]])
    if finish_time < start_time:
        raise ValueError("Finish time should be larger than start time.")
    if float(start_time) == total_duration:
        raise ValueError("Start time should be smaller than total duration.")
    if finish_time > total_duration:
        print(finish_time)
        print(start_time)
        raise ValueError("Finish time should be smaller than the total duration of the pitch series.")
    p_set = ps[0]
    duration_set = ps[1]
    result_ps = [[], []]  # 返回结果
    start_index = 0
    finish_index = 0
    d_counter = 0
    start_cou = False
    # 获取被截截段的断点列表：
    interval_point_set = [0]
    d_counter2 = 0.0
    for d in duration_set:
        d_counter2 += float(d)
        interval_point_set.append(d_counter2)
    # print(interval_point_set)

    # 给索引赋值，注意终点值已经舍掉了最后一位。
    for duration_i in range(len(duration_set)):
        d_counter += duration_set[duration_i]
        if d_counter >= start_time and start_cou is False:
            start_index = duration_i
            start_cou = True
        if d_counter > finish_time:
            finish_index = duration_i
            break
    # 给结果列表赋值，并且返回：
    if start_time not in interval_point_set and finish_time not in interval_point_set:  # 始终索引都不在断点时：
        for i in range(start_index, finish_index):
            result_ps[0].append(ps[0][i])
            result_ps[1].append(ps[1][i])
    elif start_time not in interval_point_set and finish_time in interval_point_set:  # 始索引不在断点，终索引在断点时：
        for i in range(start_index, finish_index):
            result_ps[0].append(ps[0][i])
            result_ps[1].append(ps[1][i])
    elif start_time in interval_point_set and finish_time not in interval_point_set:  # 始索引在断点，终索引不在断点时：
        for i in range(start_index, finish_index):
            result_ps[0].append(ps[0][i])
            result_ps[1].append(ps[1][i])
    elif start_time in interval_point_set and finish_time in interval_point_set:  # 始终索引都在断点时：
        for i in range(start_index, finish_index):
            result_ps[0].append(ps[0][i])
            result_ps[1].append(ps[1][i])
    return result_ps


def find_nearest(array, value):
    """
    This function returns the number in a sorted linear array that is closest to the given number.
    该函数返回 numpy 一维数组（有序的）内离参数value最近的数。
    """
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx - 1]) < math.fabs(value - array[idx])):
        return array[idx - 1]
    else:
        return array[idx]


# 自定义随机数生成方式
# TODO: unfinished
def _random_number(_loc, _scale, _size=None):
    n = np.random.normal(loc=_loc, scale=_scale, size=None)
    n += _scale
    return


# 通过高斯分布，随机生成一个和弦

# @_prt_func_run_num
# @_prt_funcs_time(100)
def randomChord(note_num, scale=7, loc=60):
    if scale > 15:
        raise ValueError("Scale expects a number less than 16")
    if note_num > 15:
        raise ValueError("Note_num expects a number less than 16")
    chord = []
    while len(chord) != note_num:
        n = int(np.random.normal(loc=loc, scale=scale, size=None) + 0.5)
        if n < loc + 1.5 * scale and n not in chord:
            chord.append(n)
    return chord


# TODO: unfinished
def counterpoint(original_pitch_segment, average_interval, counterpoint_p_num, new_pset_scale_from_origin):
    original_p_set = original_pitch_segment[0]
    original_d_set = [float(num) for num in original_pitch_segment[1]]
    original_average_p = np.mean(original_p_set)
    original_scale = np.std(np.array(original_pitch_segment))
    _duration = np.sum(original_d_set)
    _new_avr_p = original_average_p - average_interval
    _new_d_set = randomRhythm(counterpoint_p_num, _duration, "smooth")  # TODO: way to get original 'style' unfinished
    print(_new_d_set)
    # 添加音符
    _new_p_set = []
    _sub_ps_set = []
    start_t = 0.0
    for j in range(counterpoint_p_num):
        finish_t = start_t + _new_d_set[j]
        print(start_t, end='——>')
        print(finish_t)
        sub_ps = get_segments_subsegment(original_pitch_segment, start_t, finish_t)
        _sub_ps_set.append(sub_ps)
        start_t += float(_new_d_set[j])
    print(_sub_ps_set)
    return [_new_p_set, _new_d_set]


# 根据长度生成一个随机相对音高序列
def random_relative_pitch_set(note_num, scale=3):
    if scale > 6:
        raise ValueError("Scale expects a number less than 7")
    # 初始化音符序列
    pitch_set = []
    # 添加音符
    while len(pitch_set) != note_num:
        n = np.random.normal(loc=10, scale=scale, size=None)
        pitch_set.append(int(n))
    min_note = np.min(pitch_set)
    if min_note == 0:
        return pitch_set
    else:
        pitch_set = [pitch - min_note for pitch in pitch_set]
    return pitch_set


# 根据音符数量和总时值生成一个随机时值序列
def randomRhythm(note_num, total_duration, style):
    if style not in style_group:
        raise ValueError("Invalid style")
    if total_duration not in range(1, 20):
        if total_duration not in [j + 0.5 for j in range(1, 20)]:
            raise ValueError("The total_duration should be a multiple of 0.5")
    if total_duration > 4 * note_num:
        raise ValueError("The total_duration is too large")
    if total_duration < note_num / 3:
        raise ValueError("The note_num is too large")
    all_available_durations = [0.25, 1 / 3, 0.5, 2 / 3, 0.75, 1, 1.25, 4 / 3, 1.5, 5 / 3, 1.75, 2, 2.5, 3, 4]
    smooth_ad = np.array([0.5, 1, 1.5, 2, 2.5, 3, 4])
    m_do_n_ad = np.array([0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.5, 3, 4])
    triple_ad = np.array([1 / 3, 2 / 3, 1, 4 / 3, 5 / 3, 2, 3, 4])
    avr_dur = total_duration / note_num  # 平均时值
    rhythm_set = []
    flag = True
    while flag:
        rhythm_set.clear()

        if style == "smooth":
            if note_num == total_duration:
                return ['1'] * note_num
            for j in range(note_num - 1):
                if note_num < total_duration:
                    n = int(np.random.normal(loc=avr_dur, scale=avr_dur/2, size=None) + 0.5)
                    rhythm_set.append(str(n)) if n > 0 else rhythm_set.append('1')
                if note_num > total_duration:
                    n = find_nearest(smooth_ad, np.random.normal(loc=avr_dur, scale=avr_dur/2, size=None))
                    rhythm_set.append(str(Fraction(n))) if n > 0 else rhythm_set.append('1/2')

        elif style == "more doted notes":
            for j in range(note_num - 1):
                if j != 0:  # 模拟附点音符
                    if rhythm_set[-1] == '3/2' and avr_dur > 0.75:
                        rhythm_set.append('1/2')
                        continue
                    if rhythm_set[-1] == '3/4' and avr_dur > 0.37:
                        rhythm_set.append('1/4')
                        continue
                n = find_nearest(m_do_n_ad, np.random.normal(loc=avr_dur, scale=avr_dur, size=None))
                rhythm_set.append(str(Fraction(n))) if n > 0 else rhythm_set.append('1/4')
            for j in range(1, 5):
                if j * note_num == total_duration and rhythm_set == [j] * note_num:
                    flag = False

        elif style == "triple":
            for j in range(note_num - 1):
                n = find_nearest(triple_ad, np.random.normal(loc=avr_dur, scale=avr_dur / 2, size=None))
                rhythm_set.append(str(Fraction(n))) if n > 0 else rhythm_set.append('1/3')
                # print(n)

        _sum = sum([Fraction(i) for i in rhythm_set])
        rest_duration = round(total_duration - _sum, 2)
        if float(_sum) < total_duration and rest_duration in all_available_durations:
            flag = False
        else:
            print("Failed: rest duration:" + str(rest_duration))
    rhythm_set.append(str(total_duration - sum([Fraction(i) for i in rhythm_set])))
    return rhythm_set


# 随机生成一个音集截段（包括节奏）
def randomSegment(note_num, total_duration, first_note, note_scale=3, style="smooth", _type='str'):
    random_r_p_set = random_relative_pitch_set(note_num, note_scale)
    first_r_note = random_r_p_set[0]
    random_pitch_set = [r_p + first_note - first_r_note for r_p in random_r_p_set]
    ds = randomRhythm(note_num, total_duration, style)
    ds = [str(d) for d in ds] if _type == 'str' else ds
    return [random_pitch_set, ds]


if __name__ == "__main__":
    """
    series = random_segment(4, 5, note_scale=4, first_note=64, style='smooth')

    for i in range(len(series[0])):
        relative_pitch = str(series[0][i])
        duration = str(series[1][i])
        print(relative_pitch + " " * (4 - len(relative_pitch)), end="")
        print(duration)
    play_pitch_segment(None, series, bpm=120)
    """
    segment = [[61, 62, 63, 64, 65, 66], [1, 2, 1, 1, 2, 1]]
    print(segment)
    counterpoint(segment, average_interval=2, counterpoint_p_num=4, new_pset_scale_from_origin=0)
