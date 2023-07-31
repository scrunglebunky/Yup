# WELCOME TO YUP
## WHAT IS YUP?
- Yup is a small shoot-em-up game that takes heavy referencing off of games like Galaga, Astro Warrior, and some other classics.
- Everything within the game is an attempt to stay modular, with each part being its own file, class, or function for me to use in other projects.
- This is the fourth iteration of the game. In the third one, I got too obsessed with optimization and changing everything up.
- This is my last attempt: a refresher that ensures that I make a simple, intuitive game that I do not overthink about.

# YUP DEVLOG
## PART ONE- GETTING IT ALL TOGETHER
- 7/31/23: started working on title screen
- 7/31/23: made high score graphics that are able to be used in the game
- 7/31/23: revamped text values into sprites that can be now handled separately
- 7/23/23: added a pause menu
- 7/??/23: added an options screen
- 7/10/23: Removed old and bad sprites, replaced with simple shapes | tweaked anim | started working on config file | backgrounds move with character optionally
- 6/30/23: made the configuration file usable
- 6/30/23: made the screen and play dimensions resizeable, changed original resolution to 600x800 but scaled down
- 6/24/23: FIXED THE FPS ISSUE
- 6/24/23: sounds load and play now ; loading failsafe in place
- 6/23/23: state_play's window now works as a separate surface that can be drawn to the window on its own, allowing for borders to now work.
- 6/23/23: Formations can now randomly generate as well as manually generate, chances and specific details for formation modes now work
- 6/22/23: Made it so manual formations will now loop 
- 6/22/23: Made formations actually spawn the correct characters
- 6/22/23: (originally 6/20/23) images can now be resized, the ui bar is its own class in its own file
- 6/18/23: formations now respawn when the level is completed
- 6/06/23: changed animations to return surface ; fixed player invincibility bug
- 6/06/23: formation spawns characters, makes characters attack, and checks for fomration completion
- 6/05/23: added level documentation docstring for reference, as there's a lot of options ; used level to change dymanic intensities or whatnot ; made the level file decide everything in a bg
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
- [ ] Make text and logos able to become its own state - used for the bar, and all the states - These will be able to be animated and move from place to place.
- [x] A second value that can be added to the state, specifically for options to know what to return to. 
- [ ] implement changes in intensity
- [x] sending characters into attack mode
- [x] starting a new level when the formation is empty
- [x] figure out what makes bg lag so bad
- [ ] actually implement background changes in speed
- [x] Contain more background info, like speeds, changes in speed, 
- [x] Loading all JSON files
- [x] Loading a "world order" file in the levels folder (ignored by the level loader) that says what order the files go into 
- [x] Add gameplay elements from MAIN to State_Game_Play
- [x] Make the gameplay level acknowledge the playing field over the pygame window
- [x] Add lives
- [ ] Let the player die 
- [x] Barriers upon movement based on bar argument
- [x] Shooting with the space bar
- [x] Shooting bullet limit
- [x] Getting hurt if collided, which goes with the universal "on_collide" function in characters
- [x] Playing animations with jumping, hitting the wall, getting hit
- [x] Loop formations or create new ones if there are no more formations left
- [x] Recognize a completed level and start a new one
- [ ] Recognize a completed world and start a new one
- Levels are loaded by the gameplay state. 
- The gameplay state does not exit and go to game over states, it just reruns \_\_init\_\_. 
- Characters do not individually run their own collision worries. This would be far too much code to run every frame. Instead, gameplay will individually check and run collision points for sprite classes whenever it is deemed fit. It worked for Shoot the Baby, it will work here.
- [ ] Main has some universal variables that slowly get annoying to pass around as arguments. Maybe I can make it so all classes have them as global variables and MAIN gives them out pre-declaration, instead of in __init__?
- [ ] States having a string element saying what state to go to next, for MAIN to recognize
- [ ] "Mod Folders" where the program has to recognize words with "anim_loadlist", "levels","order", etc. to plug into main.
## SEPARATE -- NEW CHARACTER WORLD MAP
- There will now be five classes for each formation made, for the characters to now each fly in together
- - A (turret), B (generic), C (kamikazee). D (special), E (optional) (special2)
- Instead of spawning each character in individually to a set pace, the characters will each rush in in their own pattern, together.
- 


# BUG REPORTS / ISSUES
## BACKGROUNDS
- With the background 'draw' function, the max framerate drops from 3000 to 250. It is incredibly unoptimized but I do not know what to do about it.
## MENTAL
- I notice I struggle to organize my thoughts a lot. A good example is pseudocode.
- I was always able to just sit down and program something at once, as I am a very impulsive person.
- I've been working on it recently; I believe one of the largest issues was that I tried to imagine everything working all together, instead of modularly.
- I've been struggling by not following my own ideology, haha. 
