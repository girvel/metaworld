def choose(options, skip=(False, None)):
    can_be_skipped, default = skip

    print()
    for i, option in enumerate(options):
        print(f'{i + 1}. {option["line"]}')

    while True:
        try:
            o = options[int(input("> ")) - 1]
            print()
            return o
        except (ValueError, IndexError):
            if can_be_skipped:
                return default


def play_lines(lines, script_args):
    for line in lines:
        if callable(line):
            line(**script_args)
        else:
            print(line, end='')
            if not __debug__:
                input()
            else:
                print()


def describe_interior(states):
    print()
    for _, state in states.items():
        if 'line' in state:
            print(state['line'])
            print()


def finish_the_game():
    input("The end!")
    exit()