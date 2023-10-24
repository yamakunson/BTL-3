import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()
pygame.font.init()
pygame.mixer.init()
font = pygame.font.Font('freesansbold.ttf', 32)
font_endgame = pygame.font.Font('freesansbold.ttf', 120)
pygame.display.set_caption("Platformer")
kurukuru = pygame.mixer.Sound("Kurukuru.mp3")
kururing = pygame.mixer.Sound("Kururing.mp3")
nice = pygame.mixer.Sound("nice.mp3")
boom = pygame.mixer.Sound("boom.mp3")
hit = pygame.mixer.Sound("hit.mp3")
scream = pygame.mixer.Sound("scream.mp3")
WIDTH, HEIGHT = 1200, 800
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))
class game_manager:
    def __init__(self):
        self.game_status = 0
        self.objects = None
        self.enemies = None
        self.items = None
        self.particles = None
        self.player = None
        self.button = None
        self.music = True
manager = game_manager()

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

def load_sprite_sheets_3dir(dir1, dir2, dir3,  width, height, direction=False):
    path = join("assets", dir1, dir2,dir3)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

def load_1_sprite(dir1, dir2, image_name, width, height, direction=False):
    path = join("assets", dir1, dir2)
    image = image_name
    width *= 2
    height *= 2
    sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
    sprite_sheet = pygame.transform.scale(sprite_sheet,(sprite_sheet.get_width()*2,sprite_sheet.get_height()*2))
    sprites = []
    for i in range(sprite_sheet.get_width() // width):
        surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        rect = pygame.Rect(i * width, 0, width, height)
        surface.blit(sprite_sheet, (0, 0), rect)
        sprites.append(pygame.transform.scale2x(surface))
    return sprites

def get_block(size,type):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    if type == 1:
        rect = pygame.Rect(0, 0, size, size)
    elif type == 2:
        rect = pygame.Rect(0, 64, size, size)
    elif type == 3:
        rect = pygame.Rect(0, 128, size, size)
    elif type == 4:
        rect = pygame.Rect(96, 0, size, size)
    elif type == 5:
        rect = pygame.Rect(96, 64, size, size)
    elif type == 6:
        rect = pygame.Rect(96, 128, size, size)
    elif type == 7:
        rect = pygame.Rect(272, 64, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def get_fruit(size):
    path = join("assets", "Items","Fruits", "Strawberry.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

class Button:
    def __init__(self ,x,y,width,height,content,font,size,color,rect_color,name,draw_rect = True, image = None ):
        self.button_rect = pygame.Rect(x,y,width,height)
        self.font = pygame.font.Font(font, size)
        self.text = self.font.render(content,True,color)
        self.rect_color = rect_color
        self.draw_rect = draw_rect
        self.name = name
    def draw(self):
        text_rect = self.text.get_rect(center=(self.button_rect.x+self.button_rect.width/2, self.button_rect.y+self.button_rect.height/2))
        if self.draw_rect:
            pygame.draw.rect(window,self.rect_color,self.button_rect)
        window.blit(self.text, text_rect)
class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)
    ANIMATION_DELAY = 3
    GHOST_PARTICLE = load_1_sprite("Enemies","Ghost","Ghost Particles.png", 16 , 16)

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.hp = 5
        self.score = 0
        self.sprint = False
        self.cooldown = FPS 
        self.can_shoot = True
    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def shoot_player(self):
        if self.cooldown > 0:
            return
        dx = 0
        if self.direction == "right":
            dx = 10
            bullet = Bullet(self.rect.right,self.rect.y,32,32,"Player_Particle",self.GHOST_PARTICLE,FPS * 3,dx,0)
        else: 
            dx = -10
            bullet = Bullet(self.rect.x,self.rect.y,32,32,"Player_Particle",self.GHOST_PARTICLE,FPS * 3,dx,0)
        manager.particles.append(bullet)
        self.cooldown = FPS/4
            
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self,hp_lost):
        self.hit = True
        if(self.hit_count == 0):
            self.hp -= hp_lost
            pygame.mixer.Sound.play(hit)

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        if(self.fall_count > 0):
            self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        
        self.cooldown -= 1
        if self.cooldown <0:
            self.cooldown = 0
            
        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        self.ANIMATION_DELAY = 3
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            if(pygame.key.get_pressed()[pygame.K_LSHIFT]) and self.sprint:
                self.ANIMATION_DELAY = 2
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.type = "Object"
        self.width = width
        self.height = height
        self.name = name
        self.status = True
        self.animated = False
        self.breakable = False
    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y,type,breakable = False):
        size = 96
        super().__init__(x, y, size, size)
        block = get_block(size,type)
        if type in [4,5,6]:
            self.type = "Terrain"
        elif type in [1,2,3,7]:
            self.type = "Block"
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.breakable = breakable

class Fruit(Object):
    ANIMATION_DELAY = 3
    def __init__(self, x, y,name):
        super().__init__(x, y, 32, 32, name)
        self.fruit = load_sprite_sheets("Items", "Fruits", 32, 32)
        self.type = "Item"
        self.image = self.fruit[name][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.sprites = self.fruit[name]
        self.animation_count = 0
    def loop(self):
            sprite_index = (self.animation_count //
                            self.ANIMATION_DELAY) % len(self.sprites)
            self.image = self.sprites[sprite_index]
            self.animation_count += 1

            self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
            self.mask = pygame.mask.from_surface(self.image)

            if self.animation_count // self.ANIMATION_DELAY > len(self.sprites):
                self.animation_count = 0

class Checkpoint(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, ):
        super().__init__(x, y, 64, 64, "Checkpoint")
        self.SPRITE = load_sprite_sheets_3dir("Items", "Checkpoints","Checkpoint", 64, 64)
        self.image = self.SPRITE["Idle"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.type = "Item"
        self.animation_count = 0
        self.animation_name = "Idle"

    def loop(self):
        sprites = self.SPRITE[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0
class Bullet(Object):
    ANIMATION_DELAY = 3
    def __init__(self, x, y, width, height,name, SPRITES, exist_time, dx,dy):
        super().__init__(x, y, width, height, name)
        self.type = "Bullet"
        self.sprites = SPRITES
        self.image = self.sprites[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.exist_time = exist_time 
        self.dx = dx
        self.dy = dy
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    def loop(self):
        self.exist_time -= 1 
        if self.exist_time <= 0:
            self.status = False
        if self.status == True:
            self.move(self.dx, self.dy)
            
            for obj in manager.objects:
                if pygame.sprite.collide_mask(self, obj) and obj.breakable == True:
                    self.status = False
                    obj.status = False
                    pygame.mixer.Sound.play(boom)
                    break        
            for enemy in manager.enemies:
                if pygame.sprite.collide_mask(self, enemy) and self.name == "Player_Particle":
                    self.status = False
                    enemy.hit = True
                    pygame.mixer.Sound.play(boom)
                    break        
            sprite_index = (self.animation_count //
                            self.ANIMATION_DELAY) % len(self.sprites)
            self.image = self.sprites[sprite_index]
            self.animation_count += 1
            self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
            self.mask = pygame.mask.from_surface(self.image)
            if self.animation_count // self.ANIMATION_DELAY > len(self.sprites):
                self.animation_count = 0                        
class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.type = "Block"
        self.animation_count = 0
        self.animation_name = "on"
        self.animated = True

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

class Enemy(pygame.sprite.Sprite):
    GRAVITY = 1
    ANIMATION_DELAY = 3

    def __init__(self, x, y, name):
        super().__init__()
        self.hp = 5
        if name == "AngryPig":
            width = 36
            height = 30
        elif name == "Ghost":
            width = 44
            height = 30
        self.rect = pygame.Rect(x, y, width, height)
        self.SPRITE = load_sprite_sheets("Enemies", name, width, height, True)
        self.type = "Enemy"
        self.name = name
        self.x_vel = -3
        self.y_vel = 0
        self.mask = None
        self.direction = "right"
        self.animation_count = 0
        self.animation_name = "None"
        self.fall_count = 0
        self.hit = False
        self.hit_count = 0
        self.status = True
        self.hp = 5

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True

    def loop(self, fps,):
        if self.rect.y > HEIGHT:
            self.status = False
        if self.status == False:
            return
        if(self.fall_count > 0 ):
            self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        
        if self.hit:
            if self.hit_count == 0:
                self.hp -=1
            self.hit_count += 1
        if self.hit_count > fps:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def update_sprite(self):
        self.ANIMATION_DELAY = 3
        self.animation_name = "Idle"
        sprite_sheet = self.animation_name
        if self.name == "AngryPig":
            sprite_sheet = "Run"
        if self.hit and self.name == "AngryPig":
            sprite_sheet = "Hit 1"
        elif self.hit and self.name == "Ghost":
            sprite_sheet = "Hit"
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITE[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

class AngryPig(Enemy):
    def __init__(self, x, y):
        super().__init__(x,y,"AngryPig")
        self.hp = 3
    def loop(self, fps):
        if self.rect.y > HEIGHT or self.hp <= 0:
            self.status = False
            pygame.mixer.Sound.play(nice)
        if self.status == False:
            return
        if(self.fall_count > 0 ):
            self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        
        if self.hit:
            if self.hit_count == 0:
                self.hp -=1
            self.hit_count += 1
        if self.hit_count > fps:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def update_sprite(self):
        self.ANIMATION_DELAY = 3
        self.animation_name = "Idle"
        sprite_sheet = self.animation_name
        sprite_sheet = "Run"
        if self.hit :
            sprite_sheet = "Hit 1"
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITE[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()
class Ghost(Enemy):
    GHOST_PARTICLE = load_1_sprite("Enemies","Ghost","Ghost Particles.png", 16 , 16)
    def __init__(self, x, y):
        super().__init__(x,y,"Ghost")
        self.cooldown = FPS * 4
        self.hp = 5
        
    def shoot_player(self):
        dx = 0
        if manager.player.rect.right <= self.rect.x:
            if self.x_vel > 0:
                self.x_vel *= -1
                self.direction = "right"
            dx = -6
            bullet = Bullet(self.rect.x,self.rect.y,32,32,"Ghost_Particle",self.GHOST_PARTICLE,FPS * 3,dx,0)
            manager.particles.append(bullet)
        elif manager.player.rect.left > self.rect.x:
            if self.x_vel < 0:
                self.x_vel *= -1
                self.direction = "left"
            dx = 6
            bullet = Bullet(self.rect.right,self.rect.y,32,32,"Ghost_Particle",self.GHOST_PARTICLE,FPS * 3,dx,0)
            manager.particles.append(bullet)
            
        

    def loop(self, fps):
        if self.rect.y > HEIGHT or self.hp <= 0:
            self.status = False
            pygame.mixer.Sound.play(scream)
        if self.status == False:
            return
        
        if(self.fall_count > 0 ):
            self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        self.cooldown -= 1
        if self.cooldown <0:
            self.cooldown = 0
        if self.cooldown == 0:
            self.shoot_player()
            self.cooldown = FPS * 4
        if self.hit:
            if self.hit_count == 0:
                self.hp -= 2
            self.hit_count += 1
        if self.hit_count > fps:
            self.hit = False
            self.hit_count = 0
        self.fall_count += 1
        self.update_sprite()

    def update_sprite(self):
        self.ANIMATION_DELAY = 3
        self.animation_name = "Idle"
        sprite_sheet = self.animation_name
        if self.hit :
            sprite_sheet = "Hit"
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITE[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

def draw(window, bg_image, offset_x , display):
    window.blit(bg_image, (0,0))
    for item in manager.items:
        if item.status == True:
            item.draw(window, offset_x)
    for obj in manager.objects:
        obj.draw(window, offset_x)
    for particle in manager.particles:
        if particle.status == True:
            particle.draw(window, offset_x)
    manager.player.draw(window, offset_x)
    for enemy in manager.enemies:
        if enemy.status == True:
            enemy.draw(window, offset_x)
    
    for i in range(0,manager.player.hp):
        window.blit(display[0],(i*48,0))
    window.blit(display[1],(20,64))
        
    pygame.display.update()


def handle_vertical_collision(dy):
    collided_objects = []
    for obj in manager.objects:
        if pygame.sprite.collide_mask(manager.player, obj):
            if dy >= 0 and manager.player.rect.bottom < obj.rect.bottom:
                manager.player.rect.bottom = obj.rect.top
                manager.player.landed()
            #elif dy < 0:
                #player.rect.top = obj.rect.bottom
                #player.hit_head()
            collided_objects.append(obj)
    for enemy in manager.enemies:
        if enemy.status == False:
            continue
        if pygame.sprite.collide_mask(manager.player, enemy):
            if dy >= 0 and enemy.name == "AngryPig":
                manager.player.rect.bottom = enemy.rect.top
                manager.player.landed()
                manager.player.y_vel = -5
                enemy.status = False
                pygame.mixer.Sound.play(nice)
                
    return collided_objects


def collide(dx):
    manager.player.move(dx, 0)
    manager.player.update()
    collided_object = None
    for obj in manager.objects:
        if pygame.sprite.collide_mask(manager.player, obj):
            collided_object=obj
            break
    for item in manager.items:
        if pygame.sprite.collide_mask(manager.player, item):
            collided_object=item
            break
    for particle in manager.particles:
        if particle.status == False:
            continue
        if pygame.sprite.collide_mask(manager.player, particle):
            collided_object=particle
            break
    for enermy in manager.enemies:
        if enermy.status == False:
            continue
        if pygame.sprite.collide_mask(manager.player, enermy):
            collided_object=enermy
            break
    manager.player.move(-dx, 0)
    manager.player.update()
    return collided_object

def enemy_collide(enemy,dx):
    enemy.move(dx, 0)
    enemy.update()
    collided_object = None
    for obj in manager.objects:
        if pygame.sprite.collide_mask(enemy, obj):
            collided_object=obj
            break
    enemy.move(-dx, 0)
    enemy.update()
    return collided_object    


def handle_move():
    keys = pygame.key.get_pressed()
    manager.player.x_vel = 0
    collide_left = collide( -PLAYER_VEL * 2)
    collide_right = collide( PLAYER_VEL * 2)

    if keys[pygame.K_a] and (collide_left == None or collide_left.type in ["Enemy","Bullet","Item"]):
        if(keys[pygame.K_LSHIFT]) and manager.player.sprint:
            manager.player.move_left(PLAYER_VEL*1.5)
        else:
            manager.player.move_left(PLAYER_VEL)
    if keys[pygame.K_d] and (collide_right == None or collide_right.type in ["Enemy","Bullet","Item"]):
        if(keys[pygame.K_LSHIFT]) and manager.player.sprint:
            manager.player.move_right(PLAYER_VEL*1.5)
        else:
            manager.player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(manager.player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name == "fire":
            manager.player.make_hit(1)
        elif obj and obj.name == "AngryPig" and obj.status == True:
            manager.player.make_hit(1)
        elif obj and obj.name == "Ghost" and obj.status == True:
            manager.player.y_vel = -4
            manager.player.jump_count = 2
            manager.player.make_hit(1)
        elif obj and obj.name == "Ghost_Particle" and obj.status == True:
            manager.player.y_vel = -4
            manager.player.jump_count = 2
            manager.player.make_hit(3)            
            obj.status = False
def handle_enemy_move(enermy):
    collide_left = enemy_collide(enermy, -PLAYER_VEL )
    collide_right = enemy_collide(enermy, PLAYER_VEL )
    if (collide_left and collide_left.type == "Block") or (collide_right and collide_right.type == "Block") :
        enermy.x_vel *= -1
        if enermy.direction == "left":
            enermy.direction = "right"
        else:
            enermy.direction = "left"
    for obj in manager.objects:
        if pygame.sprite.collide_mask(enermy, obj):
            if enermy.y_vel >= 0 and enermy.rect.bottom < obj.rect.bottom:
                enermy.rect.bottom = obj.rect.top
                enermy.y_vel = 0
    
def handle_items():
    col = collide(0)
    if col and col.name == "Apple" and col.status == True:
        manager.player.score+=1
        col.status = False
        if manager.music:
            pygame.mixer.Sound.play(kururing)
    elif col and col.name == "Bananas" and col.status == True:
        manager.player.score+=1
        manager.player.sprint =True
        col.status = False
        if manager.music:
            pygame.mixer.Sound.play(kururing)
    elif col and col.name == "Cherries" and col.status == True:
        manager.player.score+=5
        manager.player.hp += 3
        manager.player.can_shoot = True
        col.status = False
        if manager.music:
            pygame.mixer.Sound.play(kururing)
    elif col and col.name == "Checkpoint" and len(manager.enemies) == 0:
        col.animation_name = "No Flag"
        manager.game_status = 3
        if manager.music:
            pygame.mixer.Sound.play(nice)

def play():
    clock = pygame.time.Clock()
    background = pygame.transform.scale(pygame.image.load(join("assets", "Background", "background.jpg")), (WIDTH,HEIGHT))
    hp_img = get_fruit(32)
    block_size = 96
    manager.game_status = 1
    manager.player = Player(100, 100, 50, 50)

    manager.items = [Fruit(700,HEIGHT - block_size * 3 , "Apple"),Fruit(1015,HEIGHT - block_size * 3 ,"Apple"),
                       Fruit(block_size*14+10,HEIGHT - block_size * 4 , "Bananas"), Fruit(block_size*-13 + 25,HEIGHT - block_size * 4 , "Cherries"),
                       Checkpoint(57*block_size,HEIGHT-block_size*2-32), Fruit(1950,HEIGHT - block_size * 2 , "Cherries")] + [Fruit(1950 + 300*i, HEIGHT - block_size*2, "Apple") for i in range(1,4)]
    manager.objects= [Block(i * block_size, HEIGHT - block_size,4) 
             for i in range(-1, 8)] + [Block(- block_size, HEIGHT - block_size*i, 2) 
                                        for i in range(2,4)] + [Block(i * block_size, HEIGHT - block_size,4)
                                                                 for i in range(10, 12)] + [Block(i * block_size, HEIGHT - block_size, 4)
                                                                                            for i in range(17, 32)] + [Block(i * block_size, HEIGHT - block_size, 4) for i in range(43, 59)]
    manager.objects +=  [Block(- block_size, HEIGHT - block_size*i, 2) 
               for i in range(2,4)] + [Block(block_size*59, HEIGHT - block_size*i, 2) 
                                        for i in range(1,6)] 
    manager.objects += [Block(14 * block_size, HEIGHT - block_size*3, 4),Block(-7* block_size, HEIGHT - block_size*3, 4),Block(-13* block_size, HEIGHT - block_size*3, 4), 
                Block(7 * block_size, HEIGHT - block_size*2, 2), Block(37 * block_size, HEIGHT - block_size*2, 4), Block(32 * block_size, HEIGHT - block_size*2, 2),
                Block(43 * block_size, HEIGHT - block_size*2, 2), Block(1930, HEIGHT - block_size*2, 3,True)]                                       
    manager.particles = []
    manager.enemies = [Ghost(4500,HEIGHT-block_size-50),AngryPig(600,HEIGHT-block_size-50),AngryPig(2850,HEIGHT-block_size-50),AngryPig(4600,HEIGHT-block_size-50)] 
    manager.objects += [Fire(2100+300*i, HEIGHT - block_size - 64, 16, 32) for i in range(0,3)] + [Fire(300, HEIGHT - block_size - 64, 16, 32)]
    offset_x = 0
    scroll_area_width = 300
    endgame = None
    run = True
    while run:
        clock.tick(FPS)
        if manager.game_status != 1:
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                manager.game_status = -1
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and manager.player.jump_count < 2:
                    manager.player.jump()
                if event.key == pygame.K_LCTRL and manager.player.can_shoot:
                    manager.player.shoot_player()
        for obj in manager.objects:
            if obj.status == False:
                manager.objects.remove(obj)
        for obj in manager.particles:
            if obj.status == False:
                manager.particles.remove(obj)
        for obj in manager.items:
            if obj.status == False:
                manager.items.remove(obj)
        for obj in manager.enemies:
            if obj.status == False:
                manager.enemies.remove(obj)
        manager.player.loop(FPS)
    
        for enemy in manager.enemies:
            enemy.loop(FPS)
        for obj in manager.objects:
            if obj.animated == True:
                obj.loop()
        for obj in manager.items:
            obj.loop()
        for obj in manager.particles:
            obj.loop()
            
        handle_move()        
        for enermy in manager.enemies:
            handle_enemy_move(enermy)        
        handle_items()
        score = font.render("Score: " + str(manager.player.score), True, (255, 255, 0),None)
        if manager.player.rect.y >HEIGHT or manager.player.hp <= 0:
            manager.player.rect.x = 0
            manager.player.rect.y = HEIGHT
            manager.game_status = 2
            run = False
            
        display = [hp_img,score]
        draw(window, background, offset_x,display)
        if ((manager.player.rect.right - offset_x >= 800) and manager.player.x_vel > 0) or (
                (manager.player.rect.left - offset_x <= 400) and manager.player.x_vel < 0):
            offset_x += manager.player.x_vel

def menu():
    clock = pygame.time.Clock()
    background = pygame.transform.scale(pygame.image.load(join("assets","Menu_Background.png")), (WIDTH,HEIGHT))
    manager.button = [Button(WIDTH/2 - 175,HEIGHT/2 - 250,400,200,"New Game",'freesansbold.ttf',80,(255, 0, 0),(255, 255, 0),"New Game",False),
                      Button(WIDTH/2 - 175,HEIGHT/2 - 50,400,150,"Option",'freesansbold.ttf',80,(255,0,0),(255, 255,255),"Option",False),
                      Button(WIDTH/2 - 175,HEIGHT/2 + 150,400,150,"Exit",'freesansbold.ttf',80,(255,0,0),(255, 255,255),"Exit",False)]
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                manager.game_status = -1
                break
            elif event.type== pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in manager.button:
                    if button.button_rect.collidepoint(pos):
                        if button.name == "New Game":
                            run = False
                            manager.game_status = 1
                            break
                        elif button.name == "Exit":
                            run = False
                            manager.game_status = -1
                            break
                        elif button.name == "Option":
                            run = False
                            manager.game_status = 4
                            break
        window.blit(background, (0,0))
        for but in manager.button:
            but.draw()
        pygame.display.update()

def lose():
    clock = pygame.time.Clock()
    background = pygame.transform.scale(pygame.image.load(join("assets", "Background", "background.jpg")), (WIDTH,HEIGHT))
    manager.button = [Button(WIDTH/2 - 150,HEIGHT/2 - 250,400,200,"WASTED",'freesansbold.ttf',120,(255, 0, 0),(255, 255, 0),"",False),
                      Button(WIDTH/2 - 150,HEIGHT/2 - 50,400,150,"Try again",'freesansbold.ttf',80,(0,0,0),(255, 255,255),"TryAgain",False),
                      Button(WIDTH/2 - 150,HEIGHT/2 + 100,400,150,"Menu",'freesansbold.ttf',80,(0,0,0),(255, 255,255),"Menu",False)]
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                manager.game_status = -1
                break
            elif event.type== pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in manager.button:
                    if button.button_rect.collidepoint(pos):
                        if button.name == "TryAgain":
                            run = False
                            manager.game_status = 1
                            break
                        if button.name == "Menu":
                            run = False
                            manager.game_status = 0
                            break
        window.blit(background, (0,0))
        for but in manager.button:
            but.draw()
        pygame.display.update()

def victory():
    clock = pygame.time.Clock()
    background = pygame.transform.scale(pygame.image.load(join("assets", "Background", "background.jpg")), (WIDTH,HEIGHT))
    manager.button = [Button(WIDTH/2 - 250,HEIGHT/2 - 350,600,200,"VICTORY",'freesansbold.ttf',96,(255, 255, 0),(135,206,235),"",False),
                      Button(WIDTH/2 - 150,HEIGHT/2 - 150,400,150,"Your Score is : " + str(manager.player.score),'freesansbold.ttf',80,(255,0,0),(255, 255,255),"",False),
                      Button(WIDTH/2 - 150,HEIGHT/2 ,400,150,"New Game",'freesansbold.ttf',80,(0, 0, 0),(255, 255, 0),"New Game",False),
                      Button(WIDTH/2 - 150,HEIGHT/2 + 150,400,150,"Menu",'freesansbold.ttf',80,(0,0,0),(255, 255,255),"Menu",False)]
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                manager.game_status = -1
                break
            elif event.type== pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in manager.button:
                    if button.button_rect.collidepoint(pos):
                        if button.name == "New Game":
                            run = False
                            manager.game_status = 1
                            break
                        elif button.name == "Menu":
                            run = False
                            manager.game_status = 0
                            break
        window.blit(background, (0,0))
        for but in manager.button:
            but.draw()
        pygame.display.update()

def music():
    clock = pygame.time.Clock()
    background = pygame.transform.scale(pygame.image.load(join("assets","Menu_Background.png")), (WIDTH,HEIGHT))
    image_on = pygame.transform.scale(pygame.image.load(join("assets","Menu","music_on.png")), (200,200))
    image_off = pygame.transform.scale(pygame.image.load(join("assets","Menu","music_off.png")), (200,200))
    image_rect = pygame.Rect(WIDTH/2-100,HEIGHT-400,200,200)
    manager.button = [Button(WIDTH/2 - 175,HEIGHT/2 - 250,400,200,"Menu",'freesansbold.ttf',80,(255, 0, 0),(255, 255, 255),"Menu",False)]
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                manager.game_status = -1
                break
            elif event.type== pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in manager.button:
                    if button.button_rect.collidepoint(pos):
                        if button.name == "Menu":
                            run = False
                            manager.game_status = 0
                            break
                if image_rect.collidepoint(pos):
                    manager.music = not manager.music
        window.blit(background, (0,0))
        for but in manager.button:
            but.draw()
        if manager.music:
            window.blit(image_on, image_rect)
        else:
            window.blit(image_off, image_rect)
        pygame.display.update()     
        
def main():
    while(manager.game_status != -1):
        if manager.game_status == 0:
            menu()
        elif manager.game_status == 1:
            play()        
        elif manager.game_status == 2:
            lose()
        elif manager.game_status == 3:
            victory()    
        elif manager.game_status == 4:
            music()    
    pygame.quit()
    quit()
    

if __name__ == "__main__":
    main()
