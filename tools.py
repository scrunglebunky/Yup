from math import sqrt

#a moving point class that calculates the distances and how much to move
class MovingPoint():
    def __init__(self,pointA:tuple,pointB:tuple,distance:float=None,speed:int=1):
        self.pointA,self.pointB = pointA,pointB #saving points
        self.position = list(self.pointA)
        self.distance = MovingPoint.calc_distance(pointA,pointB)
        self.move_vals = MovingPoint.calc_move_vals(pointA,pointB,self.distance,speed) #calculating values

    def update(self):
        self.position[0] += self.move_vals[0]
        self.position[1] += self.move_vals[1]

    @staticmethod
    def calc_move_vals(pointA:tuple,pointB:tuple,distance:float=None,speed:int=1) -> tuple: #calculating how much to move
        if type(distance) != float:
            distance=calc_distance(pointA,pointB)
        return (
            (speed * (pointB[0] - pointA[0]) / distance),
            (speed * (pointB[1] - pointA[1]) / distance)
        )
    
    @staticmethod
    def calc_distance(pointA:tuple,pointB:tuple): #calculating distance, self explanatory
        return sqrt(
                ((pointB[0]-pointA[0])**2) + 
                ((pointB[1]-pointA[1])**2)
            ) 

class Clock(): # a redo of pygame.clock to add more values
    def __init__(self,clock,FPS=60): #initiating stuff
        self.FPS = FPS
        self.clock = clock
        self.offset = 2
    def tick(self): #updating clock
        self.clock.tick(self.FPS)
        self.offset = 60/(self.clock.get_fps() if self.clock.get_fps() != 0 else 60)
