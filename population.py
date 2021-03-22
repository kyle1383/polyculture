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

#Creates a population objects - stores a number of robots set by constants - contains functions to perform evolution on the population
class POPULATION: 
    #initialized with robots array which stores the actual population, and environment used for training in EVO
    #immediately sets seed
    #sets file to write evolution fitnesses to 
    def __init__(self, k):
        self.robots = [] 
        self.env = c.trainingEnv
        self.popNum = k 
        numpy.random.seed(c.seed)
        random.seed(c.seed)

        self.evoString = '/Users/kylemorand/Desktop/pyrosim/polyculture/images/evolutionaryData/'+ str(c.focusPopOne) + str(c.focusPopTwo) + '-' + str(c.fleetTitle) + '-' + str(k) + '.csv'
#########################EXTERNAL FUNCTIONS######################### - called from external file
    #Create 30 random robots and append them to self.robots
    def initialize(self):
        for i in range(c.popSize):
            genome = numpy.random.random_sample((6,9)) * 2 - 1
            self.robots.append(ROBOT(fleetId = c.fleetId, genome = genome, i = i, age = 0))
        #create file may need mkdir | record fitnesses, ages, ids ,seed and gen of each robot/the process
        with open(self.evoString, mode='w') as openFile:
            openFile = csv.writer(openFile, delimiter=',')
            openFile.writerow(('fitness', 'age', 'seed', 'gen', 'uuid'))
            for robot in self.robots:
                openFile.writerow([str(robot.fitness),robot.age, str(c.seed), str(0), robot.uuid])

    #Run AFPO to evolve robots 
        #generate random population 
        #copy all of them but one and mutate 
        #evaluate all robots 
        #age them 
        #insert new robot age 0
        #Eliminate random dominated robots (lowerr fitness and higher age) until returned to population size
    def evolve(self, j):
            #lists for plot
            data = numpy.empty(((c.popSize*c.numGens),4))
            #evaluate the parents | test them on training environment and return fitness  
            self.evaluate(-1)
            for g in range(int(c.numGens)):
                #update seed
                c.seed+=1
                numpy.random.seed(c.seed)
                random.seed(c.seed)
                #create child population and populate through AFPO | takes same age as parents - children have same age as genes are as old, only random individuals are considered younger
                children = POPULATION(self.popNum) 
                uncopiedIndex = numpy.random.randint(0,c.popSize)
                children.copyAFPO(self.robots, uncopiedIndex)
                #mutate and age children | age parents 
                children.mutate()
                children.age()
                self.age()
                #add random bot, age 0, youngest in population 
                children.addBabyBot()
                #append children to parents and evaluate
                self.copy(children)
                self.evaluate(g)
                #eliminate dominated robots(lowerr fitness and higher age) until returned to popSize
                self.tournamentSelection()
               
                #calculate and print lineages | generation - age
                self.chartLineage(g)
                #add robots to data so they can be charted
                for i in range(len(self.robots)): 
                    data[g*30+i] = [g, i,self.robots[i].fitness, self.robots[i].age]
                #calculate unique fitnesses to check if all robots are converging on a local optima
                fitnesses_1 = []
                for robot in self.robots:
                    fitnesses_1.append(robot.fitness)
                print("Amount of unique fitnesses:", len((numpy.unique(fitnesses_1))))

                #Save data to a file | used to track entire progression of robots through evolution
                print("Save")
                self.saveToFile(self.evoString, g)

            #Write data in temporary rainbow.csv file
            with open ('rainbow.csv', mode = 'w') as openFile:
                openFile = csv.writer(openFile, delimiter=',')
                for row in data:
                    openFile.writerow(row)
                
            #print and chart data too rainbow waterfall
            print("Data:", data)
            rainbow_waterfall_plot(data=data,max_gens = 200, save_loc = 'images/' +str(c.trainingEnv) + 'to' + str(c.testingEnv) +'-' + str(c.focusPopOne) + str(c.focusPopTwo) +'-'+ str(c.fleetTitle) + 'T' + str(c.trial) + 'pop' + str(j) + '.png')

    #return robot with highest fitness
    def getWinner(self):
        fitnesses = [] 
        for robot in self.robots:
            fitnesses.append(robot.fitness)
        maxIndex = fitnesses.index(max(fitnesses)) 
        return self.robots[maxIndex] 

########################INTERNAL FUNCTIONS########################## - called from within population.py
    #copy each robot from parent to children by individually copying each gene | should be copy.deepcopy, but it doesn't work 
    #uncopied index is random robot which is not copied - this way we can add a random new bot later
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

    #select and change a random gene | use Gaussian distribution to assure it is close to parent
    def mutate(self): 
        for i in range(0, len(self.robots)):
            self.robots[i].mutate()

    #add a single random robot with age 0 
    def addBabyBot(self): 
        genome = numpy.random.random_sample((6,9)) * 2 - 1
        self.robots.append(ROBOT(c.fleetId, genome, len(self.robots), 0)) 
    
    #add all robots from other to self | append children to parents
    def copy(self, other):
        for i in range (0, len(other.robots)):
            genome = numpy.random.random_sample((6,9)) * 2 - 1
            for row in range(0, 6):
                for col in range (0,9):
                    genome[row,col] = copy.copy(other.robots[i].genome[row,col]) 
            self.robots.append(ROBOT(fleetId = c.fleetId, genome= genome, i = i, age = other.robots[i].age))

    #test each robot on training envitronment | parents pre-evaluated so if passed g only do children, if -1 do everything 
    def evaluate(self, generation):
        if generation == -1: 
            start = 0 
        else: 
            start = c.popSize

        for i in range(start, len(self.robots)): 
            self.robots[i].fitness = 0
                
        for i in range(start, len(self.robots)): 
            self.robots[i].evaluate(c.trainingEnv)

    #run tournaments of k robots | k = 2 | dominated robots (lower fitness, higher age) are eliminated | 
    #goes until we return to population size |original algorithm allows for expanded population but that can mess with this experiment's consistency 
    def tournamentSelection(self):
        #store comparisons in case no robots are dominated | There is probably a more efficienct way to do this
        completedComparisons = [] 
        while len(self.robots) > c.popSize:
            #compare two different robots A and B, add (A,B) and (B,A) to completedCompatisons 
            num1 = numpy.random.randint(0,len(self.robots))
            num2 = numpy.random.randint(0,len(self.robots))
            while num2 == num1 or ([num1,num2]) in completedComparisons: 
                num1 = numpy.random.randint(0,len(self.robots))
                num2 = numpy.random.randint(0,len(self.robots))

            completedComparisons.append([num1,num2])
            completedComparisons.append([num2,num1])

            #eliminate dominated robot 
            if( self.robots[num1].fitness < self.robots[num2].fitness and self.robots[num1].age >= self.robots[num2].age ):
                self.robots.pop(num1)
            elif( self.robots[num2].fitness < self.robots[num1].fitness and self.robots[num2].age >= self.robots[num1].age ):
                self.robots.pop(num2)
            
            #if all comparisons complete -> eliminate a random robot != highest fitness
            n = len(self.robots)
            if len(completedComparisons) >= (n*(n-1))/2:
                while len(self.robots) > c.popSize:
                    fitnesses = []
                    for robot in self.robots:
                        fitnesses.append(robot.fitness)
                    maxVal = numpy.max(fitnesses)
                    tries = 0
                    num1 = numpy.random.randint(0,len(self.robots))
                    #make sure highest fitness robot isn't eliminated
                    while self.robots[num1].fitness == maxVal:
                        num1 = numpy.random.randint(0,len(self.robots))
                        tries += 1
                        if tries > 100:
                            print("Exceeded 100 random robots | eliminating robot with highest fitness")
                            break


                    print("Eliminated Random bot: " + str(self.robots[num1].fitness))
                    self.robots.pop(num1)

    #increase age of each robot in population by 1
    def age(self):
        for robot in self.robots: 
            robot.age += 1

    #create a list of lineages used when charting robots
    def chartLineage(self, g):
        lineages = [] 
        for robot in self.robots: 
            lineage = g - robot.age +1 
            lineages.append(lineage)

        print("Lineages", lineages)

    #record each robot's data in a given file
    def saveToFile(self, writeFile, gen):
        fitnessFile = writeFile
       
        with open(fitnessFile, mode='a') as openFile:
            openFile = csv.writer(openFile, delimiter=',')
            for robot in self.robots:
                openFile.writerow([str(robot.fitness), robot.age, str(c.seed), str(gen), robot.uuid])



