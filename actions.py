from pyboy import WindowEvent

ACTIONS = {
    'down': [WindowEvent.PRESS_ARROW_DOWN, WindowEvent.RELEASE_ARROW_DOWN],
    'turn': [WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A],
    'left': [WindowEvent.PRESS_ARROW_LEFT, WindowEvent.RELEASE_ARROW_LEFT],
    'right': [WindowEvent.PRESS_ARROW_RIGHT, WindowEvent.RELEASE_ARROW_RIGHT]
}

START_HEIGHT = 24
    
    
def turn(pyboy):
    pyboy.send_input(ACTIONS['turn'][0])
    pyboy.tick()
    pyboy.send_input(ACTIONS['turn'][1])
    pyboy.tick()
    
def move_sides(pyboy, action):
    pyboy.send_input(ACTIONS[action][0])
    pyboy.tick()
    pyboy.send_input(ACTIONS[action][1])
    pyboy.tick()
    
def move_down(pyboy):
    pyboy.send_input(ACTIONS['down'][0])
    pyboy.tick()
    pyboy.send_input(ACTIONS['down'][1])

def drop(pyboy):
    """Drops block until it hits the bottom"""
    move_down(pyboy)
    # 0xc201 stores current block height
    while pyboy.get_memory_value(0xc201) != START_HEIGHT:
        move_down(pyboy)
    
def apply_actions(pyboy, side, n_move, n_turn):
    """Return pos"""
    for _ in range(n_turn):
        turn(pyboy)

    if side != 'none':
        for _ in range(n_move):
            move_sides(pyboy, side)
        
    drop(pyboy)
    
    return {
        'turn': n_turn,
        'left': n_move if side == 'left' else 0,
        'right': n_move if side == 'right' else 0
    }
