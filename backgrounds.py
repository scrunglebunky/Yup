#CODE BY ANDREW CHURCH
import pygame,anim

#06/23/2023 - WHAT IS A BACKGROUND
# The background is a class that stores an image and a position
# This may be a little overkill for an entire class, but it works for organization purposes in my opinion
class Background():
    def __init__(self,img:str,resize:tuple,speed:tuple,**kwargs):
        # It stores an image, a position tuple, and a speed tuple
        self.image = anim.all_loaded_images[img]
        self.image = pygame.transform.scale(self.image,resize)
        self.size = resize
        self.pos = [0,0]
        self.speed = speed
        
    def update(self):
        #updates positioning and such
        self.pos[0] += self.speed[0] #x pos
        self.pos[1] += self.speed[1] #y pos
        #resetting positioning
        if self.pos[0] > pygame.display.play_dimensions[0] or self.pos[0]*-1 > pygame.display.play_dimensions[0]:
            self.pos[0] = 0 #x position
            # print('reset x')
        if self.pos[1] > pygame.display.play_dimensions[1] or self.pos[1]*-1 > pygame.display.play_dimensions[1]:
            self.pos[1] = 0 
            # print('reset y')
        

    def draw(self,window:pygame.display):
        #drawing the image to the window
        window.blit(self.image,self.pos)
        #activating duplicates
        if self.pos != [0,0]:
            self.duplicates(window)


    def duplicates(self,window:pygame.display):
        #drawing repeats of the background if any of it is offscreen
        if self.pos[0] > 0:#LEFT
            window.blit(
                self.image,(
                    self.pos[0]-self.size[0],
                    self.pos[1])
                    )
        elif self.pos[0] < 0:#RIGHT
            window.blit( 
                self.image,(
                    self.pos[0]+self.size[0],
                    self.pos[1])
                    )
        if self.pos[1] > 0:#UP
            window.blit( 
                self.image,(
                    self.pos[0],
                    self.pos[1]-self.size[1])
                    )
        elif self.pos[1] < 0:#DOWN
            window.blit( 
                self.image,(
                    self.pos[0],
                    self.pos[1]+self.size[1])
                    )
        if self.pos[0] > 0 and self.pos[1] > 0:#UPLEFT
            window.blit(
                self.image,(
                    self.pos[0]-self.size[0],
                    self.pos[1]-self.size[1])
                    )
        if self.pos[0] > 0 and self.pos[1] < 0:#DOWNLEFT
            window.blit(
                self.image,(
                    self.pos[0]-self.size[0],
                    self.pos[1]+self.size[1])
                    )
        if self.pos[0] < 0 and self.pos[1] > 0:#UPRIGHT
            window.blit( 
                self.image,(
                    self.pos[0]+self.size[0],
                    self.pos[1]-self.size[0])
                    )
        if self.pos[0] < 0 and self.pos[1] < 0:#DOWNRIGHT
            window.blit( 
                self.image,(
                    self.pos[0]+self.size[0],
                    self.pos[1]+self.size[1])
                    )