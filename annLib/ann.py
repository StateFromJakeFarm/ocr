import os

# Class to execute the artificial neural network
class ANN:
    # Nested class for individual neurons
    class Neuron:
        def __init__(self, weights):
            self.weights = weights[:]

    # Constructor simply sets meta member variables
    def __init__(self, train_dir, structure_file, alpha, iters):
        self.train_dir = train_dir
        self.structure_file = structure_file
        self.alpha = alpha
        self.iters = iters

        # Members set internally
        self.num_chars = 0
        self.neurons = []

    def get_num_chars(self):
        found_chars = []
        for filename in os.listdir(self.train_dir):
            this_char = filename[0]
            if this_char not in found_chars:
                found_chars.append(this_char)

        self.num_chars = len(found_chars)
