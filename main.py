from fleet import FLEET
from population import POPULATION 
import constants.currentConstants as c 
import os 
import rainbow_waterfall_plot


#Get user input - sets parameters which will run(What fleet, what environments)
c.seed = int(input("Seed:"))


#Run AFPO Evolutionary algorithm 10 times and populate a fleet instance with the champion of each run 
#Champion:  robot with the highest fitness in the final population after a single run of evolution
fleet = FLEET()
for k in range (c.fleetSize):
    #create an empty population
    population = POPULATION()
    #fill it with 10 random robot
    population.initialize()
    #run evolution on the population
    #k - passed to poulation for book keeping 
    population.evolve(k)
    #add the champion tothe fleet
    fleet.add(population.getWinner())
    #update seed - Unnceessary here I think, but playingit safe
    c.seed += 1 



#run the robots in FLEET in the testEnvironment 
fleet.evaluate()

#save the final fitnesses to a file 
fleetString = '/Users/kylemorand/Desktop/pyrosim/polyculture/data/exp1/' + str(c.focusPopOne) + str(c.focusPopTwo) + str(c.trainingEnv) + 'to' + str(c.testingEnv) + '-' + str(c.fleetTitle) + '-S' + str(c.trial)
try:
    os.mkdir(fleetString)
except OSError:
    print("OSERROR")
fleet.saveToFile(fleetString)


