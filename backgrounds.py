#CODE BY ANDREW CHURCH
import pygame,anim,options

#06/23/2023 - WHAT IS A BACKGROUND
# The background is a class that stores an image and a position
# This may be a little overkill for an entire class, but it works for organization purposes in my opinion
class Background():
    def __init__(self,img:str,resize:list,speed:list,border_size:tuple=pygame.display.play_dimensions,**kwargs):
        # It stores an image, a position tuple, and a speed tuple
        self.image = anim.all_loaded_images[img]
        self.image = pygame.transform.scale(self.image,resize)
        self.size = resize.copy()
        self.pos = [0,0]
        self.speed = speed.copy()
        self.border = border_size

    def update(self):
        #updates positioning and such
        self.pos[0] += self.speed[0] #x pos
        self.pos[1] += self.speed[1] #y pos
        #resetting positioning
        if self.pos[0] > self.border[0] or self.pos[0]*-1 > self.border[0]:
            self.pos[0] = 0 #x position
            # print('reset x')
        if self.pos[1] > self.border[1] or self.pos[1]*-1 > self.border[1]:
            self.pos[1] = 0 
            # print('reset y')
        

    def draw(self,window:pygame.display):
        #drawing the image to the window
        window.blit(self.image,self.pos)
        #activating duplicates
        if self.pos != [0,0]:
            self.duplicates(window,pos=self.pos)

    def change(self,img,resize,speed,border_size:tuple=pygame.display.play_dimensions):
        # It stores an image, a position tuple, and a speed tuple
        self.image = anim.all_loaded_images[img]
        self.image = pygame.transform.scale(self.image,resize)
        self.size = resize.copy()
        self.pos = [0,0]
        self.speed = speed.copy()
        self.border = border_size


    def duplicates(self,window:pygame.display,pos:tuple=None):
        #7/10/2023 - adding a default position
        pos = self.pos if pos is None else pos 
        #drawing repeats of the background if any of it is offscreen
        #07/10/2023 - instead of individually blitting, it makes a list for easy modification
        blit_list = [ ] 
        if pos[0] > 0:#LEFT
            blit_list.append((pos[0]-self.size[0],pos[1]))
        elif pos[0] < 0:#RIGHT
            blit_list.append((pos[0]+self.size[0],pos[1]))
        if pos[1] > 0:#UP
            blit_list.append((pos[0],pos[1]-self.size[1]))
        elif pos[1] < 0:#DOWN
            blit_list.append((pos[0],pos[1]+self.size[1]))
        if pos[0] > 0 and pos[1] > 0:#UPLEFT
            blit_list.append((pos[0]-self.size[0],pos[1]-self.size[1]))
        if pos[0] > 0 and pos[1] < 0:#DOWNLEFT
            blit_list.append((pos[0]-self.size[0],pos[1]+self.size[1]))
        if pos[0] < 0 and pos[1] > 0:#UPRIGHT
            blit_list.append((pos[0]+self.size[0],pos[1]-self.size[0]))
        if pos[0] < 0 and pos[1] < 0:#DOWNRIGHT
            blit_list.append((pos[0]+self.size[0],pos[1]+self.size[1]))


        #displaying all blits
        for blit in blit_list:
             window.blit( 
                self.image,blit
                )