import os
import math
import random
import shutil
from img_funcs import get_grayscale_vals, find_chars
from basic_funcs import sort_file_by_int_key

class ANN:
    """Class to execute the artificial neural network"""
    class Neuron:
        """Nested class for individual neurons"""
        def __init__(self):
            self.weights = []
            self.a = 0
            self.err = 0

        def assign_weights(self, weights_line):
            """Assign the Neuron its weights"""
            self.weights = [float(w) for w in weights_line.strip(' ').split(' ')]

    def __init__(self, train_dir, read_dir, structure_file, alpha, iters):
        """Constructor simply sets meta member variables"""
        self.train_dir = train_dir
        self.read_dir = read_dir
        self.structure_file = structure_file
        self.alpha = alpha
        self.iters = iters
        self.encodings = {}

        # Members set internally
        self.chars = []
        self.layers = []

    def get_chars(self, file):
        """Get the number of characters we are training on"""
        # Load characters from file
        all_chars = []
        if self.train_dir:
            file.readline()
            all_chars = [f_name[0] for f_name in os.listdir(self.train_dir)] 
        # Find unique characters in training directory
        else:
            all_chars = file.readline().strip(' \n').split(' ')

        for this_char in all_chars:
            if this_char not in self.chars:
                self.chars.append(this_char)

    def build_structure(self, file):
        """Construct the Neuron web based on the structure file"""
        layer_depths = ['1'] + file.readline().strip(' \n').split(' ')
        self.layers = [[ANN.Neuron() for n in range(int(l))] for l in layer_depths]

        # Dummy neuron always has activation value of 1 (easy way to handle biases)
        self.layers[0][0].a = 1

    def assign_all_weights(self, file, dummy=0.01, mini=-0.5, maxi=0.5):
        """Assign all the Neurons their starting (or testing) weights"""
        # Attempt to grab weights from file
        all_lines = file.read().split('\n')

        # Hold values for dummy neuron
        dummies = []

        # Randomize starting weights if file does not specify weights
        if all_lines == ['']:
            for l in range(len(self.layers[1:-1])):
                for n in self.layers[l+1]:
                    weights_ln = ''
                    for w in self.layers[l+2]:
                        weights_ln += str( random.uniform(mini, maxi) ) + ' '
                    all_lines.append(weights_ln)
        # Grab the dummy neuron's saved weights
        else:
            dummies = all_lines[0].split(' ')

        # Set all dummy neuron weights and use 2-d list to store weights
        i = 0
        self.layers[0][0].weights.append([])
        for l in range(len(self.layers[1:])):
            this_layer_weights = []
            for n in range(len(self.layers[l+1])):
                # Use passed dummy neuron value if we aren't loading a network
                if len(dummies) == i:
                    dummies += [dummy]
                this_layer_weights.append(float(dummies[i]))
                i += 1
            self.layers[0][0].weights.append(this_layer_weights)

        # Assign weights to every other neuron
        i = 1
        for l in self.layers[1:-1]:
            for n in l:
                n.assign_weights(all_lines[i])
                i += 1

    def build(self):
        """Construct the network and load weights (if any)"""
        with open(self.structure_file, 'r') as file:
            self.build_structure(file)
            self.get_chars(file)
            self.assign_all_weights(file)
            self.assign_encodings()
            file.close()

    def save(self, f_name=''):
        """Save the structure and learned weights for this network"""
        while f_name == '':
            f_name = input('Enter save file name ([N/n] to skip): ')

        if f_name in ['N', 'n']:
            return

        with open(f_name, 'w') as file:
            # Save structure
            for l in range(len(self.layers[1:])):
                file.write( str(len(self.layers[l+1])) + ' ' )
            file.write('\n')

            # Save characters this network is trained for
            for char in self.chars:
                file.write(char + ' ')
            file.write('\n')

            # Save dummy neuron weights
            for l in self.layers[0][0].weights:
                for w in l:
                    file.write( str(w) + ' ' )
            file.write('\n')

            # Save all other neuron weights
            for l in self.layers[1:-1]:
                for n in l:
                    file.write( ' '.join(map(str, n.weights)) + '\n' )
            file.close()

    def assign_encodings(self):
        """Create unique encodings for all characters based on number of output nodes"""
        # VERY basic right now...
        for c, char in enumerate(sorted(self.chars)):
            self.encodings[char] = []
            for n in range(len(self.layers[-1])):
                val = 0.1
                if c == n:
                    val = 0.9

                self.encodings[char].append(val)

    def activation(self, in_sum):
        """Activation function"""
        return 1.0 / (1 + math.exp(-1*in_sum))

    def calc_activations(self, img_file_path):
        """Function to calculate neuron activation values"""
        # Use image grayscale values as activation values for first layer (1)
        pix_vals = get_grayscale_vals(img_file_path)
        pix_vals_len = len(pix_vals)
        for i in range(len(self.layers[1])):
            # The area-based resize can come up slightly short of actual desired area,
            # so assume all pixels that got cut-off are blank
            pix_val = 255
            if i < pix_vals_len:
                pix_val = pix_vals[i]

            self.layers[1][i].a = pix_val / 255.0

        # Calculate activation values for all other neurons (2, 3)
        for l, current_layer in enumerate(self.layers[2:]):
            l += 2
            for n in range(len(current_layer)):
                # Start with weight from dummy neuron (because it's activation always = 1)
                in_sum = self.layers[0][0].weights[l][n]

                # Add weight * activation for all neurons in previous layer
                for prev in self.layers[l-1]:
                    weight_to_current = prev.weights[n]
                    prev_activation   = prev.a

                    in_sum += prev_activation * weight_to_current

                # Set the current neuron's activation value using chosen activation function
                self.layers[l][n].a = self.activation(in_sum)

    def get_most_likely(self):
        """Return the most likely character"""
        lowest_dist = None
        most_likely = ''

        for char, char_vals in self.encodings.items():
            dist_sum = 0
            i = 0
            for neuron in self.layers[-1]:
                dist_sum += (neuron.a - char_vals[i])**2
                i += 1

            euclid_dist = math.sqrt(dist_sum)
            if lowest_dist is None or euclid_dist < lowest_dist:
                most_likely = char
                lowest_dist = euclid_dist

        return most_likely

    def backpropagate(self, norm=255):
        """Run main backpropagation algorithm for training"""
        # Run for specified number of iterations
        all_files = os.listdir(self.train_dir)
        for k in range(self.iters):
            # Randomize input order
            print('Training Iteration: ' + str(k+1) + ' / ' + str(self.iters), end='\r')
            random.shuffle(all_files)
            for i, img_file in enumerate(all_files):
                # Calculate activation values for all neurons
                self.calc_activations(os.path.join(self.train_dir.strip('\/'), img_file))

                # Calculate output layer errors (4)
                expected_outputs = self.encodings[img_file[0]]
                for n, current_neuron in enumerate(self.layers[-1]):
                    current_neuron.err = current_neuron.a * (1 - current_neuron.a) * (expected_outputs[n] - current_neuron.a)

                # Calculate errors for all other neurons (5, 6)
                for l, current_layer in reversed(list(enumerate(self.layers[:-1]))):
                    if l <= 0:
                        break

                    for current_neuron in current_layer:
                        err_sum = 0
                        for f, further_neuron in enumerate(self.layers[l+1]):
                            err_sum += further_neuron.err * current_neuron.weights[f]

                        current_neuron.err = current_neuron.a * (1 - current_neuron.a) * err_sum

                # Update weights (7)
                for l, current_layer in enumerate(self.layers[1:]):
                    l += 1
                    for current_neuron in current_layer:
                        for w in range(len(current_neuron.weights)):
                            current_neuron.weights[w] = current_neuron.weights[w] + self.alpha * current_neuron.a * self.layers[l+1][w].err

                # Special case for dummy neuron
                dummy_activation = self.layers[0][0].a
                for l, current_layer in enumerate(self.layers[1:]):
                    l += 1
                    for w, current_neuron in enumerate(current_layer):
                        self.layers[0][0].weights[l][w] = self.layers[0][0].weights[l][w] + self.alpha * dummy_activation * current_neuron.err

        # Clear terminal line
        print()

    def read(self):
        """Run the backpropagation algorithm without adjusting weights, then attempt to read images as characters"""
        for string_img_file in os.listdir(self.read_dir):
            string_img_file = os.path.join(self.read_dir.strip('\/'), string_img_file)

            # Create directory to hold all the characters we find in this image
            found_chars_dir = string_img_file + 'found_chars'
            find_chars(string_img_file, found_chars_dir, int(math.sqrt(len(self.layers[1]))))

            # Classify each character we find in the image
            print(string_img_file + ' says: ', end='')
            for found_char_file in sorted(os.listdir(found_chars_dir), key=sort_file_by_int_key):
                found_char_file = os.path.join(found_chars_dir, found_char_file)
                self.calc_activations(found_char_file)

                print(self.get_most_likely(), end='')

            # Remove directory for this image once we're done reading it
            shutil.rmtree(found_chars_dir)

            # Clear line
            print()
