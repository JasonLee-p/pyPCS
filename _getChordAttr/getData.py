import json
from _ctypes import PyObj_FromPtr
import re
from pyPCS import Chord


def chroma_vector_transposition(chroma_vector, add):
    return [chroma_vector[(j + add) % 12] for j in range(12)]


NoteNames = [
    "C",
    '#C',
    'D',
    '#D',
    'E',
    'F',
    '#F',
    'G',
    'bA',
    'A',
    'bB',
    'B',
]
ChordNames = [
    'C',
    'Cm',
    'C6',
    'Cm7',
    'Csus2',
    'C57',
    'C56',
    'Csus2sus4',
    'Cadd9',
    'Cmadd11',
    'C6add9',
    'C23',
    'C7',
    'Cm6',
    'Cdim',
    'C2#4',
    'C2b6',
    'C9',
    'C23#4',
    'Caug',
    'Caugadd9',
    'Caugadd11',
    'C2#4b6',
    'Caugadd9#11',  # TODO: add11变s11
    'Cdim7',
    'C23#4b67',
    'CM7',
    'Cadd11',
    'Cmadd9',
    'CM9',
    'Cm9',
    'C5M7',
    'C5b6',
    'C56M7',
    'C5b67',
    'C567',
    'Cadd9add11',
    'Cmadd9add11',
    'Cm11',
    'C2b3',
    'C2M7',
    'C#11',
    'Cmb9',
    'C67',
    'Cm67',
    'Cm6add9',
    'C7add11',
    'Csus4M7',
    'Csus2b6',
    'C57b9',
    'C56#11',
    'Cadd9#11',
    'Cmb9add11',
    'C11',
    'Cm11b9',
    'C5b9',
    'C5#11',
    'Cb6',
    'CmM7',
    'Caddb3',
    'Cm#11',
    'Cb9',
    'C7b9',
    'Cm6#11',
    'C6addb3',
    'Cm7add3',
    'Cb67',
    'Cm6M7',
    'Cb6add9',
    'CmM7add11',
    'C7#11',
    'Cm6b9',
    'C56b9',
    'C57#11',
    'C3addb3',
    'C3addb9',
    'Cdimadd3',
    'Cdimadd9',
    'C9#11',
    'C9b6',
    'CM7#11',
    'CM7add11',
    'Cdimb9add11',
    'Cm11b5b9',
    'CM11',
    'CM9#11',
    'C5M7#11',
    'CM7addb3',
    'CM7b6',
    'CmM9',
    'Cb6b9',
    'Caddb3#11',
    'Cmaddb3b9',
    'C6M7addb3',
    'Cmb67add3',
    'Cm6M7#11',
    'C11b9',
    'Cm7add3b9',
    'C6addb3#11',
    'C5b6M7',
    'C567b9',
    'C567#11',
    'C2b3M7',
    'Cb67add11',
    'Cm6M9',
    'Cm67b9',
]


class NoIndent(object):
    """ Value wrapper. """
    def __init__(self, value):
        self.value = value


class MyEncoder(json.JSONEncoder):
    FORMAT_SPEC = '@@{}@@'
    regex = re.compile(FORMAT_SPEC.format(r'(\d+)'))

    def __init__(self, **kwargs):
        # Save copy of any keyword argument values needed for use here.
        self.__sort_keys = kwargs.get('sort_keys', None)
        super(MyEncoder, self).__init__(**kwargs)

    def default(self, obj):
        return (self.FORMAT_SPEC.format(id(obj)) if isinstance(obj, NoIndent)
                else super(MyEncoder, self).default(obj))

    def encode(self, obj):
        format_spec = self.FORMAT_SPEC  # Local var to expedite access.
        json_repr = super(MyEncoder, self).encode(obj)  # Default JSON.

        # Replace any marked-up object ids in the JSON repr with the
        # value returned from the json.dumps() of the corresponding
        # wrapped Python object.
        for match in self.regex.finditer(json_repr):
            # see https://stackoverflow.com/a/15012814/355230
            id = int(match.group(1))
            no_indent = PyObj_FromPtr(id)
            json_obj_repr = json.dumps(no_indent.value, sort_keys=self.__sort_keys)

            # Replace the matched id string with json formatted representation
            # of the corresponding Python object.
            json_repr = json_repr.replace(
                            '"{}"'.format(format_spec.format(id)), json_obj_repr)

        return json_repr


if __name__ == "__main__":
    ChordAttrs = {}
    C = Chord([60, 64, 67])
    Cm = Chord([60, 63, 67])
    C6 = Chord([60, 64, 67, 69])
    Cm7 = Chord([60, 63, 67, 70])
    Csus2 = Chord([60, 62, 67])
    C57 = Chord([60, 67, 70])
    C56 = Chord([60, 67, 69])
    Csus2sus4 = Chord([60, 62, 65, 67])
    Cadd9 = Chord([60, 62, 64, 67])
    Cmadd11 = Chord([60, 63, 65, 67])
    C6add9 = Chord([60, 62, 64, 67, 69])
    C23 = Chord([60, 62, 64])
    C7 = Chord([60, 64, 67, 70])
    Cm6 = Chord([60, 63, 67, 69])
    Cdim = Chord([60, 63, 66])
    C2s4 = Chord([60, 62, 66])
    C2b6 = Chord([60, 62, 68])
    C9 = Chord([60, 62, 64, 67, 70])
    C23s4 = Chord([60, 62, 64, 66])
    Caug = Chord([60, 64, 68])
    Caugadd9 = Chord([60, 62, 64, 68])  # TODO:
    Caugadd11 = Chord([60, 64, 66, 68])
    C2s4b6 = Chord([60, 62, 66, 68])
    Caugadd9s11 = Chord([60, 62, 64, 66, 68])
    Cdim7 = Chord([60, 63, 66, 69])
    C23s4b67 = Chord([60, 62, 64, 66, 68, 70])
    CM7 = Chord([60, 64, 67, 71])
    Cadd11 = Chord([60, 64, 65, 67])
    Cmadd9 = Chord([60, 62, 63, 67])
    CM9 = Chord([60, 62, 64, 67, 71])
    Cm9 = Chord([60, 62, 63, 67, 70])
    C5M7 = Chord([60, 67, 71])
    C5b6 = Chord([60, 67, 68])
    C56M7 = Chord([60, 67, 69, 71])
    C5b67 = Chord([60, 67, 68, 70])
    C567 = Chord([60, 67, 68, 70])
    Cadd9add11 = Chord([60, 62, 64, 65, 67])
    Cmadd9add11 = Chord([60, 62, 63, 65, 67])
    Cm11 = Chord([60, 62, 63, 65, 67, 70])
    C2b3 = Chord([60, 62, 63])
    C2M7 = Chord([60, 62, 71])
    Cs11 = Chord([60, 64, 66, 67])
    Cmb9 = Chord([60, 61, 63, 67])
    C67 = Chord([60, 64, 67, 69, 70])
    Cm67 = Chord([60, 63, 67, 69, 70])
    Cm6add9 = Chord([60, 62, 63, 67, 69])
    C7add11 = Chord([60, 64, 65, 67, 70])
    Csus4M7 = Chord([60, 65, 67, 71])
    Csus2b6 = Chord([60, 62, 67, 68])
    C57b9 = Chord([60, 61, 67, 70])
    C56s11 = Chord([60, 66, 67, 69])
    Cadd9s11 = Chord([60, 62, 64, 66, 67])
    Cmb9add11 = Chord([60, 61, 63, 65, 67])
    C11 = Chord([60, 62, 64, 65, 67, 70])
    Cm11b9 = Chord([60, 61, 63, 65, 67, 70])
    C5b9 = Chord([60, 61, 67])
    C5s11 = Chord([60, 66, 67])
    Cb6 = Chord([60, 64, 67, 68])
    CmM7 = Chord([60, 63, 67, 71])
    Caddb3 = Chord([60, 63, 64, 67])
    Cms11 = Chord([60, 63, 66, 67])
    Cb9 = Chord([60, 61, 64, 67])
    C7b9 = Chord([60, 61, 64, 67, 70])
    Cm6s11 = Chord([60, 63, 66, 67, 69])
    C6addb3 = Chord([60, 63, 64, 67, 69])
    Cm7add3 = Chord([60, 63, 64, 67, 70])
    Cb67 = Chord([60, 64, 67, 68, 70])
    Cm6M7 = Chord([60, 63, 67, 69, 71])
    Cb6add9 = Chord([60, 62, 64, 67, 68])
    CmM7add11 = Chord([60, 63, 65, 67, 71])
    C7s11 = Chord([60, 64, 66, 67, 70])
    Cm6b9 = Chord([60, 61, 63, 67, 69])
    C56b9 = Chord([60, 61, 67, 69])
    C57s11 = Chord([60, 66, 67, 70])
    C3addb3 = Chord([60, 63, 64])
    C3addb9 = Chord([60, 61, 64])
    Cdimadd3 = Chord([60, 63, 64, 66])
    Cdimadd9 = Chord([60, 62, 63, 66])
    C9s11 = Chord([60, 62, 64, 66, 67, 70])
    C9b6 = Chord([60, 62, 64, 67, 68, 70])
    CM7s11 = Chord([60, 64, 66, 67, 71])
    CM7add11 = Chord([60, 64, 66, 67, 71])
    Cdimb9add11 = Chord([60, 61, 63, 65, 66])
    Cm11b5b9 = Chord([60, 61, 63, 65, 66, 70])
    CM11 = Chord([60, 62, 64, 65, 67, 71])
    CM9s11 = Chord([60, 62, 64, 66, 67, 71])
    C5M7s11 = Chord([60, 66, 67, 71])
    CM7addb3 = Chord([60, 63, 64, 67, 71])
    CM7b6 = Chord([60, 64, 67, 68, 71])
    CmM9 = Chord([60, 62, 63, 67, 71])
    Cb6b9 = Chord([60, 61, 64, 67, 68])
    Caddb3s11 = Chord([60, 63, 64, 66, 67])
    Cmaddb3b9 = Chord([60, 61, 63, 64, 67])
    C6M7addb3 = Chord([60, 63, 64, 67, 69, 71])
    Cmb67add3 = Chord([60, 63, 64, 67, 69, 70])
    Cm6M7s11 = Chord([60, 63, 66, 67, 69, 71])
    C11b9 = Chord([60, 61, 64, 65, 67, 70])
    Cm7add3b9 = Chord([60, 61, 63, 64, 67, 70])
    C6addb3s11 = Chord([60, 63, 64, 66, 67, 69])
    C5b6M7 = Chord([60, 67, 68, 71])
    C567b9 = Chord([60, 61, 67, 69, 70])
    C567s11 = Chord([60, 66, 67, 69, 70])
    C2b3M7 = Chord([60, 62, 63, 71])
    Cb67add11 = Chord([60, 64, 65, 67, 68, 70])
    Cm6M9 = Chord([60, 62, 63, 67, 69, 71])
    Cm67b9 = Chord([60, 61, 63, 67, 69, 70])
    c_vectors = [chord.chroma_vector for chord in Chord.all_chords]
    for note_name in NoteNames:
        if note_name != 'C':
            for i in range(len(ChordNames)):
                name = f"{note_name}{ChordNames[i][1:]}"
                ##########################################
                ChordAttrs[name] = [
                    vector := chroma_vector_transposition(c_vectors[i], 1),
                    Chord.get_colourTian_from_chromaVector(vector)
                ]
        else:  # C，初始化
            for i in range(len(ChordNames)):
                ##########################################
                ChordAttrs[ChordNames[i]] = [
                    vector := c_vectors[i],
                    Chord.get_colourTian_from_chromaVector(vector)
                ]
    for i in ChordAttrs.items():
        print(i)
    for chord in ChordAttrs:
        ChordAttrs[chord] = NoIndent(ChordAttrs[chord])
    with open('ChordAttr.json', 'wb') as wf:
        wf.write(json.dumps(ChordAttrs,
                            indent=2, ensure_ascii=False, cls=MyEncoder).encode('utf-8'))
