"""

"""
import math
from fractions import Fraction
# from .._player import play_pitch_segment
import time

import numpy as np
from .._basicData import _prt_func_time, _prt_funcs_time, _prt_func_run_num

style_group = ["smooth", "more doted notes", "triple"]


if __name__ == "__main__":
    """
    segment = random_segment(4, 5, note_scale=4, first_note=64, style='smooth')

    for i in range(len(segment[0])):
        relative_pitch = str(segment[0][i])
        duration = str(segment[1][i])
        print(relative_pitch + " " * (4 - len(relative_pitch)), end="")
        print(duration)
    play_pitch_segment(None, segment, bpm=120)
    """
    segment = [[61, 62, 63, 64, 65, 66], [1, 2, 1, 1, 2, 1]]
    print(segment)
    counterpoint(segment, average_interval=2, counterpoint_p_num=4, new_pset_scale_from_origin=0)
