import time
import pygame

from gui import CordBox, MainMenu
from map import Point, Tile
from settings import *
from spiders import Units
from game_screen_manager import GameScreenSizeManager
from utils import Color, GameState, IsometricConversions
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

    def run(self):
        self.state = GameState.MAIN_MENU
        #TODO:: start game

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

                self.units.spawn_spider(pos=((self.isometric_conversions.get_random_coord_value())))

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
        print('TOGGLE FULLSCREEN')

    def exit_game(self):
        self.state = GameState.QUITTING
        print('QUITTING')
