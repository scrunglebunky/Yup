#PROGRAM BY ANDREW CHURCH
import pygame,os,text,random,json

FPS=60
clock = pygame.time.Clock()
run=True; cur_state = None

#07/04/2023 - importing settings to use the universal file\
from options import settings

#setting window values - THE OPTIONS IMPORT DOES HALF OF THE JOB ALREADY - THIS IS THE REST
defaultcolor = "#AAAAAA"
window = pygame.display.get_surface() 
pygame.display.play_pos = 20,20
pygame.display.play_dimensions = 600,800 #oh cool, I can make a self variable in the pygame.display. hot.
pygame.display.set_caption("YUP RevD")


#GAME STUFF
sprites = {
    0:pygame.sprite.Group(), #ALL SPRITES
    1:pygame.sprite.Group(), #PLAYER SPRITE, INCLUDING BULLETS ; this is because the player interacts with characters the same way as bullets
    2:pygame.sprite.Group(), #ENEMY SPRITES
}

#07/04/2023 - UNIVERSAL ARGS PROBLEM
# I wanted these gone a while ago but its the only way to make integers into pointers
data = {
    "score":0,
    "clock_offset":1,
}

#06/01/2023 - IMPORTING GAME-RELATED STUFF NEEDED AFTER ALL IS SET UP
import state_play,ui_border,options,state_pause

#06/22/2023 - SETTING BORDER IMAGE / SPRITESHEET
border = ui_border.Border()




#07/02/2023 - ADDING SPECIFIC STATES
# Since states are classes, each time you make a new one a new object will be created
# However, there is no need to have several state classes open at once
# Because of this, it's just gonna start up every state as an object instead of a class
states = {}
state = "pause"
states["play"] = state_play.State(data=data,sprites=sprites,window=window,campaign="main_story.order")
states["options"] = options.State(window=window)
states["pause"] = state_pause.State(window=window,play_state=states["play"])

#07/23/2023 - SWITCHING STATES
# States have an issue now where, since they are all initialized at startup, some things that should only be run when the state *actually* starts still appears.
# States now have a method called "on_start" that will remedy this, which will be called in a function here
# All states need to have a value called "next state", too, which will make it able to tell if the state is finished or not
def state_switch(
    cur_state #the current state used
    ):
    next_state = cur_state.next_state
    if type(next_state) == str and next_state.lower() in states.keys():
        cur_state.on_end(); cur_state.next_state = None #resetting next state
        cur_state = states[next_state.lower()] #switching state
        cur_state.on_start() #telling state it's been started
    elif type(next_state) == tuple and (type(next_state[0]) == str and next_state[0].lower() in states.keys()):
        cur_state.on_end(); cur_state.next_state = None
        cur_state = states[next_state[0].lower()]
        cur_state.on_start(return_state = next_state[1])
    return cur_state
    


#setting the state
cur_state = states[state]
while run:

    #filling the screen in case something is offscreen
    window.fill(defaultcolor)

    #06/23/2023 - drawing border to window 
    border.draw(window)
    #06/x/2023 - adding numbers to be drawn to the border
    if state == "play":
        border.draw_specific(
            window = window, 
            lives = cur_state.player.health, 
            nums = [
                data["score"],
                round(clock.get_fps(),2),
                round(data["clock_offset"],2),
                round(clock.get_fps()*data["clock_offset"],2),
                ]
            ) 

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()
            #DEBUG - max FPS
            if event.key == pygame.K_1:
                FPS = 0 if FPS == 60 else 60
                

            
                

        cur_state.event_handler(event=event)

    #updating states
    cur_state.update()
    # checking if the state has to be changed
    cur_state = state_switch(cur_state)

    #general update
    pygame.display.update()
    clock.tick(FPS)

    data["clock_offset"] = 60/(clock.get_fps() if clock.get_fps() != 0 else 60)

 

pygame.quit()
exit()
