import pygame,random
from anim import all_loaded_images as img
from anim import AutoImage as AImg
from bullets import * 
from enemies import Template

#a boss contains a collection of autoimages and hitboxes in order to check for very specific collision
class Boss():
    #the boss behaves like a puppet master to a bunch of different boss "attributes". it may be as simple as a small png, or as complex as a series of limbs and a head with jaws
    def __init__(self,kwargs:dict):
        self.sprites = kwargs['sprites']
        print("BOSS ACTIVE. BOSS HAS BEEN ACTIVATED.")
        self.attributes = {
            #a collection of other sprites to be added to the boss: the main body, arms, head maybe?
        }
        self.info = {
            #a series of information pieces on the boss. 
            'health':10,
        }
    def update(self):
        ...
    def collision_master(self,collidername,collide_type,collided):
        #first value -> attribute that found collision #second value -> type of sprite the attribute collided with #third value -> same but with a pygame type() definition
        ...
    def addAttribute(self,name:str,attribute):
        self.attributes[name] = attribute
        self.sprites[0].add(attribute)
        self.sprites[2].add(attribute)


#a piece of a boss. think of the boss as some sort of hand controlling a bunch of puppets.
class BossAttribute(pygame.sprite.Sprite):
    def __init__(self,host:Boss, sprites:dict, name:str="placeholder", image:str = "placeholder.bmp", pos:tuple = (100,100)):
        #basic initialization
        pygame.sprite.Sprite.__init__(self)
        self.sprites=sprites
        
        #image info
        self.autoimage = AImg(name=image)
        self.image = self.autoimage.image

        #positioning info
        self.rect = self.image.get_rect()
        self.rect.center = pos

        #naming info
        self.host = host
        self.name = name
    def on_collide(self,collide_type:int,collided:pygame.sprite.Sprite):
        self.host.collision_master(self.name,collide_type,collided)
    def update(self):...
    def shoot(self, type: str="point", spd: int=7, info: tuple=((0,0),(100,100)), shoot_if_below: bool=True):
        bullet=None
        if (shoot_if_below) or (type != 'point') or (info[0][1] < info[1][1]-50):
            bullet = HurtBullet(type=type,spd=spd,info=info,texture=None)
            self.sprites[0].add(bullet)
            self.sprites[2].add(bullet)
        return bullet

        


class UFO(Boss):
    def __init__(self,**kwargs):
        Boss.__init__(self,kwargs=kwargs)
        self.addAttribute(name='body' , attribute = BossAttribute(host=self,sprites=self.sprites,name='body',image="ufo.png",pos=(100,100)))
    def update(self,**kwargs):
        self.attributes['body'].shoot(type='angle',spd=7,info=(self.attributes['body'].rect.center,random.randint(0,360)),shoot_if_below=True)

    



loaded = {
    "ufo":UFO,
}
    