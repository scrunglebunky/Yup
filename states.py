import pygame,os,player,text,random,levels,json,formation,anim,audio,tools,events,score,enemies,enemies_bosses
from anim import all_loaded_images as img
from text import loaded_text as txt
from backgrounds import Background as Bg
from backgrounds import Floor as Fl
from emblems import Emblem as Em
from bullets import emptyBulletMax as eBM

#basic template for states to go off of
class Template():
    def __init__(self):
        self.next_state = None #Needed to determine if a state is complete
    def on_start(self):
        ...
    def on_end(self):
        ...
    def event_handler(self,event):
        ...




#gameplay
class Play(Template):
    sprites = { #sprites are now state-specific hahaha
            0:pygame.sprite.Group(), #ALL SPRITES
            1:pygame.sprite.Group(), #PLAYER SPRITE, INCLUDING BULLETS ; this is because the player interacts with enemies the same way as bullets
            2:pygame.sprite.Group(), #ENEMY SPRITES
            # 4:pygame.sprite.Group(), #UI SPRITES
        }
    demo_sprites = { #sprites exclusively for the demo state
            0:pygame.sprite.Group(), #ALL SPRITES
            1:pygame.sprite.Group(), #PLAYER SPRITE, INCLUDING BULLETS ; this is because the player interacts with enemies the same way as bullets
            2:pygame.sprite.Group(), #ENEMY SPRITES
            4:pygame.sprite.Group(), #UI SPRITES
        }

    def __init__(self,
                 window:pygame.display,
                 campaign:str = "main_story.order",
                 world:int = 4,
                 level:int = 1,
                 level_in_world:int = 0,
                 is_restart:bool = False, #so init can be rerun to reset the whole ass state
                 is_demo:bool=False, #a way to check if the player is simulated or not
                 ):

        self.next_state = None #Needed to determine if a state is complete
        self.fullwindow = window

        self.debug = {0:[],1:[]}
        self.is_demo = is_demo


        #resetting the sprite groups
        for group in (Play.sprites if not self.is_demo else Play.demo_sprites).values():
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
            
        self.player = player.Player(bar=self.bar,sprite_groups=(self.sprites if not self.is_demo else self.demo_sprites),demo=self.is_demo)
        (self.sprites if not self.is_demo else self.demo_sprites)[1].add(self.player)

        #06/01/2023 - Loading in level data
        self.campaign = campaign
        self.world = world
        self.level = level #the total amount of levels passed, usually used for intensities or score
        self.level_in_world = level_in_world #the amount of levels completed in the world currently 
        self.world_data = levels.fetch_level_info(campaign_world = (self.campaign,self.world))


        #event data - an event that plays over all else.
        self.event = events.NewLevelEvent(level=self.level,window=self.window) if not self.is_demo else None
        

        #updating based on intensity
        if self.world_data["dynamic_intensity"]:
            levels.update_intensities(self.level,self.world_data)

        #06/01/2023 - loading the formation
        #the formation handles spawning and management of most enemies, but the state manages drawing them to the window and updating them
        self.formation = formation.Formation(
            player = self.player,
            world_data = self.world_data,
            level=self.level,
            level_in_world=self.level_in_world, 
            sprites=(self.sprites if not self.is_demo else self.demo_sprites),
            window=self.window,
            is_demo = self.is_demo)

        #06/03/2023 - Loading in the background
        self.background = Bg(self.world_data['bg'], resize = self.world_data['bg_size'], speed = self.world_data['bg_speed'])
        #also loading in the floor if it exists
        self.floor = Fl(image=self.world_data['floor_img'],player=self.player,window=self.window,move=self.world_data['floor_move'],scale=self.world_data['floor_size']) if self.world_data['floor_img'] is not None else None


        #relating to advance sprite
        self.in_advance:bool = False #if true, will not update much besides the background and player

        #what boss the boss state pulls from
        self.curBossName = "ufo"

   
    
    def on_start(self,**kwargs):#__init__ v2, pretty much.
        #06/24/2023 - Playing the song
        audio.play_song(self.world_data["song"])
        self.player.sprite_groups = (self.sprites if not self.is_demo else self.demo_sprites)
        eBM()



    def on_end(self,**kwargs): #un-init, kind of
        pygame.mixer.music.stop()
        if tools.debug: print(self.debug.values())
        eBM()


    
    def update(self, draw=True):
        #Drawing previous gameplay frame to the window -- don't ask why, it just does. 
        if draw: self.fullwindow.blit(pygame.transform.scale(self.window,pygame.display.play_dimensions_resize),pygame.display.play_pos)


        #Updating backgrounds - drawing to window
        self.background.update()
        self.background.draw(self.window)
        if self.floor is not None:
            self.floor.draw(self.window)
        self.formation.draw_img(window=self.window) #displaying a special formation image if necessary


        #updating all individual sprites, with the fourth group having special priority.
        (self.sprites if not self.is_demo else self.demo_sprites)[0].update()
        (self.sprites if not self.is_demo else self.demo_sprites)[1].update()
        (self.sprites if not self.is_demo else self.demo_sprites)[2].update()
        (self.sprites if not self.is_demo else self.demo_sprites)[0].draw(self.window)
        (self.sprites if not self.is_demo else self.demo_sprites)[1].draw(self.window)
        (self.sprites if not self.is_demo else self.demo_sprites)[2].draw(self.window)
        # (self.sprites if not self.is_demo else self.demo_sprites)[4].draw(self.window)

        #ending function early if event playing
        if self.event is not None and self.event.playing:
            self.event.update()
            return


        #only updating the formation after checking for events, to prevent the level starting beforehand.
        self.formation.update()

        #print debug positions
        for pos in self.debug[0]:
            self.window.blit(pygame.transform.scale(img["placeholder.bmp"],(10,10)),pos)

        

        #ending function early if advancing
        if self.in_advance: return 
        
        #calling collision
        self.collision()
        

        
        #06/18/2023 - Starting a new level
        if self.formation.cleared:
            #checking to start the advance state
            if self.level_in_world >= self.world_data["levels"]:
                self.next_state = "advance"
                return
            #checking to see if the next world should be a boss intermission -- does not update levels
            elif self.level_in_world + 1 in self.world_data['boss_levels']:
                self.next_state = "boss"
                self.curBossName = self.world_data['bosses'][self.world_data['boss_levels'].index(self.level_in_world + 1)]
                self.level_in_world += 1
                return
            #if not, updating everything
            else:
                self.level += 1
                self.level_in_world += 1
                self.formation.empty()
                
            #restarting the formation
            self.formation.__init__(
                world_data = self.world_data,
                level=self.level,
                level_in_world=self.level_in_world, 
                sprites=(self.sprites if not self.is_demo else self.demo_sprites),
                player=self.player,window=self.window,
                is_demo = self.is_demo)
            #restarting the new level event
            if self.event is not None: self.event.__init__(window=self.window,level=self.level)
        #08/21/2023 - Game Over - opening a new state if the player is dead
        if self.player.health <= 0:
            self.next_state = "gameover"



    def collision(self):
        #Detecting collision between players and enemies 
        collidelist=pygame.sprite.groupcollide((self.sprites if not self.is_demo else self.demo_sprites)[1],(self.sprites if not self.is_demo else self.demo_sprites)[2],False,False,collided=pygame.sprite.collide_mask)
        for key,value in collidelist.items():
            for item in value:
                key.on_collide(2,item)
                item.on_collide(1,key)



    def new_world(self):
        self.world += 1
        self.level_in_world = 0
        self.world_data = levels.fetch_level_info(campaign_world = (self.campaign,self.world))
        #changing bg
        self.background.__init__(self.world_data['bg'], resize = self.world_data['bg_size'], speed = self.world_data['bg_speed'])
        #changing floor
        self.floor = Fl(image=self.world_data['floor_img'],player=self.player,window=self.window,move=self.world_data['floor_move'],scale=self.world_data['floor_size']) if self.world_data['floor_img'] is not None else None


    def event_handler(self,event):
        if self.is_demo: return
        self.player.controls(event)
        #changing what comes next
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.next_state = "options","play"
            if event.key == pygame.K_ESCAPE:
                self.next_state = "pause"
            if tools.debug: 
                if event.key == pygame.K_b:
                    (self.sprites if not self.is_demo else self.demo_sprites)[0].add(
                        Em(
                            im=None,
                            coord=(random.randint(0,pygame.display.dimensions[0]),random.randint(0,pygame.display.dimensions[1])),
                            isCenter=True,animated=True,animation_resize=(random.randint(10,500),random.randint(10,500)),animation_killonloop=True
                    ))
                if event.key == pygame.K_4:
                    self.debug[0].pop(len(self.debug[0])-1)
                    self.debug[1].pop(len(self.debug[1])-1)
                if event.key == pygame.K_5:
                    print("@@@@@@@@@@@")
                    for item in self.formation.spawned_list:
                        print(item.info['state'])
                    print("@@@@@@@@@@@")
                if event.key == pygame.K_6:
                    self.formation.empty()
                    self.formation.finished = True
        if event.type == pygame.MOUSEBUTTONDOWN and tools.debug:
            pos = tuple(pygame.mouse.get_pos())
            pos = [pos[0]-pygame.display.play_pos[0],pos[1]-pygame.display.play_pos[0]]
            pos2 = [pygame.display.play_dimensions_resize[0]-pos[0],pos[1]]
            self.debug[0].append(pos)
            self.debug[1].append(pos2)
            print(pos,pos2)





#title screen
class Title(Template):
    emblems = {}
    emblems_perm = {}
    sprites=pygame.sprite.Group()

    def __init__(self,window:pygame.Surface,border): #Remember init is run only once, ever.
        self.window=window
        self.border=border
        self.next_state = None
        

        self.demo_state = Play(window = self.window, world = random.randint(0,6), level = random.randint(0,50), is_demo = True) #this is different from the tools.demo value, as this is just to simulate a player
        self.hiscoresheet = score.generate_scoreboard()

        #basic events that will occur during the title
        self.events = [
            "demo",
            "hiscore",
        ]
        self.event = 0
        self.timer = 0
        self.image_placements = {
            "welcome":(pygame.display.rect.width*0.01,pygame.display.rect.height*0.01),
            "else":(pygame.display.rect.width*0.01 + img["demo.png"].get_width() + pygame.display.rect.width*0.01 ,
                    pygame.display.rect.height*0.01),
        }
    
    
    def on_start(self):
        self.event = self.id = 0
        self.demo_state.__init__(window = self.window, world = random.randint(0,6), level = random.randint(0,50), is_demo = True)

    def on_end(self):...


    def update(self):
        
        #drawing
        self.window.blit(img['demo.png'],self.image_placements['welcome'])
        
        #demo
        if self.events[self.event] == 'demo':
            #updating and drawing
            self.demo_state.update(draw=False)
            self.window.blit(pygame.transform.scale(self.demo_state.window,(450,600)),self.image_placements['else'])
            #demo player controls
            event = pygame.event.Event(random.choice([pygame.KEYDOWN,pygame.KEYUP]), key = random.choice([pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT,pygame.K_z,pygame.K_x])) #create the event        
            #stopping constant movement
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                if event.key == pygame.K_LEFT: self.demo_state.player.momentum = self.demo_state.player.speed*-1 if not self.demo_state.player.movement[4] else self.demo_state.player.crouch_speed*-1
                else: self.demo_state.player.momentum = self.demo_state.player.speed if not self.demo_state.player.movement[4] else self.demo_state.player.crouch_speed
            else: self.demo_state.player.controls(event)
    
        #high score
        elif self.events[self.event] == 'hiscore':
            self.window.blit(self.hiscoresheet,self.image_placements['else'])

        #timer updating
        self.timer += 1
        if self.timer > 360:
            self.event = self.event + 1 if self.event + 1 < len(self.events) else 0
            self.timer = 0 
            



        


    def event_handler(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.next_state = "play"
            if event.key == pygame.K_ESCAPE:
                self.next_state = "quit"





# 08/08/2023 - THE GAME OVER STATE
# The game over state will use the gameplay state and modify it so everything slows down and the assets disappear and a graphic shows
class GameOver(Template):
    sprites=pygame.sprite.Group()
    def __init__(self,window,play_state):
        #08/08/2023 - PSEUDOCODE 
        # Remember, playstate has a separate surface that is drawn to the window, again, entirely separately. 
        # GameOverState will, animated-ly, blow up everything onscreen, then make the surface do a falling animation.
        # The separate surface is ignored from there on out. A game over graphic appears, which shows your score and how you did, before giving a rating.
        # Pressing enter brings you back to the main menu.
        self.next_state = None
        self.window = window
        self.play_state = play_state
        self.bg_multiplier = 0
        #timers
        self.timer = 0 #timer measurement
        self.events = [            
            120, #time until screen explodes
            360, #time until everything stops exploding, and shows your score
            1200, #time until high score is shown
            1500, #finishing high score
        ]
        self.events_func = [
            self.event0,
            self.event1,
            self.event2,
            self.event3,
            self.event4
        ]
        self.state = 0

        #event 1 explosion
        self.event1_ = [
            0, #angle transform
            0, #y momentum
            0, #y 
        ]

        #game over background
        self.background = Bg(img = "game_over_bg.png" , resize = [pygame.display.rect.width,pygame.display.rect.height], speed=[1.25,1], border_size=pygame.display.dimensions)        
        
        #needed to check for exit input
        self.exit_ok:bool = False

        #high score information
        self.name=""
        self.scoregraphic=Em(force_surf=score.generate_graphic(score.score,""),coord=(0,0),isCenter=True)

    def on_start(self):
        #kabooming the player 
        self.kaboom(coord=self.play_state.player.rect.center,animation_resize=(150,150),play=True)
        self.play_state.formation.start_state_leave()
        self.play_state.background.speed[1] *= 3
        self.bg_multiplier = self.play_state.background.speed[1] * 0.1
        



    def on_end(self):
        pygame.mixer.music.stop()

    def update(self):
        self.events_func[self.state]() #running each function

        #update the timer
        self.timer += 1
        if self.state<len(self.events) and self.timer >= self.events[self.state]:
            self.state += 1

        #updating any used sprites
        GameOver.sprites.update()
        GameOver.sprites.draw(self.window )


    def event0(self): #SLOWING EVERYTHING DOWN
        #the first state, which slows everything down
        #updating current state
        self.play_state.update()
        #changing bg
        self.play_state.background.speed[1] -= self.bg_multiplier
        self.bg_multiplier *= 1.025
    
    def event1(self): #BLOWING EVERYTHING UP
        if self.timer == 121: audio.play_song("gameover.mp3")
        self.play_state.update(draw=False)

        #shaking
        if self.timer < 180:
            self.window.blit(
                pygame.transform.scale(
                    self.play_state.window,pygame.display.play_dimensions_resize),
                    (pygame.display.play_pos[0]*random.uniform(0.7,1.3),pygame.display.play_pos[1]*random.uniform(0.7,1.3))
                    )
            if self.timer % 2 == 0:
                self.kaboom(animation_resize=(150,150),coord=(random.randint(0,pygame.display.dimensions[0]),random.randint(0,pygame.display.dimensions[1])))
    
        #Big explosion
        elif self.timer < 360:
            if self.timer == 181:
                self.event1_[1] = -30
                self.kaboom(
                    coord=(
                        pygame.display.play_pos[0]+(pygame.display.play_dimensions[0]/2),
                        pygame.display.play_pos[1]+(pygame.display.play_dimensions[1]/2)
                        ),animation_resize=(500,500))
                
            self.event1_[1] += 0.75
            self.event1_[2] += self.event1_[1]
            self.event1_[0] -= 1
            #falling window
            self.window.blit(
                pygame.transform.rotate(
                    pygame.transform.scale(self.play_state.window,pygame.display.play_dimensions_resize),
                    self.event1_[0]),
                (
                    pygame.display.play_pos[0],
                    (pygame.display.play_pos[1])+self.event1_[2])
                    )
            
            #kabooms
            if self.timer == 330 or self.timer == 340:
                self.kaboom(coord=(random.randint(0,pygame.display.dimensions[0]),random.randint(0,pygame.display.dimensions[1])),animation_resize=(random.randint(500,1000),random.randint(500,1000)))
            elif self.timer == 350:
                self.kaboom(coord=pygame.display.rect.center,animation_resize=(3000,3000))
            
            


    def event2(self):
        self.background.update()
        self.background.draw(window=self.window)

        #spawning in the game over logo
        if self.timer == 400:
            GameOver.sprites.add(Em(im="gameover.png",coord=(pygame.display.rect.center[0]*0.35,pygame.display.rect.center[1]*0.30),isCenter=True))
        #icons
        if self.timer == 500:
            GameOver.sprites.add(Em(im="gameover_score.png",coord=(pygame.display.rect.center[0]*0.35,pygame.display.rect.height*0.35),isCenter=True))
        if self.timer == 650:
            GameOver.sprites.add(Em(im="gameover_level.png",coord=(pygame.display.rect.center[0]*0.35,pygame.display.rect.height*0.45),isCenter=True))
        if self.timer == 800:
            GameOver.sprites.add(Em(im="gameover_rank.png",coord=(pygame.display.rect.center[0]*0.35,pygame.display.rect.height*0.90),isCenter=True))
        #numbers
        if self.timer == 530:
            GameOver.sprites.add(Em(force_surf = text.load_text(text=str(score.score),size=40) ,coord=(pygame.display.rect.center[0]*0.75,pygame.display.rect.height*0.32),isCenter=False))
        if self.timer == 680:
            GameOver.sprites.add(Em(force_surf = text.load_text(text=str(self.play_state.level),size=40),coord=(pygame.display.rect.center[0]*0.75,pygame.display.rect.height*0.42),isCenter=False,))
        #rank
        if self.timer == 830:
            GameOver.sprites.add(Em(force_surf = text.load_text(text=self.generate_rank(),size=40),coord=(pygame.display.rect.center[0],pygame.display.rect.height*0.90),isCenter=True,))
        
        #either high score screen or telling game to kill itself
        if self.timer == 1000:
            if self.got_high_score():
                self.timer = 1200
                GameOver.sprites.empty()
                self.kaboom(coord=pygame.display.rect.center,animation_resize=(3000,3000))
                return
            else:
                sp = Em(im="gameover_return.png",coord=(pygame.display.rect.width*0.75,pygame.display.rect.center[1]),isCenter=True)
                sp.pattern="sine"
                GameOver.sprites.add(sp)
                self.exit_ok = True

        if self.timer > 1190:
            self.timer = 1001
        


    def event3(self):
        self.background.update()
        self.background.draw(window=self.window)

        if self.timer == 1201:
            #speeding up bg
            self.background.speed=[-7,-7]
            #high score image 
            sp = Em(im="hiscore.png",coord=(pygame.display.rect.center[0]*0.35,pygame.display.rect.center[1]*0.30),isCenter=True)
            sp.pattern = "jagged";GameOver.sprites.add(sp)
        if self.timer == 1260:
            #showing the high scores, showing yours, and telling you to input
            GameOver.sprites.add(
                Em(force_surf=score.scoreboard,coord=(pygame.display.rect.width*0.75,pygame.display.rect.height*0.5),isCenter=True)
            )
            #scoregraphic
            GameOver.sprites.add(self.scoregraphic)
            self.scoregraphic.change_pos(pos=(pygame.display.rect.width*0.25,pygame.display.rect.height*0.4),isCenter=True)
            #telling you
            x = Em(im="hiscore_name.png",coord=(pygame.display.rect.width*0.25,pygame.display.rect.height*0.5),isCenter=True) ; x.pattern = "sine"
            GameOver.sprites.add(x)
        #stopping it from advancing if you don't enter your name in time
        if self.timer >= 1490 and self.timer < 1500: self.timer = 1300

    
    def event4(self):
        if self.timer == 1501:
            GameOver.sprites.empty()
            self.kaboom(coord=pygame.display.rect.center,animation_resize=(1000,1000))
            #updating the new scoreboard
            score.scores = score.add_score(score=score.score,name=self.name,scores=score.scores)
            score.scoreboard = score.generate_scoreboard()
            GameOver.sprites.add(Em(force_surf=score.scoreboard,coord=pygame.display.rect.center,isCenter=True))

        if self.timer >= 1740:
            self.finish()

    def event_handler(self,event):
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_z or event.key == pygame.K_x) and (self.exit_ok):
                self.finish()
            if self.state == 3:
                if event.key == pygame.K_BACKSPACE:
                    self.hiscore_updatename(backspace=True)
                elif event.key == pygame.K_RETURN:
                    self.timer = 1500 #finishing it all off
                else:
                    self.hiscore_updatename(pygame.key.name(event.key))



    def generate_rank(self) -> str:
        #makes a rank value and gives you a set of ranks based off of it
        rank_val = score.score * (1 + 0.01*self.play_state.world) * (1+(0.01*self.play_state.level))
        ranks = {
            0:("so bad its a joke",), #joke 
            1000:("horrible",), #horrible
            5000:("bad",), #bad
            10000:("not bad but not good",), #not good
            50000:("mid",), #mid
            100000:("ok",), #ok
            250000:("good",), #good 
            500000:("great",), #great (shitpost)
            1000000:("amazing",), #amazing
            2500000:("cracked",), #cracked 1
            7500000:("crackeder",), #cracked 2
            10000000:("crackedest",), #cracked 3
            999999999:("holy hell",) #holy shit
        }
        #figuring out what rank to put you into
        rank_key=None
        for val in ranks.keys():
            if rank_val >= val:
                rank_key = int(val)
            else:
                break
        #giving the rank
        rank = random.choice(ranks[rank_key])
        return rank

    def got_high_score(self) -> bool: #it says if you got a high score or not
        if score.score > score.scores[0][1]: return True
        else: return False

    def hiscore_updatename(self,text:str="",backspace:bool=False):
        if backspace and len(self.name) > 0: 
            tempname = list(self.name)
            tempname[len(tempname)-1] = ''
            self.name = ''
            self.name.join(tempname)
        else: self.name += (text.upper() if text.upper() != "SPACE" else " ")
        self.scoregraphic.autoimage.image = score.generate_graphic(score.score,self.name)



        
    def kaboom(self,coord:tuple,animation_resize:tuple,play:bool=False,): #because kaboom happens so much
            (GameOver.sprites if not play else self.play_state.sprites[0]).add(
            Em(
                im="kaboom",
                coord=coord,
                isCenter=True,
                animation_killonloop=True,
                resize=animation_resize
                ))

    def finish(self):
        #the finishing part
        GameOver.sprites.empty()
        score.score = 0
        self.play_state.__init__(
            window=self.play_state.fullwindow,
            is_restart=True
        )
        self.__init__(window=self.window,play_state=self.play_state)
        score.save_scores(scores=score.scores)
        self.next_state="title"





#paused
class Pause(Template):
    def __init__(self,window:pygame.Surface,play_state):
        
        self.next_state = None #Needed to determine if a state is complete
        self.return_state = "play"
        self.play_state = play_state
        self.window = window
        self.bg = play_state.window
        self.logo_pos:list = [0,0] #[frames_in,y_pos] 
        self.bgpos = pygame.display.play_pos[0] + 35 , pygame.display.play_pos[1] + 38

    def on_start(self,**kwargs): #__init__ v2, pretty much.
        audio.play_song("kurosaki.mp3")
        if 'return_state' in kwargs.keys(): self.return_state = kwargs['return_state']
    def on_end(self,**kwargs): #un-init, kind of
        pygame.mixer.music.stop()

    def update(self):
        #displaying of all the pause graphics and such - likely heavily unoptimized.
        self.bg.blit(img["paused.png"],(0,0))
        self.bg.blit(img["paused.png"],(0,600))
        self.window.blit(pygame.transform.scale(img["pauseborder.png"],pygame.display.play_dimensions_resize),pygame.display.play_pos)
        self.window.blit(pygame.transform.scale(self.bg,(390,270)),self.bgpos)

    def event_handler(self,event):
        #changing what comes next
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.next_state = "options","pause"
            if event.key == pygame.K_q:
                self.next_state = "title"
                self.play_state.__init__(
                    window=self.play_state.fullwindow,
                    is_restart=True
                )
            if event.key == pygame.K_ESCAPE:
                self.next_state = self.return_state





#when a world is completed
class Advance(Template):
    sprites=pygame.sprite.Group()
    def __init__(self,window,play_state):
        #setting values
        self.window = window
        self.play_state = play_state
        self.frames = 0
        self.next_state = None
        
    def on_start(self):
        #startup
        self.frames = 0 
        self.play_state.player.aimg.change_anim("yay")
        self.play_state.player.reset_movement()
        self.play_state.in_advance = True #stopping play_state from doing weird shit

    def on_end(self):
        self.frames = 0
        self.play_state.player.aimg.change_anim("idle")
        self.play_state.in_advance = False #letting play_state be goofy again

    def update(self):
        self.frames += 1
        #adding some emblems for now, will update to be better later
        if self.frames==1: Advance.sprites.add(Em(im="levelcomplete.png",coord=(pygame.display.play_dimensions_resize[0]/2+pygame.display.play_pos[0],pygame.display.play_dimensions_resize[1]*0.25+pygame.display.play_pos[1]),isCenter=True,pattern="jagged"))
        #speeding everything up
        if self.frames < 150:
            for i in range(2):
                if self.play_state.background.speed[i] <= 150:
                    self.play_state.background.speed[i] *= 1.05
        #changing the play_state stored world
        if self.frames == 150:
            Advance.sprites.empty()
            self.play_state.new_world()
            self.kaboom(
                coord=(pygame.display.play_dimensions_resize[0]/2+pygame.display.play_pos[0],pygame.display.play_dimensions_resize[1]/2+pygame.display.play_pos[1]),
                animation_resize=(500,500))
        #ending
        if self.frames > 300:
            self.next_state = "play"

        self.play_state.player.invincibility_counter = 60

        self.play_state.update()

        Advance.sprites.update()
        Advance.sprites.draw(self.window)



    def event_handler(self,event):
        pass    
    
    def kaboom(self,coord:tuple,animation_resize:tuple,play:bool=False,): #because kaboom happens so much
            (Advance.sprites if not play else self.play_state.sprites[0]).add(
            Em(
                im='kaboom',
                coord=coord,
                isCenter=True,
                animation_killonloop=True,
                resize=animation_resize
                ))





#same as gameplay but there is now a boss involved
class Boss(Template):
    sprites = {
        0:pygame.sprite.Group(), #other
        1:pygame.sprite.Group(), #player sprite
        2:pygame.sprite.Group(), #boss's sprites
    }
    def __init__(self,play_state:Play):
        Template.__init__(self)
        #Bosses do a majority of what playstate does, except instead of a formation being in place there is a boss.
        #Due to this, there is a new set of sprite groups: player, boss, and bullet
        #Mostly everything is super simplified. 
        self.playstate = play_state
        self.is_demo = self.playstate.is_demo

        self.window = self.playstate.window
        self.fullwindow = self.playstate.fullwindow
        
        self.player = self.playstate.player

        self.background = self.playstate.background
        self.floor = self.playstate.floor

        self.playstate.curBossName="sun"
        self.boss = enemies_bosses.loaded[self.playstate.curBossName](sprites=Boss.sprites,player=self.player,window=self.playstate.window,state=self)

    def on_start(self):
        audio.play_song('twisted_inst.mp3' if self.playstate.curBossName == "crt" else "golden_inst.mp3")
        
        #killing all previous sprites
        eBM()
        for group in Boss.sprites.values():
            group.empty()

        #player code
        self.player.sprite_groups = Boss.sprites
        Boss.sprites[1].add(self.player)

        #redoing what was done in __init__
        self.__init__(play_state = self.playstate)


    def on_end(self):
        eBM() #emptying bullet max
        pygame.mixer.music.stop()
        for group in Boss.sprites.values():
            group.empty()


    def update(self,draw=True): 
        for sprite in self.sprites[0]:pygame.draw.rect(self.window, 'blue', sprite.rect, width=3)
        #     pygame.draw.rect(self.window, 'black', sprite.mask.get_rect(), width=1)

        for sprite in self.sprites[1]:pygame.draw.rect(self.window, 'green', sprite.rect, width=3)
        #     pygame.draw.rect(self.window, 'black', sprite.mask.get_rect(), width=1)

        for sprite in self.sprites[2]:pygame.draw.rect(self.window, 'red', sprite.rect, width=3)
        #     pygame.draw.rect(self.window, 'blue', sprite.mask.get_rect(), width=1)


        #Drawing previous gameplay frame to the window -- don't ask why, it just does. 
        if draw: self.fullwindow.blit(pygame.transform.scale(self.window,pygame.display.play_dimensions_resize),pygame.display.play_pos)

        

        #updating backgrounds
        self.background.update()
        self.background.draw(self.window)
        #updating floor
        if self.floor is not None:
            self.floor.update()
            self.floor.draw(self.window)
        #updating all 
        Boss.sprites[1].update()
        Boss.sprites[2].update()
        Boss.sprites[0].update()
        #updating boss
        self.boss.update()
        #draw
        Boss.sprites[2].draw(self.window)
        Boss.sprites[1].draw(self.window)
        Boss.sprites[0].draw(self.window)

        #collision
        self.collision()
        #death - somewhat broken atm
        if self.player.dead:
            self.next_state = "gameover"
        #figuring out what to do when the boss dies
        elif self.boss.info['ENDBOSSEVENT']:
            self.next_state = "play" if not self.boss.info['ENDWORLD'] else 'advance'

    def event_handler(self,event):
        self.player.controls(event)
        #changing what comes next
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.next_state = "options","boss"
            if event.key == pygame.K_ESCAPE:
                self.next_state = "pause","boss"


    def collision(self):
        #between player and enemy
        collidelist=pygame.sprite.groupcollide(
            Boss.sprites[1],
            Boss.sprites[2],
            False,False,collided=pygame.sprite.collide_mask)
        #telling the assets that stuff collided
        for key,value in collidelist.items():
            for item in value:
                key.on_collide(2,item)
                item.on_collide(1,key)
        


