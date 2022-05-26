import re
from pathlib import Path

import termcolor
import colorama
colorama.init()


def draw(file):
    text = Path(file).read_text()

    for target, fg in [
        (r'(\(~+\))', 'blue'),
        (r'\b(o)\b', 'yellow'),
        (r'(\(X\))', 'red'),
    ]:
        text = re.sub(target, termcolor.colored(r'\1', fg), text)

    print(text)

if __name__ == '__main__':
    draw('map_of_southern_provinces.txt')
    print(termcolor.COLORS)
