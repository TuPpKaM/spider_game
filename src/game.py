import time

import pygame

from game_screen_manager import GameScreenSizeManager
from gui import CordBox, MainMenu
from map import Point, Tile
from registry import Registry
from settings import *
from spiders import Units
from utils import AnimationManager, Color, GameState, IsometricConversions
from world import World


class Game():

    def __init__(self):
        self.state = GameState.INITIALIZING

        self.screen_size_manager = GameScreenSizeManager()
        screen_w, screen_h = self.screen_size_manager.get_screen_size()
        self.screen = pygame.display.set_mode((screen_w, screen_h))
        pygame.display.set_caption(GAME_TITLE_WINDOW)
        self.clock = pygame.time.Clock()
        
        self.isometric_conversions = IsometricConversions(self.screen_size_manager)
        self.world = World(self.isometric_conversions)
        self.units = Units(self.isometric_conversions)

        self.prev_clicked_tile = None
        self.prev_left_click_pos = None
        self.font = pygame.font.Font(None, 36)
        self.cord_box = CordBox(self.font)
        self.main_menu = MainMenu(self.start_game, self.close_menu, self.change_volume,
                                  self.toggle_fullscreen, self.exit_game)

        self.state = GameState.INITIALIZED

    def load_saved_instances(self):
        self.state = GameState.LOADING

        Registry._registry = []
        self.animation_manager = AnimationManager(cache_size=100)
        self.spiders = pygame.sprite.LayeredUpdates()
        self.eggs = pygame.sprite.LayeredUpdates()
        Registry.load_from_file('instances.json', self.isometric_conversions, self.animation_manager, self.spiders, self.eggs)
        self.units.spiders = self.spiders #TODO:: load more than spiders
        self.units.eggs = self.eggs #TODO:: init Units using funcetions instead of directly

        self.state = GameState.LOADED

    def run(self):
        self.load_saved_instances()

        #TODO:: start game correctly
        self.state = GameState.MAIN_MENU

        self.state = GameState.GAME
        while self.state != GameState.QUITTING:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = GameState.QUITTING

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.state = GameState.MAIN_MENU

                if self.state == GameState.MAIN_MENU:
                    if event.key == pygame.K_UP:
                        self.main_menu.move_up()
                    elif event.key == pygame.K_DOWN:
                        self.main_menu.move_down()
                    elif event.key == pygame.K_RETURN:
                        self.main_menu.select()


            if event.type == pygame.MOUSEBUTTONDOWN: 
                x,y = event.pos
                self.prev_left_click_pos = ((x,y))

                
                self.units.spawn_spider(pos=((self.isometric_conversions.get_random_coord_value())), spider_type = 1)

                #self.units.spawn_spider(pos=((self.isometric_conversions.get_grid_start())))
                #self.units.spawn_spider(pos=((self.isometric_conversions.grid_to_iso(12,0))))

                collisions = pygame.sprite.spritecollide(Point(x,y), self.world.get_grid_sprites(), False, pygame.sprite.collide_mask) #TODO grid_sprites
                if collisions:
                    for sprite in collisions:
                        if isinstance(sprite, Tile):
                            print(sprite.name)
                            if self.prev_clicked_tile is not None:
                                self.prev_clicked_tile.change_image(pygame.image.load("assets\\tiles\\floor_32_32.png").convert_alpha())

                            sprite.change_image(pygame.image.load("assets\\tiles\\floor_32_32_red.png").convert_alpha())
                            self.prev_clicked_tile = sprite

    def update(self):
        if self.state == GameState.MAIN_MENU:
            pass

        if self.state == GameState.GAME:
            if self.prev_left_click_pos:
                self.cord_box.update(self.prev_left_click_pos)
            self.units.update()

    def draw(self):
        self.screen.fill(Color.DARK_BLUE)

        if self.state == GameState.MAIN_MENU:
            self.main_menu.draw(self.screen)
        
        if self.state == GameState.GAME:
            self.world.draw(self.screen)
            if self.prev_left_click_pos:
                self.cord_box.draw(self.screen)
            self.units.draw(self.screen)

        #DEBUG
        pygame.draw.circle(self.screen, Color.LIGHT_BLUE, self.isometric_conversions.grid_to_iso(0,0), 3)
        pygame.draw.circle(self.screen, Color.RED, self.isometric_conversions.grid_to_iso(11,0), 3)
        pygame.draw.circle(self.screen, Color.BLACK, self.isometric_conversions.grid_to_iso(11,17), 3)
        pygame.draw.circle(self.screen, Color.ORANGE, self.isometric_conversions.grid_to_iso(0,17), 3)
        #DEBUG
        pygame.draw.circle(self.screen, Color.WHITE, self.world.tile_grid.get_array()[0][0], 1)
        pygame.draw.circle(self.screen, Color.WHITE, self.world.tile_grid.get_array()[11][0], 1)
        pygame.draw.circle(self.screen, Color.WHITE, self.world.tile_grid.get_array()[11][17], 1)
        pygame.draw.circle(self.screen, Color.WHITE, self.world.tile_grid.get_array()[0][17], 1)
        #DEBUG

        pygame.display.flip()

    #Main menu callbacks
    def start_game(self):
        self.state = GameState.GAME
        print('GAME STARTING')

    def close_menu(self):
        self.state = GameState.GAME
        print('CLOSE MENU')

    def change_volume(self, volume: float = 0.0):
        print(f'NEW VOLUME {volume}') #TODO

    def toggle_fullscreen(self):
        Registry.save_to_file('instances.json') #TODO:: move to correct
        print('TOGGLE FULLSCREEN')

    def exit_game(self):
        self.state = GameState.QUITTING
        print('QUITTING')
