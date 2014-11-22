# python model of a perceptron
# this node model is used in neural.py
# Author:  Richard Salter

from random import *
from math import *

## Perceptron class implements a single perceptron using the weights and activation function provided
#   A activation function derivative field is provided in anticipation of the use of this class
#   in neural.py
#   By using a default derivative of lambda x: 1, all computed delta values are equal to error values

class Perceptron:
    def __init__(self, weights, activationFn, dActivationFn=lambda x: 1, bias=True):
        self.weights = weights
        self.activationFn = activationFn
        self.dActivationFn = dActivationFn
        self.bias = bias
        self.delta = 0
    def size(self):
        return len(self.weights)-1 if self.bias else len(self.weights)
    def fire(self, *inputs):
        if len(inputs) != self.size():
            raise Exception("inputs do not match perceptron")
        if self.bias:
            inputs = [1]+list(inputs)
        wtsum = sum(map(lambda x,y: x*y, self.weights, inputs))
        return self.activationFn(wtsum)
    def train(self, dat, delta=0, eta=0.2):
        self.delta = delta
        self.weights = list(map(lambda w,x: w + eta*self.delta*x, self.weights, [1]+list(dat)))
    def clone(self):
        return Perceptron(self.weights, self.activationFn, self.dActivationFn, self.bias)

### classify builds training data input and the objective function from the training data
#    and calls learn

def classify(p, tset, eta, epsilon=0):
    datlist = dsmaker(tset)
    obj = objmaker(tset)
    return learn(p, datlist, obj, eta, epsilon)

### learn loops by calling epoch to execute an epoch
#    learn returns with the trained perceptron when one is computed

def learn(p, datlist, obj, eta, epsilon=0, verbose=True):
    n = 1
    while True:
        if verbose:
            print("Epoch %d: %s" % (n, trunc(p.weights)))
        (p, done) = epoch(p, datlist, obj, eta, epsilon, verbose)
        if done:
            return p
        n += 1

### epoch runs through the datlist once, firing the perceptron and adjusting weights as needed
#    epoch returns a tuple with the current perceptron and True/False, depending on whether
#    training is complete.

def epoch(p0, datlist, obj, eta, epsilon, verbose=True):
    done = True
    for dat in datlist:
        F = obj(*dat)
        f = p0.fire(*dat)
        err = F - f
        delta = p0.dActivationFn(f)*err
        w0 = p0.weights
        w1 = p0.weights
        if abs(err) > epsilon:
            p1 = p0.clone()
            p1.train(dat, delta, eta)
            w1 = p1.weights
            p0 = p1
            done = False            
        if verbose:
            rw0 = trunc(w0)
            rw1 = trunc(w1)
            dat1 = [1] + list(dat) if p0.bias else dat
            print("  testing %s on %s; should get %s, got %s, error %s:" % (rw0, dat1, F, f, err))
            print("   no change" if w0 == w1 else "   %s -> %s" % (rw0, rw1))
    return (p0, done)


### Threshold functions
                                
# step function

def step(thresh, lo, hi):
    return lambda x: lo if x <= thresh else hi

step001 = step(0, 0, 1)

# sigmoid function (and derivative)

def sigma(lam):
    return lambda x: 1/(1+exp(-lam*x))

def dsigma(lam):
    return lambda x: lam*x*(1-x)

# hyperbolic tangent function (and derivative)

def tanh(lam):
    return lambda x: 1 + (exp(lam*x)-exp(-lam*x))/(exp(lam*x)+exp(-lam*x))

def dtanh(lam):
    return lambda x: lam*(1-x**2)

### Help functions

# trunc truncates the values in a list of floating point values for printing purposes

def trunc(l):
    return list(map(lambda z: float(int(z*1000))/1000, l))

# dsmaker creates training input from a training set

def dsmaker(tset):
    return list(map(lambda z: z[0:-1], tset))

# objmaker creates an objective function from a training set

def objmaker(tset):
    def search(l, ls):
        if ls == []:
            return None
        if l == ls[0][0:-1]:
            return ls[0][-1]
        return search(l, ls[1:])
    return lambda *dat: search(list(dat), tset)

## random perceptron builder on n inputs

def rand_p(n, x=1, act=step001, dact=lambda x: 1, bias=True):
    wts = list(map(lambda z: uniform(-x,x), [0]*n))
    return Perceptron(wts, act, dact, bias)

#### Examples
eta = 0.2

p = Perceptron([0, -0.2, 0.4], step001)
ps = Perceptron([0, -0.2, 0.4], sigma(10), dsigma(10))
pps = Perceptron([0, -0.2, 0.4], sigma(10))

# and,or,xor training sets

tset_or = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
tset_and = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]]
tset_xor = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]


