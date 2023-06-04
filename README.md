# WELCOME TO YUP
## WHAT IS YUP?
- Yup is a small shoot-em-up game that takes heavy referencing off of games like Galaga, Astro Warrior, and some other classics.
- Everything within the game is an attempt to stay modular, with each part being its own file, class, or function for me to use in other projects.
- This is the fourth iteration of the game. In the third one, I got too obsessed with optimization and changing everything up.
- This is my last attempt: a refresher that ensures that I make a simple, intuitive game that I do not overthink about.
## YUP LORE
- Yup is a species of YUPparian, a race of creature that rapidly evolved into different subspecies based off their environment. 
- Some turned red, some grew spikes, and some just turned into fish. 
- YUP is one of the last five (no lore importance) of the purebreeds of her species, and grows intolerant with her species as nothing is done to conserve the dying group.
- It all comes to a head at one point when YUP loses her *HAM AND TURKEY SANDWICH*, causing her to blast off in a fit of rage to try and find it.
- She has to blast through militant troops of each planet to uncover her food! Will she find it, or will she uncover something else?
## MISCELLANEOUS YUP INFORMATION
- Yup's species is a space ship, like the creatures in Fantasy Zone; she has an entirely humanoid body, roughly 2 heads tall in proportions, that retracts into her head in a cartoony manner.
- This entire storyline is not meant to be taken seriously or to get too deep; it's stupid; it's YUP.
- Mustard is dry. 08206

# YUP DEVLOG
## PART ONE- GETTING IT ALL TOGETHER
- 6/03/23: added a little bar rectangle for the UI, when the 
- 6/03/23: programmed backgrounds; layering for scrolling images; resizing;
- 6/02/23: made individual image loading
- 6/02/23: made the formation somewhat functional, with a graphical representation of its position
- 6/02/23: learned that \*\*kwargs is a thing, also working on fixing arguments to be more universal per everything (characters, formations, states, etc)
- 6/01/23: made a data file called "loadlist" that calls for everything to be preloaded; replaces RevC's large glob of image loading
- 6/01/23: scrapped the class, made it a function for easier navigation and less confusing-ness; it now just returns a loaded level
- 6/01/23: Made a class that takes the level data into account
- 6/01/23: started loading all level files in /levels/
- 5/31/23: started working on json files for levels 
- 5/31/23: ADDED levels.py, universal levels class/func to handle data
- 5/31/23: Fixed up text.py and added finishing touches
- 5/30/23: ADDED text.py, made numbers and text displayed
- 5/30/23: halted player shoot animation if too many bullets onscreen
- 5/30/23: organized files
- 5/29/23: [START WORKING ON LOADING TEXT]
- 5/28/23: Added new states instead of holding everything in main
- 5/26/23: Added player collision; added default enemy death; made collision federally controlled; started bullets 
- 5/25/23: Added player movement barriers, made shooting animations, made early collision recognition
- 5/24/23: Started working on Player. I realized I do not have to make everything interconnect at the start, as it makes me overthink everything. I just need to program YUP and get it all done with. She has values such as health and momentum, but movement is most of it: a dictionary containing information about moving up, down, left, and right. 
- 5/?/23: Made a character template with **char_template.py**, which stores default values and functions for characters to fall back to when there is not a unique value programmed. Examples include state, health, points, what to do when attacking, defending, etc. 
- 5/?/23: Made **anim.py**, which is a class that *loads* all spritesheets and data, *analyzes* animation JSONs, and *updates* frames; sprites use it as a reference to pull a spritesheet frame and use it in the sprite/set self.image to it. 
- 5/11/23: Used old sprite-gen program to make individual images into spritesheets and respective JSON files. 
- 5/11/23: Created new game folder; created outline files; created MAIN loop
- 4/17/23: Conceptualization begins

# TO DO / THOUGHT DUMP
## LEVELS
- [ ] Contain more background info, like speeds, changes in speed, 
- [x] Loading all JSON files
- [x] Loading a "world order" file in the levels folder (ignored by the level loader) that says what order the files go into 
## MISC 
- [x] Add gameplay elements from MAIN to State_Game_Play
- [x] Make the gameplay level acknowledge the playing field over the pygame window
## THE PLAYER
- [x] Barriers upon movement based on bar argument
- [x] Shooting with the space bar
- [x] Shooting bullet limit
- [x] Getting hurt if collided, which goes with the universal "on_collide" function in characters
- [x] Playing animations with jumping, hitting the wall, getting hit
## GAMEPLAY STATE / LEVELS
- Levels are loaded by the gameplay state. 
- The gameplay state does not exit and go to game over states, it just reruns \_\_init\_\_. 
- Characters do not individually run their own collision worries. This would be far too much code to run every frame. Instead, gameplay will individually check and run collision points for sprite classes whenever it is deemed fit. It worked for Shoot the Baby, it will work here.
# FUTURE OPTIMIZATION
- [ ] Main has some universal variables that slowly get annoying to pass around as arguments. Maybe I can make it so all classes have them as global variables and MAIN gives them out pre-declaration, instead of in __init__?
- [ ] States having a string element saying what state to go to next, for MAIN to recognize
- [ ] "Mod Folders" where the program has to recognize words with "anim_loadlist", "levels","order", etc. to plug into main.
# BUG REPORTS / ISSUES
## MENTAL
- I notice I struggle to organize my thoughts a lot. A good example is pseudocode.
- I was always able to just sit down and program something at once, as I am a very impulsive person.
- I've been working on it recently; I believe one of the largest issues was that I tried to imagine everything working all together, instead of modularly.
- I've been struggling by not following my own ideology, haha. 
