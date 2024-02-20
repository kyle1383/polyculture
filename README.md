# Polyculture 
A research project performed with the UVM Morphology Evolution and Cognition Lab.

## The Problem 
Monocultures are a problem in all sorts of domains. If a large crop of corn is identical, a single virus can cause massive damage. This type of problem extends to the domain of robotics and software as well. If a fleet of autonomous cars all share identical software, malicious software could take down the entire fleet. Similarly, an unexpected obstacle could render a fleet obsolete. Suppose you send 10 rovers to mars to explore a crater. If they are all identical, an impassible obstacle would mean an end to the mission. Having diverse robots, in both neural networks and morphology, might increase the odds of a successful mission. 

## The Experiment 
I used pyrosim [Pyrosim](https://ccappelle.github.io/pyrosim/ "Pyrosim"), a simulation software developed in our lab top create virtual robots. The default robot is a quadruped, with two joints on each leg. It has sensors at the tips of its 'feet' which send feedback to the neural network. Genomes are randomized and create the neural networks. These networks respond to stimuli to output motion to the 'motors' controlling the legs. To create an effective robot, a population of around 100 random genomes is created. Robots are then simulated with the goal of walking forward as far as possible in 10 seconds. The best robots are copied and mutated, while the worst are eliminated from the population. This continues for around 100 generations, after which the robots are fairly effective at walking. 

Using this method I created three distinct groups 
1. **Homogeneous robots**: After 100 generations the best robot is selected and 10 copies are created.
2. **Diverse Neural Networks**: After 100 generations the 10 best robots are selected.
3. **Diverse Morphology**: The genome is extended to control the position of the limbs. The 10 best robots are again selected.

These groups of 10 are then tested in two environments 
1. **Flatland**: A simple flat environment, equivalent to where the robots were trained
2. **Obstacle**: An object is randomly inserted in front of the robots.

The robots are then evaluated to see which group best performs in the unfamiliar environment.

## Results 

              | Flatland | Obstacle
------------- | ------------- | ----------
Homogeneous Robots | 10.21m | 3.2m
Diverse NN | 10.11m | 7.4m 
Diverse Morphology | 12.2m | 7.15m 

These results supported some of the expectations, while opening some other questions. I expected that generally the more diverse robots would perform better. On flatland this proved to be true. When obstacles were introduced the homogeneous robots did perform the worst. However, the morphologically diverse robots underperformed the robots with only diverse neural networks. This was a somewhat surprising result. It may highlight that in this environment, a standard quadruped is one of the most efficient morphologies. Introducing variability likely created some morphologies which were more effective, but a majority which were not.

## Further Research 
It may be interesting to modify that way morphologies are randomized. Perhaps the number of legs can vary, as well as joints. Perhaps legs aren’t restricted to be on the central cross section of the robots body, and can be anywhere. This might better demonstrate whether morphologies should be evolved to avoid monocultures. 

## Conclusions
It seems that having diverse robots does improve the performance of robotic fleets when exposed to unfamiliar obstacles. This suggests that in many domains robots for the same task should not all be the same. This may not apply in domains such as autonomous driving, as the priority is the safest possible solution as opposed to robustness for unexpected situations. However, for situations such as rovers, where some robots are expendable if the final task is executed, diverse fleets are the optimal solution.
