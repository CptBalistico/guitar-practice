import copy
from enum import Enum

from multipledispatch import dispatch


class NoteType(Enum):
    SHARP = '#'
    FLAT = '♭'
    REGULAR = ''

    def __str__(self):
        return self.value


class Note(Enum):
    A = (1, 1, 1)
    B = (2, 0, 1)
    C = (3, 1, 0)
    D = (4, 1, 1)
    E = (5, 0, 1)
    F = (6, 1, 0)
    G = (7, 1, 1)

    def __init__(self, num: int, next_dist: int, prev_dist: int):
        self.num = num
        self.next_dist = next_dist
        self.prev_dist = prev_dist

    def next(self):
        next_num: int = (self.num % 7) + 1
        for note in Note:
            if note.num == next_num:
                return note
        raise ValueError(f"Could not find next note for {self}")

    def has_sharp(self) -> bool:
        return self.next_dist == 1

    def has_flat(self) -> bool:
        return self.prev_dist == 1

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class NoteState:

    def __init__(self, note: Note, note_type: NoteType = NoteType.REGULAR):
        self.note = note
        self.note_type = note_type

    def progress(self):
        match self.note_type:
            case NoteType.SHARP:
                self.next()
                self.note_type = NoteType.REGULAR
            case NoteType.FLAT:
                raise NotImplementedError("Not implemented")
            case NoteType.REGULAR:
                if self.note.has_sharp():
                    self.note_type = NoteType.SHARP
                else:
                    self.next()
                    self.note_type = NoteType.REGULAR
        return self

    @dispatch()
    def next(self) -> 'NoteState':
        self.note = self.note.next()
        return self

    @dispatch(int)
    def next(self, jumps: int) -> 'NoteState':
        for i in range(jumps):
            self.progress()
        return self

    def go_to(self, note: Note) -> int:
        shift_count: int = 0
        while self.note != note:
            self.next()
            shift_count += 1
        return shift_count

    def __str__(self):
        return f'{self.note}{self.note_type}'

    def __repr__(self):
        return self.__str__()


class String(Enum):
    E_LOW = (1, Note.E)
    A = (2, Note.A)
    D = (3, Note.D)
    G = (4, Note.G)
    B = (5, Note.B)
    E_HIGH = (6, Note.E)

    def __init__(self, num: int, note: Note):
        self.num = num
        self.note = note

    def __str__(self):
        return self.name

    def major_of(self, note_state: NoteState) -> [(int, NoteState)]:
        major_scale_intervals: [int] = [2, 2, 1, 2, 2, 2, 1]
        shift_count: int = self.find(note_state)
        current_position: int = shift_count
        major: [NoteState] = [copy.deepcopy((current_position, note_state))]
        for interval in major_scale_intervals:
            current_position += interval
            major.append(copy.deepcopy((current_position, note_state.next(interval))))
        return major

    def find(self, note_state: NoteState) -> int:
        current_note: Note = self.note
        shift_count: int = 0
        # if current_note.has_sharp():
        #     shift_count += 1
        while current_note != note_state.note:
            if current_note.has_sharp():
                shift_count += 2
            else:
                shift_count += 1
            current_note = current_note.next()
        return shift_count

"""


F 1
G 3
A 5
B 7
C 8
D 10

"""
