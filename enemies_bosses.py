import pygame
from anim import all_loaded_images as img
from anim import AutoImage as AImg

#a boss contains a collection of autoimages and hitboxes in order to check for very specific collision
class Boss(pygame.sprite.Sprite):
    def __init__(self,pos:tuple=(100,100)):
        pygame.sprite.Sprite.__init__(self)
        self.image = img['placeholder.bmp'] #a placeholder to figure out the positioning of the boss.
        self.attributes = {
            #a collection of other sprites to be added to the boss: the main body, arms, head maybe?
        }
    def update(self):
        ...
    def collision_master(self,collidername):...


#a piece of a boss. think of the boss as some sort of hand controlling a bunch of puppets.
class BossAttribute(pygame.sprite.Sprite):
    def __init__(self,host:Boss, name:str="placeholder", image:str = "placeholder.bmp", pos:tuple = (100,100)):
        #image info
        self.autoimage = AImg(name=image)
        self.image = self.autoimage.image

        #positioning info
        self.rect = self.image.get_rect()
        self.rect.center = pos

        #naming info
        self.host = host
        self.name = name
    def on_collide(self):...
    def update(self):...