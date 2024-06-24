import pygame

from map import Floor, Tile_grid, WallLeft, WallRight
from settings import *
from utils import SpriteLoader


class World:

    def __init__(self):
        self.tile_grid = Tile_grid(block_h=TILE_H, block_w=TILE_W, array_w=TILE_COUNT_W, array_h=TILE_COUNT_H)
        self.loader = SpriteLoader()
        
        self.world_start_pos_top_x , self.world_start_pos_top_y = self.tile_grid.get_start_pos_top()
        self.grid_sprites = self.tile_grid.get_grid_group()
        self.floor_sprites = self.generate_floors()
        self.wall_sprites = self.generate_walls()

    def get_grid_sprites(self) -> pygame.sprite.LayeredUpdates:
        return self.grid_sprites

    def generate_walls(self) -> pygame.sprite.LayeredUpdates:
        wall_sprites = self.loader.split_sprite('assets\\tiles\\WallBrick_Tall_01.png', 4, 1, scale=0.5)
        walls_group = pygame.sprite.LayeredUpdates()

        walls_left_count = int(TILE_COUNT_W/6)
        walls_right_count = int(TILE_COUNT_H/6)

        for i in range(walls_left_count-1, -1, -1):
            wall = WallLeft(wall_sprites[0], self.world_start_pos_top_x, self.world_start_pos_top_y, TILE_W, TILE_H, i)
            walls_group.add(wall)
            walls_group.move_to_back(wall)

        for i in range(walls_right_count-1, -1, -1):
            wall = WallRight(wall_sprites[1], self.world_start_pos_top_x, self.world_start_pos_top_y, TILE_W, TILE_H, i)
            walls_group.add(wall)
            walls_group.move_to_back(wall)
        
        return walls_group

    def generate_floors(self) -> pygame.sprite.LayeredUpdates:
        floor_sprites = self.loader.split_sprite('assets\\tiles\\Floor_Corner_01.png', 4, 1, scale=0.5)
        floor_group = pygame.sprite.LayeredUpdates()

        floor = Floor(floor_sprites[0],self.world_start_pos_top_x, self.world_start_pos_top_y,0,0,0)
        floor_group.add(floor)
        floor_group.move_to_back(floor)

        return floor_group
    

    def update(self):
        pass

    def draw(self, screen):
        self.floor_sprites.draw(screen)
        self.wall_sprites.draw(screen)
        self.grid_sprites.draw(screen)