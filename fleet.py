#FLEET CLASS
#Stores untested copies of winners from evolutionary runs (AFPO)
#Always uses testing environment 
import constants.currentConstants as c 
import csv 
import numpy 
import copy
from pyrosim import pyrosim #VisCode problem
from robot import ROBOT
#An object which stores 10 robots
#Fleets are designed to hold evolved robots so that they can be tested as a group in new environments
class FLEET:
    def __init__(self):
        self.winners = [] 
        self.biggestWinner = -1
    
    #PYROSIM has a problem when copying robots: if the robot has already been evaluated in an environment, it can't be copied 
    #typically deepcopy is used, but there is for some reason a problem with that 
    #This function adds a robot to the fleet. To do so it must copy the previous robot genome by genome
    def add(self, robot):
        genome = numpy.random.random_sample((6,9)) * 2 - 1
        for row in range(0, 6):
            for col in range (0,9):
                genome[row,col] = copy.copy(robot.genome[row,col]) 
        self.winners.append(ROBOT(fleetId = robot.fleetId, genome= genome, i = len(self.winners), age = robot.age))

        #this cause error, must copy first

    #Evaluate each robot on the testing environment
    #If Fleet A - Only evaluate the best individual robot  
    #use fpb variable to determine if fleet evaluations are shown
    def evaluate(self):
        if c.fleetId == 1:
            currentVal = 0
            for winner in self.winners:
                if winner.fitness > currentVal:
                    self.biggestWinner = self.winners.index(winner)
                    currentVal = winner.fitness
            #################issue exists here##################################################################################
            #I'm confident it comes from 'setSIM' as there is no problem with robots pre FLEET
            #self.winners[self.biggestWinner].setSim(pyrosim.Simulator(play_paused=c.pp, eval_time=c.evalTime, play_blind=c.fpb))
            self.winners[self.biggestWinner].evaluate(c.testingEnv)
        else:
            for winner in self.winners:
                #winner.setSim(pyrosim.Simulator(play_paused=c.pp, eval_time=c.evalTime, play_blind=c.fpb))
                winner.evaluate(c.testingEnv)
        
    #adjust to save only the best in case of fleet A 
    def saveToFile(self,writeFile):
        #give extension of either /fitness or /genome
        fitnessFile = writeFile + c.saveFile
        genomeFile = writeFile + c.genomeFile
        with open (genomeFile, mode = 'w') as openFile:
            openFile = csv.writer(openFile, delimiter=',')
            for bot in range(len(self.winners)):
                openFile.writerow(self.winners[bot].genome)

        with open (fitnessFile, mode = 'w') as openFile:
            openFile = csv.writer(openFile, delimiter=',')
            if c.fleetId == 1:
                openFile.writerow([self.winners[self.biggestWinner].fitness])
            else:
                for bot in range(len(self.winners)):
                    openFile.writerow([self.winners[bot].fitness])
            openFile.writerow("seed" + str(c.seed))
            openFile.writerow("fleetSize" + str(c.fleetSize))
            openFile.writerow("popSize" + str(c.popSize))
            openFile.writerow("gens" + str(c.numGens))
            openFile.writerow("evalTime" + str(c.evalTime))
