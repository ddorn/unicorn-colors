import colorsys
from unicorn import Terminal


def deg_to_rgb(deg):
    rgb = colorsys.hsv_to_rgb(deg, 1, 1)
    return map(lambda x: int(x * 255), rgb)

def main():

    TERM = Terminal()
    try:

        LEFT = TERM.width // 2 - 3
        TOP = TERM.height // 2 - 1

        with TERM.move:
            with TERM.virtual_screen:
                deg = 0
                while True:

                    deg += 0.0001
                    if deg > 1:
                        deg = 0

                    with TERM.on_rgb(*deg_to_rgb(deg)):
                        for i in range(3):
                            TERM.move(TOP + i, LEFT)
                            print(' ' * 6)

    except KeyboardInterrupt:
        quit(0)

if __name__ == '__main__':
    main()
