def demo():
    import colour
    import superprompt
    import colorama
    colorama.init()
    from unicorn.core import Terminal

    term = Terminal()

    while True:
        try:
            color = superprompt.prompt_choice('>', colour.COLOR_NAME_TO_RGB, prompt_suffix=' ', only_in_poss=False)
        except KeyboardInterrupt:
            break

        try:
            func = getattr(term, color)
        except AttributeError:
            pass
        else:
            print(func('Coucou !'))

if __name__ == '__main__':
    demo()
