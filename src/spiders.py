
from functools import partial
import random

import pygame

from settings import HALF_HEIGHT, HALF_WIDTH
from utils import AnimationManager, AnimationMode, SpriteLoader

class Egg():
    def __init__(self, spawned: int, grow_time: int):
        pass

class SpiderEgg(pygame.sprite.Sprite, Egg):

    def __init__(self, image: pygame.Surface, width: int, height: int, spawned: int, grow_time: int):
        pygame.sprite.Sprite.__init__(self)
        Egg.__init__(self, spawned, grow_time)

        placeholder_image = pygame.image.load("assets\\tiles\\dot_purple.png").convert_alpha()

        self.image = placeholder_image
        self.rect = self.image.get_rect()
        self.rect.center = (width, height)
        self.mask = pygame.mask.from_surface(self.image)

class Units():

    def __init__(self):
        self.eggs = pygame.sprite.LayeredUpdates()
        self.spiders = pygame.sprite.LayeredUpdates()

    def spawn_spider(self, amount = 1, pos = (HALF_WIDTH, HALF_HEIGHT), spider_type = 0):
        match spider_type:
            case 0:
                new_spider = RedSpider(self.add_egg, pos[0], pos[1])
                self.spiders.add(new_spider)
            case _:
                raise Exception()
    
    def add_egg(self, egg: SpiderEgg):
        print('added egg')
        self.eggs.add(egg)

    def update(self):
        for _ in self.spiders:
            _.update()

    def draw(self, screen):
        self.eggs.draw(screen)
        self.spiders.draw(screen)
        

class SpiderBase():
    def __init__(self, callback: Units.add_egg, x: int, y: int, update_rate: int = 3):
        self.sprite_loader = SpriteLoader()
        self.a_manager = AnimationManager()
        self.a_mode = AnimationMode.IDLE_01
        self.a_angle = 157
        self.visible_image_index = 0
        self.ticks_since_last_frame = 0
        self.width = x
        self.height = y
        self.update_rate = update_rate
        self.egg_callback = callback
        print(self.egg_callback)

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

    def __init__(self, callback: Units.add_egg, width: int, height: int, update_rate: int = 3):
        pygame.sprite.Sprite.__init__(self)
        SpiderBase.__init__(self, callback, width, height, update_rate)
        self.egg_laying_chance = 20

        self.debug = 0 #DEBUG

    def change_animation_mode(self, mode: AnimationMode):
        if mode:
            self.a_mode = mode
        else:
            self.a_mode = random.choice(list(AnimationMode)) #DEBUG

        self.a_angle = self.a_manager.random_angle(step=45.0)

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
        if(random.randint(0, 100) < self.egg_laying_chance):
            print('RedSpider: Laying egg')
            new_egg = SpiderEgg(None, self.width, self.height+10)
            self.egg_callback(new_egg)