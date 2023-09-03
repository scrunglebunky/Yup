# Code by Andrew Church
import pygame,random,score,audio,text
from backgrounds import Background as Bg
from anim import all_loaded_images as img
from emblems import Emblem as Em
#08/08/2023 - THE GAME OVER STATE
# The game over state will use the gameplay state and modify it so everything slows down and the assets disappear and a graphic shows
class State():
    def __init__(self,window,sprites,play_state):
        #08/08/2023 - PSEUDOCODE 
        # Remember, playstate has a separate surface that is drawn to the window, again, entirely separately. 
        # GameOverState will, animated-ly, blow up everything onscreen, then make the surface do a falling animation.
        # The separate surface is ignored from there on out. A game over graphic appears, which shows your score and how you did, before giving a rating.
        # Pressing enter brings you back to the main menu.
        self.next_state = None
        self.window = window
        self.sprites = sprites
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
        self.background = Bg(img = "game_over_bg.png" , resize = (pygame.display.rect.width,pygame.display.rect.height), speed=[1.25,1], border_type = 1)        
        
        #needed to check for exit input
        self.exit_ok:bool = False

        #high score information
        self.name=""
        self.scoregraphic=Em(im=score.generate_graphic(self.play_state.data["score"],""),coord=(0,0),isCenter=True)

    def on_start(self):
        #kabooming the player 
        self.kaboom(coord=self.play_state.player.rect.center,animation_resize=(150,150),group=0)
        self.play_state.formation.start_state_leave()
        self.play_state.background.speed[1] *= 3
        self.bg_multiplier = self.play_state.background.speed[1] * 0.1
        



    def on_end(self):...
    def update(self):
        self.events_func[self.state]() #running each function

        #update the timer
        self.timer += 1
        if self.state<len(self.events) and self.timer >= self.events[self.state]:
            self.state += 1

        #updating any used sprites
        self.sprites[4].update()
        self.sprites[4].draw(self.window )


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
                self.kaboom(animation_resize=(150,150),coord=(random.randint(0,pygame.display.dimensions[0]),random.randint(0,pygame.display.dimensions[1])),group=0)
    
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
            self.sprites[4].add(Em(im=img["gameover.png"],coord=(pygame.display.rect.center[0]*0.35,pygame.display.rect.center[1]*0.30),isCenter=True))
        #icons
        if self.timer == 500:
            self.sprites[4].add(Em(im=img["gameover_score.png"],coord=(pygame.display.rect.center[0]*0.35,pygame.display.rect.height*0.35),isCenter=True))
        if self.timer == 650:
            self.sprites[4].add(Em(im=img["gameover_level.png"],coord=(pygame.display.rect.center[0]*0.35,pygame.display.rect.height*0.45),isCenter=True))
        if self.timer == 800:
            self.sprites[4].add(Em(im=img["gameover_rank.png"],coord=(pygame.display.rect.center[0]*0.35,pygame.display.rect.height*0.90),isCenter=True))
        #numbers
        if self.timer == 530:
            self.sprites[4].add(Em(im=None,coord=(pygame.display.rect.center[0]*0.75,pygame.display.rect.height*0.32),isCenter=False,
                numerical=True,number=self.play_state.data["score"],number_fontsize=40))
        if self.timer == 680:
            self.sprites[4].add(Em(im=None,coord=(pygame.display.rect.center[0]*0.75,pygame.display.rect.height*0.42),isCenter=False,
                numerical=True,number=self.play_state.level,number_fontsize=40))
        #rank
        if self.timer == 830:
            self.sprites[4].add(Em(im=None,coord=(pygame.display.rect.center[0],pygame.display.rect.height*0.90),isCenter=True,
                numerical=True,number=self.generate_rank(),number_fontsize=40))
        
        #either high score screen or telling game to kill itself
        if self.timer == 1000:
            if self.got_high_score():
                self.timer = 1200
                self.sprites[4].empty()
                self.kaboom(coord=pygame.display.rect.center,animation_resize=(3000,3000))
            else:
                sp = Em(im=img["gameover_return.png"],coord=(pygame.display.rect.width*0.75,pygame.display.rect.center[1]),isCenter=True)
                sp.pattern="sine"
                self.sprites[4].add(sp)
                self.exit_ok = True
        


    def event3(self):
        self.background.update()
        self.background.draw(window=self.window)

        if self.timer == 1201:
            #speeding up bg
            self.background.speed=[-7,-7]
            #high score image 
            sp = Em(im=img["hiscore.png"],coord=(pygame.display.rect.center[0]*0.35,pygame.display.rect.center[1]*0.30),isCenter=True)
            sp.pattern = "jagged";self.sprites[4].add(sp)
        if self.timer == 1260:
            #showing the high scores, showing yours, and telling you to input
            self.sprites[4].add(
                Em(im=score.scoreboard,coord=(pygame.display.rect.width*0.75,pygame.display.rect.height*0.5),isCenter=True)
            )
            #scoregraphic
            self.sprites[4].add(self.scoregraphic)
            self.scoregraphic.change_pos(pos=(pygame.display.rect.width*0.25,pygame.display.rect.height*0.4),isCenter=True)
            #telling you
            x = Em(im=img["hiscore_name.png"],coord=(pygame.display.rect.width*0.25,pygame.display.rect.height*0.5),isCenter=True) ; x.pattern = "sine"
            self.sprites[4].add(x)
        #stopping it from advancing if you don't enter your name in time
        if self.timer >= 1490 and self.timer < 1500: self.timer = 1300

    
    def event4(self):
        if self.timer == 1501:
            self.sprites[4].empty()
            self.kaboom(coord=pygame.display.rect.center,animation_resize=(1000,1000))
            #updating the new scoreboard
            score.scores = score.add_score(score=self.play_state.data['score'],name=self.name)
            score.scoreboard = score.generate_scoreboard()
            self.sprites[4].add(Em(im=score.scoreboard,coord=pygame.display.rect.center,isCenter=True))

        if self.timer >= 1740:
            #the finishing part
            for i in range(len(self.sprites)):self.sprites[i].empty()
            self.play_state.data["score"] = 0
            self.play_state.__init__(
                data=self.play_state.data,
                sprites=self.sprites,
                window=self.play_state.fullwindow,
                is_restart=True
            )
            score.save_scores()
            self.next_state="title"

    def event_handler(self,event):
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_z or event.key == pygame.K_x) and (self.exit_ok):
                self.next_state = "title"
                self.sprites[4].empty()
            if self.timer >= 1260:
                if event.key == pygame.K_BACKSPACE:
                    self.hiscore_updatename(backspace=True)
                elif event.key == pygame.K_RETURN:
                    self.timer = 1500 #finishing it all off
                else:
                    self.hiscore_updatename(pygame.key.name(event.key))



    def generate_rank(self) -> str:
        #makes a rank value and gives you a set of ranks based off of it
        rank_val = self.play_state.data["score"] * (0.5*self.play_state.world) * (1+(0.01*self.play_state.level))
        ranks = {
            0:("WHAT THE FUCK YOU SUCK", "HOW DO YOU HAVE A SCORE OF 0","YOU WILL DIE ALONE","KILL YOURSELF","ZERO???????"), #joke 
            1000:("THERE WAS AN ATTEMPT", "pathetic", "PATHETIC, TRULY PATHETIC", "YOU'RE BAAAAD", "PRESS THE BUTTONS TO DO STUFF","SCHTINKY"), #horrible
            5000:("bad,bad,bad,bad,bad","you kinda suck","uwu ur bad","not horrendous but not good either", "I LOVE DRUGS"), #bad
            10000:("SWAGSHIT-MONEYMONEY","pm sucks","FIRST TIME?","YUP MORE LIKE... FUCKING STUPID LMAO"), #not good
            50000:("WHAT","kinda mid ngl","YOU PROBABLY DRINK WHITE MONSTER","FEMBOY PLAYIN ASS","HARDCORE PLAYER MORE LIKE MIDCORE MIDDER HAHAHA"), #mid
            100000:("WHEN","ok","better than mid ig","WOOOOOW DUDE YOU SUCK ASS (nah jk)","Not Bad!","cellular redistribution","UNDERGO MITOSIS NOW"), #ok
            250000:("WHO","hey you're pretty good at this","WOW YOU'RE OK AT THIS","sweat much?","STOP TRYING SO HARD","give up"), #good 
            500000:("I HATE   EARTH DAY", "KILL THE HOMELESS", "SHITPOST RANK", "DOUBLE DOG DOGSHIT","PLAY AGAIN IF YOU'RE RACIST","QUIT IF YOU'RE RACIST","mid, mid mid mid"), #great (shitpost)
            1000000:("this is actually the worst rank you can get, i can't believe you're so bad at the game kill yourself","ONE MILLION RANKS","WHERE","YOU'RE FUCKING GOOD AT THE GAME I GET IT"), #amazing
            2500000:("YOU'RE CRACKED","no rank","how","STOP PLAYING GOOD IT'S MAKING ME JEALOUS"), #cracked 1
            7500000:("YOU'RE CRACKEDER","gay"), #cracked 2
            10000000:("YOU'RE CRACKEDERER","cringe ass naenae rank"), #cracked 3
            999999999:("HOLY SHIT","WHAT THE FUCK","YOU'RE CHEATING","STOP DOING THIS SHIT","STOP CHEATING GODDAMN","YOU'RE CRACKEDEST","NO PM STUDENT WILL GET THIS RANK","cisgender") #holy shit
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
        if self.play_state.data["score"] > score.scores[0][1]: return True
        else: return False

    def hiscore_updatename(self,text:str="",backspace:bool=False):
        if backspace and len(self.name) > 0: 
            tempname = list(self.name)
            tempname[len(tempname)-1] = ''
            self.name = ''
            self.name.join(tempname)
        else: self.name += (text.upper() if text.upper() != "SPACE" else " ")
        self.scoregraphic.image = score.generate_graphic(self.play_state.data["score"],self.name)



        
    def kaboom(self,coord:tuple,animation_resize:tuple,group:int=4): #because kaboom happens so much
        self.sprites[group].add(
            Em(
                im=None,
                coord=coord,
                isCenter=True,
                animated=True,
                animation_resize=animation_resize, 
                animation_killonloop=True,
                ))
