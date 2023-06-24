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

        #06/22/2023 - POSITIONING FOR LOGO
        # the logo is big and needs positioning 
        self.logo = anim.all_loaded_images['logo.png']
        self.logo_coord = (
            ((self.UI_rect.width*0.75) - (self.logo.get_width()/2)),
            pygame.display.dimensions[1]*0.15 - (self.logo.get_height()/2)
        )

        #06/22/2023 - Animation booleans / setting spritesheet info
        self.anim_bg:bool = anim_bg
        self.anim_logo:bool = anim_logo
        self.animated = self.anim_bg and self.anim_logo

    def draw(self,window:pygame.Surface):
        window.blit(self.UI_img,self.UI_rect)
        window.blit(self.logo,self.logo_coord)

    def update(self):
        if not self.animated: return 
