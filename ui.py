def choose(options):
    for i, option in enumerate(options):
        print(f'{i + 1}. {option["line"]}')

    while True:
        try:
            return options[int(input("> ")) - 1]
        except ValueError:
            pass
        except IndexError:
            pass


def play_lines(lines, script_args):
    for line in lines:
        if callable(line):
            line(**script_args)
        elif isinstance(line, dict) and len(line) == 1:
            for speaker, line_ in line.items():
                print(f'{speaker}: {line_}', end='')
        else:
            print(line)

        if not __debug__:
            input()
        else:
            print()


def describe_interior(states):
    for _, state in states.items():
        if 'line' in state:
            print(state['line'])
            print()


def finish_the_game():
    input("The end!")
    exit()