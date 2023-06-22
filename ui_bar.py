#CODE BY ANDREW CHURCH
import pygame,anim


#06/22/2023 - UI BAR CLASS
# The UI bar is something used by playstate to display things such as the score, background image, and logo.

class UIBar():
    def __init__(self):
        #06/03/2023 - UI - Making a separate brick to the right with highest graphical priority used as a backgorund for the UI
        self.UI_art = "uibox.png"
        self.UI_rect = pygame.Rect(
            pygame.display.play_dimensions[0],
            0,
            (pygame.display.get_window_size()[0]-pygame.display.play_dimensions[0]),
            pygame.display.get_window_size()[1]
            )
        self.UI_img = pygame.Surface(((pygame.display.get_window_size()[0]-pygame.display.play_dimensions[0]),pygame.display.get_window_size()[1] ))
        self.UI_img.blit(
            pygame.transform.scale(anim.all_loaded_images[self.UI_art],(self.UI_rect[2],self.UI_rect[3])),
            (0,0))

        #06/22/2023 - POSITIONING FOR LOGO
        # the logo is big and needs positioning 
        self.logo = anim.all_loaded_images['logo.png']
        self.logo_coord = (
            pygame.display.play_dimensions[0] + ((self.UI_rect.width/2) - (self.logo.get_width()/2)),
            pygame.display.dimensions[1]*0.15 - (self.logo.get_height()/2)
        )

    def draw(self,window:pygame.Surface):
        window.blit(self.UI_img,self.UI_rect)
        window.blit(self.logo,self.logo_coord)