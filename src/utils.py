import os
import random
from enum import Enum

import pygame

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
    def __init__(self, cache_size: int = 10):
        self.loader = SpriteLoader()
        self.cache = {}
        self.max_cache_size = cache_size

    def load_animation(self, file_path: str, cols: int, rows: int, scale: float):
        file = os.path.basename(file_path)
        if file in self.cache:
            print(f"Loaded from cache: {file_path}")
            return self.cache[file]
        else:
            print(f"Loading: {file_path}")
            animation_images = self.loader.split_sprite(file_path, cols, rows, scale)
            self.cache[file] = animation_images
            self._check_cache_size()
            return animation_images

    def unload_animation(self, file_path: str):
        if file_path in self.cache:
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

    @staticmethod
    def get_center_of_screen() -> int:
        return WIDTH//2 , (HEIGHT//2)

    @staticmethod
    def get_grid_start() -> int:
        center_w, center_h = IsometricConversions.get_center_of_screen()
        center_h += 50 # 50?

        start_w = center_w - ((TILE_W * (TILE_COUNT_W + TILE_COUNT_H))/4)
        start_h = center_h + ((TILE_H * (TILE_COUNT_W))/4) - (TILE_H/2)

        if ( TILE_COUNT_H >  TILE_COUNT_W):
            start_h = center_h - ((TILE_H * (TILE_COUNT_H))/4) + (TILE_H/2)
        return start_w, start_h

    @staticmethod
    def grid_to_iso(x, y, origin_iso_x, origin_iso_y) -> int:
        iso_x = origin_iso_x + ((x+y)*(TILE_W//2)) # TODO:: x-y
        iso_y = origin_iso_y + ((x-y)*(TILE_H//2)) # TODO:: x+y
        return iso_x, iso_y
    
    @staticmethod
    def iso_to_grid(iso_x, iso_y, origin_iso_x, origin_iso_y) -> int:
        x = ((iso_x - origin_iso_x) / (TILE_W / 2) + (iso_y - origin_iso_y) / (TILE_H / 2)) / 2
        y = abs(((iso_y - origin_iso_y) / (TILE_H / 2) - (iso_x - origin_iso_x) / (TILE_W / 2)) / 2) # TODO:: not abs
        return int(x), int(y)
    
    @staticmethod
    def get_random_coordinate_value(array_2d: list) -> int:
        row_index = random.randint(0, len(array_2d) - 1)
        col_index = random.randint(0, len(array_2d[row_index]) - 1)
        return array_2d[row_index][col_index]
    
    @staticmethod
    def get_random_coordinate_index(array_2d: list) -> int:
        row_index = random.randint(0, len(array_2d) - 1)
        col_index = random.randint(0, len(array_2d[row_index]) - 1)
        return row_index, col_index


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

class GameState(Enum):
    INITIALIZING = 0
    INITIALIZED = 1
    MAIN_MENU = 2
    GAME = 3
    QUITTING = 10