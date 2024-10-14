from survey import routines

from guitar_practice.guitar_string import String, NoteState, Note


def prompt_user():
    options_string: dict[str, String] = dict((string.name, string) for string in String)
    options_note: dict[str, NoteState] = dict((note.name, NoteState(note)) for note in Note)

    # Ask user to keep going or stop
    running: bool = True
    while running:
        string_index: int = routines.select('Pick a string: ', options=options_string)
        string_choice: String = list(options_string.values())[string_index]

        note_index: int = routines.select('Pick a note: ', options=options_note)
        note_choice: NoteState = list(options_note.values())[note_index]

        routines.inquire('Play the major scale of the note. Continue? ', default=True)

        major: [NoteState] = string_choice.major_of(note_choice)

        print()
        print(f'Offset: {string_choice} {major[0][0]}\n')
        for position, note_state in major[1:]:
            print(f'{note_state}\t{string_choice} {position}')
        print()

        running = routines.inquire('Another round? ', default=True)
        if not running:
            print('Goodbye!')


if __name__ == '__main__':
    prompt_user()