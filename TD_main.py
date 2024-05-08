# Checklist to reccord progress and future targets
'''
Done!
Lives - enemies cost 1 life when leaked - death at 0 - displayed on screen
tower placement guide
enemy hp scaling
money per kill + tower cost (gold) + new colour for invalid tower placement if gold is too low
add a "hold space tp place towers" instruction on screen (temporary)
add wave pattern + spawning loops
Different Tower types - Basic, Slammer
Tower info pannel when placing - cost (currently affordable?), damage, range, fire rate(rps)  - blit on other side of map to cursor.
Upgrade pannel implimented
FIX THE SPINNY BIT ON SLAMMER
for upgrade pannel: if mouse collide with self.rect: dragged = True if mouseX the other side and dragged swap sides. if mouse not down dragged=False
new Towers index their info from the "~database~" (list)

Next Steps:

IMPROVE PANNEL PERFOMANCE! -scan for changes to avoid re-encoding text each frame? -Avoid creating new surfaces over 100 times a second.

draw tower bases first, then turrets, then range to prevent overlaps
FIX - when selected and hovered over, tower tange draws twice
re-order blit sequence to ensure important stuff (lives, money, etc) doesnt get overlapped!
make a display for gold, lives, hours spent debugging, waves, etc
        gamestate screens - menu, play, PAUSE, tutorial, Upgrades, stats, etc

later: (unprioritised)
Music?
SFX
Hide instructions inside a button/dropdown/PAUSE MENU instead of users_face.blit(instructions)
tower upgrades (both in-game and perminent "research" style)
different enemies -pulse to disable towers for a time? -Fast -Armoured(-30% -2 damage modifier) -invisible when hit for 5s -BOSS BOI
different tower types  (Trap-(1x2 either side of track, covers the 2x2 square on track), Piercing shot, !necrotower!-(enemies that die in its range resurect as allies, 0 dmg), Missile launcher-(min. range?), shotgun tower, ice launcher-(slow effect), flame thrower-(cancels freeze))
buff items - tower amplifiers (maybe only 1 square instead of 2x2?)
? fuse tower types when in a 2x2 array and upgraded? (steal from BTTD series)
abilities to freeze enemies, buff towers in a zone, place blockades on tracks...
launch config window before game (sepperate while loop) to allow user to choose a window size, then impliment a scale function for all rect objects

add smart wave calling (if len(enemies)==0, if wave_spawn counter==wavestyle[1], or instantly (currently the only one used))
'''
# Instructions:
''' (big green button is start)
Hold space and press w to select a standard tower, press a to select a Slammer tower, click to place. drag the info box when selecting 
a tower to move it to the other side (click a tower to select its information, or press esc to close). Towers automatically shoot, you
can see your lives in the top left corner, Gold in the top right and wave information is displayed in the terminal. Waves scale up in 
dificulty and take a random pattern
'''
import pygame, sys, time
from pygame.locals import *
from math import *
from random import *

pygame.init()

if True:  # Display setup
    scr_wi=1920
    scr_hi=1080
    disp=pygame.display.set_mode((scr_wi, scr_hi))
    pygame.display.set_caption("Tower Defence")  # Title of window
    FPS=120
    FrPS=pygame.time.Clock()
    top_surface=pygame.Surface((scr_wi, scr_hi), pygame.SRCALPHA) # A Surface to blit shapes to, such as lines for laser shots (avoiding having to make sprites)
    font = pygame.font.Font(None, 50)
    info_font = pygame.font.Font(None, 40)

lives=3  # currently low for testing - should be 20
gold = 50
if True:  # Wave marking, and spawn distribution
    wave = 1
    waveHP = int(20 + wave + (1.5*((wave**1.5)+2))*log(wave+2))
    wavestyle = (1, 15) # Wave 1. First item is spawn_delay[index], second is total enemies
    spawn_delay = [0.8, 0.5, 0.2] # [sparce, normal, dense] grouping
    wave_HPmodifier = [2.5, 1, 0.7]
    wavecomplete = True

# A list to be indexed from to grab tower info when creating new towers. will eventually become source for new tower stats (perminant upgrades)
Tower_info = [("Standard", 5, 3, 300, 10), ("Slammer", 12, 1, 120, 18)]  #(Tower Name, Damg, FR (s/s), Range, Cost)

Instructions = font.render(str("Hold SPACE to place towers. W = Basic, A = Slammer"), True, (255,255,255))

if True: # Main Menu screen setup and buttons
    TitleScreen = pygame.image.load(r"E:\Python code on VSC\Tower Defence\bad Menu Screen.png")  # formatted as raw to avoid string commands (\b)
    TitleScreen = pygame.transform.scale(TitleScreen, (scr_wi,scr_hi))
    PlayButton = pygame.Rect(1000, 800, 480, 200)
    UpgradesButton = pygame.Rect(1640, 800, 200, 200)

if True:  # Map 1 setup      
    map1=pygame.image.load("E:\Python code on VSC\Tower Defence\TD Map.png") # load in the path
    map1=pygame.transform.scale(map1,(scr_wi, scr_hi)) # scale the path
    map1NODES=[14,16,4,24,30,8,20,16,38,4,44,28] #given as a value for the updated coordinate ONLY. eg; y=currentY x=mapNODES[0]
    #map1pathbounding contains tuples, each using the cooridnates of (topleft-X,topleft-Y, bottomright-X, bottomright-Y), and is used for checking overlap weith the path when placing a tower
    map1pathbounding = [(0,120,600,200),(520,200,600,680),(120,600,520,680),(120,680,200,1000),(200,920,1240,1000),(1160,280,1240,920),(760,280,1160,360),(760,360,840,680),(840,600,1560,680),(1480,120,1560,600),(1560,120,1800,200),(1720,200,1800,1080)]
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

def in_range(ob1, ob2):    # Checks if first inputs range covers the second object
    distance = ob1.range# + ob2
    totaldistance=(sqrt(((ob1.rect.centerx-ob2.rect.centerx)**2) + (ob1.rect.centery-ob2.rect.centery)**2))
    if totaldistance<=distance:
        return True
    else:
        return False

mousedown = False
def clicked(item): # only returns true when the mouse is released (used for things that shouldnt be pressed 120 times per second...)
    global mousedown
    if mousedown and not pygame.mouse.get_pressed()[0] and item.collidepoint(mouse):
        mousedown = False
        return True
    if not pygame.mouse.get_pressed()[0] and item.collidepoint(mouse):
        mousedown = False
        return False
    elif pygame.mouse.get_pressed()[0] and item.collidepoint(mouse):
        mousedown = True

#   TOWER PLACEMENT AND UPGRADING
selection=pygame.Surface((74,74), pygame.SRCALPHA) #a visual indicator for tower placement
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
    info = pygame.image.load("E:\Python code on VSC\Tower Defence\Info Pannel Infill.png")
    info = pygame.transform.scale(info, (360,800))
    back = pygame.image.load("E:\Python code on VSC\Tower Defence\Tower Info Pannel.png")
    back = pygame.transform.scale(back, (400,800))
    back_rect = back.get_rect(topleft = (0,120))
    Rback = pygame.transform.flip(back,True,False) # flips along X as to sit properly on other side of the screen
    text_pane = pygame.Surface((360,800),pygame.SRCALPHA)
    Upgrade_pannel_static = pygame.Surface((360,800),pygame.SRCALPHA)
    info_titles = ["Damage:","Fire Rate:","Range:"]
    Y_height = [370, 410, 450]
    counter=0
    while counter < 3: # blits info_titles to their respective Y_height
        info_text = info_font.render(str(info_titles[counter]), True, (255,255,255))
        text_pane.blit(info_text, (45,Y_height[counter]))
        Upgrade_pannel_static.blit(info_text, (45,Y_height[counter]))
        counter += 1
    
    # loading in resources for updrage pannel (current tower selected)
    tower_upgrade_pannel = pygame.image.load("E:\Python code on VSC\Tower Defence\Tower Upgrade Pannel.png")
    tower_upgrade_pannel = pygame.transform.scale(tower_upgrade_pannel,(400, 960))
    Rtower_upgrade_pannel = pygame.transform.flip(tower_upgrade_pannel, True, False)
    tower_upgrade_infill = pygame.image.load("E:\Python code on VSC\Tower Defence\Tower Upgrade Infill.png")
    tower_upgrade_infill = pygame.transform.scale(tower_upgrade_infill, (360, 960))
    Rtower_upgrade_infill = pygame.image.load("E:\Python code on VSC\Tower Defence\Right Tower Upgrade Infill.png")
    Rtower_upgrade_infill = pygame.transform.scale(Rtower_upgrade_infill, (360 ,960))

pannelposition=2 # Defaults to right side of the screen
def open_info():  # opens a tower info pannel away from the cursor when space is held while towers are being placed
    global pannelposition
    current_tower_info = pygame.Surface((360,800),pygame.SRCALPHA) # new surface to clear old info when tower is changed
    Name = font.render(str(Tower_info[tower_index][0]), True, (100,150,255))
    current_tower_info.blit(Name, (80,60))  # blits Name to Info pannel instance
    Cost = font.render(str(Tower_info[tower_index][4]), True, (0,0,0))
    current_tower_info.blit(Cost, (110, 650))
    for i in range(1,4):
        item = font.render(str(Tower_info[tower_index][i]), True, (255,255,255))
        current_tower_info.blit(item, (245, Y_height[i-1]))
    if pressed_keys[K_SPACE]:
        if pygame.mouse.get_pos()[0] > 2*scr_wi/3:
            pannelposition = 1
        elif pygame.mouse.get_pos()[0] < scr_wi/3:
            pannelposition = 2
        if pannelposition == 1: #if mouse got close to right side of screen last
            back_rect = back.get_rect(topleft = (0,120))
            disp.blit(back, back_rect) #blit to left
            disp.blit(info, (0,120))
            disp.blit(text_pane, (0, 120))
            disp.blit(current_tower_info, (0, 120))
        elif pannelposition == 2: #if mouse got close to left side of screen last
            back_rect = Rback.get_rect(topright = (scr_wi,120))
            disp.blit(Rback, back_rect) #blit to right
            disp.blit(info, (scr_wi-360, 120))
            disp.blit(text_pane, (scr_wi-360, 120))    
            disp.blit(current_tower_info, (scr_wi-360, 120))                

tower_index = 0
def tower_select(index, location): # creates a tower at a location
    list = [Tower(location), Slammer(location)]
    return list[index]

def drag():  # allows the user to drag upgrade pannels to eithe side of the screen
    global Upgrade_pos, dragged
    if target != None:
        if back_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            dragged=True
        elif not pygame.mouse.get_pressed()[0]:
            dragged=False
        if dragged and mouse[0]<(scr_wi/3) and Upgrade_pos == "right":
            Upgrade_pos = "left"
        elif dragged and mouse[0]>(2*scr_wi/3) and Upgrade_pos == "left":
            Upgrade_pos = "right"

def select_tower(): # Allows the user to click on a tower to display an pannel with its info (and soon upgrades!)
    global target, gold
    text_pane = pygame.Surface((360,800),pygame.SRCALPHA)
    if pygame.mouse.get_pressed()[0] and not dragged:
        for tower in towers:
            if tower.rect.collidepoint(mouse):
                target = tower
                break
    if target != None:
        Name = font.render(str(target.name), True, (100,150,255))
        text_pane.blit(Name, (80,60))
        selected_tower_information = info_font.render(str(target.damage), True, (255,255,255))
        text_pane.blit(selected_tower_information, (245,Y_height[0]))
        selected_tower_information = info_font.render(str(target.shots_per_sec), True, (255,255,255))
        text_pane.blit(selected_tower_information, (245,Y_height[1]))
        selected_tower_information = info_font.render(str(target.range), True, (255,255,255))
        text_pane.blit(selected_tower_information, (245,Y_height[2]))
        target.draw_range(disp)
        if Upgrade_pos=="left":
            disp.blit(tower_upgrade_pannel, (0,120))
            disp.blit(tower_upgrade_infill, (0,120))
            disp.blit(Upgrade_pannel_static, (0,120))
            disp.blit(text_pane, (0,120))
            back_rect.left = 0
            sell_text = font.render(str(target.sellprice), True, (255,255,255))
            disp.blit(sell_text, (20, scr_hi-60))
            Upgrade_text = font.render(str(target.upgrade_cost), True, (255,255,255))
            disp.blit(Upgrade_text, (100, scr_hi-60))
            sell_button = pygame.Rect(0, 920, 80, 160)
            if clicked(sell_button): # Tower sold
                sell(target)
                target = None
            Upgrade_button = pygame.Rect(80, 920, 160, 160)
            if clicked(Upgrade_button) and gold>=target.upgrade_cost:
                print(target.upgrade_cost, "upgrade cost")
                gold -= target.upgrade_cost
                target.upgrade()
                print(target.level)
        elif Upgrade_pos == "right":
            disp.blit(Rtower_upgrade_pannel, ((scr_wi-400),120))
            disp.blit(Rtower_upgrade_infill, ((scr_wi-360),120)) 
            disp.blit(Upgrade_pannel_static, ((scr_wi-360),120))
            disp.blit(text_pane, ((scr_wi-360),120))
            back_rect.right = scr_wi
            sell_text = font.render(str(target.sellprice), True, (255,255,255))
            disp.blit(sell_text, (scr_wi-60, scr_hi-60))
            Upgrade_text = font.render(str(target.upgrade_cost), True, (255,255,255))
            disp.blit(Upgrade_text, (scr_wi-220, scr_hi-60))
            sell_button = pygame.Rect(1840,920, 80, 160)
            if clicked(sell_button):
                sell(target)
                target = None
            Upgrade_button = pygame.Rect(1680, 920, 160, 160)
            if clicked(Upgrade_button) and gold>=target.upgrade_cost:
                print(target.upgrade_cost, "upgrade cost")
                gold -= target.upgrade_cost
                target.upgrade()
                print(target.level)
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
    global wave, waveHP, wavestyle
    wave += 1
    wavestyle = (choice(((0, 10),(1, 15), (2, 25)))) #((dense, normal, or tightly grouped), total enemy count)
    waveHP = int(wave_HPmodifier[wavestyle[0]] * (20 + wave + int((1.5*((wave**1.5)+2))*log(wave+2)))) # provides a upward scaling that gets increasingly brutal, multiplied by HP modifier for wave type

def wavespawn(): # spawns each enemy in the wave, according to the wave type, then calls new_wave() when done
    global wavecomplete
    global timer
    global count
    if wavecomplete:
        timer = curtime
        count = wavestyle[1]
        wavecomplete = False
        print(f"count = {count} ... wave = {wave} ... waveHP = {waveHP}") # informs the user of enemy count & HP per wave
    while count>0 and curtime-timer>= spawn_delay[wavestyle[0]]:  
        bob=enemy()
        enemies.add(bob)
        count-=1
        timer=curtime
    if count==0: # detects if there are any more enemies to spawn this wave
        wavecomplete=True
        new_wave()

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
        #print(self.nodecount, "<node   -   Distance>", self.progress)            # commented out while not debugging path
        #print(f"currently at {self.rect.center} aiming for: {self.target}")

    def move(self):
        if self.HP<=0:
            self.kill()
            global gold
            gold += self.value             #################################### add MONEH ###################################
        if self.rect.centery>(scr_hi):
            global lives
            lives-=1
            self.kill()
        elif self.target[0]!= self.rect.centerx:  #check if (x = target x)
            if self.target[0]>self.rect.centerx: # traveling right
                self.rect.centerx += self.speed
            else: #traveling left
                self.rect.centerx -= self.speed
        elif self.target[1]!= self.rect.centery:
            if self.target[1]>self.rect.centery: # traveling down
                self.rect.centery += self.speed
            else: # traveling up
                self.rect.centery -= self.speed
        elif self.rect.center==self.target:
            self.pick_target()
        self.update_distance()

    def update_distance(self):
        self.node_dist = dist_per_node[self.nodecount]
        self.next_dist = dist(self.target, self.rect.center) # calculating distance left to travel until next node is hit
        self.progress = self.node_dist - abs(self.next_dist) # taking the distnace to the next node away

class Tower(pygame.sprite.Sprite):  # standard Tower. basic, does the job. not exciting
    def __init__(self, location):
        super().__init__()
        #creation metrics
        self.cost = Tower_info[0][4]
        self.name = Tower_info[0][0]
        self.ID = "Targeted"
        self.position = location
        self.turret_colour=(0,200,100)
        self.range = Tower_info[0][3]
        self.shots_per_sec = Tower_info[0][2]
        self.fire_rate = 1/self.shots_per_sec
        self.target = None
        self.shot_timer = curtime
        self.damage = Tower_info[0][1]
        self.level = 1
        self.upgrade_cost = 6
        self.sellprice = 8
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
        mousex = pygame.mouse.get_pos()[0]
        mousey = pygame.mouse.get_pos()[1]
        if self.baserect.collidepoint(mousex, mousey):
            self.draw_range(disp)

    def draw_range(self, disp):
        disp.blit(self.rangeimage, self.rangerect)

    def aim(self, target):
        self.turret_angle = 90-degrees(angle_finder(self.baserect.center, target.rect.center)) #(pi/2)---
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
        self.level += 1
        self.upgrade_cost = int((2*self.level*(self.level+2)+6)*self.cost/10)

class Slammer(pygame.sprite.Sprite): # High damage 360 degree hit area tower. no aiming.
    def __init__(self, location):
        super().__init__()
        self.cost = Tower_info[1][4]
        self.name = Tower_info[1][0]
        self.sellprice = 14
        self.ID = "NoTarget"
        self.position = location
        self.shots_per_sec = Tower_info[1][2]
        self.fire_rate = 1/self.shots_per_sec
        self.target = "NA" # cannot aim. hits everything.
        self.shot_timer = curtime
        self.damage = Tower_info[1][1]
        self.range = Tower_info[1][3]  # so smol.
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
        self.spinnybit = pygame.image.load("E:\Python code on VSC\Tower Defence\SpinnyBit.png")
        self.spinnybit = pygame.transform.scale(self.spinnybit,(60,60))
        self.spinnybit_rect = self.spinnybit.get_rect(center=location)
        self.rotated_spinnybit = self.spinnybit
        self.spinadjustment = 1
        
    def draw(self,disp):
        disp.blit(self.image, (self.baserect[0]+3,self.baserect[1]+3))
        disp.blit(self.rotated_spinnybit, self.spinnybit_rect)

        mousex = pygame.mouse.get_pos()[0]
        mousey = pygame.mouse.get_pos()[1]
        if self.baserect.collidepoint(mousex, mousey):
            self.draw_range(disp)

    def draw_range(self,disp):
        disp.blit(self.rangeimage, self.rangerect)

    def aim(self):  # due to lack of targeting, this provides aesthetic flair by spinning the pattern on the tower is accordance with charge
        if curtime-self.shot_timer < self.fire_rate:
            self.spinadjustment += (curtime-self.shot_timer)*1.5 # only increases in speed while tower is charging
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
        self.level += 1
        self.upgrade_cost = int((2*self.level*(self.level+2)+6)*self.cost/10)

class Mouse(pygame.sprite.Sprite):  # used to detect if tower placement is valid
    def __init__(self):
        super().__init__()
        self.image=pygame.Surface((41,41),pygame.SRCALPHA) #41x41 is exact pixels required to always allow valid placement, but never allow path placement
        self.image.fill((0,0,0,0))
        self.rect=self.image.get_rect()

    def update(self, pos):
        self.rect.center=pos
        disp.blit(self.image, self.rect)

towers=pygame.sprite.Group()
enemies=pygame.sprite.Group()
clock=time.time()
mouse_track=Mouse()
timer=0
towers_rects=[]
curtime = time.time()

state = 0    # (0-Menu, 1-Game, 2-Paused, 3-Upgrades)

while True:
    curtime=time.time()
    pressed_keys=pygame.key.get_pressed()
    mouse=pygame.mouse.get_pos()
    if state == 0: # Main Menu
        disp.blit(TitleScreen, (0,0))
        if PlayButton.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            state = 1
        elif UpgradesButton.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            state = 3
    elif state == 1:  # MAIN LOOPYDOOP
        top_surface.fill((0,0,0,0)) # clears the surface of shots fired previously
        if True: # Handling all text to display per frame
            disp.blit(map1, (0,0)) # push background image
            livescounter = font.render(str(f"Lives: {lives} |  Wave: {wave}    "), True, (255,255,255)) # update the lives
            disp.blit(livescounter,(10,10)) # display lives on screen
            disp.blit(Instructions,(600,10))
            gold_readout=font.render(str(gold), True, (255,255,100))
            gold_rect=gold_readout.get_rect(topright=(scr_wi-10,10))
            disp.blit(gold_readout,gold_rect)
        if pressed_keys[K_SPACE]:
            if pressed_keys[K_w]:
                tower_index = 0
            elif pressed_keys[K_a]:
                tower_index = 1
            mouse_track.update(mouse)
            location=((((mouse[0]+20)//40)*40),((mouse[1]+20)//40)*40) # locks placement to a 40px grid, and averages the center of the tower to the mouse position
            if (mouse_track.rect.collidelist(paths)!=-1) or (mouse_track.rect.collidelist(towers_rects)!=-1): # checks if tower would be blocked by other tower or path
                draw_placement_guide((255,0,0,50),(location[0]-37, location[1]-37),Tower_info[tower_index][3])
            elif (gold-Tower_info[tower_index][4]) <0: # checks cost of selection against funds
                draw_placement_guide((255,255,0,50),(location[0]-37, location[1]-37),Tower_info[tower_index][3])
            else:
                draw_placement_guide((255,255,255,50),(location[0]-37, location[1]-37),Tower_info[tower_index][3]) # draws a WHITE box where tower will appear
                if pygame.mouse.get_pressed()[0] and curtime-clock>0.1:    
                    gold-= Tower_info[tower_index][4] # removes tower price from funds
                    new_tower = tower_select(tower_index, location) #Tower(location)
                    towers.add(new_tower) 
                    print(new_tower.baserect) 
                    towers_rects.append(new_tower.baserect) # keeps track of where towers are for      efficient tower placement validation
                    clock=curtime
        wavespawn()  # handles spawning of enemies, progression of waves, HP scaling
        for bob in enemies: # move and draw enemies
            bob.move()
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
        if lives==0:
            print("you loose")
            pygame.quit()
            sys.exit()
        disp.blit(top_surface,(0,0)) # draws all tower shots
        open_info()
        drag()
        if not pressed_keys[K_SPACE]:
            select_tower()
    elif state == 2:
        pass # PAUSE    -not yet implimented
    elif state == 3:
        disp.fill((0,0,0)) # UPGRADES    -not yet implimented
    for event in pygame.event.get(): #standard quit check loop...
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
    pygame.display.flip()
    FrPS.tick(FPS)