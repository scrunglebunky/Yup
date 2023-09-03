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



#5/30/2023 - TEXT SPRITE
# The text sprite is ripped from Rev C and edited.
# It's pretty much just an text sprite that flies around and whatnot


def load_text(
    text: str = "WOW!",
    size: int = 20,  # resizable ; if None, no resize
    resize: tuple = None, #if resize
    font: str = "./data/font.ttf",  # the font ; could also be SetFont
    fg: str = "white",  # foreground color
    bg: str = "black",  # background color
    add_to_loaded:bool = True #if the text should be added to the loaded_text thing to be used later
    ):
        # Setting the image, if it is loaded
        if text in loaded_text.keys():
            image = loaded_text[text]
        # setting the image if it is not loaded
        else:
            image = pygame.font.Font(font, size).render(
                str(text), True, fg, bg
            )
            if add_to_loaded: loaded_text[text] = image
        # resizing image
        if resize is not None:
            image = pygame.transform.scale(
                image, (resize[0], resize[1])
            )
        return image
