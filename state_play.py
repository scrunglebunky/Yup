import pygame,os,player,text,random,characters,levels,json,formation,anim,backgrounds,audio
from emblems import Emblem as Em
#05/28/2023 - STATE IMPLEMENTATION
# instead of everything being handled in main, states handle every specific thing
# playstate is what handles gameplay, specifically
# therefore, this state holds quite a lot of information!

class State():
    sprites = { #sprites are now state-specific hahaha
            0:pygame.sprite.Group(), #ALL SPRITES
            1:pygame.sprite.Group(), #PLAYER SPRITE, INCLUDING BULLETS ; this is because the player interacts with characters the same way as bullets
            2:pygame.sprite.Group(), #ENEMY SPRITES
            3:pygame.sprite.Group(), #BULLET SPRITES
        }

    def __init__(self,
                 window:pygame.display,
                 campaign:str = "main_story.order",
                 world:int = 0,
                 level:int = 0,
                 level_in_world:int = 1,
                 is_restart:bool = False, #so init can be rerun to reset the whole ass state
                 ):

        self.next_state = None #Needed to determine if a state is complete
        self.fullwindow = window

        self.debug = {0:[],1:[]}


        #resetting the sprite groups
        for group in self.sprites.values():
            group.empty()

        #06/23/2023 - SETTING THE GAMEPLAY WINDOW
        # YUP has a touhou-like border surrounding the entire game as it works
        # Because of this, gameplay will have its own entire tiny display to work with 
        # It still saves the original pygame window, but this is just to draw the display to.abs
        if not is_restart: #it only makes this the first time
            self.window = pygame.Surface(pygame.display.play_dimensions).convert_alpha()

        #Player spawn
        self.bar = ( #the field the player is able to move along
            "h", #if the bar is horizontal or vertical.
            pygame.display.play_dimensions[1]*0.90, #x position if vertical, y position if horizontal.
            (20,pygame.display.play_dimensions[0]-20), #the limits on both sides for the player to move on, y positions if vertical, x positions if horizontal
            1, #gravity. 
            )
            
        self.player = player.Player(bar=self.bar,sprite_groups=State.sprites)
        State.sprites[0].add(self.player); State.sprites[1].add(self.player)

        #06/01/2023 - Loading in level data
        self.campaign = campaign
        self.world = world
        self.level = level #the total amount of levels passed, usually used for intensities or score
        self.level_in_world = level_in_world #the amount of levels completed in the world currently 
        self.world_data = levels.fetch_level_info(campaign_world = (self.campaign,self.world))
        #updating based on intensity
        if self.world_data["dynamic_intensity"]:
            levels.update_intensities(self.level,self.world_data)

        #06/01/2023 - loading the formation
        #the formation handles spawning and management of most characters, but the state manages drawing them to the window and updating them
        self.formation = formation.Formation(
            player = self.player,
            world_data = self.world_data,
            level=self.level,
            level_in_world=self.level_in_world, 
            sprites=State.sprites,)

        #06/03/2023 - Loading in the background
        self.background = backgrounds.Background(self.world_data['bg'], resize = self.world_data['bg_size'], speed = self.world_data['bg_speed'])



        #relating to advance sprite
        self.in_advance:bool = False #if true, will not update much besides the background and player

        
   
    
    def on_start(self,**kwargs):#__init__ v2, pretty much.
        #06/24/2023 - Playing the song
        audio.play_song(self.world_data["song"])

    def on_end(self,**kwargs): #un-init, kind of
        pygame.mixer.music.stop()
        print(self.debug.values())

    
    def update(self, draw=True):

        #Updating sprites
        self.background.update()
        self.background.draw(self.window)
        State.sprites[0].update()
        State.sprites[0].draw(self.window)
        self.formation.update()

        #print debug positions
        for pos in self.debug[0]:
            self.window.blit(pygame.transform.scale(anim.all_loaded_images["placeholder.bmp"],(10,10)),pos)

        #06/23/2023 - Drawing gameplay window to full window
        if draw: self.fullwindow.blit(pygame.transform.scale(self.window,pygame.display.play_dimensions_resize),pygame.display.play_pos)

        #ending function early if advancing
        if self.in_advance: return 

        #Detecting collision between players and enemies 
        collidelist=pygame.sprite.groupcollide(State.sprites[1],State.sprites[2],False,False,collided=pygame.sprite.collide_mask)
        collidelist2=pygame.sprite.groupcollide(State.sprites[2],State.sprites[3],False,False,collided=pygame.sprite.collide_mask)
        for key,value in collidelist.items():
            key.on_collide(2)
            value[0].on_collide(1)
        for key,value in collidelist2.items():
            key.on_collide(3)
            value[0].on_collide(2)

        
        #06/18/2023 - Starting a new level
        if self.formation.cleared:
            if self.level_in_world+1 > self.world_data["levels"]:
                self.next_state = "advance"
                return
            else:
                self.level += 1
                self.level_in_world += 1
                if self.world_data["dynamic_intensity"]:
                    levels.update_intensities(self.level,self.world_data)
                self.formation.empty()
                #checking to start the advance state
            self.formation.__init__(
                world_data = self.world_data,
                level=self.level,
                level_in_world=self.level_in_world, 
                sprites=State.sprites,
                player=self.player,)
        #08/21/2023 - Game Over - opening a new state if the player is dead
        if self.player.health <= 0:
            self.next_state = "gameover"


        


    def new_world(self):
        self.world += 1
        self.level_in_world = 0
        self.world_data = levels.fetch_level_info(campaign_world = (self.campaign,self.world))
        #updating based on intensity
        if self.world_data["dynamic_intensity"]:
            levels.update_intensities(self.level,self.world_data)
        #changing bg
        self.background.change(self.world_data['bg'], resize = self.world_data['bg_size'], speed = self.world_data['bg_speed'])



    def event_handler(self,event):
        self.player.controls(event)
        #changing what comes next
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.next_state = "options","play"
            if event.key == pygame.K_ESCAPE:
                self.next_state = "pause"
            if event.key == pygame.K_0:
                self.player.hurt()
            if event.key == pygame.K_2:
                self.formation.cleared = True
            if event.key == pygame.K_b:
                State.sprites[0].add(
                    Em(
                        im=None,
                        coord=(random.randint(0,pygame.display.dimensions[0]),random.randint(0,pygame.display.dimensions[1])),
                        isCenter=True,animated=True,animation_resize=(random.randint(10,500),random.randint(10,500)),animation_killonloop=True
                ))
            if event.key == pygame.K_4:
                self.debug[0].pop(len(self.debug[0])-1)
                self.debug[1].pop(len(self.debug[1])-1)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = tuple(pygame.mouse.get_pos())
            pos = [pos[0]-pygame.display.play_pos[0],pos[1]-pygame.display.play_pos[0]]
            pos2 = [pygame.display.play_dimensions_resize[0]-pos[0],pos[1]]
            self.debug[0].append(pos)
            self.debug[1].append(pos2)
            print(pos,pos2)
