#Code by Andrew Church
import pygame,text,math,random

#07/30/2023 - ADDING EMBLEM SPRITES
# These are going to be little sprites that are able to just show a normal ass surface with the ability to move from place to place
# This is mostly going to be used for the border, along with the level icons and scores and stuff.
class Emblem(pygame.sprite.Sprite):
    def __init__(self,im:pygame.Surface,coord:tuple,isCenter:bool=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = im
        self.rect = self.image.get_rect()
        self.orig_coord = coord
        self.coord = coord
        self.destination = None

        self.pattern = None #None = Not playing, then anything else is an animation playing
        self.pattern_f = 0 #frames in a pattern
        self.pattern_offset = [0,0] #what pattern affects

        if isCenter:
            self.change_pos(coord,isCenter=True)

    def update(self):
        if self.pattern is not None: self.pattern_f += 1; self.play_pattern()
        self.rect.topleft = self.coord[0]+self.pattern_offset[0],self.coord[1]+self.pattern_offset[1]
    
    def play_pattern(self):
        if self.pattern == "sine":
            self.pattern_offset[1] = math.sin(self.pattern_f/10)*10
        if self.pattern == "jagged":
            self.pattern_offset[0] = random.randint(-2,2)
            self.pattern_offset[1] = random.randint(-2,2)
    
    #instantly changing the position
    def change_pos(self,pos:tuple,isCenter:bool=False):
        if isCenter:
            self.rect.center = pos
            self.coord = self.rect.topleft
        else:
            self.coord = pos


    def reset_coord(self):
        self.coord = self.orig_coord
        