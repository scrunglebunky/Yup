import pygame,anim,random,score,bullets

class Template(pygame.sprite.Sprite):
    #default image if unchanged
    image = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(image, "red", (15, 15), 15)

    def __init__(self,offset:tuple=(0,0),pos:tuple=(0,0),difficulty:int=0,**kwargs):
        pygame.sprite.Sprite.__init__(self)

        self.idle={ #information about the idle state
            "offset":offset,
            "full":[(pos[0]+offset[0]),(pos[1]+offset[1])] # current position in idle
        }
        self.info = { #basic information on the character
            "health":1,
            "score":100,
            "dead":False,
            "difficulty":difficulty,
            "state":"enter",
        }
        self.timers = { #counters to use to check how long something is there for
            "exist":0,
            "in_state":0
        }
        self.states = { #states the enemy can be in at any time
            "enter":self.state_enter,
            "idle":self.state_idle,
            "attack":self.state_attack,
            "return":self.state_return,
        }
        #image values, including spritesheets
        self.spritesheet = None
        self.image = Template.image
        self.rect = self.image.get_rect()
        self.rect.center = self.idle["full"]

    def update(self): #this should be run the same no matter what
        #updating state
        self.states[self.info["state"]]()

        #updating spritesheet
        if type(self.spritesheet) == anim.Spritesheet:
            self.spritesheet.update()
            self.image = self.spritesheet.image
        else:
            self.image = Template.image
        
        #checking for death
        self.info['dead'] = (self.info['health'] <= 0)
        if self.info['dead']:
            self.kill(reason="health")

        #updating timers
        self.timers['exist'] += 1
        self.timers['in_state'] += 1

    ##########STATE FUNCTIONS################
    def state_enter(self):
        self.info["state"] = 'idle'
    def state_idle(self):
        self.rect.center = self.idle["full"]
    def state_attack(self):
        self.info["state"] = 'idle'
    def state_return(self):
        self.info["state"] = 'idle'


    #############SPECIAL###############
    def change_anim(self,animation):
        if type(self.spritesheet) == anim.Spritesheet:
            self.spritesheet.change_anim(animation)

    def change_state(self,state):
        self.timers['in_state'] = 0 
        self.info['state'] = state

    def kill(self,reason=None) -> int:
        if reason == "health":
            score.score += self.info["score"]
        pygame.sprite.Sprite.kill(self)
        self.info['dead'] = True

        return self.timers['exist']
        
    def on_collide(self,
                   collide_type:int #the collide_type refers to the sprite group numbers. 0 for universal (not used), 1 for other player elements, 2 for enemies
                   ):
        #5/26/23 - Updating health shizznit if interaction with "player type" class
        if collide_type == 1 or collide_type == 3:
            self.info['health'] -= 1

    def formationUpdate(self,
        new_pos:tuple #location of the formation, not including offset
        ):
        #following formation
        self.idle['full'] = [
            (new_pos[0] + self.idle["offset"][0]),
            (new_pos[1] + self.idle["offset"][1])]
        




class A(Template): #geurilla warfare
    def __init__(self,offset:tuple,pos:tuple,difficulty:int,skin='nope_A',**kwargs):
        Template.__init__(self,offset,pos,difficulty)
        self.spritesheet = anim.Spritesheet(skin,current_anim='idle') if skin is not None else None
class B(Template): #loop-de-loop
    def __init__(self,offset:tuple,pos:tuple,difficulty:int,skin='nope_B',**kwargs):
        Template.__init__(self,offset,pos,difficulty)   
        self.spritesheet = anim.Spritesheet(skin,current_anim='idle') if skin is not None else None
class C(Template): #turret
    def __init__(self,offset:tuple,pos:tuple,difficulty:int,skin='nope_C',player=None,sprites=None,**kwargs):
        Template.__init__(self,offset,pos,difficulty)  
        self.spritesheet = anim.Spritesheet(skin,current_anim='idle') if skin is not None else None
        self.sprites = sprites
        self.player=player
        self.timer = (360 - (5*self.info['difficulty']))
        self.time = random.randint(0,self.timer)
    def state_idle(self):
        Template.state_idle(self)
        self.time += 1
        if self.time >= self.timer:
            self.change_state('attack')
            self.time = 0
    def state_attack(self):
        if self.timers['in_state'] == 1:
            self.change_anim("attack") 
            bul=bullets.HurtBullet(pos=self.rect.center,target=self.player.rect.center,speed=4)
            self.sprites[0].add(bul);self.sprites[2].add(bul)
        self.change_state('idle')
            
class D(Template): #special -- uses special value to inherit from that character instead 
    def __init__(self,offset:tuple,pos:tuple,difficulty:int,skin:str='nope_D',special:str=None,**kwargs):
        #placeholder value
        Template.__init__(self,offset,pos,difficulty)
        self.spritesheet = anim.Spritesheet(skin,current_anim='idle') if skin is not None else None

class Nope(Template):
    def __init__(self,offset:tuple,pos:tuple,difficulty:int,skin:str=None,special:str=None,**kwargs):...
    
        


loaded = {
    "A":A,
    "B":B,
    "C":C,
    "D":D,
    }


########OLD


# DEFAULT CHARACTER
# class CharTemplate(pygame.sprite.Sprite):
#     #default image if unchanged
#     image = pygame.Surface((30, 30), pygame.SRCALPHA)
#     pygame.draw.circle(image, "red", (15, 15), 15)
    
#     def __init__(self,formation_position:tuple,offset:tuple,default_image = True,**kwargs):
#         #initializes sprite code
#         pygame.sprite.Sprite.__init__(self)
        
#         #TAKING ARGUMENTS
#         self.offset = offset

#         #default character code
#         self.state = "enter" #current behavior patterns
#         self.health=1 #Health for characters
#         self.scorevalue=100 #Score given to player
#         self.idlePos = [(formation_position[0]+self.offset[0]),(formation_position[1]+self.offset[1])] # current position in idle
#         self.dead = (self.health <= 0)

#         #IMAGE CODE
#         self.sh = None
#         if default_image:
#             self.image = CharTemplate.image
#             self.rect = self.image.get_rect()
    
#         #SHOOT CODE    
#         self.shoot_times = [] #the maximum amount will be like 10, which would only be achieved after level 100 or so
#         #shoot times are not generated by default

#         #STATE CODE
#         self.frames_in_state = 0 #counter for states. reset at the end of every state, but risen every frame, whether used or not.

#         #CONTAINER CODE -- ITEM DROPPER
#         self.container:tuple = None #a tuple, containing the type of item and the name of the item. the second index is usually unused if the item is not a bullet.


#     def update(self):
#         self.state_update()
#         self.collision_update()
#         self.animation_update()

#     def animation_update(self):
#         pass

#     def state_update(self):
#         self.frames_in_state += 1
#         if self.state=="enter": self.state_enter()
#         if self.state=="idle_search": self.state_idle_search()
#         if self.state=="idle": self.state_idle()
#         if self.state=="attack": self.state_attack()
#         if self.state=="return": self.state_return()

#     def state_enter(self):
#         self.stchg('idle_search')

#     def state_idle_search(self):
#         #Slowly dragging the character to the title screen
#         horizontal_condition_met = abs(self.idlePos[0] - self.rect.center[0]) <= 5
#         vertical_condition_met = abs(self.idlePos[1] - self.rect.center[1]) <= 5
#         if not horizontal_condition_met or not vertical_condition_met:
#             if not horizontal_condition_met:
#                 if self.idlePos[0] < self.rect.center[0]:
#                     self.rect.x -= 5
#                 elif self.idlePos[0] > self.rect.center[0]:
#                     self.rect.x += 5
#             if not vertical_condition_met:
#                 if self.idlePos[1] < self.rect.center[1]:
#                     self.rect.y -= 3
#                 elif self.idlePos[1] > self.rect.center[1]:
#                     self.rect.y += 3
#         else: 
#             self.stchg('idle')

#     def state_idle(self):
#         #this is the only state that does not have a frame counter
#         #this is because it does not automatically exit
#         self.rect.center=self.idlePos

#     def state_attack(self):
#         #same default as state_enter
#         if True: 
#             self.stchg("return") 

#     def state_return(self):
#         if True:
#             self.stchg("idle_search") #or 'idle'  

#     def collision_update(self):
#         #most of what this does is check for health
#         #collision is a universal term for health, positioning, etc.
#         #DO NOT CHANGE THIS. THIS WILL MESS UP THE FORMATION
#         self.dead = (self.health <= 0)
#         if self.dead:
#             self.kill(reason="health")

#     def on_collide(self,
#                    collide_type:int #the collide_type refers to the sprite group numbers. 0 for universal (not used), 1 for other player elements, 2 for enemies
#                    ):
#         #5/26/23 - Updating health shizznit if interaction with "player type" class
#         if collide_type == 1:
#             self.health -= 1

#     def formationUpdate(self,
#         new_pos:tuple #location of the formation, not including offset
#         ):
#         #following formation
#         self.idlePos = [
#             (new_pos[0] + self.offset[0]),
#             (new_pos[1] + self.offset[1])]
    
#     def stchg(self,state:str): #changing the state 
#         self.frames_in_state = 0 
#         self.state = state
    
#     def kill(self,reason=None):
#         if reason == "health":
#             score.score += self.scorevalue
#         pygame.sprite.Sprite.kill(self)
       
#     def change_anim(self,anim:str) -> bool:
#         try:
#             self.sh.change_anim(anim)
#             return True
#         except: return False

# class Nope(CharTemplate):

#     image = pygame.Surface((30, 30), pygame.SRCALPHA)
#     pygame.draw.rect(image,"red",pygame.Rect(0,0,30,30))


#     def __init__(self,sprites:dict,level:int,formation_position:tuple,offset:tuple,data:dict,**kwargs):
#         CharTemplate.__init__(self,level=level,formation_position=formation_position,offset=offset,data=data,default_image=False,**kwargs)
#         #img code
#         # self.sh = anim.Spritesheet("NOPE","idle")
#         self.image = Nope.image
#         self.rect = self.image.get_rect()

#         #06/06/23 - enter state - copied from revC
#         self.enter_dir = random.choice(('l','r')) #where the character is entering FROM
#         self.rect.center = (pygame.display.play_dimensions[0],pygame.display.play_dimensions[1]/2) if self.enter_dir == 'r' else (0,pygame.display.play_dimensions[1]/2)
#         self.parabola = (pygame.display.play_dimensions[0],pygame.display.play_dimensions[1]*0.75) if self.enter_dir == 'r' else (25,pygame.display.play_dimensions[1]*0.75)

#         #07/09/2023 - the way the character will move in attack state
#         self.atk_patterns = [] 
#         self.spd = 0

#     def update(self):
#         CharTemplate.update(self)
#         # self.image = Nope.image
#         self.image = Nope.image
#         if self.state == 'attack':
#             self.image = pygame.transform.rotate(Nope.image,3*self.spd)

#     def state_enter(self):
#         self.rect.x = self.rect.x-2 if self.enter_dir == 'r' else self.rect.x+2

#         self.rect.y = (-(1 / 50) * ((self.rect.x + (
#             self.parabola[0] if self.enter_dir == 'l' else (self.parabola[0]*-1) )
#             ) ** 2) + self.parabola[1])

#         if abs(225-self.rect.x) <= 100 or abs(100 - self.rect.y) <= 50:
#             self.stchg("idle_search")
    
#     def state_attack(self):
#         if self.frames_in_state == 1:
#             #07/09/2023 - FIRST FRAME IN STATE - SETTING POSITIONS
#             self.atk_patterns = [random.randint(10,pygame.display.play_dimensions[0]-10) for i in range(20)]

#         # moving down
#         self.rect.y+=5

#         # moving left and right based on atk_patterns
#         if len(self.atk_patterns) > 0:
#             if abs(self.rect.center[0] - self.atk_patterns[0]) > 20:
#                 self.spd = (0.05 * (self.atk_patterns[0] - self.rect.center[0]))
#                 self.spd = -5 if self.spd < -5 else 5 if self.spd > 5 else self.spd
#                 self.rect.x += self.spd


#             else:
#                 self.spd = 0 
#                 self.atk_patterns.pop(0)



#         # exit code
#         if self.rect.top>=pygame.display.play_dimensions[1]:
#             self.rect.bottom=0
#             self.frames_in_state = 0
#             self.stchg('return') 
# class Spike(CharTemplate):
#     image = pygame.Surface((30, 30), pygame.SRCALPHA)
#     pygame.draw.rect(image,"orange",pygame.Rect(0,0,30,30))
#     def __init__(self,formation_position:tuple,offset:tuple,**kwargs):
#         #default
#         CharTemplate.__init__(self,formation_position,offset,**kwargs)
#         #setting images
#         self.image = Spike.image
#         self.rect = self.image.get_rect()

