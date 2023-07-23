import pygame,os,player,text,random,characters,levels,json,formation,anim,backgrounds,audio
#05/28/2023 - STATE IMPLEMENTATION
# instead of everything being handled in main, states handle every specific thing
# playstate is what handles gameplay, specifically
# therefore, this state holds quite a lot of information!

class State():
    data:dict = None
    sprites:dict = None

    def __init__(self,
                 data:dict,
                 sprites:dict,
                 window:pygame.display,
                 campaign:str = "main_story.order",
                 world:int = 1,
                 level:int = 1,
                 level_in_world:int = 1,
                 repeat:bool = False
                 ):

        self.next_state = None #Needed to determine if a state is complete
        self.sprites = sprites
        self.data = data
        self.fullwindow = window

        #06/23/2023 - SETTING THE GAMEPLAY WINDOW
        # YUP has a touhou-like border surrounding the entire game as it works
        # Because of this, gameplay will have its own entire tiny display to work with 
        # It still saves the original pygame window, but this is just to draw the display to.abs
        self.window = pygame.Surface(pygame.display.play_dimensions).convert_alpha()

        #Player spawn
        self.bar = ( #the field the player is able to move along
            "h", #if the bar is horizontal or vertical.
            pygame.display.play_dimensions[1]*0.90, #x position if vertical, y position if horizontal.
            (20,pygame.display.play_dimensions[0]-20), #the limits on both sides for the player to move on, y positions if vertical, x positions if horizontal
            1, #gravity. 
            )
            
        self.player = player.Player(bar=self.bar,sprite_groups=self.sprites)
        sprites[0].add(self.player); sprites[1].add(self.player)

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
            data=self.data,
            level_in_world=self.level_in_world, 
            sprites=self.sprites)

        #06/03/2023 - Loading in the background
        self.background = backgrounds.Background(self.world_data['bg'], resize = self.world_data['bg_size'], speed = self.world_data['bg_speed'])
        self.background.player_multiplier = self.world_data["bg_player_move"]

        # TEST - text spawn
        for i in range(0):
            spd=random.randint(-5,5)
            if spd == 0: spd = 1
            txt=text.Text(text=random.choice(["owo","uwu","hewwo","cwinge","howy fuck"]),vertex=(random.randint(0,450),random.randint(0,600)),pos=(random.randint(0,450),random.randint(0,600)),pattern="sine",duration=3600,modifier=random.randint(1,100),modifier2=(random.randint(1,25)/random.randint(1,100)),speed=spd)
            sprites[0].add(txt)

        #06/24/2023 - Playing the song
        audio.play_song(self.world_data["song"])
    
    def on_start(self):... #__init__ v2, pretty much.

    def update(self):
        #Updating sprites
        self.background.update()
        if self.world_data["bg_player_move"] != 0: self.background.update_offset(pos=self.player.rect.center[0])
        self.background.draw(self.window)
        self.sprites[0].update()
        self.sprites[0].draw(self.window)
        self.formation.update()
        #06/23/2023 - Drawing gameplay window to full window
        self.fullwindow.blit(pygame.transform.scale(self.window,pygame.display.play_dimensions_resize),pygame.display.play_pos)

        #Detecting collision between players and enemies 
        collidelist=pygame.sprite.groupcollide(self.sprites[1],self.sprites[2],False,False,collided=pygame.sprite.collide_mask)
        for key,value in collidelist.items():
            key.on_collide(2)
            value[0].on_collide(1)

        #06/01/2023 - TEST - drawing positioning for the formation for test purposes
        # self.window.blit(anim.all_loaded_images["placeholder.bmp"],self.formation.pos)

        #06/18/2023 - Displaying the score
        # text.display_numbers(self.data["score"],pos=(pygame.display.dimensions[0],0),window=self.window,reverse=True)

        #06/18/2023 - Starting a new level
        if self.formation.completed_level:
            self.level += 1
            self.level_in_world += 1
            if self.world_data["dynamic_intensity"]:
                levels.update_intensities(self.level,self.world_data)
            self.formation.empty()
            self.formation.__init__(self.player,self.world_data,self.sprites,self.data,self.level,self.level_in_world)
   
    def event_handler(self,event):
        self.player.controls(event)
        #changing what comes next
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.next_state = "options"
            if event.key == pygame.K_ESCAPE:
                self.next_state = "pause"