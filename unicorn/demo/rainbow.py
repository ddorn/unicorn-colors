import colorsys
import random
from time import sleep

import sys

from unicorn import Terminal


def deg_to_rgb(deg):
    rgb = colorsys.hsv_to_rgb(deg, 1, 1)
    return map(lambda x: int(x * 255), rgb)




def main():

    TERM = Terminal()

    FULL = len(sys.argv) >= 2 and sys.argv[1].lower() in ('true', 'yes', 'full', 'y')
    MAX_Y = 25
    MIN_Y = 5
    WIDTH = TERM.width
    NCATS = WIDTH // 3 if FULL else 7
    SCROLL_SPEED = 4 if FULL else 20
    LOOP = 42 * SCROLL_SPEED

    if FULL:
        cats_x = list(range(0, WIDTH, 3))
    else:
        cats_x = []
        while len(cats_x) < NCATS:
            x = random.randint(0, WIDTH - 4)
            for catx in cats_x:
                if x in range(catx - 3, catx + 3):
                    break
            else:
                cats_x.append(x)
    cats_y = [10] * NCATS
    cats_offset = [random.randint(0, LOOP) for _ in range(NCATS)]
    cats_speed = [1] * NCATS

    def show_cat(i):
        with TERM.on_rgb(*deg_to_rgb((turn + cats_offset[i]) % LOOP / LOOP)):
            TERM.move(cats_y[i], cats_x[i])
            print('   ', end='')


    turn = 0
    with TERM.move:
        with TERM.hide_cursor:
            while True:

                turn += 1

                if turn % SCROLL_SPEED == 0:
                    TERM.scroll(1)
                    for cat in range(NCATS):
                        cats_y[cat] -= 1

                for cat in range(NCATS):
                    if turn % cats_speed[cat] == 0:
                        cats_y[cat] += 1
                    if cats_y[cat] > MAX_Y:
                        cats_speed[cat] = random.randint(SCROLL_SPEED + 1, 2 * SCROLL_SPEED)
                    if cats_y[cat] < MIN_Y:
                        cats_speed[cat] = random.randint(SCROLL_SPEED // 2, SCROLL_SPEED - 1)

                    show_cat(cat)

                # sleep(0.001)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        quit(0)
