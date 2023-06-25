#PROGRAM BY ANDREW CHURCH
import pygame,os,text,random

FPS=60
clock = pygame.time.Clock()

#display stuff
defaultcolor = (100,50,50)
screen_dimensions = 720,720
play_dimensions = 450,600
play_pos = 50,50

window = pygame.display.set_mode(screen_dimensions)
pygame.display.play_dimensions = play_dimensions #oh cool, I can make a self variable in the pygame.display. hot.
pygame.display.dimensions = screen_dimensions #see previous line, connect dots
pygame.display.play_pos = play_pos
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

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()
            if event.key == pygame.K_1:
                FPS = 0 if FPS == 60 else 60
        cur_state.event_handler(event=event)

    #updating states
    cur_state.update()

    #displaying tezt
    #5/30/2023 - test display of fps
    text.display_numbers(round(clock.get_fps(),2),(pygame.display.dimensions[0],320),window,reverse=True)
    text.display_numbers(round(data["clock_offset"],2),(pygame.display.dimensions[0],350),window,reverse=True)
    text.display_numbers(round(clock.get_fps()*data["clock_offset"],2),(pygame.display.dimensions[0],380),window,reverse=True)

    #general update
    pygame.display.update()
    clock.tick(FPS)

    data["clock_offset"] = 60/(clock.get_fps() if clock.get_fps() != 0 else 60)

pygame.quit()
exit()
