#PROGRAM BY ANDREW CHURCH
import pygame,os,text,random,json 
from options import settings 
import tools

clock = tools.Clock(pygame.time.Clock())
run=True; cur_state = None

defaultcolor = "#AAAAAA"
window = pygame.display.get_surface() 
pygame.display.rect = pygame.display.get_surface().get_rect()
pygame.display.play_pos = 20,20
pygame.display.play_dimensions = 600,800 #oh cool, I can make a self variable in the pygame.display. hot.
pygame.display.set_caption("YUP RevD")


#GAME STUFF
universal_sprite_group = pygame.sprite.Group() #This used to be a dictionary used everywhere but all groups have now been moved to their own respective states

#06/01/2023 - IMPORTING GAME-RELATED STUFF NEEDED AFTER ALL IS SET UP
import options,score,ui_border
import states as all_states

#06/22/2023 - SETTING BORDER IMAGE / SPRITESHEET
border = ui_border.Border()

tools.debug = True

# 7/02/2023 - ADDING SPECIFIC STATESx
# Since states are classes, each time you make a new one a new object will be created
# However, there is no need to have several state classes open at once
# Because of this, it's just gonna s up every state as an object instead of a class
states = {}
state = "boss"
states["play"] = all_states.Play(window=window,campaign="main_story.order")
states["options"] = options.State(window=window,border=border)
states["pause"] = all_states.Pause(window=window,play_state=states["play"])
states["title"] = all_states.Title(window=window,border=border)
states["gameover"] = all_states.GameOver(window=window,play_state=states["play"])
states["advance"] = all_states.Advance(window=window,play_state=states["play"])
states["boss"] = all_states.Boss(play_state=states["play"])

#07/23/2023 - SWITCHING STATExzS
# States have an issue now where, since they are all initialized at startup, some things that should only be run when the state *actually* starts still appears.
# States now have a method called "on_start" that will remedy this, which will be called in a function here
# All states need to have a value called "next state", too, which will make it able to tell if the state is finished or not
def state_switch(
    cur_state,state #the current state used
    ):
    if cur_state.next_state is not None:
        state = cur_state.next_state
    else: return cur_state,state
    if type(state) == str and state.lower() in states.keys():
        cur_state.on_end(); cur_state.next_state = None #resetting next state
        cur_state = states[state.lower()] #switching state
        cur_state.on_start() #telling state it's been started
    elif type(state) == tuple and (type(state[0]) == str and state[0].lower() in states.keys()):
        cur_state.on_end(); cur_state.next_state = None
        cur_state = states[state[0].lower()]
        cur_state.on_start(return_state = state[1])
    else:
        global run
        run = False
    return cur_state,state
    

#setting the state
cur_state = states[state] ; cur_state.on_start()

freeze = False

# tools.demo = True #DELETE AFTERWARDS

while run:

    #filling the screen in case something is offscreen
    window.fill(defaultcolor)

    #06/23/2023 - drawing border to window 
    border.draw(window)
    #06/x/2023 - adding numbers to be drawn to the border
    border.draw_specific(
        window = window, 
        lives = states["play"].player.health,
        nums = [
            score.score,
            round(clock.clock.get_fps(),2),
            round(clock.offset,2),
            round(clock.clock.get_fps()*clock.offset,2),
            ]
        ) 

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if tools.demo:
                pass
                # print("haha")
            else:
                run = False
                # print("false")
        if event.type == pygame.KEYDOWN:
            #DEBUG - max FPS
            if event.key == pygame.K_1:
                if tools.debug: clock.FPS = 0 if clock.FPS == 60 else 60
            if event.key == pygame.K_u:
                if tools.debug: freeze = not freeze
                

        cur_state.event_handler(event=event)

    #debug pause function

    if not freeze:
        #updating states 
        cur_state.update()
        # checking if the state has to be changed
        cur_state,state = state_switch(cur_state,state)
        # print(state)
        border.update()
    elif freeze:
        window.blit(states["play"].window,(0,0))

    #general update
    pygame.display.update()
    clock.tick()


 

pygame.quit()
exit()
