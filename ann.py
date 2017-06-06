import os
import math
import random

class ANN:
    """Class to execute the artificial neural network"""
    class Neuron:
        """Nested class for individual neurons"""
        def __init__(self):
            self.weights = []

        def assign_weights(self, weights_line):
            """Assign the Neuron its weights"""
            self.weights = [float(w) for w in weights_line.strip(' ').split(' ')]

    def __init__(self, train_dir, structure_file, alpha, iters):
        """Constructor simply sets meta member variables"""
        self.train_dir = train_dir
        self.structure_file = structure_file
        self.alpha = alpha
        self.iters = iters

        # Members set internally
        self.num_chars = 0
        self.layers = []

    def get_num_chars(self):
        """Get the number of characters we are training on"""
        found_chars = []
        for filename in os.listdir(self.train_dir):
            this_char = filename[0]
            if this_char not in found_chars:
                found_chars.append(this_char)

        self.num_chars = len(found_chars)

    def build_structure(self, file):
        """Construct the Neuron web based on the structure file"""
        layer_depths = ['1'] + file.readline().strip('\n').split(' ')
        self.layers = [[ANN.Neuron() for n in range(int(l))] for l in layer_depths]

    def assign_all_weights(self, file, dummy=0.01, mini=-0.5, maxi=0.5):
        """Assign all the Neurons their starting (or testing) weights"""
        # Set all dummy neuron weights and use 2-d list to store weights
        for l in range(len(self.layers[1:])):
            this_layer_weights = []
            for n in range(len(self.layers[l+1])):
                this_layer_weights.append(dummy)
            self.layers[0][0].weights.append(this_layer_weights)

        # Attempt to grab weights from file
        all_lines = file.read().split('\n')[:-1]

        # Randomize starting weights if file does not specify weights
        if len(all_lines) <= 0:
            for l in range(len(self.layers[1:-1])):
                for n in self.layers[l+1]:
                    weights_ln = ''
                    for w in self.layers[l+2]:
                        weights_ln += str( random.uniform(mini, maxi) ) + ' '
                    all_lines.append(weights_ln)

        # Assign weights to each neuron
        l = 1
        n = 0
        for line in all_lines:
            if line == '' or line == '\0':
                l += 1
                n = 0
            else:
                self.layers[l][n].assign_weights(line)

    def build(self):
        """Construct the network and load weights (if any)"""
        with open(self.structure_file, 'r') as file:
            self.build_structure(file)
            self.assign_all_weights(file)
            file.close()

    def save_network(self):
        """Save the structure and learned weights for this network"""
        pass
