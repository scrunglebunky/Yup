import pygame,text,anim,score

class State():
    def __init__(self,window:pygame.Surface):
        self.window=window
        self.next_state = None

        self.id = 0
        self.elements = ["title","highscores","title","lore","title","gameplay"]
        self.pos = [-100,-100,-100,-100,-100,-100]
        self.stretch = []
    def on_start(self):...
    def on_end(self):...
    def update(self):
        #07/27/2023 - PLANS FOR THE TITLE SCREEN
        # The logo is now flying up and down in a sinewave motion
        # The UI elements are missing; gone, and most of what is happening is just random icon shennanigans
        # A few things will flash by, like the high score menu, some gameplay snippets, and the lore
        # This stuff will all cycle by from left to right, in the same sinewave motion
        # CHANGE THE WAY TEXT.PY WORKS FIRST. DO IT NOW. RIGHT NOW. WHEN YOU WAKE UP.
        self.window.blit(score.scoreboard,(0,0))
    def event_handler(self,event):...