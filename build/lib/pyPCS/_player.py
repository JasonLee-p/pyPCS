"""
    This module defines how to play various music elements (in midi file).
"""
import pygame
import pygame.midi as pm

pm.init()  # init midi _player
BPM = 120


def play_note(_player_, note, beats, bpm=80):
    _player = 0
    if _player_ is None:
        _player = pm.Output(0)
        _player.set_instrument(0)
    else:
        _player = _player_
    _player.note_on(note, 80)
    pygame.time.wait(int(60000 * eval(str(beats))) // bpm)
    _player.note_off(note, 80)
    if _player_ is None:
        del _player


def play_pitch_segment(_player, pitch_segment, bpm=80, instrument='Piano'):
    """
    :param _player: Pygame.midi.Output(int) variable.
    :param pitch_segment: Pitch segment, duration_list is included
    :param bpm: Beats per minutes.
    :param instrument: 'Piano' or 'Strings'
    :return: None
    """
    pitch_set = pitch_segment[0]
    duration_set = pitch_segment[1]
    if _player is None:
        _player = pm.Output(0)
    if instrument == 'Piano':
        _player.set_instrument(0)
    if instrument == 'Strings':
        _player.set_instrument(44)
    for i in range(len(pitch_set)):
        pitch = pitch_set[i]
        duration = str(duration_set[i])
        _player.note_on(pitch, 80)
        pygame.time.wait(int(60000 * eval(duration)) // bpm)
        _player.note_off(pitch, 80)
    print("Done")


def play_chord(_player_, note_list, duration=4, bpm=80):
    _player = 0
    if _player_ is None:
        _player = pm.Output(0)
        _player.set_instrument(0)
    else:
        _player = _player_
    for note in note_list:
        _player.note_on(note, 80)
    pygame.time.wait(60000 * eval(str(duration)) // bpm)
    for note in note_list:
        _player.note_off(note, 80)

    if _player_ is None:
        del _player


def play_chord_set(_player_, chord_set, duration_set, bpm, instrument):
    """

    :param _player_: Pygame.midi.Output(int) variable.
    :param chord_set: A set of class Chord (in 'chorder' model) variable.
    :param duration_set: A set of notes' durations.
    :param bpm: Beats per minutes.
    :param instrument: 'Piano' or 'Strings'
    :return: None
    """
    _player = 0
    if _player_ is None:
        _player = pygame.midi.Output(0)
    else:
        _player = _player_
    if instrument == 'Piano':
        _player.set_instrument(0)
    if instrument == 'Strings':
        _player.set_instrument(44)
    for i in range(len(chord_set)):
        note_list = chord_set[i].pitch_group()
        duration = duration_set[i]
        play_chord(_player, note_list, duration, bpm)
    if _player_ is None:
        del _player


if __name__ == "__main__":
    player = pm.Output(0)
