#Code by Andrew Church
import pygame,anim,math,bullets,audio,tools

# "bar":(
#         "h", #if the bar is horizontal or vertical.
#         450, #x position if vertical, y position if horizontal.
#         (10,590), #the limits on both sides for the player to move on, y positions if vertical, x positions if horizontal
#         1, #gravity. 
#         )



class Player(pygame.sprite.Sprite):

    image = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.rect(image,"white",pygame.Rect(0,0,30,30))

    def __init__(self,bar,sprite_groups, demo=False): #again, the demo here is different from tools.demo
        pygame.sprite.Sprite.__init__(self)

        #ARGUMENTATIVE 
        self.bar=bar
        self.sprite_groups = sprite_groups
        self.demo = demo

        #IMAGE AND POSITIONING
        self.sh = anim.Spritesheet("YUP","idle")
        self.image = anim.all_loaded_spritesheets[self.sh.name][1][self.sh.image_displayed]
        self.rect = self.image.get_rect()
        self.rect.center = (300,self.bar[1])
        

        #MOVEMENT CODE
        self.movement = [
            0, #y velocity
            False, #moving left
            False, #moving right
            False, #jumping
            False, #crouching
        ]
        #how fast the character moves
        self.speed = 7
        self.crouch_speed = 3
        self.momentum = 0

        #HEALTH
        self.health = 3
        self.invincibility_counter = 0 
        self.dead = self.health < 1

        #EXTRA
        self.autoshoot = False



    def update(self):
        #SETTING THE IMAGE. I have no issue resetting the image every frame because it's just a callback to an object
        try:
            self.sh.update()
            self.image = self.sh.image
        except: 
            self.image = Player.image
        

        #07/09/2023 - rotating the image based on movement
        try:
            if self.momentum != 0 and not self.movement[4]:
                self.image = pygame.transform.rotate(self.image,self.momentum*-2)
        except:...

        #collision is just movement
        self.collision()
        self.health_update()


        #debug
        if self.autoshoot:
            bullet=bullets.Bullet(self.rect.center)
            bullets.Bullet.count-=1
            self.sprite_groups[0].add(bullet)
            self.sprite_groups[3].add(bullet)

        #demo
        if self.demo:
            self.invincibility_counter = 6




    def controls(self,event):
        #ENGAGING movement
        if event.type == pygame.KEYDOWN:
            #ENGAGING the movement
            if event.key == pygame.K_LEFT:
                self.movement[1] = True
            if event.key == pygame.K_RIGHT:
                self.movement[2] = True


            #STARTING THE JUMPS
            if event.key == pygame.K_UP and not self.movement[3]:
                self.bounce()
            if event.key == pygame.K_DOWN and self.movement[3]:
                self.movement[0]=25
            elif event.key == pygame.K_DOWN:
                #crouching
                self.change_anim("crouch")
                self.movement[4] = True
                

            #SHOOTING
            if (event.key == pygame.K_x or event.key == pygame.K_z) and not self.movement[4]:
                bullet=bullets.Bullet(self.rect.center,is_default=not self.demo)
                self.sprite_groups[0].add(bullet)
                self.sprite_groups[3].add(bullet)
                if not bullet.kill_on_spawn: self.change_anim("shoot")

            #AUTOSHOOT
            if tools.debug:
                if event.key == pygame.K_2:
                    self.autoshoot = not self.autoshoot
                if event.key == pygame.K_3:
                    self.health += 10


        #RELEASING movement
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.movement[1] = False
            if event.key == pygame.K_RIGHT:
                self.movement[2] = False
            #un-crouching
            if event.key == pygame.K_DOWN:
                self.movement[4] = False
                self.change_anim('idle')
        
    def collision(self):
    
        #most collision will now be done in the state, instead of by invidual characters
        #this is so there's not a huge loop of characters colliding
        #it removes a *shred* of universality, but it's fine
        if self.movement[1]:
            self.momentum = self.speed*-1 if not self.movement[4] else self.crouch_speed*-1
        elif self.movement[2]: 
            self.momentum = self.speed if not self.movement[4] else self.crouch_speed

        self.momentum *= 0.85 if (self.momentum > 1 or self.momentum < -1) else 0

        #jumping code
        #doing y momentum stuffystuff
        if self.movement[3]:
            self.rect.y += self.movement[0]
            self.movement[0] += .3
            if self.rect.center[1]>self.bar[1]:
                #finishing the jump, including stopping values
                self.rect.center = (self.rect.center[0],self.bar[1])
                self.movement[3] = False
                self.movement[0] = 0
                self.change_anim("land")
                #AUTO CROUCH
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    #crouching
                    self.change_anim("crouch")
                    self.movement[4] = True
        


        #Actually making the player move, bouncing the character off the bars if needed
        if (self.rect.center[0] + self.momentum) < self.bar[2][0] or (self.rect.center[0] + self.momentum) > self.bar[2][1]: 
            self.momentum = 0
            self.change_anim("squish")
        self.rect.x += self.momentum

    def health_update(self):
        #HEALTH checking
        ##invincibility
        if self.invincibility_counter >= 0: self.invincibility_counter -= 1 
        ##checking for death
        self.dead = self.health < 1



    def on_collide(self,
                   collide_type:int, #the collide_type refers to the sprite group numbers. 0 for universal (not used), 1 for other player elements, 2 for enemies
                   collided:pygame.sprite.Sprite, #the specific object being collided with
                   ):
        ... #moved to enemy classes
            



    def hurt(self,amount:int=1):
        if self.invincibility_counter < 1:
            self.change_anim("hurt")
            self.health -= amount
            self.invincibility_counter = 60
            audio.play_sound("ouch.mp3" if self.health > 0 else "death.mp3",)
            if self.health <= 0: self.kill()

    def bounce(self):
        #make the player bounce
        self.movement[0]=-7.5
        self.movement[3]=True
        self.change_anim("jump")
        
    def reset_movement(self):
        self.movement = [
            0, #frames in up jumping movement, 30 frame limit
            0, #frames in down jumping movement, 30 frame limit
            False, #moving left
            False, #moving right
            False, #crouching
        ]
    def display_health(self):
        pass

    def change_anim(self, anim:str):
        if "sh" in dir(self):
            self.sh.change_anim(anim)
            self.sh.update()
            self.image = self.sh.image
            
