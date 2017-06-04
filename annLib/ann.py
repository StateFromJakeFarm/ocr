import os
import math
import random

# Class to execute the artificial neural network
class ANN:
    # Nested class for individual neurons
    class Neuron:
        def __init__(self):
            self.weights = []

        # Assign the Neuron its weights
        def assign_weights(self, weights_line):
            self.weights = [float(w) for w in weights_line.strip(' ').split(' ')]
            print(self.weights)

    # Constructor simply sets meta member variables
    def __init__(self, train_dir, structure_file, weights_file, alpha, iters):
        self.train_dir = train_dir
        self.structure_file = structure_file
        self.weights_file = weights_file
        self.alpha = alpha
        self.iters = iters

        # Members set internally
        self.num_chars = 0
        self.layers = []

    # Get the number of characters we are training on
    def get_num_chars(self):
        found_chars = []
        for filename in os.listdir(self.train_dir):
            this_char = filename[0]
            if this_char not in found_chars:
                found_chars.append(this_char)

        self.num_chars = len(found_chars)

    # Construct the Neuron web based on the structure file
    def build_structure(self):
        with open(self.structure_file, 'r') as file:
            layer_depths = ['1'] + file.read().split('\n')[:-1]
            self.layers = [[ANN.Neuron() for n in range(int(l))] for l in layer_depths]
            file.close()

    # Assign all the Neurons their starting (or testing) weights
    def assign_all_weights(self, mini=-10, maxi=10):
        all_lines = []

        # Grab weights from file
        if self.weights_file:
            with open(self.weights_file, 'r') as file:
                all_lines = file.read().split('\n')[:-1]
                file.close()
        # Randomize starting weights
        else:
            for l in range(len(self.layers[1:-1])):
                print("l = " + str(l))
                for n in self.layers[l+1]:
                    print("  n = " + str(n))
                    weights_ln = ''
                    for w in self.layers[l+2]:
                        print("    w = " + str(w))
                        weights_ln += str( random.randint(mini, maxi) ) + ' '
                    all_lines.append(weights_ln)

                    if l != len(self.layers):
                        all_lines.append('')

        # Assign weights to each neuron
        l = 1
        n = 0
        for line in all_lines:
            if line == '' or line == '\0':
                l += 1
                n = 0
            else:
                self.layers[l][n].assign_weights(line)
