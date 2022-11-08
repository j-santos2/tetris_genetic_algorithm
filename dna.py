import numpy as np


# Weights starting range
GEN_LOW = -0.5
GEN_HIGH = 0.5

# Mutation probability
MUTATION_RATE = .05
# Mutation strength
MUTATION_STEP = .2

# Number of parameters taken into account
# 1 weight per parameter
NUM_PARAMETERS = 7
# aggregated_height, n_holes, adj_abs_height_diff, cleared, num_empty_cols, n_cols_with_holes, high peak

class Dna:
    """Holds genes for a player."""
    def __init__(self, genes = None):
        """If genes are provided those are used, otherwise random ones are generated."""
        self.genes = genes if genes else np.random.uniform(low=GEN_LOW, high=GEN_HIGH, size=NUM_PARAMETERS)

    def crossover(self, other_dna):
        new_genes = [0] * len(self.genes)
        for i in range(len(self.genes)):
            new_genes[i] = self.genes[i] if np.random.choice([True, False]) else other_dna.genes[i]
        new_dna = Dna(new_genes)
        new_dna.mutate()
        return new_dna

    def mutate(self, mutation_rate=MUTATION_RATE):
        for i in range(len(self.genes)):
            if mutation_rate > np.random.random():
                self.genes[i] = self.genes[i]  + MUTATION_STEP * (np.random.uniform(low=0, high=1) * 2 - 1)
