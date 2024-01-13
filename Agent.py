# This is Q-agent class  that is used to define all the policies and algorithms used by the child classes i.e. agents
# CREATED ON 04-12-2022
import pickle
import numpy as NUMPY
import random
from collections import defaultdict


# q learning agent class
class QLA:

    def __init__(self, environment, alpha, gamma, nA):
        self.Qtable = defaultdict(lambda: NUMPY.zeros(self.nA))
        self.environment = environment
        self.gamma = gamma
        self.alpha = alpha
        self.nA = nA


    def save(self): #  Once the agents have learned, this function will set a iteration based on what they have learnt.
        currentIteration = defaultdict(lambda:0)
        for s, a in self.Qtable.items():
            currentIteration[s] = NUMPY.argmax(a)
        self.iteration = currentIteration


    def greedyAlgorithm(self, currentState, epsilon): 
        probability = random.random()
        if probability < epsilon:
            return NUMPY.random.choice(NUMPY.arange(self.nA))
        else:
            return NUMPY.argmax(self.Qtable[currentState])
            

    def teach(self, currentState, work, incentive, nextState): 
        self.Qtable[currentState][work] += self.alpha*(incentive + self.gamma * NUMPY.max(self.Qtable[nextState]) - self.Qtable[currentState][work])


    def saveEachIteration(self, index): 
        iteration = dict(self.iteration)
        with open(f'iteration{index}.pickle', 'wb') as f:
            pickle.dump(iteration, f)


    def takeAction(self, currentState): # Try to copy the policies that were set in the previous itertations
        return self.iteration[currentState]

    def changeIteration(self, directory): # TO change the iteration based on the previous iteration
        with open(directory, 'rb') as f:
            newIteration = pickle.load(f)
        self.iteration = defaultdict(lambda: 0, newIteration)
        print('Next Iteration')


