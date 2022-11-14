import logging
import uuid

import numpy as np
from pathos.helpers import cpu_count
from pathos.multiprocessing import ProcessingPool as Pool
from pyboy import PyBoy

from actions import drop, move_sides, turn, apply_actions
from blocks import number_of_moves_possible, number_of_turns_possible
from dna import Dna
from tetris_utils import save_game_state, load_game_state, get_block
from utils import get_board_info, get_binary_board

# Popoulation size (number of players)
SIZE = 20
# Number of generations to train
GENERATIONS = 15

# Set pyboy logger level to ERROR only
pyboy_logger = logging.getLogger('pyboy')
pyboy_logger.setLevel(logging.ERROR)

# Create logger to write results
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

log_formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
# Log to console 
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.INFO)
root_logger.addHandler(console_handler)
# Log to file
file_handler = logging.FileHandler('training.log')
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.DEBUG)
root_logger.addHandler(file_handler)


class Population:
    def __init__(self, size = SIZE, generations=GENERATIONS, play_weights=None, show_best=False):
        self.size = size
        self.generations = 0
        self.total_generations = generations
        self.players = []
        self.play_weights = play_weights
        self._show_best = show_best

    def train(self):
        """Creates tetris instance and runs players"""
        init = True
        self.players = []
        
        for j in range(self.total_generations):
            if init:
                for i in range(self.size):      
                        player = Player(uuid.uuid4(), Dna())
                        self.players.append(player)
            else:
                self.evolve()
            init = False
            root_logger.info(f'STARTING GENERATION {j} TRAINING')
            # CPU DISPONIBLES - 2
            cpus = cpu_count()-2 if cpu_count()>2 else 1
            pool = Pool(cpus)
            ps = pool.map(self._launch_player_train, [i for i in range(self.size)])
            self.players = ps  
        
    def evolve(self):
        root_logger.info(f'GEN {self.generations} evaluated')
        gen_fitnesses = [p.fitness for p in self.players]
        root_logger.info(f'GEN {self.generations} avg fitness: {np.average(gen_fitnesses)}')
        sorted_players = sorted(self.players, key= lambda t: t.fitness, reverse=True)
        # reset players
        new_players = []
        # add best player
        new_players.append(sorted_players[0])
        root_logger.info(f'Elite fitness {new_players[0].id}: {new_players[0].fitness}')
        # select top .5
        selected = sorted_players[:int(len(sorted_players)/3)]
        selected_dna = [a.dna for a in selected]

        def get_random_dna(dna_list):
            return np.random.choice(dna_list)

        for _ in range(SIZE-1):
            new_players.append(Player(uuid.uuid4(), get_random_dna(selected_dna).crossover(get_random_dna(selected_dna))))

        self.generations += 1

        self.players = new_players        

    def play(self):
        pyboy = PyBoy('tetris.gb', game_wrapper=True)
        pyboy.set_emulation_speed(0)
        tetris = pyboy.game_wrapper()
        tetris.start_game()

        # Set block animation to fall instantly
        pyboy.set_memory_value(0xff9a, 2)

        self.players = [Player(uuid.uuid4(), Dna(self.play_weights))]
        self.players[0].run_child(pyboy, tetris, train=False)

        pyboy.stop()

    def _launch_player_train(self, idx):
        if idx == 0 and self._show_best:
            pyboy = PyBoy('tetris.gb', game_wrapper=True)  
        else:
            pyboy = PyBoy('tetris.gb', window_type="headless", game_wrapper=True)
        pyboy.set_emulation_speed(0)
        tetris = pyboy.game_wrapper()
        tetris.start_game()
        root_logger.debug(f'Starting player index {idx}')
        self.players[idx].run_child(pyboy, tetris)
        root_logger.debug(f'Finished player index  {idx}')
        pyboy.stop()
        return self.players[idx]

class Player:
    def __init__(self, _id, dna):
        self.id = _id
        self.dna = dna
        self.fitness = 0

    def calculate_move_score(self, tetris, cleared_lines):
        score = 0
        board = get_binary_board(tetris)
        params = get_board_info(board, tetris, cleared_lines)
        for i in range(len(params)):
            score += params[i] * self.dna.genes[i]
        return score

    def run_child(self, pyboy, tetris, train=True):
        max_score = 99999

        block_placed = 0
        lost = False
        won = False

        while True:
            # Beginning of action
            best_action_score = np.NINF
            best_action = {'turn': 0, 'left': 0, 'right': 0}
            begin_state = save_game_state(pyboy)
            # Cleared of lines before placing new block
            cleared_lines = tetris.lines

            # Gets block type, number of posible rotations and moves
            block = get_block(pyboy)
            turns_needed = number_of_turns_possible(block)
            lefts_needed, rights_needed = number_of_moves_possible(block)

            # No moving
            for turns in range(turns_needed):
                move_dir = apply_actions(pyboy, 'none', n_move=0, n_turn=turns)
                score = self.calculate_move_score(tetris, cleared_lines)
                if score is not None and score >= best_action_score:
                    best_action_score = score
                    best_action = {'turn': move_dir['turn'],
                                'left': move_dir['left'],
                                'right': move_dir['right']}
                load_game_state(pyboy, begin_state)

            # Left moves
            for turns in range(turns_needed):
                for moves_needed in range(1, lefts_needed + 1):
                    move_dir = apply_actions(pyboy, 'left', n_move=moves_needed, n_turn=turns)
                    score = self.calculate_move_score(tetris, cleared_lines)
                    if score is not None and score >= best_action_score:
                        best_action_score = score
                        best_action = {'turn': move_dir['turn'],
                                    'left': move_dir['left'],
                                    'right': move_dir['right']}
                    load_game_state(pyboy, begin_state)

            # Right moves
            for turns in range(turns_needed):
                for moves_needed in range(1, rights_needed + 1):
                    move_dir = apply_actions(pyboy, 'right', n_move=moves_needed, n_turn=turns)
                    score = self.calculate_move_score(tetris, cleared_lines)
                    if score is not None and score >= best_action_score:
                        best_action_score = score
                        best_action = {'turn': move_dir['turn'],
                                    'left': move_dir['left'],
                                    'right': move_dir['right']}
                    load_game_state(pyboy, begin_state)

            # Do best move
            for _ in range(best_action['turn']):
                turn(pyboy)
            for _ in range(best_action['left']):
                move_sides(pyboy, 'left')
            for _ in range(best_action['right']):
                move_sides(pyboy, 'right')

            drop(pyboy)
            pyboy.tick()
            block_placed += 1

            # End conditions
            if tetris.game_over():
                lost = True
                break      
            elif tetris.score == max_score:
                won = True
                break
        
        root_logger.debug(f'{self.id}\t| Blocks placed: {block_placed}')
        root_logger.debug(f'{self.id}\t| Lost: {lost}')
        root_logger.debug(f'{self.id}\t| Win: {won}')
        
        win_reward = 9999 if won else 0

        # Set fitness
        # Score + small increase for each level completed + win reward
        self.fitness = tetris.score + int(tetris.level/10 * tetris.score) + win_reward

        tetris.reset_game()
        root_logger.debug(f'{self.id}\t| Fitness: {self.fitness}')
        root_logger.debug(f'{self.id}\t| Final Weights: {self.dna.genes}')

if __name__ == '__main__':
    p = Population(show_best=True)
    p.train()
