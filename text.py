# ANDREW CHURCH - 2023
import pygame,math
pygame.font.init()

#5/30/2023 - START OF TEXT PROGRAMMING
# this is an asset I can use in a lot of different programs
# static text, flying text, classes, functions
# most of it relies on this "loaded text" dictionary, which stores the names of the values 
# any library of classified numbers (IE 'winning ranks' or 'numbers') are to be stored in their own list citing keys to the dictionary
loaded_text = {}


#5/30/2023 - LOADING NUMBERS
load_list = [".","-","+",0,1,2,3,4,5,6,7,8,9]
for num in load_list:
    loaded_text[str(num)] = pygame.font.Font("./data/font.ttf",30)
    loaded_text[str(num)] = loaded_text[str(num)].render(str(num),False,"white","black")

#5/31/2023 - LOADING NUMBERS   
# pretty much it opens a file and loads all items inside
with open("./data/text.txt","r") as file:
    load_list = file.read().split(",")
for item in load_list:
    loaded_text[str(item)] = pygame.font.Font("./data/font.ttf",30)
    loaded_text[str(item)] = loaded_text[str(item)].render(str(item),False,"white","black")


#5/30/2023 - DISPLAY_NUMBERS
# There is separate function for displaying numbers because I'm not gonna store several numbers as their own stupid variables, as that would take up too much RAM
# What it does here, instead, is split the number into each individual digit and displays them separately 
def display_numbers(num:int,pos:tuple,window:pygame.display,reverse:tuple = False):
    num = str(num) if not reverse else str(num)[::-1]
    width = loaded_text["8"].get_width() #made width one process to save a sliver of processor space
    for i in range(len(num)):
        window.blit(loaded_text[num[i]],(
            ( (pos[0]+(width*i)) if not reverse else (pos[0]-(width*(i+1)) ) ,
            pos[1]
            )))


#5/31/2023 - LOADING NUMBERS   
# pretty much it opens a file     
def display_text(text:str,pos:tuple,window:pygame.display):
    if text not in loaded_text.keys():
        loaded_text[str(text)] = pygame.font.Font("./data/font.ttf",30)
        loaded_text[str(text)] = loaded_text[str(text)].render(str(text),False,"black","white")
    else:
        window.blit(loaded_text[str(text)],pos)


#5/30/2023 - TEXT SPRITE
# The text sprite is ripped from Rev C and edited.
# It's pretty much just an text sprite that flies around and whatnot


def load_text(
    text: str = "WOW!",
    pattern: str = "static",  # pattern, random.choice( [ "static", "linear", "sine", "squared" ] )
    duration: str = -1,  # how many frames the item should last for. -1 equals infinity
    size: int = None,  # resizable ; if None, no resize
    font: str = "./data/font.ttf",  # the font ; could also be SetFont
    fg: str = "white",  # foreground color
    bg: str = "black",  # background color
    pos: tuple = (0, 0),  # where item is placed, or the vertex of the function
    vertex: tuple = (0, 0),  # used for sine and squared
    modifier: int = 1,  # slope, sine vertical stretch, etc
    modifier2: int = 1,  # sine horizontal stretch, idk what else
    speed: int = 1,  # self explanatory - vertical movement
    ):
        # Setting the image, if it is loaded
        if text in loaded_text.keys():
            self.image = loaded_text[text]
        # setting the image if it is not loaded
        else:
            loaded_text[text] = pygame.font.Font(font, 20).render(
                str(text), True, fg, bg
            )
            image = loaded_text[text]
        # resizing image
        if size is not None:
            image = pygame.transform.scale(
                image, ((size // 2) * len(text), size)
            )
        return image

class Text(pygame.sprite.Sprite):
    possible_patterns = ["static", "linear", "sine", "squared", "static sine"]
    screen_rect = pygame.Rect(0, 0, 450, 600)

    def __init__(
        self,
        text: str = "WOW!",
        pattern: str = "static",  # pattern, random.choice( [ "static", "linear", "sine", "squared" ] )
        duration: str = -1,  # how many frames the item should last for. -1 equals infinity
        size: int = None,  # resizable ; if None, no resize
        font: str = "./data/font.ttf",  # the font ; could also be SetFont
        fg: str = "white",  # foreground color
        bg: str = "black",  # background color
        pos: tuple = (0, 0),  # where item is placed, or the vertex of the function
        vertex: tuple = (0, 0),  # used for sine and squared
        modifier: int = 1,  # slope, sine vertical stretch, etc
        modifier2: int = 1,  # sine horizontal stretch, idk what else
        speed: int = 1,  # self explanatory - vertical movement
    ):
        pygame.sprite.Sprite.__init__(self)

        # FIXING PATTERN
        self.pattern = (
            "static"
            if pattern not in Text.possible_patterns or pattern == "static"
            else pattern
        )

        # IMAGE REGISTRATION
        if text in loaded_text.keys():
            # if the image is loaded
            self.image = loaded_text[text]
        else:
            # if the image is not loaded
            print("TEXT NOT PRESENT, ADDING...")
            loaded_text[text] = pygame.font.Font(font, 20).render(
                str(text), True, fg, bg
            )
            self.image = loaded_text[text]
        # resizing image
        if size is not None:
            self.image = pygame.transform.scale(
                self.image, ((size // 2) * len(text), size)
            )
        self.rect = self.image.get_rect()

        # positioning image
        self.rect.center = pos

        # turning around if wrong way
        if (pos[0] < 0 and speed < 0) or (pos[0] > 450 and speed > 0):
            speed *= -1
        # making class items
        self.pos, self.vertex = pos, vertex
        self.modifier, self.modifier2 = modifier, modifier2
        self.speed = speed

        # counting up
        self.counter = 0 if duration >= 0 else -2
        self.duration = duration

    def update(self):

        #main update
        self.counter += 1

        #kill code
        if (self.counter >= 60 and not self.on_screen()) or (
            (self.duration != -1) and (self.counter >= self.duration)
        ):
            # print("ded")
            self.kill()


        # no movement
        if self.pattern == "static":
            return
        
        # sine in-place
        elif self.pattern == "static sine":
            # print(self.counter)
            self.rect.center = (
                self.rect.center[0],
                # based off counter since this one doesn't move the x position
                (
                    self.modifier
                    * math.sin((self.modifier2 * (self.counter)) + self.vertex[0])
                )
                + self.vertex[1],
            )

        # sine moving
        elif self.pattern == "sine":
            self.rect.center = (
                self.rect.center[0] + self.speed,
                # based off x position since this one moves the x position
                (
                    self.modifier
                    * math.sin(
                        (self.modifier2 * (self.rect.center[0])) + self.vertex[0]
                    )
                )
                + self.vertex[1],
            )

        elif self.pattern == "slope":
            pass

        else:
            self.kill()

    def on_screen(self):
        return self.rect.colliderect(Text.screen_rect)
