import pygame

from gui import CordBox
from map import Point, Tile
from settings import *
from utils import Color
from world import World


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_TITLE_WINDOW)
        self.clock = pygame.time.Clock()
        self.running = True
        self.prev_clicked_tile = None
        self.map = World()
        self.font = pygame.font.Font(None, 36)
        self.last_left_click_pos = None
        self.cord_box = CordBox(self.font)

    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN: 
                x,y = event.pos
                self.last_left_click_pos = ((x,y))

                collisions = pygame.sprite.spritecollide(Point(x,y), self.map.get_grid_sprites(), False, pygame.sprite.collide_mask) #TODO grid_sprites
                if collisions:
                    for sprite in collisions:
                        if isinstance(sprite, Tile):
                            print(sprite.name)
                            if self.prev_clicked_tile is not None:
                                self.prev_clicked_tile.change_image(pygame.image.load("assets\\tiles\\floor_32_32.png").convert_alpha())

                            sprite.change_image(pygame.image.load("assets\\tiles\\floor_32_32_red.png").convert_alpha())
                            self.prev_clicked_tile = sprite

    def update(self):
        if self.last_left_click_pos:
            self.cord_box.update(self.last_left_click_pos)

    def draw(self):
        self.screen.fill(Color.DARK_BLUE)
        self.map.draw(self.screen)
        if self.last_left_click_pos:
            self.cord_box.draw(self.screen)
        pygame.display.flip()
