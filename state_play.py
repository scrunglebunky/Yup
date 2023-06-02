import pygame,os,player,text,random,characters,levels,json,formation,anim
#05/28/2023 - STATE IMPLEMENTATION
# instead of everything being handled in main, states handle every specific thing
# playstate is what handles gameplay, specifically
# therefore, this state holds quite a lot of information!

class State():
    def __init__(self,
                 data:dict,
                 sprites:dict,
                 window:pygame.display,
                 campaign:str = "main_story.order",
                 world:int = 1,
                 level:int = 1,
                 level_in_world:"int" = 1,
                 ):
        self.sprites = sprites
        self.data = data
        self.window = window

        #Test character
        ch=characters.CharTemplate(formation_position=(100,450),data=self.data)
        sprites[0].add(ch); sprites[2].add(ch)

        #Player spawn
        self.player = player.Player(bar=data["bar"],sprite_groups=self.sprites)
        sprites[0].add(self.player); sprites[1].add(self.player)

        #Loading in level data
        self.campaign = campaign
        self.world = world
        self.level = level #the total amount of levels passed, usually used for intensities or score
        self.level_in_world = level_in_world #the amount of levels completed in the world currently 
        self.leveldata = levels.update_intensities(self.level,levels.fetch_level_info(campaign_world = (self.campaign,self.world)))

        #loading the formation
        self.formation = formation.Formation(player = self.player,leveldata = self.leveldata,level=self.level,level_in_world=self.level_in_world)


        #text spawn
        for i in range(0):
            spd=random.randint(-5,5)
            if spd == 0: spd = 1
            txt=text.Text(text=str("uwu"),vertex=(random.randint(0,450),random.randint(0,600)),pos=(random.randint(0,450),random.randint(0,600)),pattern="sine",duration=3600,modifier=random.randint(1,100),modifier2=(random.randint(1,25)/random.randint(1,100)),speed=spd)
            sprites[0].add(txt)

    def update(self):
        #Updating sprites
        self.sprites[0].update()
        self.sprites[0].draw(self.window)
        self.formation.update()

        #Detecting collision between players and enemies 
        collidelist=pygame.sprite.groupcollide(self.sprites[1],self.sprites[2],False,False)
        for key,value in collidelist.items():
            key.on_collide(2)
            value[0].on_collide(1)

        #drawing positioning for the formation for test purposes
        self.window.blit(anim.all_loaded_images["placeholder.bmp"],self.formation.pos)
       
    def event_handler(self,event):
        self.player.controls(event)