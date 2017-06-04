# Class to execute the artificial neural network
class ANN:
    # Nested class for individual neurons
    class Neuron:
        def __init__(self, weights):
            self.weights = weights[:]
