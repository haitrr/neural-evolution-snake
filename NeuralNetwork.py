#### Libraries
# Standard library
import json
import random
import sys

# Third-party libraries
import numpy as np


#### Main Network class
class NeuralNetwork(object):
    def __init__(self, sizes):
        """Constructor of the neral network
        """
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.weight_initializer()

    def weight_initializer(self):

        self.biases = np.array([np.random.randn(y, 1) for y in self.sizes[1:]])
        self.weights = np.array([
            np.random.randn(y, x) / np.sqrt(x)
            for x, y in zip(self.sizes[:-1], self.sizes[1:])
        ])

    def feed_forward(self, a):
        """Return the output of the network if ``a`` is input."""
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a) + b)
        return a

    def save(self, filename):
        """Save the neural network to the file ``filename``."""
        data = {
            "sizes": self.sizes,
            "weights": [w.tolist() for w in self.weights],
            "biases": [b.tolist() for b in self.biases],
        }
        f = open(filename, "w")
        json.dump(data, f)
        f.close()


#### Loading a Network
def load(filename):

    f = open(filename, "r")
    data = json.load(f)
    f.close()
    net = NeuralNetwork(data["sizes"], cost=cost)
    net.weights = [np.array(w) for w in data["weights"]]
    net.biases = [np.array(b) for b in data["biases"]]
    return net


def sigmoid(z):
    """The sigmoid function."""
    return 1.0 / (1.0 + np.exp(-z))
