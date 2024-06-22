import pygame

from gui import CordBox
from map import Point, Tile
from settings import *
from spiders import Units
from utils import Color, GameState
from world import World


class Game():

    def __init__(self):
        self.state = GameState.INITIALIZING

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_TITLE_WINDOW)
        self.clock = pygame.time.Clock()
        self.map = World()
        self.units = Units()
        self.units.spawn_spider()
        self.prev_clicked_tile = None
        self.prev_left_click_pos = None
        self.font = pygame.font.Font(None, 36)
        self.cord_box = CordBox(self.font)

        self.state = GameState.INITIALIZED

    def setup(self):
        pass

    def run(self):
        self.setup()
        self.state = GameState.MAIN_MENU

        while self.state != GameState.QUITTING:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = GameState.QUITTING

            if event.type == pygame.MOUSEBUTTONDOWN: 
                x,y = event.pos
                self.prev_left_click_pos = ((x,y))

                self.units.spawn_spider(pos=((x,y)))

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
        if self.prev_left_click_pos:
            self.cord_box.update(self.prev_left_click_pos)
        self.units.update()

    def draw(self):
        self.screen.fill(Color.DARK_BLUE)
        self.map.draw(self.screen)
        if self.prev_left_click_pos:
            self.cord_box.draw(self.screen)
        self.units.draw(self.screen)
        pygame.display.flip()

