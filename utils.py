import numpy as np


def get_binary_board(tetris):
    """Return board as a binary array."""
    board = np.asarray(tetris.game_area())
    return np.where(board != 47, 1, 0)

def get_board_info(board, tetris, cleared_lines_before):
    """Calculates and returns parameters for a game state."""
    # Columns heights
    peaks = get_peaks(board)
    highest_peak = np.max(peaks) 
    highest_peak_weighted = highest_peak ** 1.5
    # Aggregated height
    aggregated_height = np.sum(peaks)

    holes = get_holes(peaks, board)
    # Number of empty holes
    n_holes = np.sum(holes)
    # Number of columns with at least one hole
    n_cols_with_holes = np.count_nonzero(np.array(holes) > 0)

    # Height differences between adjacent cols sum
    adj_height_diff_sum = get_adj_height_diff_sum(peaks)

    # Number of cols with zero blocks
    num_empty_cols = np.count_nonzero(np.count_nonzero(board, axis=0) == 0)

    # The number of lines gained with the move
    cleared = (tetris.lines - cleared_lines_before) * 10
    
    row_tran = get_row_transition(board, highest_peak)

    col_tran = get_col_transition(board, peaks)

    return aggregated_height, n_holes, adj_height_diff_sum, cleared, \
        num_empty_cols, n_cols_with_holes, highest_peak_weighted#, row_tran, col_tran

def get_peaks(board):
    """Returns peak heights per column."""
    peaks = np.array([])
    for col in range(board.shape[1]):
        # If column != empty
        if 1 in board[:, col]:
            # Height - empty spaces from top
            p = board.shape[0] - np.argmax(board[:, col], axis=0)
            peaks = np.append(peaks, p)
        else:
            # No block => no peak
            peaks = np.append(peaks, 0)
    return peaks

def get_adj_height_diff_sum(peaks):
    """Returns the sum of height changes between adjacent columns."""
    h_diff = 0
    for i in range(9):
        h_diff += np.abs(peaks[i] - peaks[i + 1])
    return h_diff


def get_holes(peaks, board):
    """Returns amount of holes per column."""
    holes = []
    for col in range(board.shape[1]):
        peak = -peaks[col]
        # No peaks => no blocks
        if peak == 0:
            holes.append(0)
        else:
            # From peak to bottom count empty spaces
            holes.append(np.count_nonzero(board[int(peak):, col]))
    return holes

def get_row_transition(area, highest_peak):
    sum = 0
    # From highest peak to bottom
    for row in range(int(area.shape[0] - highest_peak), area.shape[0]):
        for col in range(1, area.shape[1]):
            if area[row, col] != area[row, col - 1]:
                sum += 1
    return sum


def get_col_transition(area, peaks):
    sum = 0
    for col in range(area.shape[1]):
        if peaks[col] <= 1:
            continue
        for row in range(int(area.shape[0] - peaks[col]), area.shape[0] - 1):
            if area[row, col] != area[row + 1, col]:
                sum += 1
    return sum

def calculate_move_score(params, weights):
    """Returns move value given the calculated parameters from the move and weights"""
    score = 0
    for i in range(params):
        score += params[i] * weights[i]
    return score
