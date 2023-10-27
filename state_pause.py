import pygame,text,math,anim
class State():
    def __init__(self,window:pygame.Surface,play_state):
        
        self.next_state = None #Needed to determine if a state is complete
        self.play_state = play_state
        self.window = window
        self.bg = play_state.window
        self.logo_pos:list = [0,0] #[frames_in,y_pos] 
        self.bgpos = pygame.display.play_pos[0] + 35 , pygame.display.play_pos[1] + 38

    def on_start(self,**kwargs):... #__init__ v2, pretty much.
    def on_end(self,**kwargs):... #un-init, kind of

    def update(self):
        #displaying of all the pause graphics and such - likely heavily unoptimized.
        self.bg.blit(anim.all_loaded_images["paused.png"],(0,0))
        self.bg.blit(anim.all_loaded_images["paused.png"],(0,600))
        self.window.blit(pygame.transform.scale(anim.all_loaded_images["pauseborder.png"],pygame.display.play_dimensions_resize),pygame.display.play_pos)
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
                self.next_state = "play"
