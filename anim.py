#PROGRAM BY ANDREW CHURCH - test?
import pygame,os,json


# 5/8/23 - FIXING THE SPRITESHEETS
# the way spritesheets work right now is that the loaded images are stored in the spritesheet object upon creation
# this is not optimized, as that means each character will have an new instance of all the images again
# to negate this, there is going to be a dict called "all loaded spritesheets" that all sprites have by default, which contains a dictionary for all the character files loaded 
all_loaded_spritesheets = {}
all_loaded_images = {}

    
#5/8/23 - DEFINING THING TO LOAD ALL IMAGES
def get_image(sheet,
                  wh:tuple,
                  xy:tuple,
                  scale:float=1.0,
                  colorkey:tuple=(0,0,0)):
        #making empty surface
        output = pygame.Surface((wh[0],wh[1])).convert_alpha()
        output.fill(colorkey)
        #outputting parts of the image onto the surface
        output.blit(sheet,(0,0),(xy[0],xy[1],wh[0],wh[1]))
        #scaling
        output = pygame.transform.scale(output,(wh[0]*scale,wh[1]*scale)).convert_alpha()
        #"greenscreen"ing
        output.set_colorkey(colorkey)
        #output
        return output

def generate_sprite(data):
    spritesheet=[]
    raw=pygame.image.load(data["NAME"]+".png").convert_alpha()
    #LOADING ALL SPRITE IMAGES
    for row in range(data["ROWS/COLUMNS"][0]):
        #it's easier for me, screw off.
        for column in range(data["ROWS/COLUMNS"][1]):
            cur_img = get_image(sheet=raw,wh=data["TILE_SIZE"],
                    xy=(data["TILE_SIZE"][0]*column,data["TILE_SIZE"][1]*row),
                    scale=data["scale"],colorkey=data["colorkey"],).convert()
            spritesheet.append(cur_img)
    return spritesheet

def generate_masks(spritesheet):
    masks = []
    for sprite in spritesheet:
        masks.append(pygame.mask.from_surface(sprite))
    return masks

#06/01/2023 - USING ANIM_LOADLIST TO FIND OUT WHAT TO LOAD
with open("./data/anim_loadlist.json","r") as raw:
    anim_loadlist = json.load(raw)


#06/01/2023 - REVAMP OF OLD CODE - LOADING THE ANIM LOADLIST
for directory,filelist in anim_loadlist.items():
    #There is no longer a break if there's no json, as the list contains all the json files needed without any scraping
    for filename in filelist:
        with open(directory+filename+".json") as raw:
            current_file = json.load(raw)
        #generating spritesheet
        spritesheet = generate_sprite(current_file)
        masksheet = generate_masks(spritesheet)
        #adding to main directory, generating a spritesheet
        all_loaded_spritesheets[filename] = (current_file,spritesheet,masksheet)
        #loading animation files if existent
        if current_file["ANIM"] is not None:
            with open("./images/characters/anim/"+str(current_file["ANIM"]),"r") as raw:
                anim_file = json.load(raw)
                all_loaded_spritesheets[filename][0]["anim"] = anim_file
            #5/25/23 - FIXING ANIMATION FPSes"
            for animation in anim_file.keys():
                anim_file[animation]["FPS"] = 60/anim_file[animation]["FPS"]
        else:
            with open("./images/characters/anim/default.json","r") as raw:
                anim_file = json.load(raw)
                all_loaded_spritesheets[filename][0]["anim"] = anim_file
            #5/25/23 - FIXING ANIMATION FPSes"
            for animation in anim_file.keys():
                anim_file[animation]["FPS"] = 60/anim_file[animation]["FPS"]


#06/01/2023 - LOADING NON-ANIMATED IMAGES
with open("./data/img_loadlist.json","r") as raw:
    img_loadlist = json.load(raw)
for directory,filelist in img_loadlist.items():
    #06/22/2023 - RESIZING IMAGES
    # The last index of the loadlist will be 'resize', with each index being [imagename, [width,height]]
    if directory == "resize":
        for filename in filelist:
            all_loaded_images[str(filename[0])] = pygame.transform.scale(all_loaded_images[str(filename[0])],filename[1])
        continue
    for filename in filelist:
        all_loaded_images[str(filename)] = pygame.image.load(directory+filename).convert_alpha()


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
                 all_loaded_spritesheets:dict = all_loaded_spritesheets,
                 resize:tuple=None
                 ): #DO NOT CONTAIN EXTENSION IN PATH

        
        #DEFINITIONS
        self.name = name
        self.all_loaded_spritesheets = all_loaded_spritesheets #for external use
        self.all_anim = dict(all_loaded_spritesheets[name][0]["anim"].copy()) #self-explanatory
        self.current_anim = current_anim #current animation played
        self.current_anim_loop = 0 #amount of loops
        self.current_anim_frame = 0 #frame of animation; NOTE THIS IS THE INDEX OF THE all_anim["frames"] TUPLE, NOT SPRITESHEETS
        self.current_anim_frame_len = 0 #length of frame of animation
        self.image_displayed = 0 #the index of self.spritesheet; callback to actual sprite played\\
        self.resize = resize
        self.image = all_loaded_spritesheets[self.name][1][self.image_displayed]
        self.mask = all_loaded_spritesheets[self.name][2][self.image_displayed]
        if self.resize is not None: self.image = pygame.transform.scale(self.image,self.resize)
        self.changed = False #a way to tell if the image was changed, so the image isn't being reset every frame
        self.looped = False #a checker for emblem to tell if an asset should be deleted

    def update(self) -> pygame.Surface: #this will be called every frame in the respective sprite
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
            self.changed = True
            
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
            self.looped = True

        #updating the actual current image being used, as a numerical frame
        self.image_displayed = self.all_anim[self.current_anim]["frames"][self.current_anim_frame]

        #changing values if needed to
        if self.changed:
            self.image = all_loaded_spritesheets[self.name][1][self.image_displayed]
            self.mask = all_loaded_spritesheets[self.name][2][self.image_displayed]

            if self.resize is not None: self.image = pygame.transform.scale(self.image,self.resize)
            self.changed = False #resetting

        
    
    def change_anim(self,new:str,overwrite:bool=False):
        #checking for if the animation even exists
        if new not in self.all_anim.keys():return
        #checking for if the animation is "interruptable" - for the record, you are able to add "interruptable" to an animation and mark it False to make no other animation take priority over it
        if "interrupt" in self.all_anim[self.current_anim].keys() and not self.all_anim[self.current_anim]["interrupt"] and not overwrite:return
        #resets all frames, changes current animation
        self.current_anim = new
        self.current_anim_frame = 0
        self.current_anim_frame_len = 0
        self.current_anim_loop = 0 




#AUTOIMAGE CLASS
# A LOT of entity classes in this game have to manually check for animations and such, or if it's just using a static image
# However, this class is going to streamline it, by doing all the checking for spritesheets on its own
class AutoImage():
    def __init__(self,name:str=None,current_anim:str='idle',force_surf:pygame.Surface=None):
        self.name = name
        self.spritesheet = None
        self.image = None
        #figuring out what kind of asset to use
        self.type = AutoImage.fetch_info(name=self.name)
        if self.type == 'img':
            self.image = all_loaded_images[self.name]
        elif self.type == 'anim':
            self.spritesheet = Spritesheet(name=self.name,current_anim=current_anim)
            self.image = self.spritesheet.image
        elif force_surf is not None:
            self.image = force_surf
        else:
            self.image = all_loaded_images['placeholder.bmp']
    
    def update(self):
        if self.spritesheet is not None: 
            self.spritesheet.update()
            self.image = self.spritesheet.image

    def change_anim(self,anim:str,overwrite:bool=False):
        if self.spritesheet is not None:
            self.spritesheet.change_anim(anim,overwrite=overwrite)


    @staticmethod
    def fetch_info(name:str = "placeholder.bmp") -> str:
        #checking to see if the name is an image
        if name in all_loaded_images.keys():
            return 'img'
        elif name in all_loaded_spritesheets.keys():
            return 'anim'
        else:
            return 'err'
