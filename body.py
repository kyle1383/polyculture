import constants.currentConstants as c 
class BODY:
    def __init__(self, sim, fleetNum, wts):
        print("", end = "")
        xLoc = 0
        yLoc = 0
        self.genome = wts

        self.coorX = 1
        self.coorY = 1
        self.coorX1 = 1
        self.coorY1 = 1
        self.coorX2= 1
        self.coorY2 = 1
        self.coorX3 = 1
        self.coorY3 = 1
        
        if fleetNum == 1 or fleetNum == 2:
            self.send_objects(sim, xLoc, yLoc)
            self.send_joints(sim, xLoc, yLoc)
    
        elif fleetNum == 3:
            self.send_objects3(sim)
            self.send_joints3(sim, xLoc, yLoc)

        sim.assign_collision('robot', 'robot')

        

        




    def send_objects(self, sim, xLoc, yLoc):
        
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
    
 
    def cosine(self, item):
        item = math.cos(item)
        return item
    
    def sin(self, item):
        item = math.sin(item)
        return item
    
    """def send_objects3(self, sim):
        O0 = sim.send_cylinder(x=0, y=0, z=c.L + c.R, length=c.R/4, radius=c.L/2, r=0.5, g=0.5, b=0.5, collision_group='robot')

        O1 = sim.send_cylinder(x = self.cosine(math.radians(self.genome[0,8]))*c.L, y = self.sin(math.radians(self.genome[0,8]))*c.L, z=c.L + c.R, r1= self.cosine(math.radians(self.genome[0,8])-math.pi), r2 = self.sin(math.radians(self.genome[0,8])-math.pi), r3 = 0, length=c.L, radius=c.R, r=0.6, g=0.15, b=0.15, collision_group='robot')
        O2 = sim.send_cylinder(x = self.cosine(math.radians(self.genome[1,8]))*c.L, y = self.sin(math.radians(self.genome[1,8]))*c.L, z=c.L + c.R, r1=self.cosine(math.radians(self.genome[1,8])-math.pi), r2 = self.sin(math.radians(self.genome[1,8])-math.pi), r3 = 0, length=c.L, radius=c.R, r=0.15, g=0.6, b=0.15, collision_group='robot')
        O3 = sim.send_cylinder(x = self.cosine(math.radians(self.genome[2,8]))*c.L, y = self.sin(math.radians(self.genome[2,8]))*c.L, z=c.L + c.R, r1=self.cosine(math.radians(self.genome[2,8])-math.pi), r2 = self.sin(math.radians(self.genome[2,8])-math.pi), r3 = 0, length=c.L, radius=c.R, r=0.15, g=0.15, b=0.6, collision_group='robot')
        O4 = sim.send_cylinder(x = self.cosine(math.radians(self.genome[3,8]))*c.L, y = self.sin(math.radians(self.genome[3,8]))*c.L, z=c.L + c.R, r1=self.cosine(math.radians(self.genome[3,8])-math.pi), r2 = self.sin(math.radians(self.genome[3,8])-math.pi), r3 = 0, length=c.L, radius=c.R, r=0.6, g=0.15, b=0.6, collision_group='robot')
        #LOWER LEGS#############
        O5 = sim.send_cylinder(x = 1.5*self.cosine(math.radians(self.genome[0,8]))*c.L, y = 1.5*self.sin(math.radians(self.genome[0,8]))*c.L, z=(c.L + c.R)/2, r1=0, r2 = 0, r3 = 1, length=c.L, radius=c.R, r=0.6, g=0.15, b=0.15, collision_group='robot')
        O6 = sim.send_cylinder(x = 1.5*self.cosine(math.radians(self.genome[1,8]))*c.L, y = 1.5*self.sin(math.radians(self.genome[1,8]))*c.L, z=(c.L + c.R)/2, r1=0, r2 = 0, r3 = 1, length=c.L, radius=c.R, r=0.15, g=0.6, b=0.15, collision_group='robot')
        O7 = sim.send_cylinder(x = 1.5*self.cosine(math.radians(self.genome[2,8]))*c.L, y = 1.5*self.sin(math.radians(self.genome[2,8]))*c.L, z=(c.L + c.R)/2, r1=0, r2 = 0, r3 = 1, length=c.L, radius=c.R, r=0.15, g=0.15, b=0.6, collision_group='robot')
        O8 = sim.send_cylinder(x = 1.5*self.cosine(math.radians(self.genome[3,8]))*c.L, y = 1.5*self.sin(math.radians(self.genome[3,8]))*c.L, z=(c.L + c.R)/2, r1=0, r2 = 0, r3 = 1, length=c.L, radius=c.R, r=0.6, g=0.15, b=0.6, collision_group='robot')
        self.O = {}
        self.O[0] = O0
        self.O[1] = O1
        self.O[2] = O2
        self.O[3] = O3
        self.O[4] = O4
        self.O[5] = O5
        self.O[6] = O6
        self.O[7] = O7
        self.O[8] = O8"""   
    
    def send_joints(self, sim, xLoc, yLoc):
        J0 = sim.send_hinge_joint(first_body_id=self.O[0], second_body_id=self.O[1], x=xLoc, y=c.L / 2 + yLoc,
                                  z=c.L + c.R, n1=-1, n2=0, n3=0, lo=-3.14159 / 2, hi=3.14159 / 2)
        
        J2 = sim.send_hinge_joint(first_body_id=self.O[0], second_body_id=self.O[2], x=c.L / 2 + xLoc, y=yLoc,
                                  z=c.L + c.R, n1=0, n2=-1, n3=0, lo=-3.14159 / 2, hi=3.14159 / 2)
        
        J4 = sim.send_hinge_joint(first_body_id=self.O[0], second_body_id=self.O[3], x=xLoc, y=-c.L / 2 + yLoc,
                                  z=c.L + c.R, n1=-1, n2=0, n3=0, lo=-3.14159 / 2, hi=3.14159 / 2)
        
        J6 = sim.send_hinge_joint(first_body_id=self.O[0], second_body_id=self.O[4], x=-c.L / 2 + xLoc, y=yLoc,
                                  z=c.L + c.R, n1=0, n2=-1, n3=0, lo=-3.14159 / 2, hi=3.14159 / 2)
       
                                  #neeeees
        J1 = sim.send_hinge_joint(first_body_id=self.O[1], second_body_id=self.O[5], x=2*c.L*self.coorX, y=2*c.L*self.coorY,
                                  z=c.L + c.R, n1=-1, n2=0, n3=0, lo=-3.14159 / 2, hi=3.14159 / 2)
        J3 = sim.send_hinge_joint(first_body_id=self.O[2], second_body_id=self.O[6],x=2*c.L*self.coorX1, y=2*c.L*self.coorY1,
                                  z=c.L + c.R, n1=0, n2=-1, n3=0, lo=-3.14159 / 2, hi=3.14159 / 2)
        J5 = sim.send_hinge_joint(first_body_id=self.O[3], second_body_id=self.O[7], x=2*c.L*self.coorX2, y=2*c.L*self.coorY2,
                                  z=c.L + c.R, n1=-1, n2=0, n3=0, lo=-3.14159 / 2, hi=3.14159 / 2)
        J7 = sim.send_hinge_joint(first_body_id=self.O[4], second_body_id=self.O[8], x=2*c.L*self.coorX3, y=2*c.L*self.coorY3,
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
    def send_joints3(self, sim, xLoc, yLoc):
        #leg 1
        J0 = sim.send_hinge_joint(first_body_id=self.O[0], second_body_id=self.O[1], x=0, y=0, z=c.L + c.R, n1=-1, n2=0, n3=0, lo=-3.14159 / 2 , hi=3.14159 / 2)

        J1 = sim.send_hinge_joint(first_body_id=self.O[1], second_body_id=self.O[5], x=1.5*self.cosine(math.radians(self.genome[0,8]))*c.L, y=1.5*self.sin(math.radians(self.genome[0,8]))*c.L, z=c.L + c.R, n1=-1, n2=0, n3=0, lo=-3.14159 / 2 , hi=3.14159 / 2)
        #leg 2
        J2 = sim.send_hinge_joint(first_body_id=self.O[0], second_body_id=self.O[2], x=0, y=0, z=c.L + c.R, n1=-1, n2=0, n3=0, lo=-3.14159 / 2 , hi=3.14159 / 2)

        J3 = sim.send_hinge_joint(first_body_id=self.O[2], second_body_id=self.O[6], x=1.5*self.cosine(math.radians(self.genome[1,8]))*c.L, y=1.5*self.sin(math.radians(self.genome[1,8]))*c.L, z=c.L + c.R, n1=-1, n2=0, n3=0, lo=-3.14159 / 2 , hi=3.14159 / 2)
        #leg3
        J4 = sim.send_hinge_joint(first_body_id=self.O[0], second_body_id=self.O[3], x=0, y=0, z=c.L + c.R, n1=-1, n2=0, n3=0, lo=-3.14159 / 2 , hi=3.14159 / 2)

        J5 = sim.send_hinge_joint(first_body_id=self.O[3], second_body_id=self.O[7], x=1.5*self.cosine(math.radians(self.genome[2,8]))*c.L, y=1.5*self.sin(math.radians(self.genome[2,8]))*c.L, z=c.L + c.R, n1=-1, n2=0, n3=0, lo=-3.14159 / 2 , hi=3.14159 / 2)
        #leg4
        J6 = sim.send_hinge_joint(first_body_id=self.O[0], second_body_id=self.O[4], x=0, y=0, z=c.L + c.R, n1=-1, n2=0, n3=0, lo=-3.14159 / 2 , hi=3.14159 / 2)

        J7 = sim.send_hinge_joint(first_body_id=self.O[4], second_body_id=self.O[8], x=1.5*self.cosine(math.radians(self.genome[3,8]))*c.L, y=1.5*self.sin(math.radians(self.genome[3,8]))*c.L, z=c.L + c.R, n1=-1, n2=0, n3=0, lo=-3.14159 / 2 , hi=3.14159 / 2)
        
        self.J = {}
        self.J[0] = J0
        self.J[1] = J1
        self.J[2] = J2
        self.J[3] = J3
        self.J[4] = J4
        self.J[5] = J5
        self.J[6] = J6
        self.J[7] = J7
