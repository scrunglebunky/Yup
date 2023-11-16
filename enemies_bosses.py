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
        self.timers['total'] += 1
        self.timers['in_state'] += 1
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
    def update(self):...
    def shoot(self, type: str="point", spd: int=7, info: tuple=((0,0),(100,100)), shoot_if_below: bool=True):
        bullet=None
        if (shoot_if_below) or (type != 'point') or (info[0][1] < info[1][1]-50):
            bullet = HurtBullet(type=type,spd=spd,info=info,texture=None)
            self.sprites[0].add(bullet)
            self.sprites[2].add(bullet)
        return bullet

        


class UFO(Boss):
    def __init__(self,**kwargs):
        Boss.__init__(self,kwargs=kwargs)
        self.addAttribute(name='body' , attribute = UfoBody(host=self,sprites=self.sprites))
        self.info['health'] = 50

        self.atk_info["angle"]=0 #what angle the enemy is shooting at
        self.atk_info["when"]=random.randint(60,120) #when the enemy should convert to an attack
        self.atk_info['types']=1 #the enemy has two attacks
        self.atk_info['movepoint']= MovingPoint(pointA=self.attributes['body'].rect.center,pointB=self.player.rect.center,speed=5)

        self.info['invincible'] = False
    
    #a master collision function that checks based off which item is being collided with 
    def collision_master(self,collider,collide_type,collided):
        if collider.name == 'UfoBody':
            if type(collided) == Player:
                if ((collider.rect.centery) > collided.rect.bottom-collided.movement[0]):
                    #bouncing the player up
                    collided.bounce()
                    #making the player invincible for six frames to prevent accidental damage
                    collided.invincibility_counter = 18
                    #taking damage
                    self.hurt()
                collided.hurt()
            elif collide_type == 1:
                collided.hurt()
                self.hurt()

    def state_enter(self,start=False):
        if start:...
        self.change_state('idle')

    def state_idle(self,start=False):
        self.attributes['body'].shoot(type='angle',spd=6,info=(self.attributes['body'].rect.center, self.atk_info['angle']),shoot_if_below=True)
        self.attributes['body'].rect.centerx = 300 + sin(self.timers['total']/15)*100
        self.attributes['body'].rect.centery = 100 + sin(self.timers['total']/5)*25
        self.atk_info['angle'] += 13

        #figuring out when to go into the attack phase
        if self.timers['in_state'] >= self.atk_info['when']: self.change_state('attack')

    def state_attack(self,start=False):
        if start:
            self.atk_info['type'] = random.randint(0,self.atk_info['types'])
            self.atk_info['movepoint']= MovingPoint(pointA=self.attributes['body'].rect.center,pointB=self.player.rect.center,speed=5)

        elif self.atk_info['type'] == 0:
            #updating direction
            if self.timers['in_state']%10 == 0: self.atk_info['movepoint'].change_all(pointB=self.player.rect.center)
            #moving
            self.atk_info['movepoint'].update()
            self.attributes['body'].rect.center = self.atk_info['movepoint'].position
            #finishing:
            if self.timers['in_state']>360:
                self.change_state('return')

        elif self.atk_info['type'] == 1:
            #aggressively shooting
            self.attributes['body'].shoot(type="point",spd=random.randint(5,12),info=(self.attributes['body'].rect.center,self.player.rect.center))
            if self.timers['in_state']>70:
                self.change_state('return')
            
    def state_return(self,start=False):
        if start:
            #setting how to return to home base
            self.atk_info['movepoint'] = MovingPoint(pointA = self.attributes['body'].rect.center,pointB=(300,100),speed=10,check_finished=True)
        else:
            #returning to home base
            self.atk_info['movepoint'].update()
            self.attributes['body'].rect.center = self.atk_info['movepoint'].position
            if self.atk_info['movepoint'].finished:
                self.change_state('idle')


    def state_die(self,start=False):
        if start:
            self.atk_info['angle'] = 2
        else:
            #movement
            self.attributes['body'].rect.centerx += random.randint(-5,5)
            self.attributes['body'].rect.centery += random.randint(-5,5)
            #explosion
            if self.timers['in_state'] % 5 == 0:
                self.sprites[0].add(Em(
                    im='kaboom',
                    coord=(random.randint(0,600),random.randint(0,500)),
                    isCenter=True,
                    animation_killonloop=True,
                    resize=(100,100)
                    ))
            #shooting
            self.atk_info['angle'] *= 1.1
            self.attributes['body'].shoot(type='angle',spd=5,info=(self.attributes['body'].rect.center, self.atk_info['angle']),shoot_if_below=True)
            #score
            score.score += 10
            #finihsing
            if self.timers['in_state'] > 360:
                Boss.state_die(self)


class UfoBody(BossAttribute):
    def __init__(self,host,sprites):
        BossAttribute.__init__(self,host=host,sprites=sprites,name="UfoBody",image="ufo.png",pos=(300,100))
    



loaded = {
    "ufo":UFO,
}
    