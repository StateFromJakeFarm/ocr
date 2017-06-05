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

    def __init__(self, train_dir, structure_file, weights_file, alpha, iters):
        """Constructor simply sets meta member variables"""
        self.train_dir = train_dir
        self.structure_file = structure_file
        self.weights_file = weights_file
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

    def build_structure(self):
        """Construct the Neuron web based on the structure file"""
        with open(self.structure_file, 'r') as file:
            layer_depths = ['1'] + file.read().split('\n')[:-1]
            self.layers = [[ANN.Neuron() for n in range(int(l))] for l in layer_depths]
            file.close()

    def assign_all_weights(self, dummy=0.01, mini=-10, maxi=10):
        """Assign all the Neurons their starting (or testing) weights"""
        # Set all dummy neuron weights and use 2-d list to store weights
        for l in range(len(self.layers[1:])):
            this_layer_weights = []
            for n in range(len(self.layers[l+1])):
                this_layer_weights.append(dummy)
            self.layers[0][0].weights.append(this_layer_weights)

        all_lines = []
        # Grab weights from file
        if self.weights_file:
            with open(self.weights_file, 'r') as file:
                all_lines = file.read().split('\n')[:-1]
                file.close()
        # Randomize starting weights
        else:
            for l in range(len(self.layers[1:-1])):
                for n in self.layers[l+1]:
                    weights_ln = ''
                    for w in self.layers[l+2]:
                        weights_ln += str( random.randint(mini, maxi) ) + ' '
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

    def save_network(self):
        """Save the structure and learned weights for this network"""
        pass
