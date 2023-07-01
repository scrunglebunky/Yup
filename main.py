#PROGRAM BY ANDREW CHURCH
import pygame,os,text,random,json

FPS=60
clock = pygame.time.Clock()


#06/30/2023 - LOADING IN THE CONFIGURATION FILE
# The config.json file is a dictionary containing info about how the game works
# This file is needed, though there is a default dictionary held here 
default_settings = {
    "fullscreen":["switch",False],

    "mute":["switch",False],
    "music_vol":["knob",0.5,0.05],
    "sound_vol":["knob",0.5,0.05],

    "screen_width":["knob",900,5],
    "screen_height":["knob",675,5],
    "gameplay_width":["knob",450,5],
    "gameplay_height":["knob",600,5]
}
# loading in the file
with open("./data/config.json","r") as set_raw:
    settings = json.load(set_raw)
del set_raw


#DEBUG DISPLAY stuff
screen_sizes,screen_size = ((400,300),(800,600),(900,675),(1200,900),(1600,1200),) , 2
rescale_sizes,rescale_size = ((225,300),(450,600),(600,800),(900,1200),) , 1
play_poses,play_pos = ((0,0),(20,20),(50,50),(100,100),) , 1
defaultcolor = "#AAAAAA"

#setting window values
pygame.display.play_dimensions = 600,800 #oh cool, I can make a self variable in the pygame.display. hot.
pygame.display.dimensions = settings["screen_width"][1],settings["screen_height"][1] #see previous line, connect dots
window = pygame.display.set_mode(pygame.display.dimensions)
pygame.display.play_pos = play_poses[play_pos]
pygame.display.play_dimensions_resize = settings["gameplay_width"][1],settings["gameplay_height"][1]
pygame.display.set_caption("YUP RevD")

#UI
run=True; cur_state = None
#IMPORTING STATES
import state_play,ui_border
states = {
    "play":state_play.State,
    }


#GAME STUFF
sprites = {
    0:pygame.sprite.Group(), #ALL SPRITES
    1:pygame.sprite.Group(), #PLAYER SPRITE, INCLUDING BULLETS ; this is because the player interacts with characters the same way as bullets
    2:pygame.sprite.Group(), #ENEMY SPRITES
}

#UNIVERSAL ARGS 
# may be phased out soon
data = {
    "score":0,
    "clock_offset":1,
}


#06/22/2023 - SETTING BORDER IMAGE / SPRITESHEET
border = ui_border.Border()


#setting the state
cur_state = state_play.State(data=data,sprites=sprites,window=window)
while run:
    #filling the screen in case something is offscreen
    window.fill(defaultcolor)

    #06/23/2023 - drawing border to window 
    border.draw(window)
    #06/x/2023 - adding numbers to be drawn to the border
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
            #DEBUG - changing sizes
            if event.key == pygame.K_p:
                #SCREEN SIZE
                screen_size = screen_size + 1 if screen_size+1 < len(screen_sizes) else 0
                pygame.display.dimensions = screen_sizes[screen_size]
                pygame.display.set_mode(pygame.display.dimensions)
                border.__init__()
            #DEBUG - changing gameplay scales
            if event.key == pygame.K_o:
                rescale_size = rescale_size + 1 if rescale_size+1 < len(rescale_sizes) else 0
                pygame.display.play_dimensions_resize = rescale_sizes[rescale_size]
                border.__init__()

            
                

        cur_state.event_handler(event=event)

    #updating states
    cur_state.update()

    #general update
    pygame.display.update()
    clock.tick(FPS)

    data["clock_offset"] = 60/(clock.get_fps() if clock.get_fps() != 0 else 60)

 

pygame.quit()
exit()
