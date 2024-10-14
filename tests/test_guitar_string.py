import unittest

from hamcrest import assert_that, equal_to

from guitar_practice.guitar_string import NoteState, Note, NoteType, String


class TestNoteState(unittest.TestCase):

    def test_note_state(self):
        note = NoteState(Note.A)
        assert_that(note.note, equal_to(Note.A))
        assert_that(note.note_type, equal_to(NoteType.REGULAR))

    def test_note_state_next(self):
        note = NoteState(Note.G)
        next_note = note.next()
        assert_that(next_note, equal_to(note))
        assert_that(note.note, equal_to(Note.A))
        assert_that(note.note_type, equal_to(NoteType.REGULAR))

    def test_note_state_progress_regular(self):
        note = NoteState(Note.A, NoteType.SHARP)
        note.progress()
        assert_that(note.note, equal_to(Note.B))
        assert_that(note.note_type, equal_to(NoteType.REGULAR))

    def test_note_state_progress_sharp(self):
        note = NoteState(Note.C)
        note.progress()
        assert_that(note.note, equal_to(Note.C))
        assert_that(note.note_type, equal_to(NoteType.SHARP))


class TestString(unittest.TestCase):

    def test_string_find_note_one(self):
        string = String.B
        note = NoteState(Note.E)
        assert_that(string.find(note), equal_to(5))

    def test_string_find_note_two(self):
        string = String.E_LOW
        note = NoteState(Note.D)
        assert_that(string.find(note), equal_to(10))

    def test_string_find_note_behind(self):
        string = String.E_HIGH
        note = NoteState(Note.B)
        assert_that(string.find(note), equal_to(7))

    def test_string_major_of(self):
        string = String.D
        note = NoteState(Note.A)
        major_scale: [int] = string.major_of(note)
        actual_positions: [int] = [position for position, _ in major_scale]
        assert_that(actual_positions, equal_to([7, 9, 11, 12, 14, 16, 18, 29]))


if __name__ == '__main__':
    unittest.main()
