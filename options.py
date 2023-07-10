## CODE BY ANDREW CHURCH
import json

#07/04/2023 - ADDING OPTIONS MENU
# The options menu is going to iterate through everything in the settings dictionary and let people modify it with the menu buttons

#06/30/2023 - LOADING IN THE CONFIGURATION FILE
# The config.json file is a dictionary containing info about how the game works
# This file is needed, though there is a default dictionary held here 
# This is held in the options file instead of MAIN, so all items can access it
default_settings = {
    "fullscreen":["switch",False],

    "mute":["switch",False],
    "music_vol":["knob",0.5,0.05],
    "sound_vol":["knob",0.5,0.05],

    "screen_width":["knob",900,5],
    "screen_height":["knob",675,5],
    "gameplay_width":["knob",450,5],
    "gameplay_height":["knob",600,5]
}
# loading in the file
with open("./data/config.json","r") as set_raw:
    settings = json.load(set_raw)
del set_raw

print('loaded_options')

#SETTINGS (KNOB) INDEX MEANINGS:
# [type,current_setting,iteration_amount,min,max]




