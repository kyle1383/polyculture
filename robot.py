import random 
import sys
import math
sys.path.append("/Users/kylemorand/Desktop/pyrosim")
from pyrosim import pyrosim 
from body import BODY 
from brain import BRAIN
import uuid

import constants.currentConstants as c 

class ROBOT:
    def __init__(self, fleetId, genome, i, age):
        self.id = i
        self.uuid = uuid.uuid4()
        self.fleetId = fleetId
        self.age = age 

        self.genome = genome
        self.sim = pyrosim.Simulator(play_paused=c.pp, eval_time=c.evalTime, play_blind=c.pb)
        self.body = BODY(self.sim, fleetId, self.genome)
        self.brain = BRAIN(sim = self.sim, other = self.body, wts = self.genome)
        
        self.fitness = 0
        
        

    def evaluate(self, env):
        #deal with environment somewhere in here 
        self.sim.start()
        self.sim.wait_to_finish()
        self.fitness = math.sqrt((self.sim.get_sensor_data( sensor_id = self.brain.S[4] , svi = 0)[-1])**2 +(self.sim.get_sensor_data( sensor_id = self.brain.S[4] , svi = 1)[-1])**2)
    
    def evaluateCustomSim(self, sim, env):
        body = BODY(sim, self.fleetNum, self.genome)
        brain = BRAIN(sim, body, self.genome)
        env = ENV(env,sim)
        env.setEnv()
        sim.start()
        sim.wait_to_finish()
        
       

        
        

    def mutate(self):
        #geneToMutate
        row = random.randint(0,4)
        col = random.randint(0,7)
        self.genome[row, col] = random.gauss( self.genome[row, col] , math.fabs(self.genome[row, col]))
        if self.genome[row,col] > 1:
            self.genome[row,col] = 1
        elif self.genome[row,col] < -1:
            self.genome[row,col] = -1
        
    def printBot(self):
        print("Bot " + str(self.id) + "|| fitness: " + str(self.fitness))
