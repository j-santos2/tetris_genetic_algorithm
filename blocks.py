BLOCK_TURNS = {
    'O': 1,
    'I': 2,
    'S': 2,
    'Z': 2,
    'L': 4,
    'J': 4,
    'T': 4
}

BLOCK_MOVES = {
    'O': (4, 4),
    'I': (4, 5),
    'S': (3, 5),
    'Z': (3, 5),
    'L': (4, 5),
    'J': (4, 5),
    'T': (4, 5)
}

def number_of_turns_possible(block):
    return BLOCK_TURNS[block]

def number_of_moves_possible(block):
    return BLOCK_MOVES[block]
