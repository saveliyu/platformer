level_map = [
    '                                             ',
    '                                             ',
    '                                             ',
    '                                             ',
    '                                             ',
    '                                             ',
    '                                             ',
    '                                             ',
    '                                             ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'X                                     X     X',
    'X                                     X     X',
    'X                                     X     X',
    'X                                     X     X',
    'X                                     G     X',
    'X                                           X',
    'X                             B             X',
    'X    X     X LXXXXXXXXXXXXTTXXXXXXXXXXXXXXXXX',
    'X            LX                              ',
    'X            LX                              ',
    'X            LX                              ',
    'X             X                              ',
    'X             X                              ',
    'X   P         X                              ',
    'XXXXXXXXXXXXXXX                              ']
# во сколько раз увеличивать все спрайты
scaling = 1

tile_size = 16 * scaling
screen_width = 600
screen_height = tile_size * len(level_map)
