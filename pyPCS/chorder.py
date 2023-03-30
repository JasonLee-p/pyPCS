"""
    In this module, we set some array to fit note strings into numbers,
    which is necessary to fit the program into 'mido'.
    We also set the class 'Chord', whose attribute is quite common in analysing chords,
    and class 'NoteSet', which is a widely acknowledged tool in analysing chords.
"""
import threading

from ._basicData import value_note, note_value, notes_names, chords_chroma_vector, note_cof_value, note_tension
import numpy as np
import random

"""
    Following functions are used in class Chord:
"""


def mod12(num):
    return int(num) % 12


# 根据预设音域生成随机音符
def random_note(lo, hi):
    if lo < 21:
        lo = 21
    if hi > 108:
        hi = 108
    return random.randint(lo, hi)


# 根据和弦音符数量生成一个随机和弦
def random_chord(number_of_notes_in_chord):
    # 初始化音符列表
    chord_note = []
    # 添加音符
    while len(chord_note) != number_of_notes_in_chord:
        n = random.randint(30, 80)
        if n not in chord_note:
            chord_note.append(n)  # 30-90是音域限制，60为C4(440Hz)
    return sorted(chord_note)


# 根据旋律音与和弦音符数量生成一个随机和弦，机制如上
def melody_random_chord(melody_note, n_of_notes_in_chord):
    chord_note = [melody_note]
    while len(chord_note) != n_of_notes_in_chord:
        n = random.randint(30, melody_note - 1)
        if n not in chord_note:
            chord_note.append(n)  # 30是根音的下限
    return sorted(chord_note)


# 根据根音与和弦音符数量生成一个随机和弦，机制如上
def root_random_chord(root, n_of_notes_in_chord):
    chord_note = [root]
    while len(chord_note) != n_of_notes_in_chord:
        n = random.randint(root + 4, 90)
        if n not in chord_note:
            chord_note.append(n)
    return sorted(chord_note)


# 根据旋律音，根音与和弦音符数量生成一个随机和弦，机制如上
def melody_root_random_chord(melody, root, n_of_notes_in_chord):
    # 判断旋律音和根音是否合法
    if melody + 2 - n_of_notes_in_chord < root:
        return None
    chord_note = [melody, root]
    while len(chord_note) != n_of_notes_in_chord:
        n = random.randint(root + 1, melody - 1)
        if n not in chord_note:
            chord_note.append(n)  # 25是旋律音相对根音的上限
    return sorted(chord_note)


# 音集(已按大小排序)
def c_interval(n_group):
    interval_g = []
    for n in n_group:
        interval = n % 12
        if interval not in interval_g:
            interval_g.append(interval)
    return sorted(interval_g)


# 计算音集中小二度的数量
def semitone_num(c_itv):
    output = 0
    if c_itv[-1] - c_itv[0] == 11:
        output += 1
    for ii in range(len(c_itv)):
        if ii != len(c_itv) - 1 and c_itv[ii + 1] - c_itv[ii] == 1:
            output += 1
    return output


# 色值计算需要五度圈关系
def c_k_colour(interval):
    spans = []
    for n in interval:
        spans.append(note_cof_value[n])
    return np.mean(spans)


# 五度圈跨度计算需要五度圈关系
def c_span(interval):
    """

    :param interval: Note set
    :return:
    """
    spans = []
    for n in interval:
        spans.append(note_cof_value[n])
    span_g = []
    for i1 in range(len(spans)):
        spans[0] = spans[0] + 12
        span = np.max(spans) - np.min(spans)
        spans.sort()
        span_g.append(span)
    return np.min(span_g)


# 该函数需要先创建空列表以导出值
def c_tension(sorted_chord, tension_g):
    interval = []
    for n1 in sorted_chord:
        for n2 in sorted_chord:
            x = n2 - n1
            if x > 0:
                interval.append(note_tension[x])
    tension = np.mean(interval)
    tension_g.append(tension)
    print("均紧张度：" + str(tension))
    return tension_g


# 根据泛音列权重法判断根音
def root_note_HS(note_g):
    _len = len(note_g)
    note_g = sorted(note_g)
    return note_g


# TODO 根据网上 Paul Hindemith 的根音计算方式把该函数写完
def root_note_PH(note_g):
    _len = len(note_g)
    note_g = sorted(note_g)

    """倾向不明显的情况"""
    # 判断是否为增三和弦，减七和弦， 四度和弦， 十二音音簇：
    if _len == 3:
        i1 = note_g[2] - note_g[1]
        i2 = note_g[1] - note_g[0]
        if mod12(i1) == mod12(i2) == 4:
            return "增三和弦"
        if mod12(i1) == mod12(i2) == 5:
            return "四度和弦"
    elif _len == 4 and \
            mod12(note_g[3] - note_g[2]) == mod12(note_g[2] - note_g[1]) == mod12(note_g[1] - note_g[0]) == 3:
        return "减七和弦"
    elif _len == 12:
        cou = 0
        for j in range(1, 12):
            if note_g[j] - note_g[j - 1] == 1:
                cou += 1
        if cou == 11:
            return "十二音音簇"

    """最一般的情况"""
    pc_itv_dict = [[], [], [], [], [], [], [], [], [], [], [], []]
    for j in range(_len):
        for k in range(j + 1, _len):
            interval = mod12(note_g[k] - note_g[j])
            # 五度四度
            if interval == 7:
                pc_itv_dict[interval].append(note_g[j])
            elif interval == 5:
                pc_itv_dict[interval].append(note_g[k])
            # 大三小六
            elif interval == 4:
                pc_itv_dict[interval].append(note_g[j])
            elif interval == 8:
                pc_itv_dict[interval].append(note_g[k])
            # 小三大六
            elif interval == 3:
                pc_itv_dict[interval].append(note_g[j])
            elif interval == 9:
                pc_itv_dict[interval].append(note_g[k])
            # TODO: 后面的有待商榷
            # 大二小七
            elif interval == 2:
                pc_itv_dict[interval].append(note_g[j])
            elif interval == 10:
                pc_itv_dict[interval].append(note_g[k])
            # 小二大七
            elif interval == 1:
                pc_itv_dict[interval].append(note_g[j])
            elif interval == 11:
                pc_itv_dict[interval].append(note_g[k])
            # 三全音
            elif interval == 6:
                pc_itv_dict[interval].append(note_g[j])
                pc_itv_dict[interval].append(note_g[k])
            elif interval == 0:
                pc_itv_dict[interval].append(note_g[j])
                pc_itv_dict[interval].append(note_g[k])
        possible_root = []
        # TODO: 算法不完善，需要引入权重
        for _interval in [7, 5, 4, 8, 3, 9]:
            for _pitch in pc_itv_dict[_interval]:
                possible_root.append(_pitch)
        if len(pc_itv_dict[0]) > 2:
            possible_root.append(_interval[0])
        if possible_root:
            print("Possible roots:" + str(pc_itv_dict))
            return min(possible_root)
        return pc_itv_dict


if __name__ == '__main__':
    pass
