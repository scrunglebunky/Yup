import pygame,text,score,random
from emblems import Emblem as Em
from anim import all_loaded_images as img
from text import loaded_text as txt
from state_play import State as Pstate 

class State():
    emblems = {}
    emblems_perm = {}
    sprites=pygame.sprite.Group()

    def __init__(self,window:pygame.Surface,border): #Remember init is run only once, ever.
        self.window=window
        self.border=border
        self.next_state = None
        

        self.demo_state = Pstate(window = self.window, world = random.randint(0,6), level = random.randint(0,50), is_demo = True) #this is different from the tools.demo value, as this is just to simulate a player

        #basic events that will occur during the title
        self.events = [
            "demo",
            "hiscore",
        ]
        self.timers = [
            480,
            240,
        ]
        self.event = 0
        self.id =  0
        self.image_placements = {
            "welcome":(pygame.display.rect.width*0.01,pygame.display.rect.height*0.01),
            "else":(pygame.display.rect.width*0.01 + img["demo.png"].get_width() + pygame.display.rect.width*0.01 ,
                    pygame.display.rect.height*0.01),
        }
    
    
    def on_start(self):
        self.event = self.id = 0
        self.demo_state.__init__(window = self.window, world = random.randint(0,6), level = random.randint(0,50), is_demo = True)

    def on_end(self):...


    def update(self):
        #updating demo state
        self.demo_state.update(draw=False)
        
        #drawing
        self.window.blit(img['demo.png'],self.image_placements['welcome'])
        self.window.blit(pygame.transform.scale(self.demo_state.window,pygame.display.play_dimensions_resize),self.image_placements['else'])
        #creating an

        event = pygame.event.Event(random.choice([pygame.KEYDOWN,pygame.KEYUP]), key = random.choice([pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT,pygame.K_z,pygame.K_x])) #create the event
        
        #stopping constant movement
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
            if event.key == pygame.K_LEFT:
                self.demo_state.player.momentum = self.demo_state.player.speed*-1 if not self.demo_state.player.movement[4] else self.demo_state.player.crouch_speed*-1
            else:
                self.demo_state.player.momentum = self.demo_state.player.speed if not self.demo_state.player.movement[4] else self.demo_state.player.crouch_speed
        else:
            self.demo_state.player.controls(event)


        


    def event_handler(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.next_state = "play"