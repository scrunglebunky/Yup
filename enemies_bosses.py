import pygame,random,score
from player import Player
from anim import all_loaded_images as img
from anim import AutoImage as AImg
from emblems import Emblem as Em
from math import sin
from bullets import * 
from enemies import Template,HurtBullet
from tools import MovingPoint


#a boss contains a collection of autoimages and hitboxes in order to check for very specific collision
class Boss():
    #the boss behaves like a puppet master to a bunch of different boss "attributes". it may be as simple as a small png, or as complex as a series of limbs and a head with jaws
    def __init__(self,kwargs:dict):
        self.sprites = kwargs['sprites']
        self.attributes = {
            #a collection of other sprites to be added to the boss: the main body, arms, head maybe?
        }
        self.info = {
            #a series of information pieces on the boss. 
            'health':10,
            "state":"enter",
            'ENDBOSSEVENT':False, #a check to see if the boss state should end
            "phase":0, #this can be a variety of factors but is usually handled specifically by the inheritors of this class, as the amount of phases varies based off boss
            'invincible':False, #a global check for invincibility. each individual asset also has invincibility. 
        }
        self.atk_info = {
            "when":120, #after how many frames in idle should I attack? 
            'type':0, #what type of attack is being went with
            'types':0, #how many types of attacks there are (0 just means 1 here don't worry)
        }
        self.timers = {
            "total":0,
            "in_state":0,
        }
        self.states = {
            "enter":self.state_enter,
            "idle":self.state_idle,
            "attack":self.state_attack,
            "return":self.state_return,
            "die":self.state_die,
        }

        #various unorganized values
        self.player = kwargs['player']
    def update(self):
        #timer update
        self.timers['total'] += 1
        self.timers['in_state'] += 1
        #state and health update
        self.states[self.info['state']]()
        if self.info['health'] <= 0 and self.info['state'] != "die":
            self.change_state("die")
        

    def collision_master(self,collidername,collide_type,collided):
        #first value -> attribute that found collision #second value -> type of sprite the attribute collided with #third value -> the actual item
        ...
    def addAttribute(self,name:str,attribute):
        self.attributes[name] = attribute
        self.sprites[0].add(attribute)
        self.sprites[2].add(attribute)

    #STATE DEFINITIONS
    #Just like how any enemy will work
    def state_enter(self,start:bool=False):...
    def state_start(self,start:bool=False):...
    def state_idle(self,start:bool=False):...
    def state_attack(self,start:bool=False):...
    def state_return(self,start:bool=False):...
    def state_die(self,start:bool=False):
        #default kill code, to tell the program that the boss is dead
        self.info['ENDBOSSEVENT'] = True
        for attribute in self.attributes.values():
            attribute.kill()
        
    #changing what state is being done
    def change_state(self,state:str):
        self.info['state'] = state
        self.timers['in_state'] = 0 
        self.states[self.info['state']](start=True)
    def hurt(self,amount=1):
        self.info['health'] -= amount
        self.sprites[0].add(Em(im='die',coord=self.attributes['body'].rect.center,isCenter=True,animation_killonloop=True))

        

#a piece of a boss. think of the boss as some sort of hand controlling a bunch of puppets.
class BossAttribute(pygame.sprite.Sprite):
    def __init__(self,host:Boss, sprites:dict, name:str="placeholder", image:str = "placeholder.bmp", pos:tuple = (100,100)):
        #basic initialization
        pygame.sprite.Sprite.__init__(self)
        self.sprites=sprites
        
        #image info
        self.autoimage = AImg(name=image)
        self.image = self.autoimage.image

        #positioning info
        self.rect = self.image.get_rect()
        self.rect.center = pos

        #naming info
        self.host = host
        self.name = name

        #health information
        self.health = 0 
        self.healthAffectGlobal = True
        self.healthProtected = False
    def on_collide(self,collide_type:int,collided:pygame.sprite.Sprite):
        self.host.collision_master(self,collide_type,collided)
    def update(self):
        #graphic update
        self.autoimage.update()
        self.image = self.autoimage.image
    def shoot(self, type: str="point", spd: int=7, info: tuple=((0,0),(100,100)), shoot_if_below: bool=True):
        bullet=None
        if (shoot_if_below) or (type != 'point') or (info[0][1] < info[1][1]-50):
            bullet = HurtBullet(type=type,spd=spd,info=info,texture=None)
            self.sprites[0].add(bullet)
            self.sprites[2].add(bullet)
        return bullet

        



#UFO
class UFO(Boss):
    def __init__(self,**kwargs):
        Boss.__init__(self,kwargs=kwargs)

        self.info['health'] = 100

        #setting attack info
        self.atk_info['when'] = random.randint(60,360)
        self.atk_info['pinch'] = False #if the boss is angry
        self.atk_info['types'] = 2 #chad spam, succ, chad kaboom
        #atk1 info
        self.atk_info['1_angle'] = 0 #during the first bullet spam, what angle is done
        #atk2 info
        self.atk_info['2_direction'] = 'l' #is the enemy coming from the left or the right during succ?
        self.atk_info['2_x'] = 0 #x velocity
        self.atk_info['2_y'] = 0 #when the enemy is getting lifted off the ground. 
        self.atk_info['2_state'] = 0 # 0: moving off to one side (l or r) ; 1: slowly speeding to the other side ; 2 - slowing back down and raising back to the 
        self.atk_info['2_swingpoint'] = 0 # 0: moving off to one side (l or r) ; 1: slowly speeding to the other side ; 2 - slowing back down and raising back to the 
        #atk3 info
        self.atk_info['3_move'] = None #tools.MovingPoint to a random position
        self.atk_info['3_bullets'] = [ ] #where all the bullets are stored
        self.atk_info['3_counter'] = 4 #how many points the boss moves to, based on health
        self.atk_info['3_count'] = 0 #what point the boss is currently at
        self.atk_info['3_wait'] = 0 #when the boss waits before moving again
        self.atk_info['3_spd'] = 15 #how fast the boss moves

        #creating
        self.addAttribute(name='body',attribute=BossAttribute(host=self,sprites=self.sprites,image="boss_ufo",name='body',pos=(300,100)))
        self.addAttribute(name='succ',attribute=BossAttribute(host=self,sprites=self.sprites,image="boss_ufo_succ",name='succ'))
        #hiding attributes
        self.attributes['succ'].rect.center = (-1000,-1000)

        #the enemy will begin the enter state now
        self.change_state('enter')

    #generally updating everything, including animations
    def update(self):
        Boss.update(self)
        # for attribute in self.attributes.values():
        #     attribute.update()

    
    #managing collision
    def collision_master(self,collider,collide_type,collided):
        if collider.name == 'body':
            if type(collided) == Player:
                if ((collider.rect.centery) > collided.rect.bottom-collided.movement[0]):
                    #bouncing the player up
                    collided.bounce()
                    #making the player invincible for six frames to prevent accidental damage
                    collided.invincibility_counter = 18
                    #taking damage
                    if self.info['state'] != 'die': self.hurt()
                #killing bullet
                collided.hurt()
            elif collide_type == 1:
                collided.hurt()
                if self.info['state'] != 'die': self.hurt()
        elif collider.name == 'succ':
            if type(collided) == Player:
                collided.movement[0] = -3



    #the whole swaying movement
    def idle_move(self) -> None:
        self.attributes['body'].rect.center = (
                300 + 200*sin(self.timers['in_state']/20),
                200 + 50*sin(self.timers['in_state']/10)
            )



    #idle state, moving from side to side
    def state_idle(self,start:bool=False):
        #figuring out when to attack
        if start:
            self.atk_info['when'] = random.randint(60,300)
        #attacking when time is met
        elif self.timers['in_state'] % self.atk_info['when'] == 0:
            self.change_state('attack')
        #movement
        self.idle_move()


        
    #enter state teehee
    def state_enter(self,start:bool=False):
        if start:
            self.attributes['body'].rect.centerx = pygame.display.play_dimensions[0]//2
            self.attributes['body'].rect.centery = -200
        #slowly lowering down to the screen
        elif abs(self.attributes['body'].rect.centery-200) > 25:
            self.attributes['body'].rect.centery = (self.timers['in_state']*3 + 10*sin(self.timers['in_state']/7)) - 200
        #bobbing up and down until enter state finished
        elif self.timers['in_state'] < 360:
            self.attributes['body'].rect.centery = 200 + 10*sin(self.timers['in_state']/10)
        #exit state
        else:
            self.change_state('idle')



    #attack state
    def state_attack(self,start:bool=False):
        #selecting what attack to do
        if start:
            self.atk_info['type'] = random.randint(0,self.atk_info['types'])
            #changing animation
            self.attributes['body'].autoimage.change_anim('chad' if (self.atk_info['type'] == 0 or self.atk_info['type'] == 2) else "succ" if self.atk_info['type'] == 1 else 'idle')
            #startup info per attack
            if self.atk_info['type'] == 1:
                self.atk_info['2_direction'] = random.choice(('l','r'))
                # self.atk_info['2_direction'] = 'r' #REMOVE THIS
        
        
        #spinning shoot
        elif self.atk_info['type'] == 0:
            #movement
            self.idle_move()
            #changing angle
            self.atk_info['1_angle'] += 15
            self.attributes['body'].shoot("angle",7,info=(self.attributes['body'].rect.center,self.atk_info['1_angle']))
            #returning (changing animation)
            if self.timers['in_state'] >= 180:
                self.atk_info['type'] = 'leave' #just so code ain't repeated, it moves to the final end statement
        
        #static shoot
        elif self.atk_info['type'] == 2:
            #adding a new spot to move to, if either the first time or
            if (type(self.atk_info['3_move']) != tools.MovingPoint) or (self.atk_info['3_spd'] == 0 and self.atk_info['3_wait'] >= 15):
                self.atk_info['3_move'] = tools.MovingPoint(pointA=self.attributes['body'].rect.center,pointB=(random.randint(0,600),random.randint(0,600)),speed=15,ignore_speed=True,check_finished=False)
                self.atk_info['3_spd'] = self.atk_info['3_move'].speed #how fast the boss moves
                self.atk_info['3_wait'] = 0 #resetting wait itmer
                self.atk_info['3_count'] += 1 #updating counter
                #checking to exit
                if self.atk_info['3_count'] > self.atk_info['3_counter']:
                    self.atk_info['type'] = 'leave' 
                    self.atk_info['3_count'] = 0
            #waiting 
            elif self.atk_info['3_spd'] == 0:
                self.atk_info['3_wait'] += 1
                #doing a shoot spam based on movement
                if self.atk_info['3_wait'] % 3 == 0:
                    for i in range(30):
                        self.attributes['body'].shoot(type="angle",spd=7,info=(self.attributes['body'].rect.center,i*15))
            #moving
            else:
                #updating speed
                self.atk_info['3_spd'] = round(self.atk_info['3_spd']*0.925,3) if self.atk_info['3_spd'] > 0.25 else 0
                self.atk_info['3_move'].speed = self.atk_info['3_spd'] 
                #updating movement values
                self.atk_info['3_move'].update()
                self.attributes['body'].rect.center = self.atk_info['3_move'].position




        #succin ya up
        elif self.atk_info['type'] == 1:

            #moving off to the left
            if self.atk_info['2_state'] == 0:
                self.attributes['body'].rect.x += (5 if self.atk_info['2_direction'] == 'r' else -5)
                if self.attributes['body'].rect.right < 0 or self.attributes['body'].rect.left > pygame.display.play_dimensions[0]:
                    #preparing the swing to the left
                    self.atk_info['2_state'] = 1
                    #telling the boss when to swing upwards
                    self.atk_info['2_swingpoint'] = pygame.display.play_dimensions[0]-200 if self.atk_info['2_direction'] == 'l' else 200
                    self.atk_info['2_x'] = 0
                    self.atk_info['2_y'] = -3
                    self.attributes['body'].rect.centery = pygame.display.play_dimensions[1] - 200


            #speeding to the sides
            elif self.atk_info['2_state'] == 1:

                #NOTE - l means it COMES FROM the left, and moves to the right, vice versa with r
                if self.atk_info['2_x'] < 15 and self.atk_info['2_x'] > -15: 
                    self.atk_info['2_x'] += 0.1 if self.atk_info['2_direction'] == 'l' else -0.1
                self.attributes['body'].rect.x += self.atk_info['2_x']

                #swinging upwards up and away wahoo
                if abs(self.attributes['body'].rect.centerx - self.atk_info['2_swingpoint']) < 30:
                    self.atk_info['2_state'] = 2

                #positioning the succinator
                self.attributes['succ'].rect.center = self.attributes['body'].rect.center


            #swinging back up
            elif self.atk_info['2_state'] == 2:
                # print("---------------------SWING BACK")
                #updating velocities
                self.atk_info['2_x'] -= (1.5 if self.atk_info['2_direction'] == 'l' else -1.5)
                self.atk_info['2_y'] += 2
                #moving
                self.attributes['body'].rect.x += self.atk_info['2_x']
                self.attributes['body'].rect.y -= self.atk_info['2_y']
                #checking to finish
                if self.attributes['body'].rect.centery < 300:
                    self.atk_info['type'] = 'finish'
                    self.atk_info['2_x'] = self.atk_info['2_y'] = self.atk_info['2_state'] = self.atk_info['2_swingpoint'] = 0
                
                #succ effect disappearance
                self.attributes['succ'].rect.centerx = self.attributes['body'].rect.centerx
                self.attributes['succ'].rect.centery += self.atk_info['2_y']


                
     
            
        else:
            #changing animation and returning
            self.attributes['body'].autoimage.change_anim('idle')
            self.change_state('idle')

        #spazzing out effect
        if self.atk_info['type'] == 0 or self.atk_info['type'] == 2:
            self.attributes['body'].rect.centerx += random.randint(-5,5)
            self.attributes['body'].rect.centery += random.randint(-5,5)
        

    
    #dying state
    def state_die(self,start:bool=False):
        if start:
            self.attributes['body'].autoimage.change_anim('dead')

        #jittering around
        self.attributes['body'].rect.centerx += random.randint(-25,25)
        self.attributes['body'].rect.centery += random.randint(-25,25)

        #borders
        if self.attributes['body'].rect.bottom > 600:
            self.attributes['body'].rect.y -= 25

        #increasing score
        score.score += 30

        
        #kaboom
        if self.timers['in_state'] % 3 == 0:
            self.sprites[0].add(Em(
                    im='kaboom',
                    coord=(random.randint(0,600),random.randint(0,500)),
                    isCenter=True,
                    animation_killonloop=True,
                    resize=(100,100)
                    ))


        #ending
        if self.timers['in_state'] > 240:
            self.info['ENDBOSSEVENT'] = True



    #hurting but with a cute animation
    def hurt(self,amount=1):
        Boss.hurt(self,amount)
        if self.info['health'] % 5 == 0:
            self.attributes['body'].autoimage.change_anim(
                'hurt' +  ("CHAD" if (self.info['state'] == 'attack' and (self.atk_info['type'] == 2 or self.atk_info['type'] == 0)) else "SUCC" if (self.info['state'] == 'attack' and self.atk_info['type'] == 1) else "" )
            )








#NOPE
class Nope(Boss):
    def __init__(self,**kwargs):
        Boss.__init__(self,kwargs=kwargs)
        #setting basic info
        self.info['health'] = 150
        self.info['state'] = 'intro'
        self.states['intro'] = self.state_intro
        #adding attributes
        self.addAttribute("intro",attribute=NopeIntro(host=self,sprites=self.sprites))
        self.addAttribute("body",attribute=BossAttribute(host=self,sprites=self.sprites,name="body",image="boss_nope",pos=(-1000,-1000)))
        #attack info
        self.atk_info['type'] = 0 #currently on 1 attack
        self.atk_info['types'] = 1 #2 attacks
        self.atk_info['idle_move'] = tools.MovingPoint(self.attributes['body'].rect.center,self.attributes['body'].rect.center,speed=0)
        self.atk_info['idle_spd'] = 0 
        #attack 2 lockon
        self.atk_info['2_state'] = 0 #0 is locking on, 1 is falling, 2 is collapsing, 3 is rising back up
        self.atk_info['2_x'] = 0 #where the boss is going, locking onto
        self.atk_info['2_wait'] = 0 #waiting at the bottom for a little bit before rising back to the top
        self.atk_info['2_bottom'] = pygame.display.play_dimensions[1]*0.9

        #attack 1 shoot
        #just as a description. the boss shoots a large bullet at you every x frames while also shooting in a bunch of other spots every x frames

    
    def update(self):
        Boss.update(self)
        # for attribute in self.attributes.values():
        #     attribute.update()


    def collision_master(self,collider,collide_type,collided):
        #collision for the decoy, 
        if collider.name == 'intro':
            #hurting player
            if type(collided) == Player:
                collided.hurt()
            #hurting self and bullet
            elif collide_type == 1:
                collider.hurt()
                collided.hurt()
                # if self.info['state'] != 'die': self.hurt()
        #collision for main boss
        if collider.name == 'body':
            if type(collided) == Player:
                if ((collider.rect.centery) > collided.rect.bottom-collided.movement[0]):
                    #bouncing the player up
                    collided.bounce()
                    #making the player invincible for six frames to prevent accidental damage
                    collided.invincibility_counter = 18
                    #taking damage
                    if self.info['state'] != 'die': self.hurt()
                #killing bullet
                collided.hurt()
            elif collide_type == 1:
                collided.hurt()
                self.hurt()
            

    def state_intro(self,start:bool=False):
        ...
        #using this for explanation purposes.
        #the start of the boss has a decoy attribute called 'intro' which is a placeholder nope enemy, and the boss only begins when that happens
        #so for the most part, this empty intro state plays while the decoy nope does all the coding.
        #All that is handled internally is the collision because it has to be to look nice. 
    


    def state_enter(self,start:bool=False):
        if start:
            #explosion when first entering the screen from the decoy
            self.attributes['body'].rect.center = self.attributes['intro'].rect.center
            self.sprites[0].add(Em(im='kaboom',coord=self.attributes['body'].rect.center,isCenter=True,animation_killonloop=True,resize=(350,350)))
        elif self.timers['in_state'] < 60: #change later
            #aggressive jittering
            self.attributes['body'].rect.centery = self.attributes['intro'].rect.centery + 10*sin(self.timers['in_state']/25) + random.randint(-1,1)
            if self.timers['in_state']%2==0:self.attributes['body'].rect.centerx = pygame.display.play_dimensions[0]/2 + random.randint(-2,2)
        else:
            #changing the state to idle
            self.change_state('idle')



    def state_idle(self,start:bool=False):
        #in the idle state, moving from point to point at random
        if self.atk_info['idle_move'].speed < (0.5 if self.info['health'] > 50 else 5):
            self.atk_info['idle_move'] = tools.MovingPoint(pointA=self.attributes['body'].rect.center,pointB=(random.randint(0,600),random.randint(0,400)),ignore_speed=True,speed=10)
            #shooting
            for i in range(15): self.attributes['body'].shoot(type="angle",spd=7,info=(self.attributes['body'].rect.center,i*24))
            #changing state
            if random.randint(1,10) == 2:
                self.change_state('attack')
        else:
            #updating movement
            self.atk_info['idle_move'].update()
            self.atk_info['idle_move'].speed *= 0.95
            self.attributes['body'].rect.centerx = self.atk_info['idle_move'].position[0]
            self.attributes['body'].rect.centery = self.atk_info['idle_move'].position[1]
            #shaking amount based on health
            self.attributes['body'].rect.centerx += random.randint((-1*(151-self.info['health'])//20),((151-self.info['health'])//20))
            self.attributes['body'].rect.centery += random.randint((-1*(151-self.info['health'])//20),((151-self.info['health'])//20))



    def state_attack(self,start:bool=False):
        if start:
            #picking an attack type to undergo
            self.atk_info['type'] = random.randint(0,self.atk_info['types'])
            #resetting info for attack type 1 - lockon
            if self.atk_info['type'] == 1:
                self.atk_info['2_state'] = 0
                self.attributes['body'].rect.centery = 100
                self.attributes['body'].autoimage.change_anim('scream')

            #setting info for attack type 0 - shoot
            elif self.atk_info['type'] == 0:
                self.attributes['body'].autoimage.change_anim('scream')

        if self.atk_info['type'] == 0:
            #shooting attack
            if (self.timers['in_state'] % 3 == 0) or (self.info['health'] < 50):
                self.attributes['body'].shoot(type="angle",spd=5,info=(self.attributes['body'].rect.center,self.timers['in_state']*13))
            if (self.timers['in_state'] % 45 == 0) or (self.info['health']<50 and self.timers['in_state'] % 35 == 0):
                self.attributes['body'].shoot(spd=10,info=(self.attributes['body'].rect.center,self.player.rect.center))
                if self.info['health'] < 50:
                    for i in range(5):
                        self.attributes['body'].shoot(spd=random.randint(7,10),info=(self.attributes['body'].rect.center,(self.player.rect.centerx+random.randint(-25,25),self.player.rect.centery+random.randint(-25,25))))

            #jittering
            self.attributes['body'].rect.x += random.randint(-1,1); self.attributes['body'].rect.y += random.randint(-1,1)
            #ending
            if self.timers['in_state'] > 360:
                self.atk_info['type'] = 9999 #this makes the end code run, anything outside of the defined values
        

        elif self.atk_info['type'] == 1:
            #following attack 
            if self.atk_info['2_state'] == 0:
                #indicating player the fall
                self.attributes['body'].rect.centerx = self.player.rect.centerx
                if self.timers['in_state'] > 120:
                    self.atk_info['2_state'] = 1
            #waiting to indicate launch
            elif self.atk_info['2_state'] == 1:
                if self.timers['in_state'] > 180:
                    self.atk_info['2_state'] = 2
                    self.attributes['body'].autoimage.change_anim('flydown')

            #launching
            elif self.atk_info['2_state'] == 2:
                #going to bounce state if hitting bottom
                if self.attributes['body'].rect.centery > self.atk_info['2_bottom']:
                    self.atk_info['2_state'] = 3
                    self.attributes['body'].autoimage.change_anim('bounce')
                    self.atk_info['2_wait'] = 0 
                #flying down if not bounced yet
                else:
                    self.attributes['body'].rect.y += 25
            #bouncing
            elif self.atk_info['2_state'] == 3:
                self.atk_info['2_wait'] += 1
                if self.atk_info['2_wait'] > 60:
                    self.attributes['body'].rect.y -= 5
                if self.attributes['body'].rect.y < 100:
                    self.atk_info['2_state'] = 4
            else:
                self.atk_info['type'] = 9999
            
        
        
        else:
            self.attributes['body'].autoimage.change_anim('idle')
            self.change_state('idle')
        
        

    def state_die(self,start:bool=False):
        if start:
            self.attributes['body'].autoimage.change_anim("dead")
        elif self.timers['in_state'] < 80:
            self.attributes['body'].rect.center = (300,100)
            self.attributes['body'].rect.x += random.randint(-5,5); self.attributes['body'].rect.y += random.randint(-3,3)

        elif self.timers['in_state'] == 80:
            self.sprites[0].add(Em(
                    im='kaboom',
                    coord=self.attributes['body'].rect.center,
                    isCenter=True,
                    animation_killonloop=True,
                    resize=(450,450)
                    ))
            self.attributes['body'].kill()

        elif self.timers['in_state'] > 240:
            self.info['ENDBOSSEVENT'] = True




    #taking damage, goofy animation, you know the jizz
    def hurt(self,amount=1):
        Boss.hurt(self,amount)
        if self.info['health'] % 5 == 0 and not self.info['state'] == 'attack':
            self.attributes['body'].autoimage.change_anim('hurt')


class NopeIntro(BossAttribute):
    #The boss decoy, which is used as a cute little intro for a nope that got way too pissed. 
    def __init__(self,host,sprites):
        #setting values
        BossAttribute.__init__(self,host=host,sprites=sprites,name="intro",image="nope_D",pos=(pygame.display.play_dimensions[0]/2,-100))
        self.state = 'enter'
        self.health = 5
        self.enter_y_momentum = 5
        self.states = {'enter':self.state_enter,'wait':self.state_wait}



    def update(self):
        #basic update
        BossAttribute.update(self)
        try: self.states[self.state]()
        except ValueError: self.kill()
        


    def state_enter(self):
        #sliding downwards 
        self.rect.centery += self.enter_y_momentum
        self.enter_y_momentum = round(self.enter_y_momentum*0.99,3)
        if self.enter_y_momentum < 1:
            self.state='wait'

    def state_wait(self):
        #doing nothing when sliding
        ...

    def hurt(self):
        #changing the boss state to enter when killed
        self.health -= 1
        self.sprites[0].add(Em(im='die',coord=self.rect.center,isCenter=True,animation_killonloop=True))
        if self.health <= 0:
            self.kill()
            self.host.change_state('enter')

        
        

 
    

loaded = {
    "ufo":UFO,
    "nope":Nope,
}
    