#CODE BY ANDREW CHURCH
import pygame,anim


#06/22/2023 - UI BAR CLASS
# The UI bar is something used by playstate to display things such as the score, background image, and logo.

class Border():
    def __init__(self,
        anim_bg:bool = False,
        anim_logo:bool = False,
        UI_art:str = "uibox.png",
        ):
        #06/03/2023 - UI - Making a separate brick to the right with highest graphical priority used as a backgorund for the UI
        self.UI_art = UI_art
        self.UI_rect = pygame.Rect(0,0,pygame.display.dimensions[0],pygame.display.dimensions[1])
        self.UI_img = pygame.Surface(pygame.display.dimensions)
        self.UI_img.blit(pygame.transform.scale(anim.all_loaded_images[self.UI_art],(self.UI_rect[2],self.UI_rect[3])),(0,0))


        #06/24/2023 - ADDING EXTRA EMBLEMS
        self.emblems = [ 
            ( #LOGO EMBLEM
                'logo.png',
                (
                    pygame.display.dimensions[0] - ( pygame.display.dimensions[0] - (pygame.display.play_dimensions[0] + pygame.display.play_pos[0])),
                    pygame.display.dimensions[1]*0.15 - (anim.all_loaded_images['logo.png'].get_height()/2)
                )
                
            ),
            ( #SCORE EMBLEM
                "score.png", 
                (
                    pygame.display.play_dimensions[0] + pygame.display.play_pos[0] + 25,
                    240
                )
            ),
            ( #DEBUG EMBLEM
                "debug.png", 
                (
                    pygame.display.play_dimensions[0] + pygame.display.play_pos[0] + 25,
                    320
                )
            ),
            ( #DEBUG EMBLEM
                "lives.png", 
                (
                    10,
                    pygame.display.dimensions[1] - anim.all_loaded_images['lives.png'].get_height() - 10
                )
            )

        ]

        #06/22/2023 - Animation booleans / setting spritesheet info
        self.anim_bg:bool = anim_bg
        self.anim_logo:bool = anim_logo
        self.animated = self.anim_bg and self.anim_logo

    def draw(self,window:pygame.Surface):
        window.blit(self.UI_img,self.UI_rect)
        for emblem in self.emblems:
            window.blit(anim.all_loaded_images[emblem[0]],emblem[1])

    def update(self):
        if not self.animated: return 
