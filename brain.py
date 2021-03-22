import constants.currentConstants as c 
#Sets up a neural network: information/NN
#Sensors - get information from environment 
#Neurons 
    #MotorNeurons - connect to joints to influence movement 
    #SensorNeurons -connect to sensors to get sensory data
#Synapses - allow neurons to communicate with eachother // sensors to influence movement
#other = BODY 
#wts = genome // influence the weights of different neurons and allow for variation in reactions to stimulation
class BRAIN:
    
    def __init__(self, sim, other, wts):
        print("", end = "")
        xLoc = 0
        yLoc = 0
        self.wts = wts
        self.send_sensors(sim, xLoc, yLoc, other)
        self.send_neurons(sim, other)
        self.send_synapses(sim, wts)

    def send_sensors(self, sim, xLoc, yLoc, other):
        #TouchSensors - sense when body comes in contact with anything
        T0 = sim.send_touch_sensor(body_id=other.O[5])
        T1 = sim.send_touch_sensor(body_id=other.O[6])
        T2 = sim.send_touch_sensor(body_id=other.O[7])
        T3 = sim.send_touch_sensor(body_id=other.O[8])
        #PositionSensor - gets position of body used to calculate fitness 
        P4 = sim.send_position_sensor(body_id=other.O[0]) 
        #L4 = sim.send_light_sensor(body_id=other.O[0])
        #R5 = sim.send_ray_sensor(body_id=other.O[0], x=xLoc, y=yLoc, z=c.L + c.R, r1=0, r2=1, r3=0)

        self.S = {}
        self.S[0] = T0
        self.S[1] = T1
        self.S[2] = T2
        self.S[3] = T3
        self.S[4] = P4
        #self.S[4] = L4
        #self.S[5] = R5

    def send_neurons(self, sim, other):
        #SensoryNeurons - generate neuron for each sensor
        self.SN = {}
        i = 0
        for s in self.S:
            i += 1
            self.SN[s] = sim.send_sensor_neuron(sensor_id=self.S[s])

        #MotorNeurons - generatee neuron for each joint
        self.MN = {}
        for j in other.J:
            self.MN[j] = sim.send_motor_neuron(joint_id=other.J[j], tau=c.tau)

    def send_synapses(self, sim, wts):
        #send a synapse connecting each sensor neuron with each motoor neuron
        #this is where weights can influence the robot
        for j in self.SN:
            for i in self.MN:
                sim.send_synapse(source_neuron_id=self.SN[j], target_neuron_id=self.MN[i], weight=wts[j, i])

        # sim.send_synapse(source_neuron_id = SN1 , target_neuron_id = MN4 , weight = wt )

        # sim.send_synapse(source_neuron_id = SN0 , target_neuron_id = MN2 , weight = -1.0 )
