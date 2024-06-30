import os
import random
from enum import Enum
from random import uniform

import pygame

from game_screen_manager import GameScreenSizeManager
from settings import *


class SpriteLoader:
    def split_sprite(self, path, cols, rows = 1, scale = 1) -> list:
        spritesheet = pygame.image.load(path).convert_alpha()

        sprite_width = spritesheet.get_width() // cols
        sprite_height = spritesheet.get_height() // rows

        sprites = []

        for row in range(rows):
            for col in range(cols):
                x = col * sprite_width
                y = row * sprite_height
                sprite = spritesheet.subsurface(pygame.Rect(x, y, sprite_width, sprite_height))
                if scale != 1:
                    sprites.append(self.scale_sprite(sprite, scale))
                else:
                    sprites.append(sprite)

        return sprites

    def scale_sprite(self, original_sprite: pygame.Surface, scale_factor: float) -> pygame.Surface:
        original_width, original_height = original_sprite.get_size()

        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)

        return pygame.transform.scale(original_sprite, (new_width, new_height))
    
    def find_sheet_in_folder(self, parent_folder: str, subfolder_name: str, angle: int) -> str:
        subfolder_path = os.path.join(parent_folder, subfolder_name)
    
        if not os.path.exists(subfolder_path):
            raise FileNotFoundError(f"The subfolder {subfolder_name} does not exist in {parent_folder}")

        for file_name in os.listdir(subfolder_path):
            if file_name.endswith(f'{angle:03d}.png'):
                file_path = os.path.join(subfolder_path, file_name)
                return file_path

        raise FileNotFoundError(f"No sheet with angle {angle} found in {subfolder_name}")


class AnimationManager:
    def __init__(self, cache_size: int = 25, print: bool = False):
        self.loader = SpriteLoader()
        self.cache = {}
        self.max_cache_size = cache_size
        self.print = print

    def load_animation(self, file_path: str, cols: int, rows: int, scale: float):
        file = os.path.basename(file_path)
        if file in self.cache:
            if self.print:
                print(f"Loaded from cache: {file_path}, cache_count: {len(self.cache)}")
            return self.cache[file]
        else:
            if self.print:
                print(f"Loading: {file_path}")
            animation_images = self.loader.split_sprite(file_path, cols, rows, scale)
            self.cache[file] = animation_images
            self._check_cache_size()
            return animation_images

    def unload_animation(self, file_path: str):
        if file_path in self.cache:
            if self.print:
                print(f"Unloading: {file_path}")
            del self.cache[file_path]

    def _check_cache_size(self):
        if len(self.cache) > self.max_cache_size:
            oldest_key = next(iter(self.cache))
            self.unload_animation(oldest_key)

    def extract_sheet_info(self, input: str):
        cols, rows, scale = input.split('|') #TODO:: errors
        return int(cols) , int(rows), float(scale)
    
    def random_angle(self, step: float = 22.5) -> int:
        random_int = random.randint(0, 337)
        nearest_multiple_index = round(random_int / step)
        angle = int(nearest_multiple_index * step)
        if(angle < 0 or angle > 337):
            raise Exception()
        else:
            return angle


class IsometricConversions:

    def __init__(self, screen_manager: GameScreenSizeManager):
        self.screen_manager = screen_manager
        self.array_2d = None

    def set_array(self, array_2d: list):
        self.array_2d = array_2d

    def get_array(self) -> list:
        return self.array_2d

    def get_center_of_screen(self) -> int:
        width, height = self.screen_manager.get_screen_size()
        return width//2 , height//2

    def get_grid_start(self) -> int:
        center_w, center_h = self.get_center_of_screen()
        center_h += 150 #TODO:: calculate from wall height and grid size

        start_w = center_w - ((TILE_W * (TILE_COUNT_W + TILE_COUNT_H))/4)
        start_h = center_h + ((TILE_H * (TILE_COUNT_W))/4) - (TILE_H/2)

        if ( TILE_COUNT_H >  TILE_COUNT_W):
            start_h = center_h - ((TILE_H * (TILE_COUNT_H))/4) + (TILE_H/2)
        return start_w, start_h

    def grid_to_iso(self, x: int, y: int) -> int:
        origin_iso_x, origin_iso_y = self.get_grid_start()

        iso_x = origin_iso_x + ((x+y)*(TILE_W//2)) # TODO:: x-y
        iso_y = origin_iso_y + ((x-y)*(TILE_H//2)) # TODO:: x+y
        return iso_x, iso_y
    
    def iso_to_grid(self, iso_x: int, iso_y: int) -> int:
        origin_iso_x, origin_iso_y = self.get_grid_start()

        x = ((iso_x - origin_iso_x) / (TILE_W / 2) + (iso_y - origin_iso_y) / (TILE_H / 2)) / 2
        y = abs(((iso_y - origin_iso_y) / (TILE_H / 2) - (iso_x - origin_iso_x) / (TILE_W / 2)) / 2) # TODO:: not abs
        return int(x), int(y)
    
    def get_random_coord_value(self) -> int:
        if self.array_2d:
            x_index = random.randint(0, len(self.array_2d) - 1)
            y_index = random.randint(0, len(self.array_2d[0]) - 1)
            return self.grid_to_iso(x_index,y_index)
        else:
            raise Exception('No array provided for calculations')
    
    def get_random_coord_index(self) -> int:
        if self.array_2d:
            x_index = random.randint(0, len(self.array_2d) - 1)
            y_index = random.randint(0, len(self.array_2d[0]) - 1)
            return x_index, y_index
        else:
            raise Exception('No array provided for calculations')


class WanderManager:

    def __init__(self, isometric_conversions: IsometricConversions, start_pos_value: tuple, speed: int, steps: int):
        self.isometric_conversions = isometric_conversions
        self.current_pos_value = start_pos_value
        self.target_pos_value = start_pos_value
        self.speed = speed
        self.steps = steps
        self.positions_to_visit_value = []
        self.animation_mode = None

    def has_positions_left(self) -> bool:
        return len(self.positions_to_visit_value) > 0
    
    def get_next_position(self) -> tuple:
        self.current_pos_value = self.positions_to_visit_value.pop(0)
        round_x = round(self.current_pos_value[0],POSITION_DECIMALS)
        round_y = round(self.current_pos_value[1],POSITION_DECIMALS)
        return round_x, round_y
    
    def get_animation_mode(self):
        if not self.has_positions_left or not self.animation_mode:
            return AnimationMode.IDLE_01
        else:
            return self.animation_mode
    
    def generate_positions(self):
        positions_added = 0
        tries = 0
        while(positions_added < 1 and tries < 30): #TODO:: replace tries with smarter logic
            tries += 1
            positions_added = self._generate_new_positions()

        if(positions_added == 0): #TODO:: debug
            raise Exception()

        self.animation_mode = AnimationMode.WALK_FORWARD #TODO::determine from direction

    def _generate_new_positions(self) -> int:
        self.positions_to_visit_value = []
        prev_pos = self.current_pos_value

        direction = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1))
        direction = direction.normalize()

        for _ in range(self.speed):
            new_pos = prev_pos + (direction * self.steps)
            
            if self._is_within_range(new_pos):
                self.positions_to_visit_value.append((new_pos))
                prev_pos = new_pos
                self.target_pos_value = prev_pos
            else:
                return len(self.positions_to_visit_value)

        return len(self.positions_to_visit_value)

    def _is_within_range(self, new_pos: tuple, ):
        array = self.isometric_conversions.get_array()
        new_pos_x_index, new_pos_y_index = self.isometric_conversions.iso_to_grid(new_pos[0], new_pos[1])

        return not (new_pos_x_index < 0 or new_pos_x_index >= len(array) or new_pos_y_index < 0 or new_pos_y_index >= len(array[0]))



class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    RED = (219, 7, 61)
    ORANGE = (219, 165, 7)
    LIGHT_BLUE = (142, 199, 210)
    MEDIUM_BLUE = (12, 105, 134)
    DARK_BLUE = (7, 72, 91)

class AnimationMode(Enum):
    IDLE_01 = 1
    IDLE_02 = 2
    ATTACK_02 = 12
    WALK_FORWARD = 21
    WALK_BACK = 22
    STRAFE_LEFT = 25
    STRAFE_RIGHT = 26

class GameState(Enum):
    INITIALIZING = 0
    INITIALIZED = 1
    MAIN_MENU = 2
    GAME = 3
    QUITTING = 10