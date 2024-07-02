
import random

import pygame

from registry import Registry, ClassRegistry
from settings import MAX_EGGS, MEDIUM_EGG_TIMER
from utils import (AnimationManager, AnimationMode, IsometricConversions,
                   SpriteLoader, WanderManager)

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

    def __init__(self, isometric_conversions: IsometricConversions):
        self.isometric_conversions = isometric_conversions
        self.animation_manager = AnimationManager(cache_size=100)
        self.eggs = pygame.sprite.LayeredUpdates()
        self.spiders = pygame.sprite.LayeredUpdates()

    def spawn_spider(self, amount = 10, pos = None, spider_type = 0):
        if not pos:
            pos = self.isometric_conversion.get_center_of_screen()

        match spider_type:
            case 0:
                RedSpider(self.isometric_conversions, self.animation_manager, self.spiders, self.eggs, pos[0], pos[1], wander=True)
            case 1:
                for _ in range(amount):
                    Spiderling(self.isometric_conversions, self.animation_manager, self.spiders, pos[0], pos[1], wander=True)
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

    def __init__(self, isometric_conversions: IsometricConversions, animation_manager, x: int, y: int, wander: bool, update_rate: int):
        self.sprite_loader = SpriteLoader()
        self.isometric_conversions = isometric_conversions
        self.a_manager = animation_manager
        self.a_mode = AnimationMode.WALK_FORWARD #IDLE_01
        self.a_angle = 157
        self.visible_image_index = 0
        self.ticks_since_last_frame = 0
        self.x = x
        self.y = y
        self.animation_update_rate = update_rate

        self.wander_manager = WanderManager(self.isometric_conversions, (x,y), speed=10, steps=3)
        self.wander = wander

        self._load_animation_images()
        self._load_image()

        Registry.register_instance(self)

    def _load_animation_images(self):
        file_path = self.sprite_loader.find_sheet_in_folder(self.sprite_parent_folder,self.a_mode.name,self.a_angle)
        cols, rows, scale = self.a_manager.extract_sheet_info(self.sprite_sheets[self.a_mode])
        self.images = self.a_manager.load_animation(file_path, cols, rows, scale)
    
    def _load_image(self):
        self.image = self.images[self.visible_image_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self): # TODO:: delta time dt ?
        if(self.ticks_since_last_frame > self.animation_update_rate): 
            self.ticks_since_last_frame = 0   
            
            # Animation image
            self.visible_image_index += 1

            if(self.visible_image_index >= len(self.images)):
                self.visible_image_index = 0

            self.image = self.images[self.visible_image_index]
            self.rect = self.image.get_rect(center=self.rect.center)
            self.mask = pygame.mask.from_surface(self.image)

            # Wander pos
            if(self.wander):   
                if(not self.wander_manager.has_positions_left()):
                    self.wander_manager.generate_positions()
                    self.a_mode = self.wander_manager.get_animation_mode()
                    wander_angle = self.wander_manager.get_animation_angle()
                    self.a_angle = self.a_manager.angle_to_animation_angle(wander_angle)
                    self._load_animation_images()
                    self._load_image()

                self.x , self.y = self.wander_manager.get_next_position()
                self.rect.center = (self.x, self.y)

                #print(f'wander pos x{self.x} y{self.y}')
        else:
            self.ticks_since_last_frame += 1
        
    def to_dict(self):
        return {
            'class_name': self.__class__.__name__,
            'a_mode': self.a_mode.name,
            'a_angle': self.a_angle,
            'visible_image_index': self.visible_image_index,
            'ticks_since_last_frame': self.ticks_since_last_frame,
            'x': self.x,
            'y': self.y,
            'animation_update_rate': self.animation_update_rate,
            'wander': self.wander
        }
    
    @classmethod
    def from_dict(cls, data, isometric_conversions, animation_manager):
        instance = cls(
            isometric_conversions, 
            animation_manager, 
            data['x'], 
            data['y'], 
            data['wander'],
            data['animation_update_rate']
        )
        instance.a_mode = AnimationMode[data['a_mode']]
        instance.a_angle = data['a_angle']
        instance.visible_image_index = data['visible_image_index']
        instance.ticks_since_last_frame = data['ticks_since_last_frame']
        return instance

class RedSpider(pygame.sprite.Sprite, SpiderBase):

    sprite_parent_folder = 'assets\\units\\red_spider'
    sprite_sheets = { #cols|rows|scale
        AnimationMode.IDLE_01:'4|3|0.5',
        AnimationMode.IDLE_02:'4|3|0.5',
        AnimationMode.ATTACK_02:'4|3|0.5',
        AnimationMode.WALK_FORWARD:'3|3|0.5'
    }

    def __init__(self, isometric_conversions: IsometricConversions, animation_manager, group, egg_group, width: int, height: int, wander: bool = False, update_rate: int = 3):
        pygame.sprite.Sprite.__init__(self, group)
        SpiderBase.__init__(self, isometric_conversions, animation_manager, width, height, wander, update_rate)
        self.egg_laying_chance = 20
        self.egg_group = egg_group

        Registry.register_instance(self)    

        self.debug = 0 #DEBUG

    def update(self):
        #DEBUG ------------------------------
        self.debug += 1
        if(self.debug == 300):
            self.debug = 0
            self.lay_eggs()
        #DEBUG ------------------------------
            
        SpiderBase.update(self)

    def lay_eggs(self, pos: tuple = None):
        if(len(self.egg_group) < MAX_EGGS):
            if(random.randint(0, 100) < self.egg_laying_chance):
                if not pos:
                    pos = (self.x, self.y+10)
                    
                SpiderEgg(self.egg_group, None, pos[0], pos[1], pygame.time.get_ticks(), MEDIUM_EGG_TIMER) #TODO image

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'class_name': self.__class__.__name__,
        })
        return data
    
    @classmethod
    def from_dict(cls, data, isometric_conversions, animation_manager, group, egg_group):
        instance = cls(
            isometric_conversions, 
            animation_manager,
            group,
            egg_group, 
            data['x'], 
            data['y'], 
            data['wander'], 
            data['animation_update_rate']
        )
        instance.a_mode = AnimationMode[data['a_mode']]
        instance.a_angle = data['a_angle']
        instance.visible_image_index = data['visible_image_index']
        instance.ticks_since_last_frame = data['ticks_since_last_frame']
        return instance

class Spiderling(pygame.sprite.Sprite, SpiderBase):

    sprite_parent_folder = 'assets\\units\\spiderling'
    sprite_sheets = { #cols|rows|scale
        AnimationMode.IDLE_01:'4|3|1',
        AnimationMode.IDLE_02:'4|3|1',
        AnimationMode.ATTACK_02:'4|3|1',
        AnimationMode.WALK_FORWARD:'3|3|1'
    }

    def __init__(self, isometric_conversions: IsometricConversions, animation_manager, group, width: int, height: int, wander: bool = False, update_rate: int = 3):
        pygame.sprite.Sprite.__init__(self, group)
        SpiderBase.__init__(self, isometric_conversions, animation_manager, width, height, wander, update_rate)

        Registry.register_instance(self) 

    def update(self):
        SpiderBase.update(self)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'class_name': self.__class__.__name__,
        })
        return data
    
    @classmethod
    def from_dict(cls, data, isometric_conversions, animation_manager, group):
        instance = cls(
            isometric_conversions, 
            animation_manager,
            group,
            data['x'], 
            data['y'], 
            data['wander'], 
            data['animation_update_rate']
        )
        instance.a_mode = AnimationMode[data['a_mode']]
        instance.a_angle = data['a_angle']
        instance.visible_image_index = data['visible_image_index']
        instance.ticks_since_last_frame = data['ticks_since_last_frame']
        return instance
    
#TODO:: register all classes
ClassRegistry.register_class(SpiderBase)
ClassRegistry.register_class(RedSpider)
ClassRegistry.register_class(Spiderling)