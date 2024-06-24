import pygame

from utils import IsometricConversions as Iso

class Tile_grid():

    def __init__(self, block_w, block_h, array_w, array_h) -> None:
        self.center_w ,self.center_h = Iso.get_center_of_screen()
        self.start_w , self.start_h = Iso.get_grid_start()
        
        self.shape_w_amount = array_w
        self.shape_h_amount = array_h
        self.block_w = block_w
        self.block_h = block_h

        self.array = self.generate_array()
    
    def generate_array(self) -> None:
        array = []
        for i in range (self.shape_h_amount):
            for j in range (self.shape_w_amount):
                if j == 0:
                    array.append([])
                w = self.start_w + (j * (self.block_w/2)) + (i * (self.block_w/2))
                h = self.start_h - (j * (self.block_h/2)) + (i * (self.block_h/2))
                array[i].append((w,h))
        return array
    
    def get_start_pos_left(self) -> tuple:
        return (self.start_w, self.start_h)
    
    def get_start_pos_top(self) -> tuple:
        return self.array[0][self.shape_w_amount-1]

    def get_array(self) -> list:
        return self.array
    
    def get_grid_group(self) -> pygame.sprite.LayeredUpdates:
        black = pygame.image.load("assets\\tiles\\floor_32_32.png").convert_alpha()
        front_edge = pygame.image.load("assets\\tiles\\floor_32_32_red.png").convert_alpha()

        floor_sprites = pygame.sprite.LayeredUpdates()

        for i, row in enumerate(self.array):
            for j, point in enumerate(row):
                if (j == 0 or i == len(self.array)-1):
                    sprite_image = front_edge
                else:
                    sprite_image = black
                
                tile = Tile(sprite_image, *point)
                floor_sprites.add(tile)

        return floor_sprites

class Tile(pygame.sprite.Sprite):

    def __init__(self, image, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (width, height)
        self.mask = pygame.mask.from_surface(self.image)

        self.name = f'x{width}y{height}'

    def change_image(self, image):
        self.image = image
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

class Point(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, x + 1, y + 1)

        self.image = pygame.Surface([1, 1])
        self.image.fill((219, 165, 7))

class WallRight(pygame.sprite.Sprite):
    
    def __init__(self, image, x , y, tile_w, tile_h, wall_index):
        pygame.sprite.Sprite.__init__(self)

        offset = (-2 + (wall_index * (3*tile_w)), 44 + (wall_index * (3*tile_h)))

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x+offset[0],y+offset[1])

class WallLeft(pygame.sprite.Sprite):
    
    def __init__(self, image, x , y, tile_w, tile_h, wall_index):
        pygame.sprite.Sprite.__init__(self)

        offset = (2 - (wall_index * (3*tile_w)), 44 + (wall_index * (3*tile_h)))

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.bottomright = (x+offset[0],y+offset[1])

class Floor(pygame.sprite.Sprite):
    
    def __init__(self, image, x , y, tile_w, tile_h, wall_index):
        pygame.sprite.Sprite.__init__(self)

        offset = ((32*3)+8,16*7)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.bottomright = (x+offset[0],y+offset[1])
    