# Code by Andrew Church
import pygame,random,score,audio,text
from backgrounds import Background as Bg
from anim import all_loaded_images as img
from emblems import Emblem as Em
#08/08/2023 - THE GAME OVER STATE
# The game over state will use the gameplay state and modify it so everything slows down and the assets disappear and a graphic shows
class State():
    sprites=pygame.sprite.Group()
    def __init__(self,window,play_state):
        #setting values
        self.window = window
        self.play_state = play_state
        self.frames = 0
        self.next_state = None
        
    def on_start(self):
        #startup
        self.frames = 0 
        self.play_state.player.change_anim("yay")
        self.play_state.player.reset_movement()
        self.play_state.in_advance = True #stopping play_state from doing weird shit

    def on_end(self):
        self.frames = 0
        self.play_state.player.change_anim("idle")
        self.play_state.in_advance = False #letting play_state be goofy again

    def update(self):
        self.frames += 1
        #adding some emblems for now, will update to be better later
        if self.frames==1: State.sprites.add(Em(im="levelcomplete.png",coord=(pygame.display.play_dimensions_resize[0]/2+pygame.display.play_pos[0],pygame.display.play_dimensions_resize[1]*0.25+pygame.display.play_pos[1]),isCenter=True,pattern="jagged"))
        #speeding everything up
        if self.frames < 150:
            for i in range(2):
                if self.play_state.background.speed[i] <= 150:
                    self.play_state.background.speed[i] *= 1.05
        #changing the play_state stored world
        if self.frames == 150:
            State.sprites.empty()
            self.play_state.new_world()
            self.kaboom(
                coord=(pygame.display.play_dimensions_resize[0]/2+pygame.display.play_pos[0],pygame.display.play_dimensions_resize[1]/2+pygame.display.play_pos[1]),
                animation_resize=(500,500))
        #ending
        if self.frames > 300:
            self.next_state = "play"

        self.play_state.player.invincibility_counter = 60

        self.play_state.update()

        State.sprites.update()
        State.sprites.draw(self.window)



    def event_handler(self,event):
        pass    
    
    def kaboom(self,coord:tuple,animation_resize:tuple,play:bool=False,): #because kaboom happens so much
            (State.sprites if not play else self.play_state.sprites[0]).add(
            Em(
                im='kaboom',
                coord=coord,
                isCenter=True,
                ))
