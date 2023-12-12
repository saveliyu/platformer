level_map = [
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'X                          X     X',
    'X                          X     X',
    'X                          X     X',
    'X                          X     X',
    'X                          G     X',
    'X                                X',
    'X       B           P B          X',
    'X   LXXXXXXXXXXXXTTXXXXXXXXXXXXXXX',
    'X   LX                            ',
    'X   LX                            ',
    'X   LX                            ',
    'X   LX                            ',
    'X   LX                            ',
    'X   LX                            ',
    'XTTXXX                               ']
# во сколько раз увеличивать все спрайты
scaling = 2

tile_size = 16 * scaling
screen_width = 1200
screen_height = tile_size * len(level_map)
