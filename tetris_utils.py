import io


def save_game_state(pyboy):
    state = io.BytesIO()
    state.seek(0)
    pyboy.save_state(state)
    return state

def load_game_state(pyboy, state):
    state.seek(0)
    pyboy.load_state(state)

def get_block(pyboy):
    return get_current_block_text(pyboy.get_memory_value(0xc203))

def get_current_block_text(block_value):
    if 0 <= block_value <= 3:
        return 'L'
    elif 4 <= block_value <= 7:
        return 'J'
    elif 8 <= block_value <= 11:
        return 'I'
    elif 12 <= block_value <= 15:
        return 'O'
    elif 16 <= block_value <= 19:
        return 'Z'
    elif 20 <= block_value <= 23:
        return 'S'
    elif 24 <= block_value <= 27:
        return 'T'
