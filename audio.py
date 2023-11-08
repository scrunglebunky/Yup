import pygame,json
DISABLED = False
try:
    pygame.mixer.init()
    pygame.mixer.set_num_channels(32)
except:
    DISABLED = True

songs = []
sounds = {}

"""CHANNEL RESERVATIONS 
0 - enemy death
1 - bullet noises
2 - player movement noises
"""

type_channels = {}
PATH_songs:str = "./songs/"
PATH_sounds:str = "./sounds/"
directory:str = "./data/audio_loadlist.json"

#06/24/2023 - LOADING ALL SONGS
# the game will load all of the audio files and play them as needed
# there are some bugs that cause the sounds not to be able to play, or even load, so I will make a boolean that can disable all sounds in general
def load_all_songs():
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
            songs.append(song)
        except:
            DISABLED = True
            return

def play_sound(name,category:str = None,channel:int = None):
    if not DISABLED and name in sounds.keys():
        if category in type_channels.keys():
            pygame.mixer.Channel(type_channels[category]).play(sounds[name])
        elif type(channel) == int:
            pygame.mixer.Channel(channel).play(sounds[name])
        else:
            sounds[name].play()
        
def play_song(name):
    if not DISABLED and name in songs: 
        pygame.mixer.music.load(PATH_songs+name)
        pygame.mixer.music.play(loops=-1)

def change_volumes(ostvol:float = None, soundvol:float = None):
    if ostvol != None:
        pygame.mixer.music.set_volume(ostvol)
    if soundvol != None:
        for sound in sounds.values():
            sound.set_volume(soundvol)


load_all_songs()

