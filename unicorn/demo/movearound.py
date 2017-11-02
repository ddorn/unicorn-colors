from random import randint

import colour

from unicorn import Terminal


if __name__ == '__main__':
    TERM = Terminal()

    COLORS = list(colour.COLOR_NAME_TO_RGB)
    random_color = lambda: COLORS[randint(0, len(COLORS) - 1)]

    mini = 20, 10
    maxi = TERM.width - 20, TERM.height - 10
    random_pos = lambda: (randint(mini[1], maxi[1]), randint(mini[0], maxi[0]))

    with TERM.move:

        try:
            while True:

                TERM.move(*random_pos())
                color = 'on_' + random_color()
                with getattr(TERM, color):
                    print(' ')

        except KeyboardInterrupt:
            pass

    with TERM.lightgreen:
        print('Done')
