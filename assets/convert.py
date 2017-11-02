import re
import unicorn
import colorama

colorama.init()

# COLOR_RE = re.compile(r"^.*?\|hex=(?P<hex>[0-9A-Fa-f]{6}).*?\|name=((\[\[[^\|]*?(\|(?P<name>.*?))|(?P<name2>.*?))|(?P<name3>.*?))[\]\}].*$")
COLOR_RE = re.compile(r"^.*?\|hex=(?P<hex>[0-9A-Fa-f]{6}).*?\|name=((\[\[[^\]\|\}]*?\|)|(\[\[))?(?P<name>[^\]\}]*)")
NICE_COLOR_RE = re.compile('(#[0-9A-Fa-f]*?) (.*)')
TERM = unicorn.Terminal()
FILE = 'colors.csv'


def convert():
    FILEBKP = 'colors.bkp.csv'

    with open(FILEBKP) as file:
        text = file.read().splitlines(keepends=False)

    for i, line in enumerate(text[:]):
        match = re.match(COLOR_RE, line)

        if match:
            # continue
            with TERM.green:
                # print(line)
                name = match.group('name')
                if len(name) > 30:
                    print(line)
                    print(name)
                    name = input()
                text[i] = '#%s %s' % (match.group('hex'), name)
                print(text[i])
        else:
            with TERM.orange:
                print(line)

    with open(FILE, 'w') as file:
        file.write('\n'.join(text))


def correct():
    with open('colors') as file:
        text = file.read().splitlines(keepends=False)

    for i, line in enumerate(text[:]):

        hex, name = re.match(NICE_COLOR_RE, line).groups()
        for char in ' ()-\'’.#':
            name = name.replace(char, '')  # type: str
        name = name.replace('é', 'e')
        name = name.replace('&', 'and')
        name = name.partition('/')[0]
        name = name.partition('|')[0]
        if name.isidentifier():
            with TERM.lightgreen:
                print(hex, name)
        else:
            with TERM.Orange:
                print(hex, name)

        text[i] = '%s %s' % (hex, name)

    with open('colors', 'w') as f:
        f.write('\n'.join(text))



if __name__ == '__main__':
    correct()
