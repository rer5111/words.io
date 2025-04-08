import pygame, random, tkinter, math
from perlin_noise import *
from data import levels, buildings


def level_get(pos, size, clr1, clr2, clrtxt, level):
    if level <= level_access:
        text = level
        pic = ""
    else:
        pic = sprites["lock"]
        text = ""
    return GUI(main_screen, pos, size, 5*height_mult, clr1, clr2, clrtxt, text, int(90*height_mult), True, pic)

def level_create(data=tuple):
    global matrix
    matrix = []
    x,y = -1, -1
    for row in data:
        x=-1
        y+=1
        matrix.append([]) 
        for tile in row:
            x+=1
            matrix[y].append(Tile(tile[0], Block(tile[1], tile[2]), [x, y]))

def matrix_get(x, y):   #in order to work with the matrix properly and not have it return the first row upon [-1] which might be out of bounds we need this
    if not x or y < 0:
        return matrix[x][y]
    else:
        return 0    # haha no execution for you

def text_draw(surface, text: str = '', font=pygame.font.Font, text_clr=tuple[float, float, float], text_pos=tuple[float, float], centered=bool):
    img = font.render(f"{text}", True, text_clr)
    if not centered:
        surface.blit(img, text_pos)
    else:
        surface.blit(img, img.get_rect(center=text_pos))

def update_gui():
    global gui_list, buttons
    for i in screens[current_screen]["GUI"]:
        gui_list.append(i)
    buttons = screens[current_screen]["Buttons"]

class GUI:
    def __init__(self, surface, coordinates=tuple[float, float], size=tuple[float, float], border_width=float, colour1=tuple[float, float, float], colour2=tuple[float, float, float], colour_text=tuple[float, float, float], text: str = "", text_size=int, centered=bool, image: str = ""):
        self.surface = surface  #on what draw
        self.x, self.y = coordinates   #where draw 
        self.width, self.height = size  #how much draw
        self.width_border = border_width    #border size (self explanatory)
        self.colour1 = colour1  #main colour
        self.colour2 = colour2  #border colour
        self.colour_text = colour_text  #colour of text if such is present
        self.text = text    #text if present
        self.text_size = text_size  #size of text if text present
        self.centered = centered    #where draw text if present
        self.img = image    #image if present

    def draw(self):
        try:    # there is a possibility for an error with very small windows, safety precaution
            if self.img == "":  #no image gui
                pygame.draw.rect(self.surface, self.colour1, pygame.Rect(self.x, self.y, self.width, self.height))
                pygame.draw.rect(self.surface, self.colour2, pygame.Rect(self.x + self.width_border, self.y + self.width_border, self.width - self.width_border*2, self.height - self.width_border*2))
                if self.text != "": #text gui
                    if self.centered:
                        text_draw(self.surface, self.text, pygame.font.SysFont("Fixedsys", self.text_size), (self.colour_text), (self.x+self.width/2, self.y+self.height/2), True) 
                    else:
                        text_draw(self.surface, self.text, pygame.font.SysFont("Fixedsys", self.text_size), (self.colour_text), (self.x + self.width_border+5, self.y + self.width_border + 5), False) 
            elif self.text == "":   #picture gui
                pygame.draw.rect(self.surface, self.colour1, pygame.Rect(self.x, self.y, self.width, self.height))
                pygame.draw.rect(self.surface, self.colour2, pygame.Rect(self.x + self.width_border, self.y + self.width_border, self.width - self.width_border*2, self.height - self.width_border*2))
                self.surface.blit(pygame.transform.scale(self.img, (self.width-self.width_border*2, self.height-self.width_border*2)), (self.x+self.width_border, self.y+self.width_border))
            else:   #combined gui
                pygame.draw.rect(self.surface, self.colour1, pygame.Rect(self.x, self.y, self.width, self.height))
                pygame.draw.rect(self.surface, self.colour2, pygame.Rect(self.x + self.width_border, self.y + self.width_border, self.width - self.width_border*2, self.height - self.width_border*2))
                self.surface.blit(pygame.transform.scale(self.img, (self.height-self.width_border*2, self.height-self.width_border*2)), (self.x+self.width_border, self.y+self.width_border))
                if self.centered:
                    text_draw(self.surface, self.text, pygame.font.SysFont("Fixedsys", self.text_size), (self.colour_text), ((self.x+(self.height-self.width_border)+self.width_border+(self.width-self.width_border*2-self.height)/2), self.y+self.height/2), True)
                else:
                    pass
        except ValueError:
            pass


class Tile:
    def __init__(self, resource, block, coordinates=tuple[int, int]):
        global zoom, camera_position, width_screen, height_screen
        self.x, self.y = coordinates
        self.resource = resource
        self.block = block
        self.pygame_rect = pygame.Rect(math.ceil(self.x * 32 * zoom + camera_position[0]*32*zoom+math.ceil(width_screen/2)), math.ceil((self.y * 32 * zoom + camera_position[1]*32*zoom+math.ceil(height_screen/2))), math.ceil(32 * zoom), math.ceil(32 * zoom))
        self.pygame_rect2 = pygame.Rect(math.ceil(self.x * 32 * zoom + camera_position[0]*32*zoom+math.ceil(width_screen/2))+3, math.ceil((self.y * 32 * zoom + camera_position[1]*32*zoom+math.ceil(height_screen/2)))+3, math.ceil(26 * zoom), math.ceil(26 * zoom))

    def update_rect(self):
        self.pygame_rect.left = math.ceil(self.x * 32 * zoom + camera_position[0]*32*zoom)
        self.pygame_rect.top = math.ceil(self.y * 32 * zoom + camera_position[1]*32*zoom)
        self.pygame_rect.width = math.ceil(32 * zoom)
        self.pygame_rect.height = self.pygame_rect.width
        self.pygame_rect2.left = self.pygame_rect.left+3
        self.pygame_rect2.top = self.pygame_rect.top+3
        self.pygame_rect2.width = math.ceil(26*zoom)
        self.pygame_rect2.height = self.pygame_rect2.width


class Block:
    def __init__(self, storage, type=str):
        self.type = type
        self.storage = storage


class Button():
    def __init__(self, pos, size):
        self.x_pos, self.y_pos = pos
        self.width, self.height = size


pygame.init()
width_screen, height_screen = 1600, 900
width_mult, height_mult = 1, 1
default_res = (width_screen, height_screen)
screen = pygame.display.set_mode(default_res, pygame.RESIZABLE)
horizontal_bars = False
vertical_bars = False
# refer to sprites if you need to load any image 
sprites = {
    "title": "sprites/title.png",
    "play": "sprites/play_icon.png",
    "settings": "sprites/settings_icon.png",
    "lock": "sprites/level_locked.png",
    "conveyor": "sprites/conveyor_up.png",
    "drill": "sprites/drill.png"
}
for sprite in sprites:  # the magical converter
    sprites[sprite] = pygame.image.load(sprites[sprite]).convert_alpha()

level_access = 1    # wow i didnt even need a dict for this one
fps = 60
clock = pygame.time.Clock()
main_screen = pygame.Surface(default_res, pygame.SRCALPHA)
pygame.display.set_caption("words.io")
pygame.display.set_icon(pygame.image.load("icon.png"))
current_tiles = []
gui_list = []
camera_position = [0, 0]
zoom = 1
running = True
main_game_running = False
test_img = pygame.image.load("icon.png").convert_alpha()
current_screen = "start"

# DATA STORAGE
def update_all_gui():   #ok so, crazy stuff, this actually need to be a function to change gui positions depending on changing variables, very cool.
    global screens
    start_screen = {
        "GUI":[
            GUI(main_screen, (400*width_mult, 50*height_mult), (800*width_mult, 200*height_mult), 5*height_mult, (200, 200, 200), (100, 100, 100), (0, 0, 0), "", 0, False, sprites["title"]),
            GUI(main_screen, (100*width_mult, 300*height_mult), (400*width_mult, 100*height_mult), 5*height_mult, (200, 200, 200), (100, 100, 100), (0, 0, 0), "Play", int(40*height_mult), True, sprites["play"]),
            GUI(main_screen, (100*width_mult, 450*height_mult), (400*width_mult, 100*height_mult), 5*height_mult, (200, 200, 200), (100, 100, 100), (0, 0, 0), "Settings", int(40*height_mult), True, sprites["settings"]),
            GUI(main_screen, (100*width_mult, 600*height_mult), (400*width_mult, 100*height_mult), 5*height_mult, (200, 200, 200), (100, 100, 100), (0, 0, 0), "Credits", int(40*height_mult), True, "")
        ],
        "Buttons":{
            Button((100*width_mult, 300*height_mult), (400*width_mult, 100*height_mult)):"current_screen = \"start2\"",
            Button((100*width_mult, 450*height_mult), (400*width_mult, 100*height_mult)):"current_screen = \"settings\"",
            Button((100*width_mult, 600*height_mult), (400*width_mult, 100*height_mult)):"current_screen = \"credits\""
        }
    }
    start_screen2 = {
        "GUI":[
            GUI(main_screen, (400*width_mult, 50*height_mult), (800*width_mult, 200*height_mult), 5*height_mult, (200, 200, 200), (100, 100, 100), (0, 0, 0), "", 0, False, sprites["title"]),
            GUI(main_screen, (100*width_mult, 300*height_mult), (400*width_mult, 100*height_mult), 5*height_mult, (200, 200, 200), (100, 100, 100), (0, 0, 0), "Play", int(40*height_mult), True, sprites["play"]),
            GUI(main_screen, (100*width_mult, 450*height_mult), (400*width_mult, 100*height_mult), 5*height_mult, (200, 200, 200), (100, 100, 100), (0, 0, 0), "Settings", int(40*height_mult), True, sprites["settings"]),
            GUI(main_screen, (100*width_mult, 600*height_mult), (400*width_mult, 100*height_mult), 5*height_mult, (200, 200, 200), (100, 100, 100), (0, 0, 0), "Credits", int(40*height_mult), True, ""),
            GUI(main_screen, (525*width_mult, 300*height_mult), (400*width_mult, 100*height_mult), 5*height_mult, (200, 200, 200), (100, 100, 100), (0, 0, 0), "Endless", int(40*height_mult), True, ""),
            GUI(main_screen, (525*width_mult, 425*height_mult), (400*width_mult, 100*height_mult), 5*height_mult, (200, 200, 200), (100, 100, 100), (0, 0, 0), "Puzzle", int(40*height_mult), True, "")
        ],
        "Buttons":{
            Button((100*width_mult, 300*height_mult), (400*width_mult, 100*height_mult)):"current_screen = \"start\"",
            Button((100*width_mult, 450*height_mult), (400*width_mult, 100*height_mult)):"current_screen = \"settings\"",
            Button((100*width_mult, 600*height_mult), (400*width_mult, 100*height_mult)):"current_screen = \"credits\"",
            Button((525*width_mult, 300*height_mult), (400*width_mult, 100*height_mult)):"current_screen = \"game\"",
            Button((525*width_mult, 425*height_mult), (400*width_mult, 100*height_mult)):"current_screen = \"level_select\""
        }
    }
    credits_screen = {
        "GUI":[
            GUI(main_screen, (1500*width_mult, 25*height_mult), (75*width_mult, 75*height_mult), 5*height_mult, (255, 0, 0), (155, 0, 0), (0, 0, 0), "X", int(100*height_mult), True, ""),
            GUI(main_screen, (500*width_mult, 50*height_mult), (600*width_mult, 100*height_mult), 5*height_mult, (200, 200, 200), (100, 100, 100), (0, 0, 0), "Credits", int(120*height_mult), True, ""),
            GUI(main_screen, (25*width_mult, 250*height_mult), (0*width_mult, 0*height_mult), 5*height_mult, (100, 100, 100), (100, 100, 100), (255, 255, 255), "Here's a list of all the wonderful people that made this game possible:", int(40*height_mult), False, ""),
            GUI(main_screen, (25*width_mult, 300*height_mult), (0*width_mult, 0*height_mult), 5*height_mult, (100, 100, 100), (100, 100, 100), (255, 255, 0), "Rer_5111", int(40*height_mult), False, ""),
            GUI(main_screen, (150*width_mult, 300*height_mult), (0*width_mult, 0*height_mult), 5*height_mult, (100, 100, 100), (100, 100, 100), (255, 255, 255), " (me) - lead designer, programmer, creator", int(40*height_mult), False, ""),
            GUI(main_screen, (25*width_mult, 350*height_mult), (0*width_mult, 0*height_mult), 5*height_mult, (100, 100, 100), (100, 100, 100), (255, 0, 0), "Tabller", int(40*height_mult), False, ""),
            GUI(main_screen, (125*width_mult, 350*height_mult), (0*width_mult, 0*height_mult), 5*height_mult, (100, 100, 100), (100, 100, 100), (255, 255, 255), " - contributor (he did cool suggestions)", int(40*height_mult), False, ""),
            GUI(main_screen, (25*width_mult, 400*height_mult), (0*width_mult, 0*height_mult), 5*height_mult, (100, 100, 100), (100, 100, 100), (0, 0, 255), "Intervinn", int(40*height_mult), False, ""),
            GUI(main_screen, (155*width_mult, 400*height_mult), (0*width_mult, 0*height_mult), 5*height_mult, (100, 100, 100), (100, 100, 100), (255, 255, 255), " - contributor (he helped optimize the game a lot and general help)", int(40*height_mult), False, ""),
            GUI(main_screen, (25*width_mult, 450*height_mult), (0*width_mult, 0*height_mult), 5*height_mult, (100, 100, 100), (100, 100, 100), (255, 120, 0), "Kotyarendj", int(40*height_mult), False, ""),
            GUI(main_screen, (175*width_mult, 450*height_mult), (0*width_mult, 0*height_mult), 5*height_mult, (100, 100, 100), (100, 100, 100), (255, 255, 255), " - artist (lots of cool sprites)", int(40*height_mult), False, "")
        ],
        "Buttons":{
            Button((1500*width_mult, 25*height_mult), (75*width_mult, 75*height_mult)):"current_screen = \"start\""
        }
    }
    settings_screen = {
        "GUI":[
            GUI(main_screen, (1500*width_mult, 25*height_mult), (75*width_mult, 75*height_mult), 5*height_mult, (255, 0, 0), (155, 0, 0), (0, 0, 0), "X", int(100*height_mult), True, ""),
            GUI(main_screen, (25*width_mult, 400*height_mult), (1550*width_mult, 150*height_mult), 5*height_mult, (200, 200, 200), (100, 100, 100), (0, 0, 0), "WIP (there are no settings yet, sorry!)", int(120*height_mult), True, ""),
        ],
        "Buttons":{
            Button((1500*width_mult, 25*height_mult), (75*width_mult, 75*height_mult)):"current_screen = \"start\""
        }
    }
    level_select = {
        "GUI":[
            GUI(main_screen, (1500*width_mult, 25*height_mult), (75*width_mult, 75*height_mult), 5*height_mult, (255, 0, 0), (155, 0, 0), (0, 0, 0), "X", int(100*height_mult), True, ""),
            GUI(main_screen, (300*width_mult, 50*height_mult), (1000*width_mult, 200*height_mult), 5*height_mult, (200, 200, 200), (100, 100, 100), (0, 0, 0), "Level select", int(160*height_mult), True, ""),
            level_get((200*width_mult, 300*height_mult), (150*width_mult, 150*height_mult), (200, 200, 200), (100, 100, 100), (0, 0, 0), 1),
            level_get((400*width_mult, 300*height_mult), (150*width_mult, 150*height_mult), (200, 200, 200), (100, 100, 100), (0, 0, 0), 2),
            level_get((600*width_mult, 300*height_mult), (150*width_mult, 150*height_mult), (200, 200, 200), (100, 100, 100), (0, 0, 0), 3),
            level_get((800*width_mult, 300*height_mult), (150*width_mult, 150*height_mult), (200, 200, 200), (100, 100, 100), (0, 0, 0), 4),
            level_get((1000*width_mult, 300*height_mult), (150*width_mult, 150*height_mult), (200, 200, 200), (100, 100, 100), (0, 0, 0), 5),
            level_get((1200*width_mult, 300*height_mult), (150*width_mult, 150*height_mult), (200, 200, 200), (100, 100, 100), (0, 0, 0), 6),
            level_get((200*width_mult, 500*height_mult), (150*width_mult, 150*height_mult), (200, 200, 200), (100, 100, 100), (0, 0, 0), 7),
            level_get((400*width_mult, 500*height_mult), (150*width_mult, 150*height_mult), (200, 200, 200), (100, 100, 100), (0, 0, 0), 8),
            level_get((600*width_mult, 500*height_mult), (150*width_mult, 150*height_mult), (200, 200, 200), (100, 100, 100), (0, 0, 0), 9),
            level_get((800*width_mult, 500*height_mult), (150*width_mult, 150*height_mult), (200, 200, 200), (100, 100, 100), (0, 0, 0), 10),
            level_get((1000*width_mult, 500*height_mult), (150*width_mult, 150*height_mult), (200, 200, 200), (100, 100, 100), (0, 0, 0), 11),
            level_get((1200*width_mult, 500*height_mult), (150*width_mult, 150*height_mult), (200, 200, 200), (100, 100, 100), (0, 0, 0), 12),
            level_get((200*width_mult, 700*height_mult), (150*width_mult, 150*height_mult), (200, 200, 200), (100, 100, 100), (0, 0, 0), 13),
            level_get((400*width_mult, 700*height_mult), (150*width_mult, 150*height_mult), (200, 200, 200), (100, 100, 100), (0, 0, 0), 14),
            level_get((600*width_mult, 700*height_mult), (150*width_mult, 150*height_mult), (200, 200, 200), (100, 100, 100), (0, 0, 0), 15),
            level_get((800*width_mult, 700*height_mult), (150*width_mult, 150*height_mult), (200, 200, 200), (100, 100, 100), (0, 0, 0), 16),
            level_get((1000*width_mult, 700*height_mult), (150*width_mult, 150*height_mult), (200, 200, 200), (100, 100, 100), (0, 0, 0), 17),
            level_get((1200*width_mult, 700*height_mult), (150*width_mult, 150*height_mult), (200, 200, 200), (100, 100, 100), (0, 0, 0), 18)
        ],
        "Buttons":{
            Button((1500*width_mult, 25*height_mult), (75*width_mult, 75*height_mult)):"current_screen = \"start\"",
            Button((200*width_mult, 300*height_mult), (150*width_mult, 150*height_mult)): "main_game_running = True\ncurrent_screen = \"game\"\nlevel_create(levels.get(1).get(\"map\"))"
        }
    }
    game_screen = {
        "GUI":[

        ],
        "Buttons":{

        }
    }
    screens = {
    "start": start_screen,
    "start2": start_screen2,
    "credits": credits_screen,
    "settings": settings_screen,
    "level_select": level_select,
    "game": game_screen
}

update_all_gui()
update_gui()

matrix = []


while running:
    screen.fill((0, 0, 0))
    main_screen.fill((100, 100, 100))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:    # If the screen gets resized we update all gui to the new main screen (also all the formulas get updated)
            if event.w/16 > event.h/9:  #normalise the screen to a 16:9 aspect ratio (creates black bars but its fine)
                horizontal_bars = True
                vertical_bars = False
                width_screen, height_screen = 16*math.floor(event.h/9), event.h
                width_mult, height_mult = width_screen/1600, height_screen/900
                print(width_mult, height_mult)
                main_screen = pygame.Surface((width_screen, height_screen), pygame.SRCALPHA)
            else:
                horizontal_bars = False
                vertical_bars = True
                width_screen, height_screen = event.w, 9*math.floor(event.w/16)
                width_mult, height_mult = width_screen/1600, height_screen/900 
                main_screen = pygame.Surface((width_screen, height_screen), pygame.SRCALPHA)
            gui_list = []
            update_all_gui()
            update_gui()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x_pressed, y_pressed = pygame.mouse.get_pos()
            if horizontal_bars:
                x_pressed -= (screen.get_width()-width_screen)/2
            else:
                y_pressed -= (screen.get_height()-height_screen)/2
            for button in buttons:
                if button.x_pos < x_pressed < button.x_pos+button.width and button.y_pos < y_pressed < button.y_pos + button.height:
                    exec(buttons.get(button))
                    gui_list = []
                    update_gui()
        if event.type == pygame.MOUSEWHEEL:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            mouse_pos1 = [camera_position[0]-(x_mouse/(32*zoom)), camera_position[1]-(y_mouse/(32*zoom))]
            if event.y == 1:
                zoom *= 1.1
                if zoom > 2.5:
                    zoom = 2.5
            if event.y == -1:
                zoom *= 0.9
                if zoom < 0.7:
                    zoom = 0.7
            mouse_pos2 = [camera_position[0]-(x_mouse/(32*zoom)), camera_position[1]-(y_mouse/(32*zoom))]
            camera_position[0]+= (mouse_pos1[0]-mouse_pos2[0])
            camera_position[1]+= (mouse_pos1[1]-mouse_pos2[1])
    if pygame.key.get_pressed()[pygame.K_w]:
        camera_position[1] += 0.25/zoom
    if pygame.key.get_pressed()[pygame.K_s]:
        camera_position[1] -= 0.25/zoom
    if pygame.key.get_pressed()[pygame.K_d]:
        camera_position[0] -= 0.25/zoom
    if pygame.key.get_pressed()[pygame.K_a]:
        camera_position[0] += 0.25/zoom
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        current_screen = "start"
        main_game_running = False
        gui_list = []
        update_gui()
    if main_game_running:
        current_tiles = []
        left_limit = math.floor(-camera_position[0])
        right_limit = math.ceil(-camera_position[0]+width_screen/32/zoom)
        top_limit = math.floor(-camera_position[1])
        bottom_limit = math.ceil(-camera_position[1]+height_screen/32/zoom)
        for i in range(abs(right_limit-left_limit)):
            for i2 in range(abs(bottom_limit-top_limit)):
                try:
                    current_tiles.append(matrix[top_limit+i2][left_limit+i])
                except IndexError:
                    pass
        for i in current_tiles:
            i.update_rect()
            pygame.draw.rect(main_screen, (220, 220, 220), i.pygame_rect)
            pygame.draw.rect(main_screen, (255, 255, 255), i.pygame_rect2)
            if i.resource != "":
                text_draw(main_screen, i.resource, pygame.font.SysFont("Fixedsys", math.floor(26*zoom)), (0, 0, 0), [i.pygame_rect.left+(16*zoom), i.pygame_rect.top+(16*zoom)])
            if i.block.type != "":
                main_screen.blit(pygame.transform.scale(sprites[i.block.type], (math.ceil(32 * zoom), math.ceil(32 * zoom))),
                    (math.ceil(i.x * 32 * zoom + camera_position[0]*32*zoom),
                    math.ceil((i.y * 32 * zoom + camera_position[1]*32*zoom))))
                exec(buildings.get(i.block.type).get("code"))
    for window in gui_list: # this is drawn over the game 
        window.draw()    
    
    if horizontal_bars:     #screen draw offset
        screen.blit(main_screen, ((screen.get_width()-width_screen)/2,0))
    else:
        screen.blit(main_screen, (0,(screen.get_height()-height_screen)/2))
    pygame.display.flip()
    clock.tick(fps)
