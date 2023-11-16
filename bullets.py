#Program by Andrew Church 5/26/23
import pygame,audio,tools
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
    max = 4

    def __init__(self,pos:tuple=(0,0),speed:int=15,is_default:bool = True,texture:str = None,**kwargs):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.autoimage = AImg(name=texture,current_anim='idle',force_surf = Bullet.image)
        self.image = self.autoimage.image
        self.rect = self.image.get_rect()
        self.rect.center=pos
        self.health = 1
        self.speed=speed
        self.kill_on_spawn = False



        #5/27/2023 - Kill Counter
        # If there are too many of a single bullet on screen, the bullet stops spawning. That's all. 
        if is_default: # 06/24/2023 addendum -> the maximum bullet check only really counts for the default bullet, as each bullet has their own individual counts
            Bullet.count += 1
            if Bullet.count > Bullet.max:
                self.kill_on_spawn = True
                return
        
        

    def update(self):
        #updating anim
        self.autoimage.update()
        self.image = self.autoimage.image

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



class TripleBullet(Bullet):
    ...


class Item(pygame.sprite.Sprite):
    def __init__(self):...


def emptyBulletMax():
    for item in LOADED:
        item.count = 0 

LOADED = [
    Bullet,
]