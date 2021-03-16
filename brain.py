import constants.currentConstants as c 
class BRAIN:
        # (sim, body, gene) 
    def __init__(self, sim, other, wts):
        print("", end = "")
        xLoc = 0
        yLoc = 0
        self.wts = wts
        self.send_sensors(sim, xLoc, yLoc, other)
        self.send_neurons(sim, other)
        self.send_synapses(sim, wts)




    def send_objects(self, sim, xLoc, yLoc):
        # self.whiteObject = sim.send_cylinder( x=0 , y=0 , z=0.6 , length = 1.0 , radius=0.1 )
        # self.redObject = sim.send_cylinder( x=0 , y=0.5 , z=1.1 , r1=0 , r2=1 , r3=0 , r=1, g=0, b=0 )
        O0 = sim.send_box(x=xLoc, y=yLoc, z=c.L + c.R, length=c.L, width=c.L, height=2 * c.R, r=0.5, g=0.5, b=0.5,
                          collision_group='robot')
        O1 = sim.send_cylinder(x=xLoc, y=c.L + yLoc, z=c.L + c.R, r1=0, r2=1, r3=0, length=c.L, radius=c.R, r=0.6,
                               g=0.15, b=0.15, collision_group='robot')
        O2 = sim.send_cylinder(x=c.L + xLoc, y=yLoc, z=c.L + c.R, r1=1, r2=0, r3=0, length=c.L, radius=c.R, r=0.15,
                               g=0.6, b=0.15, collision_group='robot')
        O3 = sim.send_cylinder(x=xLoc, y=-c.L + yLoc, z=c.L + c.R, r1=0, r2=1, r3=0, length=c.L, radius=c.R, r=0.15,
                               g=0.15, b=0.6, collision_group='robot')
        O4 = sim.send_cylinder(x=-c.L + xLoc, y=yLoc, z=c.L + c.R, r1=1, r2=0, r3=0, length=c.L, radius=c.R, r=0.5,
                               g=0.1, b=0.4, collision_group='robot')
        # lower legs
        O5 = sim.send_cylinder(x=xLoc, y=1.5 * c.L + yLoc, z=c.L / 2 + c.R, r1=0, r2=0, r3=1, length=c.L, radius=c.R,
                               r=0.9, g=0.08, b=0.08, collision_group='robot')
        O6 = sim.send_cylinder(x=1.5 * c.L + xLoc, y=yLoc, z=c.L / 2 + c.R, r1=0, r2=0, r3=1, length=c.L, radius=c.R,
                               r=0.08, g=0.9, b=0.08, collision_group='robot')
        O7 = sim.send_cylinder(x=xLoc, y=-1.5 * c.L + yLoc, z=c.L / 2 + c.R, r1=0, r2=0, r3=1, length=c.L, radius=c.R,
                               r=0.08, g=0.08, b=0.9, collision_group='robot')
        O8 = sim.send_cylinder(x=-1.5 * c.L + xLoc, y=yLoc, z=c.L / 2 + c.R, r1=0, r2=0, r3=1, length=c.L, radius=c.R,
                               r=0.6, g=0.09, b=0.65, collision_group='robot')

        self.O = {}
        self.O[0] = O0
        self.O[1] = O1
        self.O[2] = O2
        self.O[3] = O3
        self.O[4] = O4
        self.O[5] = O5
        self.O[6] = O6
        self.O[7] = O7
        self.O[8] = O8

    

    def send_joints(self, sim, xLoc, yLoc):
        J0 = sim.send_hinge_joint(first_body_id=self.O[0], second_body_id=self.O[1], x=xLoc, y=c.L / 2 + yLoc,
                                  z=c.L + c.R, n1=-1, n2=0, n3=0, lo=-3.14159 / 2, hi=3.14159 / 2)
        J1 = sim.send_hinge_joint(first_body_id=self.O[1], second_body_id=self.O[5], x=xLoc, y=1.5 * c.L + yLoc,
                                  z=c.L + c.R, n1=-1, n2=0, n3=0, lo=-3.14159 / 2, hi=3.14159 / 2)
        J2 = sim.send_hinge_joint(first_body_id=self.O[0], second_body_id=self.O[2], x=c.L / 2 + xLoc, y=yLoc,
                                  z=c.L + c.R, n1=0, n2=-1, n3=0, lo=-3.14159 / 2, hi=3.14159 / 2)
        J3 = sim.send_hinge_joint(first_body_id=self.O[2], second_body_id=self.O[6], x=1.5 * c.L + xLoc, y=yLoc,
                                  z=c.L + c.R, n1=0, n2=-1, n3=0, lo=-3.14159 / 2, hi=3.14159 / 2)
        J4 = sim.send_hinge_joint(first_body_id=self.O[0], second_body_id=self.O[3], x=xLoc, y=-c.L / 2 + yLoc,
                                  z=c.L + c.R, n1=-1, n2=0, n3=0, lo=-3.14159 / 2, hi=3.14159 / 2)
        J5 = sim.send_hinge_joint(first_body_id=self.O[3], second_body_id=self.O[7], x=xLoc, y=-1.5 * c.L + yLoc,
                                  z=c.L + c.R, n1=-1, n2=0, n3=0, lo=-3.14159 / 2, hi=3.14159 / 2)
        J6 = sim.send_hinge_joint(first_body_id=self.O[0], second_body_id=self.O[4], x=-c.L / 2 + xLoc, y=yLoc,
                                  z=c.L + c.R, n1=0, n2=-1, n3=0, lo=-3.14159 / 2, hi=3.14159 / 2)
        J7 = sim.send_hinge_joint(first_body_id=self.O[4], second_body_id=self.O[8], x=-1.5 * c.L + xLoc, y=yLoc,
                                  z=c.L + c.R, n1=0, n2=-1, n3=0, lo=-3.14159 / 2, hi=3.14159 / 2)

        self.J = {}
        self.J[0] = J0
        self.J[1] = J1
        self.J[2] = J2
        self.J[3] = J3
        self.J[4] = J4
        self.J[5] = J5
        self.J[6] = J6
        self.J[7] = J7

    def send_sensors(self, sim, xLoc, yLoc, other):
        # sensors
        T0 = sim.send_touch_sensor(body_id=other.O[5])
        T1 = sim.send_touch_sensor(body_id=other.O[6])
        T2 = sim.send_touch_sensor(body_id=other.O[7])
        T3 = sim.send_touch_sensor(body_id=other.O[8])
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
        # neurons
        self.SN = {}
        i = 0
        for s in self.S:
            i += 1
            self.SN[s] = sim.send_sensor_neuron(sensor_id=self.S[s])

        self.MN = {}
        for j in other.J:
            self.MN[j] = sim.send_motor_neuron(joint_id=other.J[j], tau=c.tau)

    def send_synapses(self, sim, wts):
        for j in self.SN:
            for i in self.MN:
                sim.send_synapse(source_neuron_id=self.SN[j], target_neuron_id=self.MN[i], weight=wts[j, i])

        # sim.send_synapse(source_neuron_id = SN1 , target_neuron_id = MN4 , weight = wt )

        # sim.send_synapse(source_neuron_id = SN0 , target_neuron_id = MN2 , weight = -1.0 )
