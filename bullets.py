#Program by Andrew Church 5/26/23
import pygame,audio,tools

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

    def __init__(self,pos:tuple=(0,0),sound:str="shoot.mp3",speed:int=15,is_default:bool = True,**kwargs):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = Bullet.image
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
        
        #06/24/2023 - playing sound
        audio.play_sound(sound,category="bullet",)
        

    def update(self):
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

class HurtBullet(pygame.sprite.Sprite):
    #DEFAULT IMAGE - rendered by pygame draw function
    image = pygame.Surface((10, 10), pygame.SRCALPHA)
    pygame.draw.circle(image, "#AA0000", (5, 5), 5)
    pygame.draw.circle(image, "red", (5, 5), 4)
    screen_rect = pygame.Rect(0, 0, 450, 600)

    #limits so the game doesnt lag
    count = 0
    max = 1000

    def __init__(self,type:str="point",spd:int=2,info:tuple=((0,0),(100,100)),image:pygame.Surface=None):
        #FOR AN ANGLE, the info is (pointa,angle)
        pygame.sprite.Sprite.__init__(self)
        
        #checking for max bullet count
        HurtBullet.count += 1
        self.killonstart = True if HurtBullet.count > HurtBullet.max else False

        #setting number values
        if type == "point":
            self.move = tools.MovingPoint(pointA=info[0],pointB=info[1],speed=spd)
        elif type == "angle":
            self.move = tools.AnglePoint(pointA=info[0],angle=info[1],speed=spd)
        self.health = 1
        
        #setting image
        if image is not None:
            self.image = pygame.transform.scale(image,(10,10))
        else:
            self.image = HurtBullet.image
        self.rect = self.image.get_rect()
        self.rect.center = self.move.position
        
    def update(self):
        self.move.update()
        self.rect.center = self.move.position
        if not Bullet.on_screen(self) or self.health <= 0 or self.killonstart: 
            self.kill()
            HurtBullet.count = HurtBullet.count - 1 if HurtBullet.count > 0 else 0 
    
    def on_collide(self,collide_type,collided):
        #5/26/23 - This is usually explained elsewhere
        #collision with enemy types
        if collide_type == 1:
            self.hurt()
            collided.hurt()
    
    def hurt(self):
        self.health -= 1


class TripleBullet(Bullet):
    ...


class Item(pygame.sprite.Sprite):
    def __init__(self):...

LOADED = [
    Bullet,
]