import random
import functools
import operator
import time

a: dict = {'a': [0, 12], 'b': [2, 14], 'c': [3, 15], 'd': [5], 'e': [7], 'f': [8], 'g': [10]}
e_low: dict = {'e': [0, 12], 'f': [1, 13], 'g': [3, 15], 'a': [5], 'b': [7], 'c': [8], 'd': [10]}

strings = {
    # 'e-high': {},
    # 'b': {},
    # 'g': {},
    # 'd': {},
    'a': a,
    'e-low': e_low
}


"""
A note has a + 1 (non-existing) number.

    Positive example: the F note is 1, the F# note is 2.
    Negative example: the B note is 7, the B# note is 8 (illegal).

Expected for low-e: {'f#': [2], 'g#': [4], 'a#': [6], 'c#': [9], 'd#': [11]}
"""
def get_sharp_notes(notes: dict):

    sharp_notes: dict = dict()
    note_positions: list = functools.reduce(operator.iconcat, notes.values(), [])

    for note, positions in notes.items():
        for position in positions:

            if not is_eligible_sharp(position, note_positions):
                continue

            sharp_note = note + "#"
            sharp_position = position + 1

            if sharp_note not in sharp_notes:
                sharp_notes[sharp_note] = [sharp_position]
            else:
                sharp_notes[sharp_note].append(sharp_position)

    return sharp_notes


# A note has a -1 (non-existing) number. This number cannot be negative.
def get_flat_notes(notes: dict):
    flat_notes: dict = dict()
    note_positions: list = functools.reduce(operator.iconcat, notes.values(), [])

    for note, positions in notes.items():
        for position in positions:

            if not is_eligible_flat(position, note_positions):
                continue

            flat_note = note + "♭"
            flat_position = position - 1

            if flat_note not in flat_notes:
                flat_notes[flat_note] = [flat_position]
            else:
                flat_notes[flat_note].append(flat_position)

    return flat_notes


def is_eligible_sharp(position: int, positions: list):
    return not (position < 1 or position > 11 or position + 1 in positions)


def is_eligible_flat(position: int, positions: list):
    return not (position < 1 or position > 12 or position - 1 in positions)


def prompt():
    pick = random.choice(list(strings.keys()))
    print("String: " + pick)
    pick = strings[pick]

    sharp_notes = get_sharp_notes(pick)
    flat_notes = get_flat_notes(pick)

    # add sharp notes
    for sharp_note, positions in sharp_notes.items():
        pick[sharp_note] = positions

    # add flat notes
    for flat_note, positions in flat_notes.items():
        pick[flat_note] = positions

    original_size = len(pick.values())

    while pick.values():
        note = random.choice(list(pick.keys()))
        print(f"[{original_size - len(pick.values())}/{original_size}] {str.upper(note)}", end=" ", flush=True)
        time.sleep(2)
        print(f"{', '.join([str(x) for x in pick[note]])}", flush=True)
        answer = input("Did you guess correctly? (y/n): ")
        if answer.strip().startswith("y"):
            dict.pop(pick, note)
        elif answer.strip().startswith("n"):
            continue
        else:
            print("Invalid input. Please try again.", flush=True)
            continue

    print("\nCongratulations! You have completed the exercise.")


if __name__ == '__main__':
    prompt()
