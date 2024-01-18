level_map = [
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'X                                     X     X',
    'X                                     X     X',
    'X                                     X     X',
    'X                                     X     X',
    'X                                     G     X',
    'X                                           X',
    'X                             B             X',
    'X            LXXXXXXXXXXXXTTXXXXXXXXXXXXXXXXX',
    'X            LX                              ',
    'X            LX                              ',
    'X            LX                              ',
    'X            LX                              ',
    'X            LX                              ',
    'X       P    LX                              ',
    'XXTTTTXXXXXXXXX                              ']
# во сколько раз увеличивать все спрайты
scaling = 2

tile_size = 16 * scaling
screen_width = 1200
screen_height = tile_size * len(level_map)
