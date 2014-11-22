# python model of a feed-forward neural net with backpropagation algorithm
# Uses perceptron.py node model with sigmoid or tanh function
# Author:  Richard Salter

from perceptron import Perceptron, sigma, dsigma, tanh, dtanh, step001
from random import *
from pprint import pprint

## Node class extends Perceptron to retain most recent output for computing delta
#  Node also includes a method wdelta to return delta * weight for backpropagation purposes

class Node(Perceptron):
    def __init__(self, index, weights, activationFn, dActivationFn=lambda x: 1):
        self.index = index
        super().__init__(weights, activationFn, dActivationFn)
    def fire(self, *inputs):
        self.inputs = inputs
        self.output = super().fire(*inputs)
        return self.output
    def wdelta(self, i):
        return self.delta * self.weights[i+1]
    def train(self, err, eta):
        delta = self.dActivationFn(self.output)*err
        super().train(self.inputs, delta, eta)

## Layer class represents a layer of nodes. It includes methods to extract lists of deltas and weights.
#   Layer also implements a fire method to fire all Nodes and collect their outputs.

class Layer:
    def __init__(self, index, wts, activationFn, dActivationFn=lambda x: 1):
        self.index = index
        self.nodes = []
        ctr = 0
        for wt in wts:
            self.nodes.append(Node(ctr, wt, activationFn, dActivationFn))
            ctr += 1
    def weights(self):
        ans = []
        for n in self.nodes:
            ans.append(n.weights)
        return ans
    def deltas(self):
        ans = []
        for n in self.nodes:
            ans.append(n.delta)
        return ans
    def fire(self, *inputs):
        self.outputs = []
        for n in self.nodes:
            self.outputs.append(n.fire(*inputs))
        return self.outputs

## Net class represents a network as a list of layers
#  Net contains a fire method to sequence layer firing, using the ouput
#   from the previous firing as the input to the next
#  Back propagation is modeled as a method that loops through the layers
#   in reverse order, first training each node with the current error,
#   then computing the next error using the weighted sum of deltas

class Net:
    def __init__(self, layers):
        self.layers = layers
        for i in range(len(self.layers)-1):
            self.layers[i+1].inputSize = len(self.layers[i].nodes)
    def weights(self):
        ans = []
        for l in self.layers:
            ans.append(l.weights())
        return ans
    def deltas(self):
        ans = []
        for l in self.layers:
            ans.append(l.deltas())
        return ans
    def fire(self, *inputs):
        for i in range(len(self.layers)):
            inputs = self.layers[i].fire(*inputs)
        self.output = inputs
        return self.output
    def node(self, i, j):
        return self.layers[i].nodes[j]
    def out(self, i, j):
        return self.layers[i].outputs[j]
    def output(self, j):
        return self.layers[-1].outputs[j]
    def backprop(self, err, eta):
        for i in range(len(self.layers)-1, -1, -1):
            layer = self.layers[i]
            for j in range(len(layer.nodes)):
                node = layer.nodes[j]
                node.train(err[j], eta)
            if i > 0:
                nerr = []
                for j in range(layer.inputSize):
                    tot = 0
                    for node in layer.nodes:
                        tot += node.wdelta(j)
                    nerr.append(tot)
                err = nerr

### classify is analogous to its version in Perceptron
#    it builds training data input and the objective function from the training data
#    and calls learn
#    Maxepochs specifies the maximum number of epochs before returing
                
def classify(net, tset, eta, epsilon=0.1, maxepochs= 20000, verbose=False):
    datlist = dsmaker(tset)
    obj = objmaker(tset)
    return learn(net, datlist, obj, eta, epsilon, maxepochs, verbose)

### learn loops by calling epoch to execute an epoch
#    learn returns with the number of epochs required if an answer is computed
#    otherwise it returns with None if maxepochs is reached without an answer

def learn(net, datlist, obj, eta, epsilon=0, maxepochs=20000, verbose=True):
    n = 1
    while n < maxepochs:
        if verbose:
            print("Epoch %d: %s" % (n, net.weights()))
        done = epoch(net, datlist, obj, eta, epsilon, verbose)
        if done:
            return n
        n += 1

### epoch runs through the datlist once, firing the network on each element
#    epoch returns True or False depending on whether a solution has been found

def epoch(net, datlist, obj, eta, epsilon, verbose=True):
    done = True
    for dat in datlist:
        F = obj(*dat)
        f = net.fire(*dat)
        err = list(map(lambda x: F[x] - f[x], list(range(len(F)))))
        if bad(err, epsilon):
            net.backprop(err, eta)
            done = False            
        if verbose:
            print("  testing %s; should get %s, got %s, error %s:" % (dat, trunc(F), trunc(f), trunc(err)))
    return done

### show presents 1 epoch of firings without backpropagation. It is used to
#    view the current state of training

def show(net, tset):
    print("Weights:")
    pprint(net.weights())
    print()
    datlist = list(map(lambda z: z[0:-1], tset))
    obj = lambda *dat: search(list(dat), tset)
    for dat in datlist:
        F = obj(*dat)
        f = net.fire(*dat)
        err = map(lambda x: F[x] - f[x], list(range(len(F))))
        print("  testing %s; should get %s, got %s, error %s:" % (dat, trunc(F), trunc(f), trunc(err)))

### Help functions

# bad return True if any error value exceeds epsilon; False otherwise

def bad(err, epsilon):
    for x in err:
        if abs(x) > epsilon:
            return True
    return False
        
# trunc truncates the values in a list of floating point values for printing purposes

def trunc(l):
    return list(map(lambda z: float(int(z*1000))/1000, l))

# dsmaker creates training input from a training set

def dsmaker(tset):
    return list(map(lambda z: z[0:-1], tset))

# objmaker creates an objective function from a training set

def objmaker(tset):
    return lambda *dat: search(list(dat), tset)

def search(l, ls):
    if ls == []:
        return None
    if l == ls[0][0:-1]:
        ans = ls[0][-1]
        return ans if type(ans)==list else [ans]
    return search(l, ls[1:])

### Network builders: inputs are lists of weight vectors; each weight vector
#     is a tuple of weights; each list represents a single layer
#    These builders deduce the network architecture from their inputs and build
#    the corresponding net

deflam = 3

def buildNetStep(*wts):
    layers = []
    for i in range(len(wts)):
        layers.append(Layer(i, wts[i], step001))
    return Net(layers)

def buildNet(*wts, lam=deflam):
    layers = []
    for i in range(len(wts)):
        layers.append(Layer(i, wts[i], sigma(lam), dsigma(lam)))
    return Net(layers)

def buildNetTanh(*wts, lam=1):
    layers = []
    for i in range(len(wts)):
        layers.append(Layer(i, wts[i], tanh(lam), dtanh(lam)))
    return Net(layers)

def u():
    return uniform(-1,1)

########## Examples

eta = 0.05

### single perceptron network

pn = buildNet([(0, -0.2, 0.4)])

def initANDORNet():
    return buildNet([(u(), u(), u())])

# or and and training set for pn
tset_or = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
tset_and = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]]

############
### parallel 2-input perceptrons (no hidden layer) to compute and and or in parallel

net_andor = buildNet([(0, -0.2, 0.4), (0, -0.2, 0.4)])

# or/and training set
tset_andor = [[0, 0, [0,0]], [0, 1, [0,1]], [1, 0, [0,1]], [1, 1, [1,1]]]

############
### xor networks (using sigma and tanh)

def initXORNet():
    return buildNet([(u(), u(), u()),
                     (u(), u(), u())],
                    [(u(), u(), u())])

def initXORTanhNet():
    return buildNetTanh([(u(), u(), u()),
                     (u(), u(), u())],
                    [(u(), u(), u())])

net_xors = initXORNet()
net_xort = initXORTanhNet()

# training set for xor
tset_xor = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]

############
### binary recognizer

def initBinNet():
    return buildNet([(u(), u(), u(), u()), (u(), u(), u(), u()), (u(), u(), u(), u())],
                    [(u(), u(), u(), u()), (u(), u(), u(), u()), (u(), u(), u(), u()), (u(), u(), u(), u()),
                     (u(), u(), u(), u()), (u(), u(), u(), u()), (u(), u(), u(), u()), (u(), u(), u(), u())])

net_b = initBinNet()

# training set for binary recognizer

tset_b = [[0, 0, 0, [1, 0, 0, 0, 0, 0, 0, 0]],
          [0, 0, 1, [0, 1, 0, 0, 0, 0, 0, 0]],
          [0, 1, 0, [0, 0, 1, 0, 0, 0, 0, 0]],
          [0, 1, 1, [0, 0, 0, 1, 0, 0, 0, 0]],
          [1, 0, 0, [0, 0, 0, 0, 1, 0, 0, 0]],
          [1, 0, 1, [0, 0, 0, 0, 0, 1, 0, 0]],
          [1, 1, 0, [0, 0, 0, 0, 0, 0, 1, 0]],
          [1, 1, 1, [0, 0, 0, 0, 0, 0, 0, 1]]]


