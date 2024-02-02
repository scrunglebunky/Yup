#Program by Andrew Church 5/26/23
import pygame,audio,tools,random
from anim import AutoImage as AImg

# 5/26/23 - This is the default bullet.
# It is rather similar to the previous version's bullet, but that's because of how simple it is
class Bullet(pygame.sprite.Sprite):
    
    #DEFAULT IMAGE - rendered by pygame draw function
    image = pygame.Surface((10, 10), pygame.SRCALPHA)
    pygame.draw.circle(image, "black", (5, 5), 5)
    pygame.draw.circle(image, "white", (5, 5), 4)
    screen_rect = pygame.Rect(0,0,pygame.display.play_dimensions[0],pygame.display.play_dimensions[1])

    count = 0
    max = 100

    def __init__(self,pos:tuple=(0,0),speed:int=15,is_default:bool = True,texture:str = None,**kwargs):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.aimg = AImg(host=self,name=texture,current_anim='idle',force_surf = Bullet.image)
        self.rect.center=pos
        self.health = 1
        self.speed=speed
        self.kill_on_spawn = False
        self.sprites = kwargs['sprites']



        #5/27/2023 - Kill Counter
        # If there are too many of a single bullet on screen, the bullet stops spawning. That's all. 
        if is_default: # 06/24/2023 addendum -> the maximum bullet check only really counts for the default bullet, as each bullet has their own individual counts
            Bullet.count += 1
            if Bullet.count > Bullet.max:
                self.kill_on_spawn = True
                return
        
        

    def update(self):
        #updating anim
        self.aimg.update()

        #updating collision
        if not self.on_screen() or self.health <= 0 or self.kill_on_spawn:
            self.kill()
        self.rect.y -= self.speed
        

    def on_screen(self) -> bool:
        return Bullet.screen_rect.colliderect(self.rect)

    def on_collide(self,collide_type,collided):
        ...
    
    def hurt(self):
        self.health -= 1

    def kill(self):
        pygame.sprite.Sprite.kill(self)
        Bullet.count = Bullet.count - 1 if Bullet.count > 0 else 0 
        if self.health <= 0:
            for i in range(5):self.sprites[0].add(BulletParticle(self.rect.center))
            # audio.play_sound("smallboom0.wav")



class TripleBullet(Bullet):
    ...


class Item(pygame.sprite.Sprite):
    def __init__(self):...


def emptyBulletMax():
    for item in LOADED:
        item.count = 0 


class BulletParticle(pygame.sprite.Sprite):
    image = pygame.Surface((5,5))
    pygame.draw.rect(image,color="black",rect=pygame.Rect(0,0,5,5))
    pygame.draw.rect(image,color="white",rect=pygame.Rect(1,1,3,3))
    def __init__(self,pos:tuple = (0,0),texture=None):
        pygame.sprite.Sprite.__init__(self)
        self.aimg = AImg(host=self,name=texture,current_anim='idle',force_surf = BulletParticle.image)
        self.rect.center = pos
        self.gravity_info = [
            random.randint(-5,5), #x movement
            random.randint(-5,-1), #y gravity
        ]
        self.duration = 0 

    def update(self):
        #moving x
        self.rect.x += self.gravity_info[0]
        #moving y
        self.rect.y += self.gravity_info[1]
        #changing x gravity
        self.gravity_info[0] = round(self.gravity_info[0]*0.98,5) if abs(self.gravity_info[0]) > 0.001 else 0
        #changing y gravity
        self.gravity_info[1] = self.gravity_info[1]+0.5 if self.gravity_info[1] < 7 else 7
        #updating duration information
        self.duration += 1
        #autokill
        if self.duration > 15:
            self.kill()

LOADED = [
    Bullet,
]


