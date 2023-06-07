#Code by Andrew Church
import pygame,anim,math,bullets

# "bar":(
#         "h", #if the bar is horizontal or vertical.
#         450, #x position if vertical, y position if horizontal.
#         (10,590), #the limits on both sides for the player to move on, y positions if vertical, x positions if horizontal
#         1, #gravity. 
#         )



class Player(pygame.sprite.Sprite):
    def __init__(self,bar,sprite_groups):
        pygame.sprite.Sprite.__init__(self)

        #ARGUMENTATIVE 
        self.bar=bar
        self.sprite_groups = sprite_groups

        #IMAGE AND POSITIONING
        #note to self - MASKS REMOVED
        #I do like masks, but it seems they should only be used for the pygame collision item
        #When used here, their position resets to (0,0) and has to be controlled separately from rects, which is too much work and makes no sense
        #If I was *not* using Pygame, I would personally have everything controlled as empty rectangles, with images drawn to them on their own
        #This would fix most mask issues and would make it so the images are not tied to the image
        self.sh = anim.Spritesheet("YUP","idle")
        self.image = anim.all_loaded_spritesheets[self.sh.name][1][self.sh.image_displayed]
        self.rect = self.image.get_rect()
        self.rect.center = (300,self.bar[1])

        #MOVEMENT CODE
        self.movement = [
            0, #frames in up jumping movement, 30 frame limit
            0, #frames in down jumping movement, 30 frame limit
            False, #moving left
            False, #moving right
        ]
        #how fast the character moves
        self.speed = 5
        self.momentum = 0

        #HEALTH
        self.health = 3
        self.invincibility_counter = 0 
        self.dead = self.health < 1



    def update(self):
        #SETTING THE IMAGE. I have no issue resetting the image every frame because it's just a callback to an object
        self.image = self.sh.update()
        #collision is just movement
        self.collision()



    def controls(self,event):
        #ENGAGING movement
        if event.type == pygame.KEYDOWN:
            #ENGAGING the movement
            if event.key == pygame.K_LEFT:
                self.movement[2] = True
            if event.key == pygame.K_RIGHT:
                self.movement[3] = True


            #STARTING THE JUMPS
            if event.key == pygame.K_UP and self.movement[0] == 0:
                if self.movement[1] > 0: 
                    self.movement[1] = 60
                else:
                    self.movement[0] = 1

            if event.key == pygame.K_DOWN and self.movement[1] == 0:
                if self.movement[0] > 0: 
                    self.movement[0] = 60
                else:
                    self.movement[1] = 1

            #SHOOTING
            if event.key == pygame.K_x or event.key == pygame.K_z:
                bullet=bullets.Bullet(self.rect.center)
                self.sprite_groups[0].add(bullet)
                self.sprite_groups[1].add(bullet)
                if not bullet.kill_on_spawn: self.sh.change_anim("shoot")


        #RELEASING movement
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.movement[2] = False
            if event.key == pygame.K_RIGHT:
                self.movement[3] = False
        
    def collision(self):
    
        #most collision will now be done in the state, instead of by invidual characters
        #this is so there's not a huge loop of characters colliding
        #it removes a *shred* of universality, but it's fine
        if self.movement[2]:
            self.momentum = self.speed*-1  
        elif self.movement[3]: 
            self.momentum = self.speed 

        self.momentum *= 0.85 if (self.momentum > 1 or self.momentum < -1) else 0

        #jumping code
        #if the frames for jumping is not 0 (active)
        if self.movement[0] > 0:
            self.movement[0] += 1
            #positioning
            self.rect.center = (
                self.rect.center[0],
                (1/9)*(((self.movement[0])-30)**2) + self.bar[1]-100
            )
            #resetting positioning
            if self.movement[0] >= 60:
                self.movement[0] = 0
                self.rect.center = (self.rect.center[0],self.bar[1])
                self.sh.change_anim("land")
        
        #jumping down - IDENTICAL to jumping up, so it is condensed to be less readable
        if self.movement[1] > 0:
            self.movement[1] += 1
            self.rect.center = (self.rect.center[0],(-1/18)*(((self.movement[1])-30)**2) + self.bar[1]+50)
            if self.movement[1] >= 60:
                self.movement[1] = 0
                self.rect.center = (self.rect.center[0],self.bar[1])
                self.sh.change_anim("land")


        #Actually making the player move, bouncing the character off the bars if needed
        if (self.rect.center[0] + self.momentum) < self.bar[2][0] or (self.rect.center[0] + self.momentum) > self.bar[2][1]: 
            self.momentum = 0
            self.sh.change_anim("squish")
        self.rect.x += self.momentum

    def health_update(self):
        #HEALTH checking
        ##invincibility
        if self.invincibility_counter > 0: self.invincibility_counter -= 1 
        ##checking for death
        self.dead = self.health < 1

    def on_collide(self,
                   collide_type:int #the collide_type refers to the sprite group numbers. 0 for universal (not used), 1 for other player elements, 2 for enemies
                   ):
        #if colliding with an enemy, hurt.
        if collide_type == 2 and self.invincibility_counter < 1 : #(the player cannot be invincible)
            self.sh.change_anim("hurt")
            print('ouch!')
            self.health -= 1
            self.invincibility_counter = 60
        
    def reset_movement(self):
        pass
    def display_health(self):
        pass
