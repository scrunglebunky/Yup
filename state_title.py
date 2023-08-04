import pygame,text,score
from emblems import Emblem as Em
from anim import all_loaded_images as img
class State():
    emblems = {}
    def __init__(self,window:pygame.Surface,sprites:dict,border): #Remember init is run only once, ever.
        self.window=window
        self.sprites=sprites
        self.border=border
        self.next_state = None

        self.id = 999
        self.frames = 999
        self.elements = ["title","highscores","title","lore",] #add "title","gameplay"
        State.emblems = {
            "title":Em(im=img["logo.png"],coord=(-999,-999)),
            "highscores":Em(im=score.scoreboard,coord=(-999,-999)),
            "lore":Em(im=img["placeholder.bmp"],coord=(-999,-999)),}
        State.emblems_perm = {}
        for emblem in State.emblems.values():
            self.sprites[3].add(emblem)
    
    
    def on_start(self):
        for emblem in self.border.emblems: #RESETTING BORDER EMBLEMS
            emblem.change_pos((-999,-999))
    def on_end(self):
        for emblem in self.border.emblems: #RESETTING BORDER EMBLEMS
            emblem.reset_coord()
        for emblem in State.emblems.values(): #RESETTING THESE EMBLEMS
            emblem.reset_coord()


    def update(self):
        #07/27/2023 - PLANS FOR THE TITLE SCREEN
        # The logo is now flying up and down in a sinewave motion
        # The UI elements are missing; gone, and most of what is happening is just random icon shennanigans
        # A few things will flash by, like the high score menu, some gameplay snippets, and the lore
        # This stuff will all cycle by from left to right, in the same sinewave motion
        # CHANGE THE WAY TEXT.PY WORKS FIRST. DO IT NOW. RIGHT NOW. WHEN YOU WAKE UP.
        self.frames += 1
        if self.frames >= 120:
            if self.id <= (len(self.elements)-1):
                State.emblems[self.elements[self.id]].pattern = None
                State.emblems[self.elements[self.id]].frames = 0
                State.emblems[self.elements[self.id]].change_pos((-999,-999))
            self.id = self.id + 1 if self.id < (len(self.elements)-1) else 0 
            State.emblems[self.elements[self.id]].pattern = "sine"
            State.emblems[self.elements[self.id]].change_pos(pygame.display.rect.center,isCenter=True)
            self.frames = 0

        #08/02/2023 - drawing graphical stuff
        self.sprites[3].draw(self.window)
    def event_handler(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.next_state = "play"