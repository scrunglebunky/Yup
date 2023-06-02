#PROGRAM BY ANDREW CHURCH 
import pygame,os,json


# 5/8/23 - FIXING THE SPRITESHEETS
# the way spritesheets work right now is that the loaded images are stored in the spritesheet object upon creation
# this is not optimized, as that means each character will have an new instance of all the images again
# to negate this, there is going to be a dict called "all loaded spritesheets" that all sprites have by default, which contains a dictionary for all the character files loaded 
all_loaded_spritesheets = {}
all_loaded_images = {}

    
#5/8/23 - DEFINING THING TO LOAD ALL IMAGES
def generate_sprite(data):
    spritesheet=[]
    raw=pygame.image.load(data["NAME"]+".png")
    def get_image(sheet,
                  wh:tuple,
                  xy:tuple,
                  scale:float=1.0,
                  colorkey:tuple=(0,0,0)):
        #making empty surface
        output = pygame.Surface((wh[0],wh[1])).convert_alpha()
        #outputting parts of the image onto the surface
        output.blit(sheet,(0,0),(xy[0],xy[1],wh[0],wh[1]))
        #scaling
        output = pygame.transform.scale(output,(wh[0]*scale,wh[1]*scale))
        #"greenscreen"ing
        output.set_colorkey(colorkey)
        #output
        return output
    #LOADING ALL SPRITE IMAGES
    for row in range(data["ROWS/COLUMNS"][0]):
        #it's easier for me, screw off.
        for column in range(data["ROWS/COLUMNS"][1]):
            spritesheet.append(
                get_image(
                    sheet=raw,
                    wh=data["TILE_SIZE"],
                    xy=(data["TILE_SIZE"][0]*column,
                        data["TILE_SIZE"][1]*row),
                    scale=data["scale"],
                    colorkey=data["colorkey"],
                    ))
    return spritesheet

#06/01/2023 - USING ANIM_LOADLIST TO FIND OUT WHAT TO LOAD
with open("./data/anim_loadlist.json","r") as raw:
    anim_loadlist = json.load(raw)
#06/01/2023 - REVAMP OF OLD CODE
for directory,filelist in anim_loadlist.items():
    #There is no longer a break if there's no json, as the list contains all the json files needed without any scraping
    for filename in filelist:
        with open(directory+filename+".json") as raw:
            current_file = json.load(raw)
        #adding to main directory, generating a spritesheet
        all_loaded_spritesheets[filename] = (current_file,generate_sprite(current_file))
        #loading animation files if existent
        if current_file["ANIM"] is not None:
            with open("./images/characters/"+str(current_file["ANIM"]),"r") as raw:
                anim_file = json.load(raw)
                all_loaded_spritesheets[filename][0]["anim"] = anim_file
            #5/25/23 - FIXING ANIMATION FPSes"
            for animation in anim_file.keys():
                anim_file[animation]["FPS"] = 60/anim_file[animation]["FPS"]
#06/01/2023 - LOADING NON-ANIMATED IMAGES
with open("./data/img_loadlist.json","r") as raw:
    img_loadlist = json.load(raw)
for directory,filelist in img_loadlist.items():
    for filename in filelist:
        all_loaded_images[str(filename)] = pygame.image.load(directory+filename)
              


"""
#5/8/23 - LOADING IN ALL IMAGES WITH DATA
jsonlist = os.listdir("./images/characters")
for item in jsonlist:
    #breaking if not json, OR if the "anim" keyword is detected
    if ".json" not in item or "anim" in item: continue
    #going through with everything
    with open("./images/characters/"+str(item),"r") as raw:
        file = json.load(raw)
    #adding to the main dictionary
    all_loaded_spritesheets[item] = (file,generate_sprite(file))
    #5/11/23 - LOADING ANIMATION FILES IF EXISTANT
    if file["ANIM"] is not None:
        with open("./images/characters/"+str(file["ANIM"]),"r") as raw:
            anim_file = json.load(raw)
            all_loaded_spritesheets[item][0]["anim"] = anim_file
        #5/25/23 - FIXING ANIMATION FPSes"
        for animation in anim_file.keys():
            anim_file[animation]["FPS"] = 60/anim_file[animation]["FPS"]
"""


# 5/8/23 - WHAT DO THE SPRITESHEETS DO?
# the spritesheet class is going to refer to the all_loaded_spritesheets dict and pull from it
# this is a way for all sprites to use the same cookie-cutter layout and hook to them fine
# earlier, it would load the spritesheets and everything, in the class. However, as read above, this would cause repeated loaded images with the creation of each character.
# spritesheet will, now, just know what frames are what. it's better for organization
# EDIT EVERYTHING IN THE JSON FILES ON YOUR OWN. YOU HEAR ME? I SWEAR TO GOD. I HATE YOU ALL.
class Spritesheet():
    def __init__(self,
                 name:str,
                 current_anim:str = None,
                 all_loaded_spritesheets:dict = all_loaded_spritesheets
                 ): #DO NOT CONTAIN EXTENSION IN PATH

        
        #DEFINITIONS
        self.name = name
        self.all_anim = all_loaded_spritesheets[name][0]["anim"] #self-explanatory
        self.current_anim = current_anim #current animation played
        self.current_anim_loop = 0 #amount of loops
        self.current_anim_frame = 0 #frame of animation; NOTE THIS IS THE INDEX OF THE all_anim["frames"] TUPLE, NOT SPRITESHEETS
        self.current_anim_frame_len = 0 #length of frame of animation
        self.image_displayed = 0 #the index of self.spritesheet; callback to actual sprite played

    def update(self): #this will be called every frame in the respective sprite
        #print("---\n",self.current_anim,self.image_displayed,self.current_anim_frame,self.current_anim_frame_len,sep="|")

        #error checking
        if self.current_anim not in self.all_anim.keys() or type(self.all_anim) is None or len(self.all_anim) < 1:
            return
        
        self.current_anim_frame_len += 1
        
        #updating animation frame
        if self.current_anim_frame_len >= self.all_anim[self.current_anim]["FPS"]:
            # print('updated frame')
            self.current_anim_frame+=1
            self.current_anim_frame_len=0
            
        #updating animation being played
        if self.current_anim_frame >= len(self.all_anim[self.current_anim]["frames"]):
            # print('updated animation')
            #updating if loop
            self.current_anim_loop += 1
            self.current_anim_frame = 0
            #if the loop is complete
            if self.current_anim_loop >= self.all_anim[self.current_anim]["loop"]:
                # print('animation loop completed')
                self.current_anim_loop = 0
                self.current_anim = self.all_anim[self.current_anim]["return_to"]

        #updating the actual current image being used
        self.image_displayed = self.all_anim[self.current_anim]["frames"][self.current_anim_frame]
    
    def change_anim(self,new:str,overwrite:bool=False):
        #checking for if the animation is "interruptable" - for the record, you are able to add "interruptable" to an animation and mark it False to make no other animation take priority over it
        if "interrupt" in self.all_anim[self.current_anim].keys() and not self.all_anim[self.current_anim]["interrupt"] and not overwrite:return
        #resets all frames, changes current animation
        self.current_anim = new
        self.current_anim_frame = 0
        self.current_anim_frame_len = 0
        self.current_anim_loop = 0 
