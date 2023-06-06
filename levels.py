#PROGRAM BY ANDREW CHURCH, STARTED 5/31/2023
# mostly pulled from previous revision

import os,json,random

"""DOCSTRING - GUIDE ON WHAT LEVEL LEVEL ASSETS ARE WHAT
- world_name: just for display
- ui_type: unused
- song: song to be played

- bg: image of bg used
- bg_size: resizing of bg, none defaults to the playfield area
- bg_speed: movement of the background, in x,y format
- bg_speed_changes: a list of movements in speed based on level ; [type_of_time,time,speed]; types of time: 'level','frames'

- levels: how long the world lasts

- char_distance_x : distance between characters in width
- char_distance_y : same but in height
- char_min_width: minimum amount of columns allowed in random generation
- char_min_height: same but with rows
- char_max_width: maximum amount of columns allowed in random generation
- char_max_height: same but with rows

- throwdown_time: amount of frames before a character is sent down to attack
- throwdown_time: amount of characters to be thrown out when a character is sent to be attacked
- spawn_time: how quickly the formation spawns characters in the startup state
- max_char: maximum amount of characters allowed to be sent out at a time
- dynamic_intensity: if the intensity values should be sent through update_intensities, which then ignores the preset values
- form_drop_speed: how quickly the formation should swoop down to kill you if you take too long 
- manual_intensity_changes: changing the intensities based on levels manually ; level,spawn_time,spawn_amount,max_char ; note these have to be put in order by level, or the game will bug out because of how JSON files work

- imports: what characters are used during random generation ; bypassed with manual formations
- bullets: what bullet drops are given
- drop_health: how many levels it takes for a health box to be dropped
- drop_bullet: how many levels it takes for a bullet to be dropped
- speed: i don't know

- manual formations: a list of lists, each list containing more lists for values on rows ; these bypass all other settings given because they are manual 
- manual_type: how the manual formations are used ; 0 - None | 1 - ordered | 2 - random chance
- manual_loop: if the manual formations loop after cycled or if they go onto random formations ; only modifies ordered and random chance
- manual_influence: percent chance that a random manual formation is used over a random one ; only works for manual_type 2 and manual_loop false
- manual_levels: what level a manual formation is used (manual_type 1) ; what level a manual formation is put into the random roster (manual_type 2)

"""


#5/31/2023 - JSON loading
# This is the start of the JSON variant of levels.py. 
# First load all json files in levels folder
# If anything is ever missing from a json file, refer to default. 
worlds = {}
campaigns = {}

#6/1/2023 - Separating worlds from levels 
for _ in os.listdir("./worlds/"):
    #.order files are what stores the levels in a campaign
    if '.order' in _:
        with open("./worlds/"+str(_), "r") as file:
            campaigns[str(_)] = file.read().split(",")
    elif '.json' in _:
        with open("./worlds/"+str(_), "r") as raw:
            worlds[str(_)] = json.load(raw)

        
#6/1/2023 - LEVEL CLASS
# The level class is going to simply ask what loaded file to pull from, and assign a class to it for easier usage 
# With this, it can assign default values from the default.json file
# It is also able to update the intensities for each level
class Level():
    def __init__(self,
                 level=1, #used to calculate difficulties
                 campaign_world:tuple = ("main_story.order",0), #What gets fed in during gameplay to figure out what level file is being used
                 world_force:str = None #takes priority over campaign_world, used in level select
                 ):
        #6/1/2023 - WHAT LEVEL TO PULL FROM 
        # Again, it checks for the forced world first, but if it is None, it pulls from campaign_world
        # There is also error checking. 
        # The world files do not need to contain all of the data seen in default
        # So, in turn, this will copy the default file and merge it with the new content
        self.alldata = worlds["default.json"]
        try:
            if world_force is not None:
                self.alldata.update(worlds[world_force])
            else: 
                self.alldata.update(worlds[campaigns[campaign_world[0]][1]])
        except KeyError:
            self.alldata = worlds["default.json"]

        self.update_intensities(level=level)

    def update_intensities(self,level):
        self.alldata["spawn_time"]=random.randint((60-level),60)
        self.alldata["spawn_amount"] = int((1+(0.1*level))//1)
        self.alldata["max_char"] = random.randint(5,int(5+(0.1*level)//1))
        # print(str(level),":",str(self.spawn_time),",",str(self.spawn_amount),",",str(self.maxChar))


#6/1/2023 - LEVEL FUNCTIONS
# Actually yeah it may have been a dumb idea to make it a class, to be fair. 
# Maybe I should just make it a function that fetches stuff and merges data
def fetch_level_info(
    campaign_world:tuple = ("main_story.order",0), #What gets fed in during gameplay to figure out what level file is being used
    world_force:str = None #takes priority over campaign_world, used in level select
   ):
    #6/1/2023 - WHAT LEVEL TO PULL FROM 
    # Again, it checks for the forced world first, but if it is None, it pulls from campaign_world
    # There is also error checking. 
    # The world files do not need to contain all of the data seen in default
    # So, in turn, this will copy the default file and merge it with the new content
    alldata = worlds["default.json"]
    try:
        if world_force is not None:
            alldata.update(worlds[world_force])
        else: 
            alldata.update(worlds[campaigns[campaign_world[0]][1]])
    except KeyError:
        alldata = worlds["default.json"]
    
    return alldata

def update_intensities(level,alldata):
    alldata["spawn_time"]=random.randint((60-level),60)
    alldata["spawn_amount"] = int((1+(0.1*level))//1)
    alldata["max_char"] = random.randint(5,int(5+(0.1*level)//1))
    # print(str(level),":",str(self.spawn_time),",",str(self.spawn_amount),",",str(self.maxChar))
    
    return alldata




#####5/31/2023 TRYING OUT JSON FILES
#I know it makes more files in the end, but json files are just well-encoded text files and I don't think it matters that much. 
#It's better than what YUP originally did, with the weird import exec()s and such.
#So, pretty much all of the next 50 lines will be commented out in favor of such
"""
#5/31/2023 - total levels
# Pretty much, every world will inherit from this level class and add new things.
# VERY similar to characters in that regard
# All levels are held in a list in order to make them easier to spawn and with less imports.
all = []
class Level():
    def __init__(self,level=1):
        #LEVEL INFORMATION
        self.worldInfo={
            "songname":'meowchill.mp3',
            "uitype":'default',
            "bg":'null'
            }
        self.level_length=10 #TEMPORARY, NORMALLY 10

        #SIZE values
        self.char_distance_x=40
        self.char_distance_y=40
        self.char_min_width=5
        self.char_min_height=1
        self.char_max_width=10
        self.char_max_height=5

        #THROWDOWN values
        self.spawn_time=0
        self.spawn_amount=0
        self.maxChar=0
        self.update_intensities(level)#dynamic value assignment based on character

        #character
        self.imports = ['nope'] #PUT DUPLICATES IN THERE FOR DIFFERENT RATES OF CHARACTERS!!!
        self.bullets = []
        self.drop_health = 5 #how often it drops an extra life
        self.drop_bullet = 20 #chance out of 100 it drops a bullet per level
        self.speed=1

        #manually-generated formations to replace randomly-generated formations 
        self.manual_formations=[]

        form={
            0:['nope'],
        };self.manual_formations.append(form)

        form={
            0:['    ','nope','nope','nope','nope','    '],
        };self.manual_formations.append(form) 

        form={
            0:['nope','nope','nope','nope','nope','nope'],
            1:['    ','nope','nope','nope','nope','    '],
            2:['    ','    ','nope','nope','    ','    '],
        };self.manual_formations.append(form)
        
        self.manual_type=0 # [0 : no influence , 1 : random order , 2 : ordered] ; 0 and 2 will overwrite manual_influence.
        self.manual_loop=False #this onl"y counts of the type is 2.
        self.manual_influence=0  #<0 is no influence, >100 is all influence ; only applies to type 1


    def update_intensities(self,level):
        self.spawn_time=random.randint((60-level),60)
        self.spawn_amount = int((1+(0.1*level))//1)
        self.maxChar = random.randint(5,int(5+(0.1*level)//1))
        # print(str(level),":",str(self.spawn_time),",",str(self.spawn_amount),",",str(self.maxChar))
"""
