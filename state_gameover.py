# Code by Andrew Church
import pygame
from text import loaded_text as text
from anim import all_loaded_images as img
#08/08/2023 - THE GAME OVER STATE
# The game over state will use the gameplay state and modify it so everything slows down and the assets disappear and a graphic shows
class State():
    def __init__(self,sprites,play_state):
        #08/08/2023 - PSEUDOCODE
        # Remember, playstate has a separate surface that is drawn to the window, again, entirely separately. 
        # GameOverState will, animated-ly, blow up everything onscreen, then make the surface do a falling animation.
        # The separate surface is ignored from there on out. A game over graphic appears, which shows your score and how you did, before giving a rating.
        # Pressing enter brings you back to the main menu.
        self.sprites = sprites
        self.play_state = play_state
        
        ...
    def on_start(self):...
    def on_end(self):...
    def update(self):...
    def event_handler(self,event):...