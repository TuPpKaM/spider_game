import pygame

from map import Floor, Tile_grid, WallLeft, WallRight
from settings import *
from utils import split_sprite


class World:

    def __init__(self):
        self.layers = []
        
        world_sprites = pygame.sprite.LayeredUpdates()

        world_grid = Tile_grid(center_w=HALF_WIDTH, center_h=HALF_HEIGHT ,block_h=TILE_H, block_w=TILE_W, array_w=TILE_COUNT_W, array_h=TILE_COUNT_H)
        self.world_start_pos_top_x = world_grid.get_start_pos_top()[0]
        self.world_start_pos_top_y = world_grid.get_start_pos_top()[1]

        self.grid_sprites = world_grid.get_grid_group()

        world_sprites.add(self.grid_sprites)

        world_sprites.add(self.generate_walls())
        world_sprites.add(self.generate_floors())

        self.layers.append(world_sprites)

    def get_grid_sprites(self) -> pygame.sprite.LayeredUpdates:
        return self.grid_sprites

    def generate_walls(self) -> pygame.sprite.LayeredUpdates:
        wall_sprites = split_sprite('assets\\tiles\\WallBrick_Tall_01.png', 4, 1, scale=0.5)
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
        floor_sprites = split_sprite('assets\\tiles\\Floor_Corner_01.png', 4, 1, scale=0.5)
        floor_group = pygame.sprite.LayeredUpdates()

        floor = Floor(floor_sprites[0],self.world_start_pos_top_x, self.world_start_pos_top_y,0,0,0)
        floor_group.add(floor)
        floor_group.move_to_back(floor)

        return floor_group
    

    def update(self):
        pass
        #for _ in self.layers:
        #    _.update()

    def draw(self, screen):
        for _ in self.layers:
            _.draw(screen)