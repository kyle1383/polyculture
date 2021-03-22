import random 
import sys
import math
sys.path.append("/Users/kylemorand/Desktop/pyrosim")
from pyrosim import pyrosim #visStudioCode problem
from body import BODY 
from brain import BRAIN
import uuid

import constants.currentConstants as c 
#Stores a single instnace of a robot: information/robot 
#ROBOT
    #Body - the sturcture of the robot
    #Brain - uses genome to influence robots behavior
    #Fitness - number measuring how well the robot performs in a given environment
class ROBOT:
    def __init__(self, fleetId, genome, i, age):
        self.id = i
        self.fleetId = fleetId
        self.age = age 
        self.uuid = uuid.uuid4()
        #Each robot has to store its own simulator settings - I forget why 
        self.genome = genome
        self.sim = pyrosim.Simulator(play_paused=c.pp, eval_time=c.evalTime, play_blind=c.pb)
        self.body = BODY(self.sim, fleetId, self.genome)
        self.brain = BRAIN(sim = self.sim, other = self.body, wts = self.genome)
        
        self.fitness = 0
    
    #Calculate the fitness as the distance a robot from its starting point using pythagorean theorem
    def evaluate(self, env):
        self.sim.start()
        self.sim.wait_to_finish()
        self.fitness = math.sqrt((self.sim.get_sensor_data( sensor_id = self.brain.S[4] , svi = 0)[-1])**2 +(self.sim.get_sensor_data( sensor_id = self.brain.S[4] , svi = 1)[-1])**2)

    #select a random gene and mutate it - Value in range [-1,1] - Uses Gaussian(Normal) distribution to assure that the mutation is close to the parent
    def mutate(self):
        #geneToMutate
        row = random.randint(0,4)
        col = random.randint(0,7)
        self.genome[row, col] = random.gauss( self.genome[row, col] , math.fabs(self.genome[row, col]))
        if self.genome[row,col] > 1:
            self.genome[row,col] = 1
        elif self.genome[row,col] < -1:
            self.genome[row,col] = -1

    def setSim(self, sim):
        self.sim = sim     
    
    def printBot(self):
        print("Bot " + str(self.id) + "|| fitness: " + str(self.fitness))
