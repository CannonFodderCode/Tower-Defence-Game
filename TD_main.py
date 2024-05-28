FilePath = ("E:\Python code on VSC\Tower Defence\\")  # edit this string to reflect the current File path to Resources Folder
# Checklist to reccord progress and future targets
'''
            Done!
Lives - enemies cost 1 life when leaked - death at 0 - displayed on screen
tower placement guide
enemy hp scaling
money per kill + tower cost (gold) + new colour for invalid tower placement if gold is too low
add a "hold space tp place towers" instruction on screen (temporary)
add wave pattern + spawning loops
Different Tower types - Basic, Slammer, Trap
Tower info pannel when placing - cost (currently affordable?), damage, range, fire rate(rps)  - blit on other side of map to cursor.
Upgrade pannel implimented
Allow user to drag upgrade pannel to either side
new Towers index their info from the "~database~" (list)
add smart wave calling

            Next Steps:
buff items - tower amplifiers (maybe only 1 square instead of 2x2?)
Ballence Tower Upgrade prices and increaces. (maybe index (another) list)
draw tower bases first, then turrets, then range to prevent overlaps
re-order blit sequence to ensure important stuff (lives, money, etc) doesnt get overlapped!
make a display for gold, lives, hours spent debugging, waves, etc
gamestate screens - menu, play, PAUSE, tutorial, Upgrades, stats, etc  -  in progress

            later: (unprioritised)
Music?
SFX
Hide instructions inside a button/dropdown/PAUSE MENU instead of users_face.blit(instructions)
different enemies -pulse to disable towers for a time? -Fast -Armoured(-30% -2 damage modifier) -invisible when hit for 5s -BOSS BOI
different tower types  (Piercing shot, !necrotower!-(enemies that die in its range resurect as allies, 0 dmg), Missile launcher-(min. range?), shotgun tower, ice launcher-(slow effect), flame thrower-(cancels freeze))
? fuse tower types when in a 2x2 array and upgraded? (steal from BTTD series)
abilities to freeze enemies, buff towers in a zone, place blockades on tracks...
maybe not needed: launch config window before game (sepperate while loop) to allow user to choose a window size, then impliment a scale function for all rect objects

Potential Bugs:
Tower wasnt upgrading properly - no gold taken, cost display updating, not saved when diselected, no stats increase. No reliable way to reproduce found so far.
Poison damage doesnt stack.
'''
#           Instructions:
''' (big green button is start)
Hold space and press w to select a standard tower, press a to select a Slammer tower, click to place. drag the info box when selecting 
a tower to move it to the other side (click a tower to select its information, or press esc to close). Towers automatically shoot, you
can see your lives in the top left corner, Gold in the top right and wave information is displayed in the terminal. Waves scale up in 
difficulty and take a random pattern. Right click in the top right to change wave calling modes: RED = instant, YELLOW = when clear, 
WHITE = on demand (left click to call)
'''
import pygame, sys, time
from pygame.locals import *
from math import *
from random import *

pygame.init()

scr_wi = 800 # initial size of config window to ensure compatability with low-spec devices
scr_hi = 600

pygame.display.set_caption("screen size config")
disp = pygame.display.set_mode((scr_wi, scr_hi))

font = pygame.font.Font(None, 50)
smallfont = pygame.font.Font(None, 30)

mousedown = [False, False, False]  # indexing a list avoids cross-talk issues when detecting objects that cna be clicked with LMB or RMB
def clicked(item, mousebutton): # only returns true when the mouse is released (used for things that shouldnt be pressed 120 times per second...)
    global mousedown
    if mousedown[mousebutton] and not pygame.mouse.get_pressed()[mousebutton] and item.collidepoint(mouse):
        mousedown[mousebutton] = False
        return True # if it was pressed, and has just been released
    if not pygame.mouse.get_pressed()[mousebutton] and item.collidepoint(mouse):
        mousedown[mousebutton] = False
        return False
    elif pygame.mouse.get_pressed()[mousebutton] and item.collidepoint(mouse):
        mousedown[mousebutton] = True


intructions = font.render("Click your desired resolution", True, (255,255,0))

button720 = pygame.Surface((200, 80))
button720.fill((120,0,0))
t720 = font.render("1280x720", True, (255,255,255))  # small screen
button720.blit(t720, (5,5))
button720_rect = button720.get_rect(topleft = (5,60))

button1080 = pygame.Surface((200, 80))
button1080.fill((120,0,0))
t1080 = font.render("1920x1080", True, (255,255,255))  # standard screen
button1080.blit(t1080, (5,5))
button1080_rect = button1080.get_rect(topleft = (5,160))

button1440 = pygame.Surface((200, 80))
button1440.fill((120,0,0))
t1440 = font.render("2560x1440", True, (255,255,255))  # big screen
button1440.blit(t1440, (5,5))
button1440_rect = button1440.get_rect(topleft = (5,260))

fullscreen = pygame.Surface((200,100))
fullscreen.fill((255,0,0))
FS_text = font.render("Fullscreen", True, (255,255,255))
fullscreen.blit(FS_text, (2,2))
FS_text = smallfont.render("click to toggle", True, (255,255,255))
fullscreen.blit(FS_text, (2,53))
FS_Button = fullscreen.get_rect(topleft = (220, 60))
fullscreenBOOL = False

def make_FS_Button(Colour):
    fullscreen.fill(Colour)
    FS_text = font.render("Fullscreen", True, (255,255,255))
    fullscreen.blit(FS_text, (2,2))
    FS_text = smallfont.render("click to toggle", True, (255,255,255))
    fullscreen.blit(FS_text, (2,53))
    FS_Button = fullscreen.get_rect(topleft = (220, 60))

while True:
    mouse = pygame.mouse.get_pos()
    disp.fill((0,0,0))
    disp.blit(intructions, (5,5))
    disp.blit(button720, button720_rect)
    disp.blit(button1080, button1080_rect)
    disp.blit(button1440, button1440_rect)
    disp.blit(fullscreen, FS_Button)

    if clicked(FS_Button, 0):
        if fullscreenBOOL:
            make_FS_Button((255,0,0))
            fullscreenBOOL = False
        elif not fullscreenBOOL:
            make_FS_Button((0,255,0))
            fullscreenBOOL = True
    if button720_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
        end_hi = 720
        end_wi = 1280
        break
    elif button1080_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
        end_hi = 1080
        end_wi = 1920
        break
    elif button1440_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
        end_hi = 1440
        end_wi = 2560
        break

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

print(scr_wi, scr_hi, fullscreenBOOL)

disp = pygame.Surface((1920, 1080))  # creates a mock window at the hardcoded resolution to scale later

def scale(number):  # designed to scale mouse coordinates when playing in resolutions other than 1080p
    return (number / end_wi) * 1920

if True:  # Display setup
    scr_wi=1920  # Hard-coded resolution. gets scaled to the selected resolution before display update
    scr_hi=1080
    pygame.display.set_caption("Tower Defence")  # Title of window
    FPS=120
    FrPS=pygame.time.Clock()
    top_surface=pygame.Surface((scr_wi, scr_hi), pygame.SRCALPHA) # A Surface to blit shapes to, such as lines for laser shots (avoiding having to make sprites)
    font = pygame.font.Font(None, 50)
    info_font = pygame.font.Font(None, 40)
    BIGFont = pygame.font.Font(None, 140)

if fullscreenBOOL:
    final_window=pygame.display.set_mode((end_wi, end_hi), pygame.FULLSCREEN)
else:
    final_window=pygame.display.set_mode((end_wi, end_hi))

lives=3  # currently low for testing - should be 20
previous_lives = lives
gold = 50
if True:  # Wave marking, and spawn distribution
    wave = 1
    waveHP = int(20 + wave + (1.5*((wave**1.5)+2))*log(wave+2))
    wavestyle = (1, 15) # Wave 1. First item is spawn_delay[index], second is total enemies
    spawn_delay = [0.8, 0.5, 0.2] # [sparce, normal, dense] grouping
    wave_HPmodifier = [2.5, 1, 0.7]
    wavecomplete = True

# A list to be indexed from to grab tower info when creating new towers. will eventually become source for new tower stats (perminant upgrades)
Tower_info = [("Standard", 4, 2.5, 300, 10, "no special"), ("Slammer", 12, 1, 120, 18, "no special"), ("Trap", 2, 4, 40, 12, 20)]  #(Tower Name, Damg, FR (s/s), Range, Cost)

Instructions = font.render(str("Hold SPACE to place towers. W = Basic, A = Slammer"), True, (255,255,255))

if True: # Main Menu screen setup and buttons
    TitleScreen = pygame.image.load(FilePath + "bad Menu Screen.png")
    TitleScreen = pygame.transform.scale(TitleScreen, (scr_wi,scr_hi))
    PlayButton = pygame.Rect(1000, 800, 480, 200)
    UpgradesButton = pygame.Rect(1640, 800, 200, 200)
    PlayButtonText = BIGFont.render("GO", True, (255,255,255))

if True:  # Map 1 setup      
    map1=pygame.image.load(FilePath + "TD Map.png") # load in the path
    map1=pygame.transform.scale(map1,(scr_wi, scr_hi)) # scale the path
    map1NODES=[14,16,4,24,30,8,20,16,38,4,44,28] #given as a value for the updated coordinate ONLY. eg; y=currentY x=mapNODES[0]
    #map1pathbounding contains tuples, each using the cooridnates of (topleft-X,topleft-Y, bottomright-X, bottomright-Y), and is used for checking overlap weith the path when placing a tower
    map1pathbounding = [(0,120,600,200),(520,120,600,680),(120,600,600,680),(120,600,200,1000),(120,920,1240,1000),(1160,280,1240,1000),(760,280,1240,360),(760,280,840,680),(760,600,1560,680),(1480,120,1560,680),(1480,120,1800,200),(1720,120,1800,1080)]
    dist_per_node = [0, 600, 1080, 1480, 1800, 2840, 3480, 3880, 4200, 4920, 5400, 5640, 6520] # total distance from start point (used for target priority)

paths=[]
for item in map1pathbounding: # setting up rects for path collision checks caus i typed out the wrong set of info and CBA to change it
    width=item[2]-item[0]
    height=item[3]-item[1]
    path=pygame.Rect(item[0],item[1],width, height)
    paths.append(path)

#   MISC
def angle_finder(start, end): # returns the angle between 2 points in radians
    angle = atan2((end[1]-start[1]),(end[0]-start[0]))
    return(angle % (2*pi))

def in_range(tower, target):    # Checks if first inputs range covers the second object
    distance = tower.range# + target
    totaldistance=(sqrt(((tower.rect.centerx-target.rect.centerx)**2) + (tower.rect.centery-target.rect.centery)**2))
    if totaldistance<=distance:
        return True
    else:
        return False

#   TOWER PLACEMENT AND UPGRADING
selection=pygame.Surface((74,74), pygame.SRCALPHA) # a visual indicator for tower placement
def draw_placement_guide(colour, location, Range):
    selection.fill(colour) # fills RED is invalid, fills WHITE if valid
    TRange = Range
    coord=location
    rangeimage = pygame.Surface((TRange*2,TRange*2), pygame.SRCALPHA)
    rangeimage.fill((0,0,0,0))
    pygame.draw.circle(rangeimage, (255,255,255,10), (TRange,TRange), TRange)
    disp.blit(selection, location)
    disp.blit(rangeimage, (coord[0]+37-TRange, coord[1]+37-TRange))

if True: # Sets up info pannel loading
    target = None
    Upgrade_pos = "left" # required for upgrade pannel start
    dragged = False
    info = pygame.image.load(FilePath + "Info Pannel Infill.png")
    info = pygame.transform.scale(info, (360,800))
    back = pygame.image.load(FilePath + "Tower Info Pannel.png")
    back = pygame.transform.scale(back, (400,800))
    back_rect = back.get_rect(topleft = (0,120))
    Rback = pygame.transform.flip(back,True,False) # flips along X as to sit properly on other side of the screen
    text_pane = pygame.Surface((360,800),pygame.SRCALPHA)
    Upgrade_pannel_static = pygame.Surface((360,800),pygame.SRCALPHA)
    info_titles = ["Damage:","Fire Rate:","Range:"]
    Y_height = [370, 410, 450, 490]
    counter=0
    while counter < 3: # blits info_titles to their respective Y_height
        info_text = info_font.render(str(info_titles[counter]), True, (255,255,255))
        text_pane.blit(info_text, (45,Y_height[counter]))
        Upgrade_pannel_static.blit(info_text, (45,Y_height[counter]))
        counter += 1
    
    # loading in resources for updrage pannel (current tower selected)
    tower_upgrade_pannel = pygame.image.load(FilePath + "Tower Upgrade Pannel.png")
    tower_upgrade_pannel = pygame.transform.scale(tower_upgrade_pannel,(400, 960))
    Rtower_upgrade_pannel = pygame.transform.flip(tower_upgrade_pannel, True, False)
    tower_upgrade_infill = pygame.image.load(FilePath + "Tower Upgrade Infill.png")
    tower_upgrade_infill = pygame.transform.scale(tower_upgrade_infill, (360, 960))
    Rtower_upgrade_infill = pygame.image.load(FilePath + "Right Tower Upgrade Infill.png")
    Rtower_upgrade_infill = pygame.transform.scale(Rtower_upgrade_infill, (360 ,960))

    # Pannel surface creation
    Pannel = pygame.Surface((400, 800), pygame.SRCALPHA)
    upgrade_pannel = pygame.Surface((400, 960), pygame.SRCALPHA)

def get_info(tower_index):
    Surface = pygame.Surface((360,800),pygame.SRCALPHA) # new surface to clear old info when tower is changed
    Name = font.render(str(Tower_info[tower_index][0]), True, (100,150,255))
    Surface.blit(Name, (80,60))  # blits Name to Info pannel instance
    Cost = font.render(str(Tower_info[tower_index][4]), True, (0,0,0))
    Surface.blit(Cost, (110, 650))
    for i in range(1,4):
        item = font.render(str(Tower_info[tower_index][i]), True, (255,255,255))
        Surface.blit(item, (245, Y_height[i-1]))
    return Surface
Standard_info_pannel = get_info(0)
Slammer_info_pannel = get_info(1)
Trap_info_pannel = get_info(2)
poison = font.render(str(Tower_info[2][5]), True, (255,255,255))
poison_text = info_font.render(str("Poison:"), True, (255,255,255))
Trap_info_pannel.blit(poison, (245,490))
Trap_info_pannel.blit(poison_text, (45,490))

update = True
previous = 1
pannelposition=2 # Defaults to right side of the screen
def open_info():  # opens a tower info pannel away from the cursor when space is held while towers are being placed
    global pannelposition, previous, update
    if tower_index == 0:
        if previous != 0:
            update = True
        current_tower_info = Standard_info_pannel
        previous = 0
    elif tower_index == 1:
        if previous != 1:
            update = True
        current_tower_info = Slammer_info_pannel
        previous = 1
    elif tower_index == 2:
        if previous != 2:
            update = True
        current_tower_info = Trap_info_pannel
        previous = 2
    if pressed_keys[K_SPACE]:
        if pygame.mouse.get_pos()[0] > 2*scr_wi/3:
            if pannelposition != 1:
                update = True
            pannelposition = 1
        elif pygame.mouse.get_pos()[0] < scr_wi/3:
            if pannelposition != 2:
                update = True
            pannelposition = 2
        if pannelposition == 1:
            if update:
                Pannel.fill((0,0,0,0))
                Pannel.blit(back, (0,0)) #blit to left 
                Pannel.blit(info, (0,0))
                Pannel.blit(text_pane, (0,0))
                Pannel.blit(current_tower_info, (0,0))
                update = False
            disp.blit(Pannel, (0,120))
        elif pannelposition == 2: #if mouse got close to left side of screen last
            if update:
                Pannel.fill((0,0,0,0))
                Pannel.blit(Rback, (0,0))
                Pannel.blit(info, (40,0))
                Pannel.blit(text_pane, (40,0))
                Pannel.blit(current_tower_info, (40,0))
                update = False
            disp.blit(Pannel, (scr_wi-400,120))

tower_index = 0
def tower_select(index, location): # creates a tower at a location
    list = [Tower(location), Slammer(location), Trap(location)]
    return list[index]
target
def drag():  # allows the user to drag upgrade pannels to eithe side of the screen
    global Upgrade_pos, dragged, update
    if target != None:
        if back_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            dragged=True
        elif not pygame.mouse.get_pressed()[0]:
            dragged=False
        if dragged and mouse[0]<(scr_wi/3) and Upgrade_pos == "right":
            Upgrade_pos = "left"
            update = True
        elif dragged and mouse[0]>(2*scr_wi/3) and Upgrade_pos == "left":
            Upgrade_pos = "right"
            update = True

def select_tower(): # Allows the user to click on a tower to display an pannel with its info (and soon upgrades!)
    global target, gold, update
    text_pane = pygame.Surface((360,800),pygame.SRCALPHA)
    if pygame.mouse.get_pressed()[0] and not dragged:
        for tower in towers:
            if tower.rect.collidepoint(mouse):
                target = tower
                update = True
                break
    if target != None:
        if update:
            Name = font.render(str(target.name), True, (100,150,255))
            text_pane.blit(Name, (80,60))
            selected_tower_information = info_font.render(str(target.damage), True, (255,255,255))
            text_pane.blit(selected_tower_information, (245,Y_height[0]))
            selected_tower_information = info_font.render(str(target.shots_per_sec), True, (255,255,255))
            text_pane.blit(selected_tower_information, (245,Y_height[1]))
            selected_tower_information = info_font.render(str(target.range), True, (255,255,255))
            text_pane.blit(selected_tower_information, (245,Y_height[2]))
            if target.name.lower() == "trap":
                text_pane.blit(poison_text, (45,Y_height[3]))
                selected_tower_information = info_font.render(str(target.poison[0]), True, (255,255,255))
                text_pane.blit(selected_tower_information, (245,Y_height[3]))
        if not target.baserect.collidepoint(mouse): # prevents range being drawn twice as mouse if over the tower
            target.draw_range(disp)
        if Upgrade_pos=="left":
            if update:
                upgrade_pannel.fill((0,0,0,0))
                upgrade_pannel.blit(tower_upgrade_pannel, (0,0))
                upgrade_pannel.blit(tower_upgrade_infill, (0,0))
                upgrade_pannel.blit(Upgrade_pannel_static, (0,0))
                upgrade_pannel.blit(text_pane, (0,0))
                back_rect.left = 0
                sell_text = font.render(str(target.sellprice), True, (255,255,255))
                upgrade_pannel.blit(sell_text, (20, 900))
                Upgrade_text = font.render(str(target.upgrade_cost), True, (255,255,255))
                upgrade_pannel.blit(Upgrade_text, (100, 900))
                update = False
            sell_button = pygame.Rect(0, 920, 80, 160)
            disp.blit(upgrade_pannel, (0,120))
            if clicked(sell_button,0): # Tower sold
                sell(target)
                target = None
            Upgrade_button = pygame.Rect(80, 920, 160, 160)
            if clicked(Upgrade_button,0) and gold>=target.upgrade_cost:
                print(target.upgrade_cost, "upgrade cost")
                gold -= target.upgrade_cost
                update = True
                target.upgrade()
        elif Upgrade_pos == "right":
            if update:
                upgrade_pannel.fill((0,0,0,0))
                upgrade_pannel.blit(Rtower_upgrade_pannel, (0,0))
                upgrade_pannel.blit(Rtower_upgrade_infill, (40,0))
                upgrade_pannel.blit(Upgrade_pannel_static, (40,0))
                upgrade_pannel.blit(text_pane, (40,0))
                back_rect.right = scr_wi
                sell_text = font.render(str(target.sellprice), True, (255,255,255))
                upgrade_pannel.blit(sell_text, (340, 900))
                Upgrade_text = font.render(str(target.upgrade_cost), True, (255,255,255))
                upgrade_pannel.blit(Upgrade_text, (180, 900))
                update = False
            sell_button = pygame.Rect(1840,920, 80, 160)
            disp.blit(upgrade_pannel, (scr_wi-400, 120))
            if clicked(sell_button,0):
                sell(target)
                target = None
            Upgrade_button = pygame.Rect(1680, 920, 160, 160)
            if clicked(Upgrade_button,0) and gold>=target.upgrade_cost:
                gold -= target.upgrade_cost
                update = True
                target.upgrade()
        if pressed_keys[K_ESCAPE]:
            target=None

def sell(item):  # sell and delete towers
    global gold
    gold += item.sellprice
    towers.remove(item)
    towers_rects.remove(item.baserect)
    item.kill()

#   WAVE HANDLING
def new_wave():  # increases wave number, and selects its wave type & calculates the HP modifier
    global wave, waveHP, wavestyle, previous_lives, gold
    wave += 1
    wavestyle = (choice(((0, 10),(1, 15), (2, 25)))) #((dense, normal, or tightly grouped), total enemy count)
    waveHP = int(wave_HPmodifier[wavestyle[0]] * (20 + wave + int((1.5*((wave**1.5)+2))*log(wave+2)))) # provides a upward scaling that gets increasingly brutal, multiplied by HP modifier for wave type
    if previous_lives == lives:
        gold +=10     # No Lives Lost bonus gold per round
    else:
        previous_lives = lives
    print("new_wave was called")

def wavespawn(): # spawns each enemy in the wave, according to the wave type, then calls new_wave() when done
    global wavecomplete
    global timer
    global count
    if wavecomplete:
        timer = curtime
        count = wavestyle[1]
        wavecomplete = False
        print(f"count = {count} ... wave = {wave} ... waveHP = {waveHP}") # informs the user of enemy count & HP per wave
    while count > 0 and curtime-timer >= spawn_delay[wavestyle[0]]:  
        bob=enemy()
        enemies.add(bob)
        count -= 1
        timer=curtime
    #if count==0: # detects if there are any more enemies to spawn this wave
        #print("c")
        #new_wave()

update_button = True
button = pygame.Surface((100,100), pygame.SRCALPHA)
button_rect = button.get_rect(topleft=(10,10))
def PauseButton(state):
    global update_button
    if clicked(button_rect, 0):
        update_button = True
        if state == 1:
            state = 2
        elif state == 2:
            state = 1
    if state == 1 and update_button:
        button.fill((0,0,0,0))
        pygame.draw.line(button, (255,255,100),(20,0), (20,100),40)
        pygame.draw.line(button, (255,255,100),(80,0), (80,100),40)
        update_button = False
    if state == 2 and update_button:
        button.fill((0,0,0,0))
        pygame.draw.polygon(button, (255,255,100), [(0,0),(0,100),(100,50)],0)
        Update_button = False
    disp.blit(button, button_rect)
    return state

wave_list = ["auto wavesend", "when killed", "on click"]
wavesend = 2
wavesymbol = pygame.Surface((100,100), pygame.SRCALPHA)
wavesymbol.fill((255,255,255))
wavesymbol_button = wavesymbol.get_rect(topright = (scr_wi-10,10))
def wavebutton():
    global wavesend, count, wavecomplete
    if wavesend == 0:
        wavesymbol.fill((255,0,0))
        if count == 0: # instant wave calls - no gap
            new_wave()
            wavecomplete=True
    elif wavesend == 1:
        wavesymbol.fill((255,255,0))
        if len(enemies) == 0 and count == 0: # all enemies dead
            new_wave()
            wavecomplete=True
    elif wavesend == 2:
        wavesymbol.fill((255,255,255))
        if clicked(wavesymbol_button, 0) and count == 0:
            new_wave()
            wavecomplete=True
    if clicked(wavesymbol_button, 2): # RMB to adjust wave calling (red = auto, yellow = when all killed, white = manual send)
        wavesend = (wavesend+1) % 3
    disp.blit(wavesymbol, wavesymbol_button)

#   CLASSES
class enemy(pygame.sprite.Sprite):  # basic enemy. comes in groups, or tanky, or normal
    def __init__(self):
        super().__init__()
        self.image=pygame.Surface((20,20))
        self.image.fill((200,0,0))
        pygame.draw.polygon(self.image, (255,255,255), [(0,0), (0,19), (19,19), (19,0)],1)
        self.rect=self.image.get_rect()
        self.rect.centerx=-10
        self.rect.centery=((4+choice((-0.5, 0.5, 0)))*40)
        self.nodecount=0
        self.speed=10
        self.target=(((map1NODES[self.nodecount]+choice((-0.5, 0.5, 0)))*40),self.rect.centery)
        self.DistToNode=0
        #print("currenyly at:",self.rect.center, "heading for", self.target)
        self.progress=0
        self.nodecount+=1
        self.HP = waveHP
        self.value = 4   # PLACEHOLDER
        self.poison = []
        self.poisoned = False
    
    def draw(self, disp):
        disp.blit(self.image, self.rect)

    def pick_target(self):
        if (self.nodecount % 2) == 0:
            self.new_x = ((map1NODES[self.nodecount]+choice((-0.5, 0.5, 0)))*40)
            self.target=(self.new_x, self.rect.centery)
        else:
            self.new_y = ((map1NODES[self.nodecount]+choice((-0.5, 0.5, 0)))*40)
            self.target=(self.rect.centerx, self.new_y)
        self.nodecount+=1

    def move(self):
        if len(self.poison)>=1:      # Dealing with poison damage (total damage, damager per tick, time)
            if self.poisoned == False:
                self.poisoned = True
                self.image.fill((0,200,0))  # updates to a green colour
                pygame.draw.polygon(self.image, (255,255,255), [(0,0), (0,19), (19,19), (19,0)],1)
            for item in self.poison:
                self.HP -= item[1]
                item[0] -= item[1]
                if item[0] <= 0:
                    self.poison.remove(item)
                if item[2] <= curtime:
                    self.poison.remove(item)
        else:
            if self.poisoned == True: # remove the poisoned effect
                self.image.fill((200,0,0))
                pygame.draw.polygon(self.image, (255,255,255), [(0,0), (0,19), (19,19), (19,0)],1)
                self.poisoned = False
        if self.HP <= 0:
            self.kill()
            global gold
            gold += self.value
        if self.rect.centery>(scr_hi):
            global lives
            lives-=1
            self.kill()
        elif self.target[0]!= self.rect.centerx:  #check if hit the target destination on X axis
            if self.target[0]>self.rect.centerx: # traveling right
                self.rect.centerx += self.speed
            else: #traveling left
                self.rect.centerx -= self.speed
        elif self.target[1]!= self.rect.centery:  #check if hit the target destination on Y axis
            if self.target[1]>self.rect.centery: # traveling down
                self.rect.centery += self.speed
            else: # traveling up
                self.rect.centery -= self.speed
        elif self.rect.center==self.target:
            self.pick_target()
        self.update_distance() # tracks self.progres for tower targeting

    def update_distance(self):
        self.node_dist = dist_per_node[self.nodecount]
        self.next_dist = dist(self.target, self.rect.center) # calculating distance left to travel until next node is hit
        self.progress = self.node_dist - abs(self.next_dist) # taking the distnace to the next node away

class Tower(pygame.sprite.Sprite):  # standard Tower. basic, does the job. not exciting
    def __init__(self, location):
        super().__init__()
        #creation metrics
        self.name = Tower_info[0][0]
        self.damage = Tower_info[0][1]
        self.shots_per_sec = Tower_info[0][2]
        self.range = Tower_info[0][3]
        self.cost = Tower_info[0][4]
        self.ID = "Targeted"
        self.position = location
        self.turret_colour=(0,200,100)
        self.saved_range = self.range
        self.fire_rate = 1/self.shots_per_sec
        self.target = None
        self.shot_timer = curtime
        self.level = 1
        self.upgrade_cost = 6
        self.upgrade_costs = (0,6,14,26,40,58,80,115,160,230)
        self.sellprice = int(self.cost*0.8)
        #base setup
        self.baseimage = pygame.Surface((74,74))
        self.baseimage.fill((180,0,50))
        self.baserect = pygame.Rect(location[0]-38,location[1]-38, 80,80)
        self.baserect.center = location
        #range circle setup
        self.rangeimage = pygame.Surface((self.range*2,self.range*2), pygame.SRCALPHA)
        self.rangeimage.fill((0,0,0,0))
        self.rangerect = self.rangeimage.get_rect(center=self.position)
        pygame.draw.circle(self.rangeimage, (255,255,255,40), (self.range,self.range), self.range)
        #Turret barrel
        self.turret_orig_image=pygame.Surface((20,60),pygame.SRCALPHA)
        self.turret_orig_image.fill(self.turret_colour)
        self.turretrect=self.turret_orig_image.get_rect(center=self.baserect.center)
        self.turretimage=self.turret_orig_image
        self.turretrect.centery-=40 # stops the barrel derping out on spawn
        #turret mount Circle
        self.turret_mount_image=pygame.Surface((40,40),pygame.SRCALPHA)
        pygame.draw.circle(self.turret_mount_image,(0,150,75),(20,20), 20)
        self.turret_mount_rect=self.turret_mount_image.get_rect(center=self.position)

        self.rect=self.baserect

    def draw(self, disp):
        disp.blit(self.baseimage, (self.baserect[0]+3,self.baserect[1]+3))
        disp.blit(self.turretimage,self.turretrect)
        disp.blit(self.turret_mount_image, self.turret_mount_rect)
        mousex = scale(pygame.mouse.get_pos()[0])
        mousey = scale(pygame.mouse.get_pos()[1])
        if self.baserect.collidepoint(mousex, mousey):
            self.draw_range(disp)

    def draw_range(self, disp):
        if self.range != self.saved_range: # avoiding constant Surface creation. only happens when range updates
            self.rangeimage = pygame.Surface((self.range*2,self.range*2), pygame.SRCALPHA)
            self.rangeimage.fill((0,0,0,0))
            self.rangerect = self.rangeimage.get_rect(center=self.position)
            pygame.draw.circle(self.rangeimage, (255,255,255,40), (self.range,self.range), self.range)
            self.saved_range = self.range
        disp.blit(self.rangeimage, self.rangerect)

    def aim(self, target):
        self.turret_angle = 90-degrees(angle_finder(self.baserect.center, target.rect.center))
        self.turretimage = pygame.transform.rotate(self.turret_orig_image, self.turret_angle)
        self.turretrect = self.turretimage.get_rect()
        self.turretrect.centerx = self.baserect.center[0]+40*cos(radians(self.turret_angle-90)) # no radians prefix, or -90deg
        self.turretrect.centery = self.baserect.center[1]-40*sin(radians(self.turret_angle-90))
    
    def shoot(self):
        if curtime-self.shot_timer > self.fire_rate:
            turret_edge = (self.baserect.center[0]+75*cos(radians(self.turret_angle-90)),self.baserect.center[1]-75*sin(radians(self.turret_angle-90)))
            pygame.draw.line(top_surface,(0,0,255),turret_edge,self.target.rect.center,5)
            self.shot_timer = curtime
            if self.target.HP < self.damage:
                self.target.HP -= self.damage
                self.target = None
            else:
                self.target.HP -= self.damage

    def upgrade(self):
        self.cost += self.upgrade_cost
        self.level += 1
        self.damage = int(self.damage * 1.3)
        self.range = int(self.range * 1.1)
        self.shots_per_sec = round(self.shots_per_sec*1.2, 1)
        self.fire_rate = 1/self.shots_per_sec
        self.upgrade_cost = self.upgrade_costs[self.level]

class Slammer(pygame.sprite.Sprite): # High damage 360 degree hit area tower. no aiming.
    def __init__(self, location):
        super().__init__()
        self.name = Tower_info[1][0]
        self.damage = Tower_info[1][1]
        self.shots_per_sec = Tower_info[1][2]
        self.range = Tower_info[1][3]  # so smol.
        self.cost = Tower_info[1][4]
        self.sellprice = int(self.cost*0.8)
        self.ID = "NoTarget"
        self.position = location
        self.fire_rate = 1/self.shots_per_sec
        self.target = "NA" # cannot aim. hits everything.
        self.shot_timer = curtime
        self.saved_range = self.range
        self.spin = 1 # wheeeeeeee
        self.hit_circle = pygame.Surface((self.range*2,self.range*2), pygame.SRCALPHA)
        self.hit_circle.fill((0,0,0,0))
        self.level = 1
        self.upgrade_cost = 13
        pygame.draw.circle(self.hit_circle, (90,50,40,150), (self.range,self.range), self.range)
        self.hit_circle_rect = self.hit_circle.get_rect(center=location)
        #image setup
        self.image = pygame.Surface((74,74), SRCALPHA)
        self.image.fill((255,180,0))
        pygame.draw.circle(self.image, (255,255,0), (37,37), 37)
        self.baserect = pygame.Rect(location[0]-38,location[1]-38, 80,80)
        self.baserect.center = location
        self.rect = self.baserect
        #range circle setup
        self.rangeimage = pygame.Surface((self.range*2,self.range*2), pygame.SRCALPHA)
        self.rangeimage.fill((0,0,0,0))
        self.rangerect = self.rangeimage.get_rect(center=self.position)
        pygame.draw.circle(self.rangeimage, (255,255,255,40), (self.range,self.range), self.range)
        #spinny bit setup
        self.spinnybit = pygame.image.load(FilePath + "SpinnyBit.png")
        self.spinnybit = pygame.transform.scale(self.spinnybit,(60,60))
        self.spinnybit_rect = self.spinnybit.get_rect(center=location)
        self.rotated_spinnybit = self.spinnybit
        self.spinadjustment = 1
        
    def draw(self,disp):
        disp.blit(self.image, (self.baserect[0]+3,self.baserect[1]+3))
        disp.blit(self.rotated_spinnybit, self.spinnybit_rect)

        mousex = scale(pygame.mouse.get_pos()[0])
        mousey = scale(pygame.mouse.get_pos()[1])
        if self.baserect.collidepoint(mousex, mousey):
            self.draw_range(disp)

    def draw_range(self, disp):
        if self.range != self.saved_range: # avoiding constant Surface creation. only happens when range updates
            self.rangeimage = pygame.Surface((self.range*2,self.range*2), pygame.SRCALPHA)
            self.rangeimage.fill((0,0,0,0))
            self.rangerect = self.rangeimage.get_rect(center=self.position)
            pygame.draw.circle(self.rangeimage, (255,255,255,40), (self.range,self.range), self.range)
            self.saved_range = self.range
        disp.blit(self.rangeimage, self.rangerect)

    def aim(self):  # due to lack of targeting, this provides aesthetic flair by spinning the pattern on the tower is accordance with charge
        if curtime-self.shot_timer < self.fire_rate:
            self.spinadjustment += (curtime-self.shot_timer) * (self.shots_per_sec**2) * 1.5 # only increases in speed while tower is charging
        self.spin += self.spinadjustment
        self.rotated_spinnybit = pygame.transform.rotate(self.spinnybit, self.spin)
        self.spinnybit_rect = self.rotated_spinnybit.get_rect(center=self.position)

    def shoot(self):
        if curtime-self.shot_timer > self.fire_rate:
            disp.blit(self.hit_circle, self.hit_circle_rect)
            self.spinadjustment = 0 # resets spin and spin speed each time tower shoots
            for bob in enemies:
                if in_range(self, bob):
                    bob.HP -= self.damage
            self.shot_timer=curtime

    def upgrade(self):
        self.cost += self.upgrade_cost
        self.level += 1
        self.damage = int(self.damage * 1.3)
        self.range = int(self.range * 1.1)
        self.shots_per_sec = round(self.shots_per_sec*1.2, 1)
        self.fire_rate = 1/self.shots_per_sec
        self.upgrade_cost = int((2*(self.level+2)+6)*self.cost/10)
        self.hit_circle = pygame.Surface((self.range*2,self.range*2), pygame.SRCALPHA)
        self.hit_circle.fill((0,0,0,0))
        pygame.draw.circle(self.hit_circle, (90,50,40,150), (self.range,self.range), self.range)
        self.hit_circle_rect = self.hit_circle.get_rect(center=self.position)

class Trap(pygame.sprite.Sprite): # a tower that gets placed directly on the track and poisons enemies
    def __init__(self, location):
        super().__init__()
        # pull stats from list
        self.name = Tower_info[2][0]
        self.damage = Tower_info[2][1]
        self.shots_per_sec = Tower_info[2][2]
        self.fire_rate = 1/self.shots_per_sec
        self.range = Tower_info[2][3]
        self.saved_range = self.range
        self.rangerect = self.range
        self.cost = Tower_info[2][4]
        self.poison = [Tower_info[2][5],(Tower_info[2][5]/(FPS*5)), 5]   # (total damage, damager per frame, time)

        self.position = location
        self.level = 1
        self.upgrade_cost = 16
        self.sellprice = int(self.cost*0.8)
        self.ID = "NoClue"
        self.target = None
        self.shot_timer = curtime
        #base setup
        self.baseimage = pygame.Surface((74,74), pygame.SRCALPHA)
        self.baseimage.fill((0,255,0,100))
        self.baserect = pygame.Rect(location[0]- 38, location[1]-38, 80,80)
        self.baserect.center = location
        self.rect = self.baserect

    def draw(self, disp):
        disp.blit(self.baseimage, (self.baserect[0]+3,self.baserect[1]+3))
    
    def draw_range(self, disp): # just here to allow compatibility with other functions
        pass

    def aim(self, target):
        pass
    
    def shoot(self):
        if in_range(self,self.target) and curtime-self.shot_timer>self.fire_rate:
            self.shot_timer = curtime
            if self.target.HP < self.damage:
                self.target.HP -= self.damage
                self.target = None
            else:
                self.target.HP -= self.damage
                self.target.poison.append([self.poison[0],self.poison[1], curtime+self.poison[2]])
    
    def upgrade(self):
        self.cost += self.upgrade_cost
        self.level += 1
        self.damage = int(self.damage * 1.3)
        self.range = int(self.range * 1.1)
        self.shots_per_sec = round(self.shots_per_sec*1.2, 1)
        self.fire_rate = 1/self.shots_per_sec
        self.poison[0] = self.poison[0] * 1.3
        self.poison[2] += 1
        self.poison[1] = self.poison[0]/(FPS*self.poison[2])
        self.upgrade_cost = int((2*(self.level+2)+6)*self.cost/10)

class Amplifier(pygame.sprite.Sprite):  # a 1x1 block that increases the stats of the towers around it
    def __init__(self, location):
        super().__init__()
        self.position = location
        self.image = pygame.Surface((40,40),pygame.SRCALPHA)
        self.image.fill((255,0,0))
        self.baserect = self.image.get_rect(center = self.position)
        self.effect_range = pygame.Rect(location[0]-5, location[1]-5, 50,50)
        self.level = 1
        self.cost = 12
        self.upgrade_cost = 8

        self.damageboost = 1.05
        self.rangeboost = 1.07
        self.FRboost = 1.07
        self.specialboost = 1.10

    def draw(self, disp):
        disp.blit(self.image, self.baserect)

class upgradesparks(pygame.sprite.Sprite):    # a visual indicator of when a tower is upgraded (a few green dots that fade away)
    def __init__(self, location):
        super().__init__()
        self.clock = 0.8    # expires after 0.8 seconds
        self.colour = (0,255,0)
        self.image = pygame.Surface((5, 5), pygame.SRCALPHA)
        self.image.fill((0,0,0,0))
        pygame.draw.circle(self.image, (self.colour), (2.5,2.5), 2.5)
        self.rect = self.image.get_rect(center = location)

    def draw(self, disp):
        self.liveimage = pygame.transform.scale(self.image,(self.clock*(5/0.8)))
        disp.blit(self.image, self.rect)

class Mouse(pygame.sprite.Sprite):  # used to detect if tower placement is valid
    def __init__(self):
        super().__init__()
        self.image=pygame.Surface((41,41),pygame.SRCALPHA) #41x41 is exact pixels required to always allow valid placement, but never allow path placement
        self.image.fill((0,0,0,0))
        self.rect=self.image.get_rect()

    def update(self, pos):
        self.rect.center=pos
        disp.blit(self.image, self.rect)

class mousetrackerthingie(pygame.sprite.Sprite): # Used for debugging across different resolution scalings.
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((5,5))
        self.image.fill((255,255,255))

    def update(self, location):
        disp.blit(self.image, location)

towers=pygame.sprite.Group()
enemies=pygame.sprite.Group()
clock=time.time()
mouse_track=Mouse()
timer=0
towers_rects=[]
curtime = time.time()
#thingiemajig = mousetrackerthingie()  # Cursor Debugging

state = 0    # (0-Menu, 1-Game, 2-Paused, 3-Upgrades)


while True:
    curtime=time.time()
    pressed_keys=pygame.key.get_pressed()
    mouse = (int(scale(pygame.mouse.get_pos()[0])), int(scale(pygame.mouse.get_pos()[1])))
    #print(f"{pygame.mouse.get_pos()} before scaling, {mouse} after scaling")
    if state == 0: # Main Menu
        disp.blit(TitleScreen, (0,0))
        disp.blit(PlayButtonText, (1165, 860))
        if PlayButton.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            state = 1
        elif UpgradesButton.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            state = 3
    elif state == 1:  # MAIN LOOPYDOOP
        top_surface.fill((0,0,0,0)) # clears the surface of shots fired previously
        if True: # Handling all text to display per frame
            disp.blit(map1, (0,0)) # push background image
            livescounter = font.render(str(f"Lives: {lives} |  Wave: {wave}    "), True, (255,255,255)) # update the lives
            disp.blit(livescounter,(120,10)) # display lives on screen
            disp.blit(Instructions,(600,10))
            gold_readout=font.render(str(gold), True, (255,255,100))
            gold_rect=gold_readout.get_rect(topright=(scr_wi-120,10))
            disp.blit(gold_readout,gold_rect)
        if pressed_keys[K_SPACE]:
            if pressed_keys[K_w]:  # w for standard
                tower_index = 0
            elif pressed_keys[K_a]:# a for slammer
                tower_index = 1
            elif pressed_keys[K_s]:# s for trap
                tower_index = 2
            mouse_track.update(mouse)
            location=((((mouse[0]+20)//40)*40),((mouse[1]+20)//40)*40) # locks placement to a 40px grid, and averages the center of the tower to the mouse position
            if tower_index == 2:
                for item in paths:
                    if mouse_track.rect.right <= item.right and mouse_track.rect.left >= item.left and mouse_track.rect.top >= item.top and mouse_track.rect.bottom <= item.bottom and (mouse_track.rect.collidelist(towers_rects)== -1):
                        placement_is_good = True
                        if gold >= Tower_info[2][4]:
                            draw_placement_guide((255,255,255,50),(location[0]-37, location[1]-37),Tower_info[tower_index][3])
                            if pygame.mouse.get_pressed()[0] and curtime-clock>0.1:
                                gold-= Tower_info[tower_index][4] # removes tower price from funds
                                new_tower = tower_select(tower_index, location) #Tower(location)
                                towers.add(new_tower) 
                                towers_rects.append(new_tower.baserect) # keeps track of where towers are for      efficient tower placement validation
                                clock=curtime
                            break # break to stop red being drawn over the top when checking next path - also helps performance
                        else:
                            draw_placement_guide((255,255,0,50),(location[0]-37, location[1]-37),Tower_info[tower_index][3])
                            break
                    else:
                        placement_is_good = False
                if not placement_is_good:
                    draw_placement_guide((255,0,0,50),(location[0]-37, location[1]-37),Tower_info[tower_index][3])
                    placement_is_good = True

            elif ((mouse_track.rect.collidelist(paths)!=-1) or (mouse_track.rect.collidelist(towers_rects)!=-1)): # checks if tower would be blocked by other tower or path
                draw_placement_guide((255,0,0,50),(location[0]-37, location[1]-37),Tower_info[tower_index][3])
            elif (gold-Tower_info[tower_index][4]) <0: # checks cost of selection against funds
                draw_placement_guide((255,255,0,50),(location[0]-37, location[1]-37),Tower_info[tower_index][3])
            else:
                if tower_index != 2:
                    draw_placement_guide((255,255,255,50),(location[0]-37, location[1]-37),Tower_info[tower_index][3]) # draws a WHITE box where tower will appear
                    if pygame.mouse.get_pressed()[0] and curtime-clock>0.1:    
                        gold-= Tower_info[tower_index][4] # removes tower price from funds
                        new_tower = tower_select(tower_index, location) #Tower(location)
                        towers.add(new_tower) 
                        towers_rects.append(new_tower.baserect) # keeps track of where towers are for      efficient tower placement validation
                        clock=curtime
        wavespawn()  # handles spawning of enemies, progression of waves, HP scaling
        wavebutton()
        for bob in enemies: # move and draw enemies
            bob.move()
            if bob.rect.colliderect(mouse_track):
                HP_readout = font.render(str(bob.HP), True, (255,255,255),(0,0,0,50))
                disp.blit(HP_readout, (scr_wi//2,scr_hi//2))
            bob.draw(disp)
        for tower in towers: # aims at target, draws tower, shoots
            if tower.ID == "NoTarget":
                tower.aim()
                for bob in enemies:
                    if in_range(tower, bob):  # only pulses when 1+ enemy is near
                        tower.shoot()
                        break
            elif tower.target==None or not in_range(tower, tower.target): # if no valid target
                for bob in enemies:
                    if tower.target==None:
                        tower.target=bob
                    if in_range(tower, bob) and tower.target!= None: # checks if enemy is in range (also avoids checking None.progress to avoid errors)
                        if bob.progress>tower.target.progress or not in_range(tower, tower.target): # gets the furthest enemy along thats currently in range
                            tower.target=bob
                            tower.aim(bob)
            elif in_range(tower, tower.target):   # keeps on target if its still in range
                tower.aim(tower.target)
                tower.shoot()
            tower.draw(disp)
        if lives == 0:
            print("you loose")
            pygame.quit()
            sys.exit()
        disp.blit(top_surface,(0,0)) # draws all tower shots
        open_info()
        drag()
        if not pressed_keys[K_SPACE]:
            select_tower()
        state = PauseButton(state)
    elif state == 2:
        state = PauseButton(state)
        pass # PAUSE    -not yet (fully) implimented
    elif state == 3:
        disp.fill((0,0,0)) # UPGRADES    -not yet implimented
        text = font.render("Page not yet implimented, click to go back", True, (255,255,255))
        disp.blit(text, (20, scr_hi//2))
        if pygame.mouse.get_pressed()[0]:
            state = 0
    for event in pygame.event.get(): #standard quit check loop...
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
    #thingiemajig.update(mouse) # Cursor Debugging
    pygame.transform.scale(disp, (end_wi,end_hi),final_window)
    pygame.display.flip()
    FrPS.tick(FPS)
