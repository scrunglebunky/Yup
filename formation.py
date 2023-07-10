import random,pygame,math,characters,random

#5/30/2023 - FORMATION CODE
# a lot of this is added from RevC as well. 
class Formation():
    data:dict = None
    sprites:dict = None
    

    def __init__(self,
                player, #player object

                world_data:dict, #level data info, for positioning and such
                sprites:dict, #sprite groups, from main

                data:dict, #universal data, from main

                level:int = 1, #the total amount of levels passed, usually used for intensities or score
                level_in_world:int = 1, #the amount of levels completed in the world currently 

                **kwargs,
                 ):
        
        #5/30/2023 - VARIABLES BASED OFF ARGUMENTS
        self.state = "start"
        self.player = player
        self.world_data = world_data
        self.level = level
        self.level_in_world = level_in_world
        self.sprites = sprites
        self.data = data

        #5/30/2023 - POSITIONING OF FORMATION
        self.pos = [225,100] #centered position of formation. 
        self.speed = 1
        self.direction = random.choice(('l','r'))
        self.duration = 0
        
        #05/30/2023 - CHARACTERS' SPAWNING
        self.spawning_timer = 0 #frame counter in the startup state for how long it takes to spawn a character
        self.spawning_index = [0,0] #counter for where in self.spawn_list the spawner is currently at, as to not get confused with anything else
        self.spawned_list = [] #a list of spawned characters, the actual objects for the formation to look at and do checks on ; unordered
        self.completed_level = False #checking if the level (formation) is complete and needs to be reset;  run with the timers

        #06/22/2023 - FIGURING OUT WHAT'S IN THE FORMATION BASED ON LEVEL DATA
        self.spawn_list = [["nope"],["nope"]] #default spawn

        #06/22/2023 - MANUAL ORDERED
        if self.world_data["manual_type"] == 1:
            spawn_len = len(self.world_data["manual_formations"])
            loops = (self.level_in_world-1) // spawn_len
            subtractor = loops * spawn_len
            #IF LOOPED:
            if self.world_data["manual_loop"] or subtractor < 0:
                self.spawn_list = self.world_data["manual_formations"][(self.level_in_world-1) - subtractor] #a list of characters to spawn, and that's it
                print('wahoo')
            #IF NOT LOOPED: 
            elif subtractor > 0 and not self.world_data["manual_loop"]:
                self.spawn_list = self.random_formation()

        #06/23/2023 - RANDOM
        elif self.world_data["manual_type"] == 2:
            # pick_manual is based off a value called "manual_influence", where if the value is satisfied, it will pick a manual formation instead of a random one
            pick_manual:bool = (random.randint(1,100) <= self.world_data["manual_influence"])
            if pick_manual: 
                self.spawn_list = random.choice(self.world_data["manual_formations"])
            # however, it usually just picks something random
            else:
                self.spawn_list = self.random_formation()
        
        else:
            self.spawn_list = self.random_formation()


            



        # #test- spawning A character
        # self.test = characters.loaded["nope"](sprites=self.sprites,level=self.level,formation_position=self.pos,offset=(0,0),data=self.data,)
        # self.sprites[0].add(self.test);self.sprites[2].add(self.test)
        
        #06/06/2023 - Timer for checking things without checking them every frame 
        self.timer:int = 0
        self.timer_dead_check:int = 30 #how many frames before checking for a dead character
        self.timer_dead_copylist = [] #a copy of the character list for kill checking purposes
        self.timer_reset_rate = 120 #how many frames before the timer resets
    
        #06/06/23 - calculating center position
        # Calculate total length of formation, divide by 2, take center screen and subtract by half length
        # this is why EVERY FORMATION SHOULD HAVE THE SAME LENGTH OF COLUMNS IN EACH ROW NO MATTER WHAT
        self.pos[0] = ((pygame.display.play_dimensions[0]/2) - (len(self.spawn_list[1])*self.world_data["char_distance_x"] /2))


    def update(self):
        #updating timer
        self.timer = self.timer + 1 if self.timer < self.timer_reset_rate else 1
        #updating states
        self.update_movement()
        if self.state == 'start':self.state_start()
        if self.state == 'idle':self.state_idle()
        if self.state == 'destroy':self.state_destroy()
        #updating misc
        self.remove_dead()
        self.check_for_atk()


    def state_start(self):
        #06/06/2023 - SPAWNING CHARACTERS
        #counts for a set amount of frames and spawns in each character in the formation
        #think like how space invaders has a set amount of "characters" in a "formation" where they all move, but they all spawn in an order to make it look nice
        #every time a character is spawned, the timer resets and the index is risen
        self.spawning_timer += 1
        if self.spawning_timer >= self.world_data["spawn_time"]:

            #06/22/2023 - figuring out what character to spawn
            to_spawn = self.spawn_list[self.spawning_index[1]][self.spawning_index[0]]
            
            if to_spawn in characters.loaded.keys():
                #spawning the character - note the data in spawning_index is what is to be spawned CURRENTLY, not previously
                cur_char = characters.loaded[to_spawn](
                    sprites=self.sprites,
                    level=self.level,
                    formation_position=self.pos,
                    offset=(
                        self.spawning_index[0]*self.world_data["char_distance_x"],
                        self.spawning_index[1]*self.world_data["char_distance_y"]),
                    data=self.data,)
                self.spawned_list.append(cur_char)
                self.sprites[0].add(cur_char);self.sprites[2].add(cur_char)
            
            #resetting timer values, raising the value of the spawning_timer's y value
            self.spawning_timer = 0
            self.spawning_index[0] += 1
            
            #the y value of spawning_timer is the x value of the spawn_list, vice versa.
            if self.spawning_index[0] > (len(self.spawn_list[self.spawning_index[1]])-1):
                self.spawning_index[0] = 0;self.spawning_index[1] += 1
            #checking for being finished
            if self.spawning_index[1] > (len(self.spawn_list)-1):
                self.state = "idle"
                self.spawning_index = (0,0)
                self.duration = 0 


    def state_idle(self):...
    

    def state_destroy(self):...


    def check_for_atk(self):
        #06/06/2023 - Spawning in characters
        # Quick thing to note, I realized there was no need to constantly update everything
        # So it only updates when a character *needs* to be thrown.
        if (self.timer%self.world_data['throwdown_time']==0):
            atk_count = 0
            idle_char = []
            #06/06/2023 - Creating values
            for _ in enumerate(self.spawned_list):
                if _[1].state == 'atk': atk_count += 1
                elif _[1].state == 'idle': idle_char.append(_[0])
            #06/06/2023 - Checking for conditions for character throwdown to be complete
            if atk_count <= self.world_data['max_char'] and len(idle_char) > 0:
                self.attack(idle_char)
            
    

    def attack(self,idle_char:list):
        for i in range(self.world_data['throwdown_amount']):
            self.spawned_list[random.choice(idle_char)].stchg('attack')


    def update_movement(self):
        self.duration += 1
        self.pos[1] = math.sin(self.duration * 0.1) * 15 + ((self.duration*0.25) if self.state != "start" else 0)
        for char in self.spawned_list:
            char.formationUpdate(self.pos)
    
    def remove_dead(self):
        #06/06/2023 - removing dead characters
        # The formation copies the list (1), enumerates through the list (2), and deletes all dead items (3)
        if self.timer % self.timer_dead_check == 0:
            self.timer_dead_copylist.append(item for item in self.spawned_list) #(1)
            for _ in enumerate(self.spawned_list,0): #(2)
                if _[1].dead: 
                    self.spawned_list.pop(_[0]) #(3)
                    # print('removed',str(_[0]))
            self.timer_dead_copylist = []
            #06/06/2023 - checking for a completed formation   
            # remember, this is used as a signal/flag externally for the playstate to 
            self.completed_level = len(self.spawned_list) <= 0

    def empty(self):
        for i in range(len(self.spawned_list)):
            self.spawned_list[i].kill()
        self.spawned_list = []
        self.state = "complete"
        self.completed_level = True

    def random_formation(self) -> list:
        #06/23/23 - GENERATING A RANDOM FORMATION FOR LOOPS, OR JUST TYPES IN GENERAL
        # return [["nope"],["nope"]] #TEMPORARY - CHANGE loaded_characters
        spawn_list = []
        # generating sizes 
        rows = random.randint(self.world_data["char_min_height"],self.world_data["char_max_height"])
        columns = random.randint(self.world_data["char_min_width"],self.world_data["char_max_width"])
        # generating spawnsheet
        for row in range(rows):
            # adding a new row
            spawn_list.append([])
            # adding individual columns
            for column in range(columns):
                spawn_list[row].append(
                    random.choice(
                        self.world_data["imports"]
                        )
                    )
        return spawn_list





# class Formation:
#     def __init__(
#         self, player, level, file=None, total_level=1  # levels in world
#     ):  # total level takes worlds into account
#         # print("==============NEW FORMATION")

#         # DEFINITIONS
#         self.state = "start"  # level's state; "start","idle", and "complete"
#         self.file = file  # level's python file
#         self.player = player  # the player object
#         self.level = level  # current level number ; for intensities

#         self.pos = [0, 100]  # position lol
#         self.direction = random.choice(["l", "r"])  # direction, either 'l' or 'r'
#         self.speed = 0  # speed the formation moves in idle
#         self.current_frame = 0  # calculating when to throw a character down, or when to spawn a character

#         self.total_characters = 0  # total amount of characters
#         self.spawn_list = {}  # spawnlist
#         self.spawned_formation = []  # spawned characters
#         available_char = self.file.imports  # characters that can be randomly generated

#         # calculating characters to use
#         self.used_char = [available_char[0]]
#         if len(available_char) >= 2:
#             chunk = self.file.level_length / (len(available_char) - 1)

#             for _ in range(int(level // chunk)):
#                 if len(self.used_char) < len(available_char):
#                     self.used_char.append(available_char[_ + 1])
#         self.formation_size = [0, 0]  # size of the formation

#         self.spawn_list = self.generate_spawn_list()

#         # FORMATION SIZE
#         # SPAWN*LIST* SIZE
#         self.formation_size[1] = len(self.spawn_list)  # vertical size is figured out
#         for row in self.spawn_list:
#             if (
#                 len(self.spawn_list[row]) > self.formation_size[0]
#             ):  # horizontal size is the longest row
#                 self.formation_size[0] = len(self.spawn_list[row])
#         # CENTERING FORMATION BASED ON SIZE
#         self.pos[0] = 225 - (self.formation_size[0] * self.file.char_distance_x / 2)

#         # formation spawn code
#         self.spawn_list_indexes = []
#         self.columns = 0  # instead of using the y value for some things, we use *columns*, because some blank indexes get left out
#         self.current_row = 0  # this is so we know when to reset columns
#         # this will append every index in the formation spawn list so the start state can add them in order without any complex loops
#         for i in range(len(self.spawn_list)):
#             self.spawned_formation.append([])
#             for j in range(len(self.spawn_list[i])):
#                 self.spawn_list_indexes.append((i, j))
#         # potential item spawn
#         self.items_to_spawn = {}
#         #puts an item in a character if the timing is right and the player has no shield#
#         if (self.player.bullet == "default") and (
#             self.level % self.file.drop_health == 0
#         ):
#             self.items_to_spawn[random.choice(self.spawn_list_indexes)] = (
#                 "health",
#                 None,
#             )
#         #puts a bullet in a character if random chance#
#         if (
#             random.randint(0, 100) < self.file.drop_bullet
#             and len(self.file.bullets) > 0
#         ):
#             self.items_to_spawn[random.choice(self.spawn_list_indexes)] = (
#                 "bullet",
#                 random.choice(self.file.bullets),
#             )
#             # print("CONDITION MET")

#     def update(self):
#         # self-explanatory
#         if self.state == "idle":
#             self.idle()
#         elif self.state == "start":
#             self.start()
#         elif self.state == "exit":
#             self.exit()

#         # self.update_size()
#         self.update_character_formation_pos()
#         if self.state != "start":
#             self.remove_dead()

#     def idle(self):
#         # actually moving
#         self.formation_move()
#         # attacking based on time
#         self.calculate_attack_time()

#     def start(self):
#         # moving formation
#         self.formation_move()

#         # checking if time has passed
#         self.current_frame += 1

#         if self.current_frame >= 20:  # DEBUG - CHANGE TO 6
#             # index = random.randint(0,len(self.spawn_))

#             # resetting timer
#             self.current_frame = 0

#             # breaking out of start state to prevent error
#             if len(self.spawn_list_indexes) <= 0:
#                 self.state = "idle"
#                 return
#             # resetting columns
#             if self.spawn_list_indexes[0][0] != self.current_row:
#                 self.current_row = self.spawn_list_indexes[0][0]
#                 self.columns = 0
#             # spawning a character
#             try:
#                 # adds a character to the formation
#                 self.spawned_formation[self.spawn_list_indexes[0][0]].append(
#                     loaded_characters[
#                         self.spawn_list[self.spawn_list_indexes[0][0]][
#                             self.spawn_list_indexes[0][1]
#                         ]
#                     ].Char(
#                         args={
#                             "groups": groups,
#                             "player": self.player,
#                             "formation_position": self.pos,
#                             "offset": (
#                                 (
#                                     self.spawn_list_indexes[0][1]
#                                     * self.file.char_distance_x
#                                 ),
#                                 (
#                                     self.spawn_list_indexes[0][0]
#                                     * self.file.char_distance_y
#                                 ),
#                             ),
#                             "level": self.level,
#                         }
#                     )
#                 )
#                 #INDEX REFERENCE
#                 #items_to_spawn: KEY, (row,column) ; VALUE, (item_type,item_name)
#                 #spawned_formation: [FIRST BRACKET], LIST OF ROWS ; [SECOND BRACKET], CHARACTERS IN ROW
#                 #
#                 # print(self.spawned_formation)
#                 for key, value in self.items_to_spawn.items():
#                     if key[0] <= (len(self.spawned_formation) - 1):
#                         # print("ROW CONDITION MET |",str(key),"|",str(self.spawned_formation))
#                         if key[1] <= len(self.spawned_formation[key[0]]) - 1:
#                             self.spawned_formation[key[0]][key[1]].container = value
#                             # print("ITEM ADDED")
#                             self.items_to_spawn.pop(key)
#                             break
#                         else:
#                             # print("COLUMN CONDITION NOT MET |", str(key) , str(self.spawned_formation[key[0]]))
#                             pass
#             # ignoring emtpy enemy spaces -
#             except KeyError:
#                 self.spawn_list_indexes.pop(0)
#                 return
#             # adding to group
#             groups["universal"].add(
#                 self.spawned_formation[self.spawn_list_indexes[0][0]][self.columns]
#             )
#             groups["enemy"].add(
#                 self.spawned_formation[self.spawn_list_indexes[0][0]][self.columns]
#             )

#             # instead of using the y value for some things, we use *columns*, because some blank indexes get left out
#             self.columns += 1

#             # deleting index 0 so the next one is in line
#             self.spawn_list_indexes.pop(0)

#     def exit(self):
#         self.current_frame += 1

#         if self.current_frame >= 6:
#             self.current_frame = 0
#             groups["universal"].add(
#                 shared.dieBoom(self.spawned_formation[0][0].rect.center, (50, 50))
#             )
#             self.spawned_formation[0][0].state = "dead"
#             self.spawned_formation[0][0].kill()

#     def calculate_attack_time(self):
#         # calculating when to make a character attack

#         self.current_frame += 1
#         total_attack_enemies = 0

#         # calcuating the amount of enemies attacking
#         for i in range(len(self.spawned_formation)):
#             for j in range(len(self.spawned_formation[i])):
#                 if self.spawned_formation[i][j].state == "attack":
#                     total_attack_enemies += 1
#         # checking if the right amount of enemies are attacking and if enough time has passed
#         if (self.file.maxChar is None or total_attack_enemies < self.file.maxChar) and (
#             self.current_frame >= self.file.spawn_time
#         ):
#             self.attack()
#             self.current_frame = 0

#     def attack(self):
#         # current characters in idle
#         idle_list = []

#         # checks characters and adds ones in idle to idle_list
#         for i in range(len(self.spawned_formation)):
#             for j in range(len(self.spawned_formation[i])):
#                 if self.spawned_formation[i][j].state == "idle":
#                     idle_list.append((i, j))
#         # picking a random character to make attack
#         if len(idle_list) > 0:
#             chosen_list = random.choice(idle_list)
#             del idle_list
#             self.spawned_formation[chosen_list[0]][chosen_list[1]].state = "attack"
#             return

#     def update_character_formation_pos(self):
#         # updating the characters on what the formation position is
#         for i in range(len(self.spawned_formation)):
#             for j in range(len(self.spawned_formation[i])):
#                 self.spawned_formation[i][j].formationUpdate(self.pos)

#     def formation_move(self):
#         # updating the movement

#         # changing the direction from right to left
#         if self.pos[0] >= (500 - (self.formation_size[0] * self.file.char_distance_x)):
#             self.speed -= self.file.speed * 0.025
#             self.direction = "l"
#         # changing the direction from left to right
#         elif self.pos[0] <= 10:
#             self.speed += self.file.speed * 0.025
#             self.direction = "r"
#         # speeding up if no direction change
#         else:
#             if self.direction == "l":
#                 self.speed = self.file.speed * -1
#             elif self.direction == "r":
#                 self.speed = self.file.speed
#         # updating positions based on speed
#         self.pos[0] += self.speed
#         self.pos[1] = math.sin(self.pos[0] / 10) * 10 + 100

#     def random_spawn_list(self):
#         # randomly generates characters and puts them in a formation
#         formation = {}

#         # column size based on current level
#         column_size = int(
#             self.file.char_min_width
#             + (  # minimum value
#                 (self.level / self.file.level_length)
#                 * (self.file.char_max_width - self.file.char_min_width)  # percent
#             )  # amount of variation
#         )
#         row_size = int(
#             self.file.char_min_height
#             + (  # minimum value
#                 (self.level / self.file.level_length)
#                 * (self.file.char_max_height - self.file.char_min_height)  # percent
#             )  # amount of variation
#         )

#         # print(str(self.level) + "|" + str(self.file.level_length) + "|" + str(column_size) + "|" + str(row_size))

#         for i in range(row_size):  # row generation
#             formation[i] = []
#             for j in range(column_size):  # column generation
#                 formation[i].append(random.choice(self.used_char))
#         return formation

#     def generate_spawn_list(self):
#         spawn_list = {}
#         # SPAWNLIST
#         manual = (
#             len(self.file.manual_formations) > 0 and self.file.manual_type != 0
#         )  # boolean value, figures out if formation is manual
#         # manual spawn list
#         if manual:
#             # random manual formation
#             if self.file.manual_type == 1:
#                 # picks a random manual_formation a certain percent of the time, randomly generates one the other percent
#                 if (
#                     random.randint(0, 100) < self.file.manual_influence
#                 ):  # chance picks a manual formation
#                     spawn_list = random.choice(self.file.manual_formations)
#                 else:  # chance picks elsewise
#                     spawn_list = self.random_spawn_list()
#             # ordered manual formation
#             elif self.file.manual_type == 2:
#                 # nonlooping
#                 if not self.file.manual_loop:
#                     # if level is within the length of the formations
#                     if self.level <= len(self.file.manual_formations):
#                         spawn_list = self.file.manual_formations[
#                             self.level - 1
#                         ]  # level -1 because it doesn't start at 0
#                     # if level has surpassed length of the formations
#                     else:
#                         spawn_list = self.random_spawn_list()
#                 # looping
#                 else:
#                     # shedding the looped numbers off of levels
#                     index = self.level - (
#                         len(self.file.manual_formations)
#                         * ((self.level - 1) // len(self.file.manual_formations))
#                     )
#                     # setting formation
#                     spawn_list = self.file.manual_formations[index - 1]
#         # random spawn list
#         else:
#             spawn_list = self.random_spawn_list()
#         return spawn_list

#     def update_size(self):
#         # UPDATING SIZE BASED OFF SPAWN
#         self.formation_size[1] = len(
#             self.spawned_formation
#         )  # vertical size is figured out
#         for row in self.spawned_formation:
#             if len(row) > self.formation_size[0]:  # horizontal size is the longest row
#                 self.formation_size[0] = len(row)

#     def remove_dead(self):
#         # deleting dead characters
#         for row in range(len(self.spawned_formation)):
#             for column in range(len(self.spawned_formation[row])):
#                 if self.spawned_formation[row][column].state == "dead":
#                     self.spawned_formation[row].pop(column)
#                 break
#         # deleting empty rows
#         for row in range(len(self.spawned_formation)):
#             if len(self.spawned_formation[row]) == 0:
#                 self.spawned_formation.pop(row)
#                 break
#         # changing state to "complete" if there are no rows
#         if len(self.spawned_formation) == 0:
#             self.state = "complete"

#     def destroy(self):
#         # deletes all characters
#         for i in range(len(self.spawned_formation)):
#             for j in range(len(self.spawned_formation[i])):
#                 self.spawned_formation[i][j].kill()
#         # empties
#         self.spawned_formation = []
#         self.state = "complete"

