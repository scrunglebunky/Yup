import pygame,anim,random,score,bullets,tools
from math import sin,cos,atan2,degrees
from player import Player

class Template(pygame.sprite.Sprite):
    #default image if unchanged
    image = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(image, "red", (15, 15), 15)

    def __init__(self,
        # offset:tuple=(0,0),
        # pos:tuple=(0,0),
        # difficulty:int=0,
        # entrance_points:dict=None,
        # entrance_speed:float=1.0,
        # entrance_shoot:list=[],
        # sprites:pygame.sprite.Group = None,
        # player:pygame.sprite.Sprite = None,
        # trip:list=(999,)
        kwargs:dict):
        pygame.sprite.Sprite.__init__(self)
        self.idle={ #information about the idle state
            "offset":kwargs['offset'],
            "full":[(kwargs['pos'][0]+kwargs['offset'][0]),(kwargs['pos'][1]+kwargs['offset'][1])] # current position in idle
        }
        self.info = { #basic information on the character
            "health":1,
            "score":100,
            "dead":False,
            "difficulty":kwargs['difficulty'],
            "state":"enter",
            "atk":False, #this is important -- it marks if the enemy can attack or not
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
        self.atk_basic = {
            "shoot_chance":(10 - self.info['difficulty'] if self.info['difficulty']<9 else 2),
            "start_shoot_chance":(5 - self.info['difficulty'] if self.info['difficulty']<4 else 1),
            "trip":kwargs['trip'],
            }
        
        
        #image values, including spritesheets
        self.spritesheet = anim.Spritesheet(kwargs['skin'],current_anim='idle') if kwargs['skin'] is not None else None
        self.image = Template.image if self.spritesheet is None else self.spritesheet.image
        self.rect = self.image.get_rect()
        self.rect.center = self.idle["full"]


        #entrance
        self.entrance_points = kwargs['entrance_points'] 
        if self.entrance_points is not None:
            self.follow = tools.MovingPoints(
                self.entrance_points[0],
                self.entrance_points,
                speed=kwargs['entrance_speed'],
                final_pos=self.idle['full'],)
        else:
            self.follow = None

        #extras
        self.sprites = kwargs['sprites']
        self.player = kwargs['player']

    def update(self): #this should be run the same no matter what
        

        #updating spritesheet
        if type(self.spritesheet) == anim.Spritesheet:
            self.spritesheet.update()
            self.image = self.spritesheet.image
            self.mask = self.spritesheet.mask
        else:
            self.image = Template.image
        
        #checking for death
        self.info['dead'] = (self.info['health'] <= 0)
        if self.info['dead']:
            self.kill(reason="health")

        #updating timers
        self.timers['exist'] += 1
        self.timers['in_state'] += 1

        #updating state
        self.states[self.info["state"]]()

    ##########STATE FUNCTIONS################
    def state_enter(self,start=False):
        if self.follow is None:
            self.info["state"] = 'idle'
        else:
            self.follow.update()
            self.rect.center = self.follow.pos
            if self.follow.finished:
                self.info['state'] = 'idle'
            #shooting based off the follow values
            if self.follow.trip and self.follow.cur_target in self.atk_basic["trip"]:
                if random.randint(0,self.atk_basic['start_shoot_chance'])==self.atk_basic['start_shoot_chance']:
                    self.shoot(type="point",spd=5,info=(self.rect.center,self.player.rect.center))
                self.follow.trip = False
    def state_idle(self,start=False):
        if start:
            self.change_anim('idle')
        self.rect.center = self.idle["full"]
    def state_attack(self,start=False):
        self.info["state"] = 'idle'
    def state_return(self,start=False):
        if start:
            #figuring out where to go
            self.follow = tools.MovingPoint(self.rect.center,self.idle['full'],speed=15,check_finished=True)
        elif not self.follow.finished:
            #going there
            self.follow.update()
            self.rect.center=self.follow.position
        elif self.follow.finished:
            #done going there
            self.change_state('idle')
        


    #############SPECIAL###############
    def change_anim(self,animation):
        if type(self.spritesheet) == anim.Spritesheet:
            self.spritesheet.change_anim(animation)

    def change_state(self,state):
        self.timers['in_state'] = 0 
        self.info['state'] = state
        self.states[self.info['state']](start=True) #the start value initializes a variable that has to be started up first

    def kill(self,reason=None) -> int:
        if reason == "health":
            score.score += self.info["score"]
        pygame.sprite.Sprite.kill(self)
        self.info['dead'] = True

        return self.timers['exist']



    def on_collide(self,
                   collide_type:int, #the collide_type refers to the sprite group numbers. 0 for universal (not used), 1 for other player elements, 2 for enemies
                   collided:pygame.sprite.Sprite,
                   ):
        #5/26/23 - Updating health shizznit if interaction with "player type" class
        # if collide_type == 1 or collide_type == 3:
        #     self.info['health'] -= 1
        #if colliding with an enemy, either hurt or bounce based on positioning
        if type(collided) == Player :
            if ((self.rect.centery) > collided.rect.bottom-collided.movement[0]): 
                #bouncing the player up
                collided.bounce()
                #making the player invincible for six frames to prevent accidental damage
                collided.invincibility_counter = 6
            else:
                collided.hurt()
            #damaging the enemy either way
            self.hurt()
        elif collide_type == 3:
            #I SAID damaging the enemy either way
            self.hurt()
            collided.hurt()

    def hurt(self):
        self.info['health'] -= 1
        self.change_anim("hurt")

    def formationUpdate(self,
        new_pos:tuple #location of the formation, not including offset
        ):
        #following formation
        self.idle['full'] = [
            (new_pos[0] + self.idle["offset"][0]),
            (new_pos[1] + self.idle["offset"][1])]
        
    def shoot(self,type:str="point",spd:int=2,info:tuple=((0,0),(100,100)), shoot_if_below:bool=False) -> bullets.HurtBullet:
        bullet=None
        if (shoot_if_below) or (type != 'point') or (info[0][1] < info[1][1]-50):
            bullet = bullets.HurtBullet(type=type,spd=spd,info=info)
            self.sprites[0].add(bullet)
            self.sprites[2].add(bullet)
        return bullet



class A(Template): #geurilla warfare
    def __init__(self,**kwargs):
        Template.__init__(self,kwargs=kwargs)   
        
        #values created for when the opponent attacks you
        self.atk={
            "x":0, #x-momentum
            "y":5, #y-momentum
            "terminal":5+(self.info['difficulty'] if self.info['difficulty']<50 else 10), #terminal x-velocity
            'turn_amt':2+(self.info['difficulty'] if self.info['difficulty']<50 else 15), #how often the enemy will turn
            'turn_vals':[], #turns x can be on
            'turn_cur':0, #which x-turn A is on.
            "acc":0.5, #acceleration
            "direct":False, #direction going in - True = Right, False = Left
            "shoot_chance":(10 - self.info['difficulty'] if self.info['difficulty']<9 else 2)
        }
        self.atk['acc'] = self.atk['terminal']/10 #fixed
        self.info['atk'] = True
        #generating first turn to see what direction is started on 
        self.atk['turn_vals'].append(random.randint(100,pygame.display.play_dimensions[0]-100))
        self.atk['direct'] = turn = self.idle['full'][0]<self.atk['turn_vals'][0]
        #adding all values to turn on
        for i in range(self.atk['turn_amt']): #i is previous index, i+i is current index.
            #as these are picking the *next* values, the direction is the direct opposite of what it should be
            if turn: 
                self.atk['turn_vals'].append(random.randint(100,self.atk['turn_vals'][i]))
            else:
                self.atk['turn_vals'].append(random.randint(self.atk['turn_vals'][i],pygame.display.play_dimensions[0]-100))
            turn = (not turn)
        del turn


    def state_attack(self,start=False):
        #resetting values to start
        if start:
            self.atk['x'] = 0
            self.atk['turn_cur'] = 0
            self.atk['direct'] = self.idle['full'][0]<self.atk['turn_vals'][0]
            #setting animation
            self.change_anim('attack')
            return
        #changing x and y by x and y velocities
        self.rect.y += self.atk['y']
        self.rect.x += self.atk['x']
        #updating x velocity by acceleration if not reached terminal velocity
        if self.atk['direct']:
            self.atk['x'] += self.atk['acc']
            if abs(self.atk['x']) > self.atk['terminal']:
                self.atk['x'] = self.atk['terminal']
        else:
            self.atk['x'] -= self.atk['acc']
            if abs(self.atk['x']) > self.atk['terminal']:
                self.atk['x'] = self.atk['terminal']*-1
        #checking to turn around to next value
        if abs(self.rect.center[0]-self.atk['turn_vals'][self.atk['turn_cur']]) < self.atk['terminal'] * 2:
            # print("FINISHED:",self.atk['turn_cur'],'OF',len(self.atk['turn_vals']),self.atk['turn_vals'][self.atk['turn_cur']])

            #updating values
            self.atk['turn_cur'] += 1
            self.atk['direct'] = not self.atk['direct']
            #looping back if reached end of turn list
            if self.atk['turn_cur'] >= len(self.atk['turn_vals']):
                self.atk['turn_cur'] = 0
                self.atk['direct'] = self.idle['full'][0]<self.atk['turn_vals'][0] 
            # shooting if needed
            if random.randint(0,self.atk['shoot_chance'])==self.atk['shoot_chance']:
                self.shoot(type="point",spd=5,info=(self.rect.center,self.player.rect.center))
            
        #resetting when hitting bottom
        if self.rect.top>pygame.display.play_dimensions[1]:
            self.change_state('return')
            return
            
    def state_return(self,start=False):
        if start:
            self.rect.center=(pygame.display.play_dimensions[0]/2,self.rect.height*-1)
            self.follow = tools.MovingPoint(self.rect.center,self.idle['full'],speed=5,check_finished=True)
            return
        
        self.follow.update()
        self.rect.center = self.follow.position

        #calling to update follow's values every 5 or so frames in order to prevent constant unneeded running
        if self.timers['exist'] % 10 == 0:
            self.follow.change_all(self.idle['full'])
        #finishing
        if self.follow.finished:
            self.change_state('idle')

        #ERROR CHECKING - fixing return state
        if self.timers['in_state'] > 120:
            self.change_state('return')
        



            

class B(Template): #loop-de-loop
    def __init__(self,**kwargs):
        Template.__init__(self,kwargs=kwargs)   
        self.info['atk'] = True

        self.atk = {
            "speed":10+((self.info['difficulty']) if (self.info['difficulty']<5) else (5+self.info['difficulty']//10) if (self.info['difficulty']<50) else 20 ) , #where the opponent goes 
            "points":[(random.randint(25,pygame.display.play_dimensions[0]-25),random.randint(25,pygame.display.play_dimensions[1]-50)) for i in range(5+(self.info['difficulty'] if self.info['difficulty']<5 else 5))], #where the opponent moves to
            "index":0, #which point the opponent is going to first
            "shoot_chance":(10 - self.info['difficulty'] if self.info['difficulty']<6 else 3), #chance of a shot coming out during attack

        }

    def state_attack(self,start=False):
        if start:
            self.atk['index'] = 0 
            self.follow = tools.MovingPoint(self.rect.center,self.atk['points'][self.atk['index']],speed=self.atk['speed'],check_finished=True,ignore_speed=True)
            self.change_anim('attack')
            return
        #updating position
        self.follow.update()
        self.rect.center=self.follow.position
        #updating follow speed
        self.follow.speed = round(self.follow.speed*0.96,2) if self.follow.speed > 2 else 2
        #updating movement patterns
        if self.follow.finished:
            self.atk['index'] += 1
            #finishing movement
            if self.atk['index'] >= len(self.atk['points']):
                self.follow=None
                self.atk['index'] = 0
                self.change_state('return')
            #updating if not finished
            else: 
                self.follow = tools.MovingPoint(self.rect.center,self.atk['points'][self.atk['index']],speed=self.atk['speed'],check_finished=True,ignore_speed=True)
            # shooting if needed
            if random.randint(0,self.atk['shoot_chance'])==self.atk['shoot_chance']:
                self.shoot(type="point",spd=5,info=(self.rect.center,self.player.rect.center))

    def state_return(self,start=False):
        if start:
            self.follow = tools.MovingPoint(self.rect.center,self.idle['full'],speed=10,check_finished=True)
            return
        #updating movement
        self.follow.update()
        self.rect.center = self.follow.position
        #changing movement every once in a while
        if self.timers['exist']%5==0:
            self.follow.change_all(self.idle['full'])
        #finishing
        if self.follow.finished:
            self.change_state('idle')
        #error checking
        if self.timers['in_state'] >= 120:
            self.change_state('return')     






class C(Template): #turret
    def __init__(self,**kwargs):
        Template.__init__(self,kwargs=kwargs)   
        self.timer = (480 - (10*self.info['difficulty'])) if (self.info['difficulty']<40) else 80
        self.time = random.randint(0,self.timer//10)
    def state_idle(self,start=False):
        Template.state_idle(self)
        self.time += 1
        if self.time >= self.timer:
            self.change_state('attack')
            self.time = 0
    def state_attack(self,start=False):
        if start:
            self.change_anim("attack") 
            self.shoot(type="point",spd=5,info=(self.rect.center,self.player.rect.center))
        else:    
            self.change_state('idle')





class D(Template): #special -- uses special value to inherit from that character instead 
    def __init__(self,**kwargs):
        #placeholder value
        Template.__init__(self,kwargs=kwargs)









class Compootr(Template): #special world 3 item
    #Limits for how many can be attacking at once
    atk_count = 0
    atk_max = 3
    def __init__(self,**kwargs):
        Template.__init__(self,kwargs=kwargs)
        self.info['atk'] = True
        self.atk = {
           "shots":10+(self.info["difficulty"]*2 if self.info['difficulty'] < 10 else 20),
           "cur_shot":0,
           "return":False,
        }
        
    def update(self):
        Template.update(self)


    def state_attack(self,start:bool=False):
        if start:
            Compootr.atk_count += 1
            if Compootr.atk_count > Compootr.atk_max:
                self.atk['return'] = True
            else:
                self.atk['return'] = False
        elif self.atk['return']:
            Compootr.atk_count = Compootr.atk_count - 1 if Compootr.atk_count > 0 else 0 
            self.change_state('idle')
        else:
            if self.timers["in_state"] < 15:
                #start
                self.rect.y += 10
            elif self.timers["in_state"] > 15 and self.atk['cur_shot'] <= self.atk['shots']:
                #shooting
                self.shoot(type="angle",spd=5,info=(self.rect.center,30*self.atk['cur_shot']))
                self.atk['cur_shot'] += 1
            else:
                #exit code
                self.rect.y -= 15
                if abs(self.rect.centery - self.idle['full'][1]) < 15:
                    self.atk['cur_shot'] = 0
                    #returning to idle
                    self.atk['return'] = True
                    return
    #special kill code due to the attack limit
    def kill(self,reason=None) -> int:
        Template.kill(self,reason=reason)
        if self.info['state'] == 'attack':
            Compootr.atk_count = Compootr.atk_count - 1 if Compootr.atk_count > 0 else 0 


            
        
        


class Jelle(Template): #special jellyfish
    #Limits for attacking
    atk_count = 0
    atk_max = 2
    def __init__(self,**kwargs):
        #placeholder value
        Template.__init__(self,kwargs=kwargs)
        self.atk_move = None
        self.info['atk']=True
        self.atk = {'return':False,'y':0,'trip':False}
    def update(self):
        Template.update(self)
        #keeping the sprite mask locked so it doesn't bounce and accidentally kill the player
        self.mask = self.spritesheet.all_loaded_spritesheets[self.spritesheet.name][2][0]

    def state_idle(self,start=False):
        self.rect.center = self.idle['full']

    def state_attack(self,start=False):
        #moving down until instructed to go back up, then returning
        if start:
            self.atk['y'] = 1
            self.atk['trip'] = False
        #going down
        elif not self.atk['trip']:
            self.rect.y += self.atk['y'] 
            self.atk['y'] = self.atk['y'] + 0.25 if self.atk['y'] < 7 else 7
            if self.rect.centery > self.player.rect.centery:
                self.atk['trip'] = True
        #returning
        elif self.atk['trip']:
            self.rect.y += self.atk['y']
            self.atk['y'] -= 0.4
            if self.rect.centery < self.idle['full'][1]:
                self.change_state('idle')

        

    def on_collide(self,
                   collide_type:int, #the collide_type refers to the sprite group numbers. 0 for universal (not used), 1 for other player elements, 2 for enemies
                   collided:pygame.sprite.Sprite,
                   ):
        #if colliding with an enemy, either hurt or bounce based on positioning
        if type(collided) == Player :
            if ((self.rect.centery) > collided.rect.bottom-collided.movement[0]): 
                #bouncing the player up
                collided.bounce()
                #this enemy only takes damage when jumped on!
                self.hurt()
                #making the player invincible for six frames to prevent accidental damage
                collided.invincibility_counter += 6
            elif collided.invincibility_counter < 1 : #(the player cannot be invincible)
                collided.hurt()
                #cutesy animation
                self.change_anim("attack")
        elif collide_type == 3:
            collided.hurt()
            self.change_anim("attack")





class Sammich(Template):
    def __init__(self,**kwargs):
        Template.__init__(self,kwargs=kwargs)
        self.info['atk'] = True
        self.atk = {
            'side':0,
            0:pygame.display.play_dimensions[0]*0.01, #left position
            1:pygame.display.play_dimensions[0]*0.99, #right position
            'momentum':0
        }
    def state_attack(self,start=False):
        #homes in on you from the sides, and then lunges at you
        if start:
            self.atk['side'] = random.randint(0,1) #selecting whether COMING FROM the right or left
        #homing in
        elif self.timers['in_state'] < 90:
            self.rect.centery = self.player.rect.centery - 10
            self.rect.centerx = self.atk[self.atk['side']]
        #stopping movement to show you where it's about to aim
        elif self.timers['in_state'] < 120:
            self.rect.center = self.rect.center
        #lunging at player
        elif self.timers['in_state'] < 150:
            self.rect.x = self.rect.x - self.atk['momentum'] if self.atk['side'] == 1 else self.rect.x + self.atk['momentum'] if self.atk['side'] == 0 else self.rect.x
            self.atk['momentum'] += 2
        else:
            self.change_state('idle')
            self.atk['momentum'] = 0 


        
    def state_return(self,start=False):
        ...


   

class Nope(Template):
    arrow:pygame.Surface = pygame.transform.scale(anim.all_loaded_images['arrow.png'],(75,75))
    arrow_rect:pygame.Rect = arrow.get_rect()
    def __init__(self,**kwargs):
        Template.__init__(self,kwargs=kwargs)
        self.atk = {}
        self.info['atk'] = True
    def state_attack(self,start=False):
        if start:
            self.atk = {
            'vert':0,
            'horiz':0,
            'REVERSEvert':False,
            'REVERSEhoriz':False,
            'speed':0,
            'angle':0,
            'arrow_rect':Nope.arrow.get_rect(),
            'pos':list(self.rect.center)
        }
        elif self.timers['in_state'] < 120:
            self.atk['angle'] = atan2(self.player.rect.centery-self.rect.centery,self.player.rect.centerx-self.rect.centerx)
            self.atk['arrow_rect'].center = self.rect.center
            self.image = pygame.transform.rotate(self.image,degrees(self.atk['angle']))
        elif self.timers['in_state'] < 180:
            #finally deciding where to go, but locking on for a second
            self.atk['speed'] = 25
            self.atk['angle'] = self.atk['angle']
            self.atk['horiz'] = cos(self.atk['angle'])
            self.atk['vert'] = sin(self.atk['angle'])
            self.image = pygame.transform.rotate(self.image,degrees(self.atk['angle']))
        elif self.atk['speed'] > 0:
            #moving, with extra code on for bouncing n shit
            self.atk['pos'][0] += self.atk['horiz'] * self.atk['speed'] * (-1 if self.atk['REVERSEhoriz'] else 1)
            self.atk['pos'][1] += self.atk['vert'] * self.atk['speed'] * (-1 if self.atk['REVERSEvert'] else 1)
            self.rect.center = self.atk['pos']
            self.atk['speed'] -= 0.1
            #bounce collision
            #if too far left
            if self.rect.left < 0:
                if self.atk['horiz'] < 0: #if its going left and goes left by default
                    self.atk['REVERSEhoriz'] = True
                elif self.atk['horiz'] > 0: #if its going left and goes right by default
                    self.atk['REVERSEhoriz'] = False
            #if too far right
            elif self.rect.right > 600:
                if self.atk['horiz'] < 0: #if its going right and goes left by default
                    self.atk['REVERSEhoriz'] = False
                elif self.atk['horiz'] > 0: #if its going right and goes right by default
                    self.atk['REVERSEhoriz'] = True
            #if too far up
            if self.rect.top < 0:
                if self.atk['vert'] < 0: #if its going up and goes up by default
                    self.atk['REVERSEvert'] = True
                elif self.atk['vert'] > 0: #if its going up and goes down by default
                    self.atk['REVERSEvert'] = False
            #if too far down
            elif self.rect.bottom > 800:
                if self.atk['vert'] < 0: #if its going down and goes up by default
                    self.atk['REVERSEvert'] = False
                elif self.atk['vert'] > 0: #if its going down and goes down by default
                    self.atk['REVERSEvert'] = True

        
        else:
            self.change_state('return')
        


class Yippee(Template):
    #a stupid little enemy that shits confetti at you
    def __init__(self,**kwargs):
        Template.__init__(self,kwargs=kwargs)
        self.info['atk'] = True
        self.atk = {
            "points":[0,1,2],
            "initial_follow":None,
            "initial_x":0,
        }
    def state_attack(self,start=False):
        #selecting initial information
        if start:
            self.atk['points'] = [random.randint(100,400) for i in range((self.info['difficulty'] // 2) if self.info['difficulty']<20 else 10)]
            self.atk['initial_follow'] = tools.MovingPoint(self.rect.center,(self.rect.centerx,50),check_finished=True,speed=10)
            self.atk['initial_x'] = random.randint(0,75)
            self.atk['y'] = self.idle['full'][1] + 100
        #going up to the top position
        elif self.timers['in_state'] < 30 and not self.atk['initial_follow'].finished:
            self.atk['initial_follow'].update()
            self.rect.center = self.atk['initial_follow'].position
        #floating around and confetti-ing
        elif len(self.atk['points']) > 0:
            self.rect.center = (  300 + sin(self.timers['in_state']/25 + self.atk['initial_x'])*250  , self.atk['y']  + sin(self.timers['in_state']/10)*10  )
            if abs(self.rect.centerx - self.atk['points'][0]) < 10:
                #confetti time
                for i in range(5):
                    confetti = Confetti(pos=self.rect.center)
                    self.sprites[0].add(confetti)
                    self.sprites[2].add(confetti)
                self.atk['points'].pop(0)
                #animation
                self.change_anim('attack')
        else:
            self.change_state('return')



class Lumen(Template):
    #points at you, and shoots a laser 
    def __init__(self,**kwargs):
        Template.__init__(self,kwargs=kwargs)
        self.info['atk'] = True
        self.atk = {
            'angle':0,
            'laser':None,
            'end_pos':(0,0),
        }
    def state_attack(self,start=False):
        if start:
            ...
        elif self.timers['in_state'] < 120:
            #locking on, moving based on where you are
            self.atk['angle'] = atan2(self.player.rect.centery-self.rect.centery,self.player.rect.centerx-self.rect.centerx)
            self.image = pygame.transform.rotate(self.image,degrees(self.atk['angle']))
            self.atk['end_pos'] = self.player.rect.center
        elif self.timers['in_state'] < 240:
            #waiting for a second to make it fair
            self.image = pygame.transform.rotate(self.image,degrees(self.atk['angle'])) 
        elif self.timers['in_state'] == 240:
            laser = Laser(start_pos = self.rect.center,angle=degrees(self.atk['angle'])) #shooting the laser
            self.sprites[0].add(laser)
            self.sprites[2].add(laser)
        else:
            self.change_state('idle')
        #no matter what, maintaining positioning
        self.rect.center = self.idle['full']

    


##SAVING ASSETS IN A DICTIONARY TO BE USED LATER
loaded = {
    "A":A,
    "B":B,
    "C":C,
    "D":D,
    'jelle':Jelle,
    'compootr':Compootr,
    'sammich':Sammich,
    'nope':Nope,
    'yippee':Yippee,
    'lumen':Lumen,
    }


#EXTRA ASSETS -- SPECIAL YIPPEE CONFETTI
class Confetti(pygame.sprite.Sprite):
    #all potential images to be used
    images = []
    for color in ["red","green","blue","purple","orange","pink"]:
        surf = pygame.Surface((10,10))
        pygame.draw.rect(surf,color=color,rect=pygame.Rect(0,0,10,10))
        images.append(surf)
    def __init__(self,pos=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(Confetti.images)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.mask = pygame.mask.from_surface(self.image)
        self.gravity_info = [
            random.randint(-20,20), #x movement
            random.randint(-20,-5), #y gravity
        ]
        self.duration = 0 

    def update(self):
        #moving x
        self.rect.x += self.gravity_info[0]
        #moving y
        self.rect.y += self.gravity_info[1]

        #changing x gravity
        self.gravity_info[0] = round(self.gravity_info[0]*0.98,5) if abs(self.gravity_info[0]) > 0.001 else 0
        #changing y gravity
        self.gravity_info[1] = self.gravity_info[1]+0.5 if self.gravity_info[1] < 7 else 7


        #updating duration information
        self.duration += 1
        #autokill
        if self.duration > 240 or self.rect.top>800:
            self.kill()
        
        
    def on_collide(self,
                   collide_type:int, #the collide_type refers to the sprite group numbers. 0 for universal (not used), 1 for other player elements, 2 for enemies
                   collided:pygame.sprite.Sprite,
                   ):
        #5/26/23 - Updating health shizznit if interaction with "player type" class
        # if collide_type == 1 or collide_type == 3:
        #     self.info['health'] -= 1
        #if colliding with an enemy, either hurt or bounce based on positioning
        if type(collided) == Player :
            collided.hurt()
            #damaging the enemy either way
            self.kill()
        elif collide_type == 3:
            #I SAID damaging the enemy either way
            self.kill()
            collided.hurt()


#EXTRA ASSETS -- SPECIAL LUMEN LASER
class Laser(pygame.sprite.Sprite):
    def __init__(self,start_pos=(0,0),angle=45,length=800):
        pygame.sprite.Sprite.__init__(self)
        #laser image code
        self.image = pygame.Surface(pygame.display.play_dimensions,pygame.SRCALPHA).convert_alpha() #a rect that spans the ENTIRE SCREEN, as only the mask is used for collision
        
        #CODE FROM kadir014 on github.io, will change around myself later
        start = pygame.Vector2(start_pos[0],start_pos[1])
        end = start + pygame.Vector2(length,0).rotate(angle)
        pygame.draw.line(self.image,'red',start,end,15)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        #duration
        self.duration = 0 
    def update(self):
        #it just sits there for a quarter of a second,lol
        self.duration += 1
        if self.duration > 15:
            self.kill()
    def on_collide(self,
                   collide_type:int, #the collide_type refers to the sprite group numbers. 0 for universal (not used), 1 for other player elements, 2 for enemies
                   collided:pygame.sprite.Sprite,
                   ):
        #5/26/23 - Updating health shizznit if interaction with "player type" class
        # if collide_type == 1 or collide_type == 3:
        #     self.info['health'] -= 1
        #if colliding with an enemy, either hurt or bounce based on positioning
        if type(collided) == Player :
            collided.hurt()
        elif collide_type == 3:
            collided.hurt()





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

