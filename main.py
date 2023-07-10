#PROGRAM BY ANDREW CHURCH
import pygame,os,text,random,json

FPS=60
clock = pygame.time.Clock()
run=True; cur_state = None

#07/04/2023 - importing settings to use the universal file
import options
settings = options.settings

#setting window values
defaultcolor = "#AAAAAA"
pygame.display.play_dimensions = 600,800 #oh cool, I can make a self variable in the pygame.display. hot.
pygame.display.dimensions = settings["screen_width"][1],settings["screen_height"][1] #see previous line, connect dots
window = pygame.display.set_mode(pygame.display.dimensions)
pygame.display.play_pos = 20,20
pygame.display.play_dimensions_resize = settings["gameplay_width"][1],settings["gameplay_height"][1]
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
import state_play,ui_border

#06/22/2023 - SETTING BORDER IMAGE / SPRITESHEET
border = ui_border.Border()




#07/02/2023 - ADDING SPECIFIC STATES
# Since states are classes, each time you make a new one a new object will be created
# However, there is no need to have several state classes open at once
# Because of this, it's just gonna start up every state as an object instead of a class
states = {}
states["play"] = state_play.State(data=data,sprites=sprites,window=window,campaign="main_story.order")



#setting the state
cur_state = states["play"]
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
