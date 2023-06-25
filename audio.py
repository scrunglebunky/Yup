import pygame,json
pygame.mixer.init()

songs = []
sounds = {}

DISABLED = False

type_channels = {}

#06/24/2023 - LOADING ALL SONGS
# the game will load all of the audio files and play them as needed
# there are some bugs that cause the sounds not to be able to play, or even load, so I will make a boolean that can disable all sounds in general
def load_all_songs(directory:str = "./data/audio_loadlist.json",PATH_songs:str = "./songs/", PATH_sounds:str = "./sounds/"):
    # opening file 
    with open(directory,"r") as raw:
        load_list = json.load(raw)

    # loading sounds
    for sound in load_list["sounds"]:
        try:
            sounds[sound] = pygame.mixer.Sound(file=(str(PATH_sounds)+str(sound)))
        except:
            DISABLED = True
            return

    # loading songs
    for song in load_list["songs"]:
        try:
            pygame.mixer.Sound(file = (str(PATH_songs) + str(song)))
        except:
            DISABLED = True
            return

def play_sound(name,category:str = None,channel:int = None):
    if not DISABLED:
        if category in type_channels.keys():
            pygame.mixer.Channel(type_channels[category]).play(sounds[name])
        elif type(channel) == int:
            pygame.mixer.Channel(channel).play(sounds[name])
        else:
            sounds[name].play()
        
    

load_all_songs()

