import copy 
import numpy 
import random 
import csv
import constants.currentConstants as c 
import matplotlib.pyplot as plt 
import numpy as np    
from robot import ROBOT
import os
from rainbow_waterfall_plot import rainbow_waterfall_plot

class POPULATION: 
    def __init__(self):
        self.robots = [] 
        self.env = c.trainingEnv
        numpy.random.seed(c.seed)
        random.seed(c.seed)

        self.evoString = '/Users/kylemorand/Desktop/pyrosim/polyculture/images/blenderChartData/seed' + str(c.seed) + str(
            c.fleetTitle) + 'ABfocus.csv'
#########################EXTERNAL FUNCTIONS#########################
    def initialize(self):
        #Make sure this doesn't create copies of the same robot
        for i in range(c.popSize):
            genome = numpy.random.random_sample((6,9)) * 2 - 1
           
            self.robots.append(ROBOT(fleetId = c.fleetId, genome = genome, i = i, age = 0))

        with open(self.evoString, mode='w') as openFile:
            openFile = csv.writer(openFile, delimiter=',')
            for robot in self.robots:
                openFile.writerow([str(robot.fitness),robot.age, robot.uuid])


    def evolve(self, k):
            #create lists to plot
        
            data = numpy.empty(((c.popSize*c.numGens),4))
            
            
                
            self.evaluate(-1)
            for g in range(int(c.numGens)):
                c.seed+=1
                numpy.random.seed(c.seed)
                random.seed(c.seed)



                children = POPULATION() 
                uncopiedIndex = numpy.random.randint(0,c.popSize)
                children.copyAFPO(self.robots, uncopiedIndex)
                
                children.mutate()
                children.age()
                self.age()
                children.addBabyBot()

                self.copy(children)
                self.evaluate(g)
                
                
                self.tournamentSelection()
               
                
                self.chartLineage(g)
                for i in range(len(self.robots)): 
                    data[g*30+i] = [g, i,self.robots[i].fitness, self.robots[i].age]
                fitnesses_1 = []
                for robot in self.robots:
                    fitnesses_1.append(robot.fitness)
                print("Amount of unique fitnesses:", len((numpy.unique(fitnesses_1))))

                # filechart
                print("Save")
                self.saveToFile(self.evoString)
            with open ('rainbow.csv', mode = 'w') as openFile:
                openFile = csv.writer(openFile, delimiter=',')
                for row in data:
                    openFile.writerow(row)
                
            #gen, ID,  fitness, age
            print("Data:", data)
            rainbow_waterfall_plot(data=data,max_gens = 200, save_loc = 'images/' +str(c.trainingEnv) + 'to' + str(c.testingEnv) + 'ABfocus'+ str(c.fleetTitle) + 'S' + str(c.squadron) + str(k) + '.png')


    def getWinner(self):
        fitnesses = [] 
        for robot in self.robots:
            fitnesses.append(robot.fitness)
        maxIndex = fitnesses.index(max(fitnesses)) 
        return self.robots[maxIndex] 


########################INTERNAL FUNCTIONS##########################
    def copyAFPO(self, other, uncopiedIndex):
        for i in range (0, len(other)-1):
            genome = numpy.random.random_sample((6,9)) * 2 - 1
            j = i
            if i >= uncopiedIndex:
                j+=1
            for row in range(0, 6):
                for col in range (0,9):
                    genome[row,col] = copy.copy(other[j].genome[row,col]) 
            self.robots.append(ROBOT(fleetId = other[j].fleetId, genome= genome, i = i, age = other[j].age))

    def mutate(self): 
        for i in range(0, len(self.robots)):
            self.robots[i].mutate()

    def addBabyBot(self): 
        genome = numpy.random.random_sample((6,9)) * 2 - 1
        self.robots.append(ROBOT(c.fleetId, genome, len(self.robots), 0)) 
    
    def copy(self, other):
        for i in range (0, len(other.robots)):
            genome = numpy.random.random_sample((6,9)) * 2 - 1
            for row in range(0, 6):
                for col in range (0,9):
                    genome[row,col] = copy.copy(other.robots[i].genome[row,col]) 
            self.robots.append(ROBOT(fleetId = c.fleetId, genome= genome, i = i, age = other.robots[i].age))

    def evaluate(self, generation):
        if generation == -1: 
            start = 0 
        else: 
            start = c.popSize

        for i in range(start, len(self.robots)): 
            self.robots[i].fitness = 0
                
        for i in range(start, len(self.robots)): 
            self.robots[i].evaluate(c.trainingEnv)

    def tournamentSelection(self):
        completedComparisons = [] 
        while len(self.robots) > c.popSize:
            num1 = numpy.random.randint(0,len(self.robots))
            num2 = numpy.random.randint(0,len(self.robots))
            while num2 == num1 or ([num1,num2]) in completedComparisons: 
                num1 = numpy.random.randint(0,len(self.robots))
                num2 = numpy.random.randint(0,len(self.robots))

            completedComparisons.append([num1,num2])
            completedComparisons.append([num2,num1])

            if( self.robots[num1].fitness < self.robots[num2].fitness and self.robots[num1].age >= self.robots[num2].age ):
                self.robots.pop(num1)
            elif( self.robots[num2].fitness < self.robots[num1].fitness and self.robots[num2].age >= self.robots[num1].age ):
                self.robots.pop(num2)
            
            n = len(self.robots)
            if len(completedComparisons) >= (n*(n-1))/2:
                while len(self.robots) > c.popSize:
                    fitnesses = []
                    for robot in self.robots:
                        fitnesses.append(robot.fitness)
                    maxVal = numpy.max(fitnesses)
                    tries = 0
                    num1 = numpy.random.randint(0,len(self.robots))
                    while self.robots[num1].fitness == maxVal:
                        num1 = numpy.random.randint(0,len(self.robots))
                        tries += 1
                        if tries > 100:
                            break


                    print("UHOH: " + str(self.robots[num1].fitness))
                    self.robots.pop(num1)

    def age(self):
        for robot in self.robots: 
            robot.age += 1

    def chartLineage(self, g):
        lineages = [] 
        for robot in self.robots: 
            lineage = g - robot.age +1 
            lineages.append(lineage)

        print("Lineages", lineages)

    def saveToFile(self, writeFile):
        fitnessFile = writeFile


        with open(fitnessFile, mode='a') as openFile:
            openFile = csv.writer(openFile, delimiter=',')
            for robot in self.robots:
                openFile.writerow([str(robot.fitness),robot.age, robot.uuid])



