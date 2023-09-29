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

        #preventing zero division
        if distance == 0:
            return (
            (speed * (pointB[0] - pointA[0]) ),
            (speed * (pointB[1] - pointA[1]) )
        )

        #normal movement calc
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

class MovingPoints(MovingPoint):
    def __init__(self,pos:tuple,points:list,speed:int=1,final_pos:list=None):
        self.pos = list(pos)
        self.points = points #points to follow
        self.cur_target = 0 #which point in points to target
        self.speed = speed
        self.distance = MovingPoint.calc_distance(self.pos,self.points[self.cur_target])
        self.move_vals = MovingPoint.calc_move_vals(self.pos,self.points[self.cur_target],self.distance,self.speed)
        
        #checking for finish
        self.finished = False
        #the final position to go to if finished
        self.final_pos = [final_pos,] if final_pos is not None else None
        #a trigger to see if the final pos has been reached yet
        self.final_trigger = False if self.final_pos is not None else True
        
    def update(self):
        if not self.finished:
            #updating
            self.pos[0] += self.move_vals[0]
            self.pos[1] += self.move_vals[1]
            self.distance = MovingPoint.calc_distance(self.pos,self.points[self.cur_target])
            #checking for completion
            if abs(self.distance)<self.speed*1.5:
                self.cur_target += 1
                #fully completing
                self.finished = self.cur_target >= len(self.points)
                if self.finished and not self.final_trigger:
                    #tripping the final position to go to
                    self.points = self.final_pos
                    self.cur_target = 0 
                    self.final_trigger = True
                    self.finished = False
                    self.distance = MovingPoint.calc_distance(self.pos,self.points[self.cur_target])
                    self.move_vals = MovingPoint.calc_move_vals(self.pos,self.points[self.cur_target],self.distance,self.speed)
    
                    return
                elif self.finished:
                    return
                #if not, updating values
                else:
                    self.distance = MovingPoint.calc_distance(self.pos,self.points[self.cur_target])
                    self.move_vals = MovingPoint.calc_move_vals(self.pos,self.points[self.cur_target],self.distance,self.speed)
    


class Clock(): # a redo of pygame.clock to add more values
    def __init__(self,clock,FPS=60): #initiating stuff
        self.FPS = FPS
        self.clock = clock
        self.offset = 2
    def tick(self): #updating clock
        self.clock.tick(self.FPS)
        self.offset = 60/(self.clock.get_fps() if self.clock.get_fps() != 0 else 60)
