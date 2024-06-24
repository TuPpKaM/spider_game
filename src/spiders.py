
import random

import pygame

from settings import HALF_HEIGHT, HALF_WIDTH, MAX_EGGS, MEDIUM_EGG_TIMER
from utils import AnimationManager, AnimationMode, SpriteLoader


class Egg():
    def __init__(self, spawned: int = 0, grow_time: int = 0):
        self.spawned = spawned #TODO
        self.grow_time = grow_time

class SpiderEgg(pygame.sprite.Sprite, Egg):

    def __init__(self, group, image: pygame.Surface, width: int, height: int, spawned: int, grow_time: int):
        pygame.sprite.Sprite.__init__(self, group)
        Egg.__init__(self, spawned, grow_time)
        self.ready = False

        placeholder_image = pygame.image.load("assets\\tiles\\dot_purple.png").convert_alpha()
        self.ready_image = pygame.image.load("assets\\tiles\\dot_blue.png").convert_alpha()

        self.image = placeholder_image
        self.rect = self.image.get_rect()
        self.rect.center = (width, height)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawned >= self.grow_time and not self.ready:
            print('GROWN')
            self.image = self.ready_image
            self.mask = pygame.mask.from_surface(self.image)
            self.ready = True

class Units():

    def __init__(self):
        self.eggs = pygame.sprite.LayeredUpdates()
        self.spiders = pygame.sprite.LayeredUpdates()

    def spawn_spider(self, amount = 1, pos = (HALF_WIDTH, HALF_HEIGHT), spider_type = 0):
        match spider_type:
            case 0:
                RedSpider(self.spiders, self.eggs, pos[0], pos[1])
            case _:
                raise Exception()

    def update(self):
        for _ in self.eggs:
            _.update()
        for _ in self.spiders:
            _.update()

    def draw(self, screen):
        self.eggs.draw(screen)
        self.spiders.draw(screen)
        

class SpiderBase():
    def __init__(self, x: int, y: int, update_rate: int = 3):
        self.sprite_loader = SpriteLoader()
        self.a_manager = AnimationManager()
        self.a_mode = AnimationMode.IDLE_01
        self.a_angle = 157
        self.visible_image_index = 0
        self.ticks_since_last_frame = 0
        self.width = x
        self.height = y
        self.update_rate = update_rate

        file_path = self.sprite_loader.find_sheet_in_folder(self.sprite_parent_folder,self.a_mode.name,self.a_angle)
        cols, rows, scale = self.a_manager.extract_sheet_info(self.sprite_sheets[self.a_mode])
        self.images = self.a_manager.load_animation(file_path, cols, rows, scale)

        self.image = self.images[self.visible_image_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.width, self.height)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if(self.ticks_since_last_frame > self.update_rate): 
            self.ticks_since_last_frame = 0   
            self.visible_image_index += 1

            if(self.visible_image_index >= len(self.images)):
                self.visible_image_index = 0

            self.image = self.images[self.visible_image_index]
            self.rect = self.image.get_rect(center=self.rect.center)
            self.mask = pygame.mask.from_surface(self.image)
        else:
            self.ticks_since_last_frame += 1

    def lay_eggs(self):
        pass

class RedSpider(pygame.sprite.Sprite, SpiderBase):

    sprite_parent_folder = 'assets\\units\\red_spider'
    sprite_sheets = { #cols|rows|scale
        AnimationMode.IDLE_01:'4|3|0.5',
        AnimationMode.IDLE_02:'4|3|0.5',
        AnimationMode.ATTACK_02:'4|3|0.5'
    }

    def __init__(self, group, egg_group, width: int, height: int, update_rate: int = 3):
        pygame.sprite.Sprite.__init__(self, group)
        SpiderBase.__init__(self, width, height, update_rate)
        self.egg_laying_chance = 20
        self.egg_group = egg_group

        self.debug = 0 #DEBUG

    def change_animation_mode(self, mode: AnimationMode):
        if mode:
            self.a_mode = mode
        else:
            self.a_mode = random.choice(list(AnimationMode)) #DEBUG

        self.a_angle = self.a_manager.random_angle(step=45.0) #DEBUG

        file_path = self.sprite_loader.find_sheet_in_folder(self.sprite_parent_folder,self.a_mode.name,self.a_angle)
        cols, rows, scale = self.a_manager.extract_sheet_info(self.sprite_sheets[self.a_mode])
        self.images = self.a_manager.load_animation(file_path, cols, rows, scale)
        self.visible_image_index = 0
        self.ticks_since_last_frame = 0

    def update(self):
        #DEBUG ------------------------------
        self.debug += 1
        if(self.debug == 300):
            self.debug = 0
            self.change_animation_mode(None)
            self.lay_eggs()
        #DEBUG ------------------------------
            
        SpiderBase.update(self)

    def lay_eggs(self, pos: tuple = None):
        if(len(self.egg_group) < MAX_EGGS):
            if(random.randint(0, 100) < self.egg_laying_chance):
                if not pos:
                    pos = (self.width, self.height+10)
                    
                SpiderEgg(self.egg_group, None, pos[0], pos[1], pygame.time.get_ticks(), MEDIUM_EGG_TIMER) #TODO image