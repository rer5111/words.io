import pygame, random, tkinter, math
from perlin_noise import *
from data import *

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
        self.centered = centered    #where draw text
        self.img = image    #image if present
    
    def draw(self):
        try:
            pygame.draw.rect(self.surface, self.colour1, pygame.Rect(self.x, self.y, self.width, self.height))
            pygame.draw.rect(self.surface, self.colour2, pygame.Rect(self.x + self.width_border, self.y + self.width_border, self.width - self.width_border*2, self.height - self.width_border*2))
            try:
                if self.text != "":
                    img = self.surface.blit(pygame.transform.scale(self.img, (self.height-self.width_border*2, self.height-self.width_border*2)), (self.x+self.width_border, self.y+self.width_border))
                else:
                    img = self.surface.blit(pygame.transform.scale(self.img, (self.width-self.width_border*2, self.height-self.width_border*2)), (self.x+self.width_border, self.y+self.width_border))
            except Exception as e:
                pass

            if self.centered:
                if self.img != "":
                    text_draw(self.surface, self.text, pygame.font.SysFont("Fixedsys", self.text_size), (self.colour_text), ((self.x+(self.height-self.width_border)+self.width_border+(self.width-self.width_border*2-self.height)/2), self.y+self.height/2), bool)
                else:
                    text_draw(self.surface, self.text, pygame.font.SysFont("Fixedsys", self.text_size), (self.colour_text), (self.x+self.width/2, self.y+self.height/2), bool) 
            else:
                text_draw(self.surface, self.text, pygame.font.SysFont("Fixedsys", self.text_size), (self.colour_text), (self.x + self.width_border+5, self.y + self.width_border + 5), bool) 

        except ValueError:
            pass

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
    "settings": "sprites/settings_icon.png"
}
for sprite in sprites:  # the magical converter
    sprites[sprite] = pygame.image.load(sprites[sprite]).convert_alpha()

fps = 60
clock = pygame.time.Clock()
main_screen = pygame.Surface(default_res, pygame.SRCALPHA)
pygame.display.set_caption("words.io")
pygame.display.set_icon(pygame.image.load("icon.png"))
matrix = []
gui_list = []
camera_position = [0, 0]
zoom = 1
running = True
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
            GUI(main_screen, (475*width_mult, 250*height_mult), (0*width_mult, 0*height_mult), 5*height_mult, (100, 100, 100), (100, 100, 100), (255, 255, 255), "Here's a list of all the wonderful people that made this game possible:", int(40*height_mult), False, ""),
            GUI(main_screen, (75*width_mult, 300*height_mult), (0*width_mult, 0*height_mult), 5*height_mult, (100, 100, 100), (100, 100, 100), (255, 255, 0), "Rer_5111", int(40*height_mult), False, ""),
            GUI(main_screen, (425*width_mult, 300*height_mult), (0*width_mult, 0*height_mult), 5*height_mult, (100, 100, 100), (100, 100, 100), (255, 255, 255), " (me) - lead designer, programmer, creator", int(40*height_mult), False, ""),
            GUI(main_screen, (75*width_mult, 350*height_mult), (0*width_mult, 0*height_mult), 5*height_mult, (100, 100, 100), (100, 100, 100), (255, 0, 0), "Tabller", int(40*height_mult), False, ""),
            GUI(main_screen, (390*width_mult, 350*height_mult), (0*width_mult, 0*height_mult), 5*height_mult, (100, 100, 100), (100, 100, 100), (255, 255, 255), " - contributor (he did cool suggestions)", int(40*height_mult), False, ""),
            GUI(main_screen, (75*width_mult, 400*height_mult), (0*width_mult, 0*height_mult), 5*height_mult, (100, 100, 100), (100, 100, 100), (0, 0, 255), "Intervinn", int(40*height_mult), False, ""),
            GUI(main_screen, (410*width_mult, 400*height_mult), (0*width_mult, 0*height_mult), 5*height_mult, (100, 100, 100), (100, 100, 100), (255, 255, 255), " - contributor (he helped a lot with code)", int(40*height_mult), False, ""),
            GUI(main_screen, (75*width_mult, 450*height_mult), (0*width_mult, 0*height_mult), 5*height_mult, (100, 100, 100), (100, 100, 100), (255, 120, 0), "Kotyarendj", int(40*height_mult), False, ""),
            GUI(main_screen, (340*width_mult, 450*height_mult), (0*width_mult, 0*height_mult), 5*height_mult, (100, 100, 100), (100, 100, 100), (255, 255, 255), " - artist (lots of cool sprites)", int(40*height_mult), False, "")
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
        ],
        "Buttons":{
            Button((1500*width_mult, 25*height_mult), (75*width_mult, 75*height_mult)):"current_screen = \"start\""
        }
    }
    screens = {
    "start": start_screen,
    "start2": start_screen2,
    "credits": credits_screen,
    "settings": settings_screen,
    "level_select": level_select
}

update_all_gui()
update_gui()


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


    for window in gui_list:
        window.draw()    
    
    if horizontal_bars:     #screen draw offset
        screen.blit(main_screen, ((screen.get_width()-width_screen)/2,0))
    else:
        screen.blit(main_screen, (0,(screen.get_height()-height_screen)/2))
    pygame.display.flip()
    clock.tick(fps)