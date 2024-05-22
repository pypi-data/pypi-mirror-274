import os
import pygame
from math import *
import copy

flags = 0
screen = 0
frames = 0
sprites = []
left_clicked = 0
right_clicked = 0
left_released = 0
right_released = 0
wheel_up = 0
wheel_down = 0
text_list = []
key_pres = 0
ascii = {chr(i): i for i in range(128)}
clock = pygame.time.Clock()
updating_sizes = 0
minimum_sizes = (0,0)
fullscreen = 0
WIDTH = 0
HEIGHT = 0
FPS = 0

def screen_size():
    return screen.get_size()

def get_text_surface(text, size = 25, color = (0,0,0), font = None, antialiasing = True):
    fontText = pygame.font.Font(font, size)
    text_surface = fontText.render(str(text), antialiasing, color)
    return text_surface

def rectangle(width, height, color):
    """color must be type _color (tuple of R,G,B)"""
    surface = pygame.Surface((width, height))
    surface.fill(color)
    return surface

def window(width = 480,height = 360,title = "window", resizable=0, smallest_window_sizes = (0,0), icon = None, full_Screen = 0):
    global minimum_sizes; minimum_sizes = smallest_window_sizes
    global fullscreen; fullscreen = full_Screen
    global flags
    global updating_sizes; updating_sizes = 1
    pygame.init()
    global screen
    if resizable:
        flags = pygame.RESIZABLE
    if fullscreen:
        flags = flags | pygame.FULLSCREEN
    screen = pygame.display.set_mode((width,height), flags)
    if icon:
        pygame.display.set_icon(pygame.image.load(icon))

    pygame.display.set_caption(title)
    return screen

def loop(fps_goal = None, background = (255,255,255)):
    global frames
    if frames > 1:
        pygame.display.flip()
    running = 1
    global FPS; FPS = int(clock.get_fps())
    frames += 1
    global screen; screen.fill(background)
    global left_clicked, right_clicked; left_clicked = 0 ; right_clicked = 0
    global right_released, left_released; right_released = 0; left_released = 0
    global wheel_up, wheel_down; wheel_down = 0; wheel_up = 0
    global text_list, key_pres; key_pres = 0
    global updating_sizes; updating_sizes = 0
    global minimum_sizes
    global flags
    global fullscreen
    global WIDTH; global HEIGHT

    if frames > (1 << 16):
        frames = 0

    for sprite in sprites:
        sprite.draw()
    for text in text_list:
        screen.blit(text[0],text[1])
    text_list = []
    if fps_goal:
        clock.tick(fps_goal)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                left_clicked = 1
            elif event.button == 3:
                right_clicked = 1
            elif event.button == 4:
                wheel_up = 1
            elif event.button == 5:
                wheel_down = 1
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                left_released = 1
            elif event.button == 3:
                right_released = 1
        elif event.type == pygame.KEYDOWN:
            key_pres = event.key
        elif event.type == pygame.VIDEORESIZE:
            updating_sizes = 1
            screen = pygame.display.set_mode((max(event.w,minimum_sizes[0]),max(event.h,minimum_sizes[1])), flags)
            WIDTH,HEIGHT = screen_size()
        if key_clicked(pygame.K_F11):
            if fullscreen:
                fullscreen = 0
                flags &= ~pygame.FULLSCREEN
                screen = pygame.display.set_mode(minimum_sizes, flags)
            else:
                fullscreen = 1
                flags |= pygame.FULLSCREEN
                screen = pygame.display.set_mode((0,0), flags)
            WIDTH,HEIGHT = screen_size()
            updating_sizes = 1    
    return running

def mouse_down(button = "left"):
    if button == "left" or button == 0:
        return pygame.mouse.get_pressed()[0]
    elif button == "right" or button == 1:
        return pygame.mouse.get_pressed()[2]

def mouse_position():
    return pygame.mouse.get_pos()

def fill(*color_value):
    global color
    if len(color_value) == 1:
        color = color_value[0]
    else:
        color = (color_value[0],color_value[1],color_value[2])

def set_smoothly(value,target,smoothness):
    return value + (target - value) / smoothness

def key_pressed(key):
    global ascii
    try:
        return pygame.key.get_pressed()[ascii[key]]
    except:
        return pygame.key.get_pressed()[key]
    
def key_clicked(key):
    global ascii
    try:
        return key_pres == ascii[key]
    except:
        return key_pres == key
    
def keys_pressed(*keys):
    pressed = 0
    for key in keys:
        pressed = key_pressed(key) or pressed
    return pressed

def keys_clicked(*keys):
    pressed = 0
    for key in keys:
        pressed = key_clicked(key) or pressed
    return pressed

def ctrl():
    return keys_pressed(pygame.K_LCTRL , pygame.K_RCTRL)

def shift():
    keys = pygame.key.get_mods()
    return keys & pygame.KMOD_SHIFT

def text(text, position = (0,0), size = 25, color = (0,0,0), font = None, antialiasing = 1, topLeft = True):
    fontText = pygame.font.Font(font, size)
    text_surface = fontText.render(str(text), antialiasing, color)
    if topLeft:
        drawPos = (position[0],position[1])
    else:
        drawPos = (position[0] - (text_surface.get_width() // 2),position[1] - (text_surface.get_height() // 2))
    text_list.append((text_surface, drawPos))

def debug_list(*list, color = (255,255,255), position = (0,0)):
    i = 0
    for item in list:
        text(str(item), (position[0],position[1]+i*20),color=color)
        i += 1

def adjust_brightness(image_surface, brightness_factor):
    black_surface = pygame.Surface(image_surface.get_size())
    black_surface.fill([brightness_factor]*3)
        
    adjusted_surface = image_surface.copy()
    adjusted_surface.blit(black_surface, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)

    return adjusted_surface

class sprite:

    def __init__(self, images = [], pos = (0,0), direction = 0, scale = 100, depth = 0, hide = 0, alpha = 255, frame = 0, sounds = []):
        """images can be surface.
        images must be list, even if only one item is given.
        
        ATTENTION: Never change sprite position from sprite.pos_Y, sprite.pos_X or sprite.position, they are read only."""    
        try:
            self.sprite_images = [(pygame.image.load("data/"+image).convert_alpha()) for image in images]
        except TypeError:
            self.sprite_images = [(image.convert_alpha()) for image in images]
        self.sound_name = [("data/" + sound) for sound in sounds]
        self.sounds = [(pygame.mixer.Sound("data/" + sound)) for sound in sounds]
        for sound in self.sounds:
            sound.set_volume(.2)
        self.pos_X = pos[0]
        self.pos_Y = pos[1]
        self.position = (pos[0],pos[1])
        self.direction = direction
        self.scale = scale
        sprites.append(self)
        self.frame = frame
        self.appearence = self.sprite_images[self.frame]
        self.hitbox = pygame.transform.scale(self.appearence, (self.appearence.get_width() / 5, self.appearence.get_height() / 5))
        self.is_clone = 0
        self.depth = depth
        self.hide = hide
        self.alpha = alpha
        self.brightness = 255
        rect = self.sprite_images[self.frame].get_rect()
        self.drawPos = (self.pos_X - (rect.width >> 1),self.pos_Y - (rect.height >> 1))
        self.ld = None
        self.sc = None
        self.lf = None
        self.br = None

    def play_sound(self,index_or_file):
        try:
            self.sounds[index_or_file]
            return self.sounds[index_or_file].play()
        except TypeError:
            self.sounds[self.sound_name.index("data/" + index_or_file)]
            return self.sounds[self.sound_name.index("data/" + index_or_file)].play()

    def update(self, forced = 0):
        if forced or not (self.direction == self.ld and self.scale == self.sc and self.frame == self.lf and self.brightness == self.br):
            self.lf = self.frame
            rect = self.sprite_images[self.frame % len(self.sprite_images)].get_rect()
            sprite_image = self.sprite_images[self.frame % len(self.sprite_images)]
            scaled_image =  pygame.transform.scale(sprite_image, (rect.width * abs(self.scale) // 100 , rect.height * abs(self.scale) // 100))
            self.appearence = pygame.transform.rotate(scaled_image, self.direction)
            self.appearence = adjust_brightness(self.appearence, self.brightness)
            self.appearence.set_alpha(self.alpha)
            rotated_rect = self.appearence.get_rect()
            self.drawPos = (self.pos_X - (rotated_rect.width // 2),self.pos_Y - (rotated_rect.height // 2))
            self.ld , self.sc , self.br = self.direction, self.scale, self.brightness
        else:
            rect = self.appearence.get_rect()
            self.drawPos = (self.pos_X - (rect.width >> 1),self.pos_Y - (rect.height >> 1))
        self.hitbox = pygame.transform.scale(self.appearence, (self.appearence.get_width() // 5, self.appearence.get_height() // 5))

    def get_sizes(self):
        return self.appearence.get_size()

    def set_position(self,*pos):
        if len(pos) == 1:
            self.pos_X,self.pos_Y = pos[0][0],pos[0][1]
        else:
            self.pos_X, self.pos_Y = pos[0],pos[1]
        self.update()

    def set_scale(self, value: int):
        self.scale = value
        self.update()

    def set_direction(self, direction: int):
        self.direction = direction
        self.update()

    def change_position(self,*pos):
        if len(pos) == 1:
            self.pos_X,self.pos_Y = self.pos_X+pos[0][0],self.pos_Y+pos[0][1]
        else:
            self.pos_X, self.pos_Y = self.pos_X+pos[0],self.pos_Y+pos[1]
        self.update()

    def get_position(self):
        return (self.pos_X, self.pos_Y)

    def draw(self):
        if not self.hide:
            screen.blit(self.appearence,self.drawPos)
    
    def move(self,speed,offset = 0, direction = ""):
        if direction == "":
            direction = self.direction + offset
        self.pos_X += cos(direction * pi / 180) * speed
        self.pos_Y -= sin(direction * pi / 180) * speed
        self.update()
    
    def point_towards(self, *pos, offset=0):
        if len(pos) == 1:
            try:
                posx,posy = pos[0][0],pos[0][1]
            except:
                posx,posy = pos[0].pos_X,pos[0].pos_Y
        else:
            posx,posy = pos[0],pos[1]
        
        self.direction = degrees(atan2(self.pos_Y - posy , posx - self.pos_X)) + offset
        self.update()

    def direction_to(self, *pos):
        if len(pos) == 1:
            try:
                posx,posy = pos[0][0],pos[0][1]
            except:
                posx,posy = pos[0].pos_X,pos[0].pos_Y
        else:
            posx,posy = pos[0],pos[1]
        
        return degrees(atan2(posy - self.pos_Y, posx - self.pos_X))

    def slide_to(self, smooth, *pos):
        if len(pos) == 1:
            posx,posy = pos[0][0],pos[0][1]
        else:
            posx,posy = pos[0],pos[1]
        if not (posx,posy) == (self.pos_X,self.pos_Y):
            self.pos_X += (posx - self.pos_X) / smooth
            self.pos_Y += (posy - self.pos_Y) / smooth
            self.update()

    def touching(self, sprite):
        self.update()
        sprite_mask = pygame.mask.from_surface(sprite.hitbox)
        self.mask = pygame.mask.from_surface(self.hitbox)
        return self.mask.overlap(sprite_mask, ((sprite.drawPos[0] - self.drawPos[0])//5, (sprite.drawPos[1] - self.drawPos[1])//5)) != None

    def touching_point(self, point):
        self.update()
        try:
            posx = (point[0] - self.pos_X) // 5 + self.hitbox.get_width() // 2
            posy = (point[1] - self.pos_Y) // 5 + self.hitbox.get_height() // 2
            if pygame.mask.from_surface(self.hitbox).get_at((posx,posy)):
                return True
        except:
            pass
        return False
    
    def touching_mouse(self):
        return self.touching_point(pygame.mouse.get_pos())
    
    def touching_mouse_fast(self):
        first_point = self.pos_X - self.appearence.get_width()//2 , self.pos_Y - self.appearence.get_height()//2
        second_point = self.pos_X + self.appearence.get_width()//2 , self.pos_Y + self.appearence.get_height()//2
        mouse_pos = mouse_position()
        return (max(first_point[0],min(second_point[0],mouse_pos[0])),max(first_point[1],min(second_point[1],mouse_pos[1]))) == mouse_pos
    
    def distance_to(self,*pos):
        if len(pos) == 1:
            return sqrt(((self.pos_X - pos[0][0]) ** 2) + ((self.pos_Y - pos[0][1]) ** 2))
        else:
            return sqrt(((self.pos_X - pos[0]) ** 2) + ((self.pos_Y - pos[1]) ** 2))
        
    def clone(self):
        self.is_clone += 1
        clone = copy.copy(self)
        sprites.insert(sprites.index(self),clone)
        self.is_clone -= 1
        return clone
        
    def kill_clone(self):
        if self.is_clone:
            sprites.remove(self)
            return self
        
    def kill(self):
        sprites.remove(self)
        return self
    
    def set_depth(self,z):
        global sprites
        if z == "first" or z == 0:
            sprites.remove(self)
            sprites.append(self)
        elif z == "last":
            sprites.remove(self)
            sprites.insert(0, self)
        else:
            self.depth = z
            sprites = sorted(sprites, key=lambda x: x.depth)

    def animate(self, frames_quantity, first_frame, speed):
        self.frame = (frames * speed//60) % frames_quantity + first_frame

    def clicked(self,mouse_button = 0):
        if mouse_button in ["right", 1] :
            return right_clicked and self.touching_mouse() and not self.hide
        elif mouse_button in ["left", 0]:
            return left_clicked and self.touching_mouse() and not self.hide
        
    def released(self, mouse_button = 0):
        if mouse_button in ["right", 1] :
            return right_released and self.touching_mouse()
        elif mouse_button in ["left", 0]:
            return left_released and self.touching_mouse()
        
def default_template(fileName):
    """
    fileName should be: __file__

    functions loads default template for pygame2.
    """
    with open(fileName, "w") as file:
        file.write("""import pygame_canvas as c

c.window(title = "game")

# sprite declaration here:
object = c.sprite((c.rectangle(50,50,(0,200,255)),),(240,180))

while c.loop(60):
    
    # your code here:
    pass
""")

def is_in(amax,amin,cmax,cmin):
    return cmin < amax and amin < cmax

def get_collisions(list = sprites):
    
    collisions = []
    potentials = []
    aMax = 0
    aMin = 0
    item = 0

    for list in sorted(list, key=lambda spr: spr.pos_X):
        cmax = list.pos_X + list.appearence.get_width() // 2
        cmin = cmax - list.appearence.get_width()
        if aMax == 0 and aMin == 0:
            aMax = cmax
            aMin = cmin
            potentials.append([list,])
        elif is_in(aMax,aMin,cmax,cmin):
            aMax = max(aMax,cmax)
            aMin = min(aMin,cmin)
            potentials[item].append(list)
        else:
            item += 1
            potentials.append([list,])
            aMax = cmax
            aMin = cmin
    for possibles in potentials:
        for i in range(len(possibles)):
            possible = possibles[i]
            for j in range(i+1,len(possibles)):
                if possible.touching(possibles[j]):
                    collisions.append((possible,possibles[j]))
    return collisions

def physics(precision = 10, *args):
    global sprites
    toCheck = [item for item in sprites if not item in args]
    for _ in range(precision // 2):
        x = get_collisions(toCheck)
        if not x:
            break
        for collider in x:
            collider[0].move(collider[0].distance_to(collider[1].get_position()) / -precision, direction = collider[0].direction_to(collider[1]))
            collider[1].move(collider[1].distance_to(collider[0].get_position()) / -precision, direction = collider[1].direction_to(collider[0]))

def flick(condition, variable):
    if condition:
        return not variable
    return variable