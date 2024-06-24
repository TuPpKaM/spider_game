
import pygame

from settings import *
from utils import Color


class CordBox:

    def __init__(self, font, pos=(10, 10)):
        self.font = font
        self.pos = pos
        self.text_surface = pygame.Surface((200, 50), pygame.SRCALPHA)
        self.text_surface.fill((0, 0, 0, 0))
        self.prev_cord_rect = pygame.Rect(pos, (200, 50))

        self.last_x = 0
        self.last_y = 0

    def update(self, click_pos: tuple):
        if(self.last_x != click_pos[0] or self.last_y != click_pos[1]):
            self.text_surface.fill((0, 0, 0, 0))
            
            text = self.font.render(f'X: {click_pos[0]}, Y: {click_pos[1]}', True, (255, 255, 255))
            self.text_surface.blit(text, (0, 0))
            
            self.prev_cord_rect = self.text_surface.get_rect(topleft=self.pos)

            self.last_x = click_pos[0]
            self.last_y = click_pos[1]

    def draw(self, screen):
        screen.fill((0, 0, 0), self.prev_cord_rect)
        screen.blit(self.text_surface, self.pos)


class MainMenu:
    
    def __init__(self, start_game, close_menu, change_volume, toggle_fullscreen, exit_game):
        self.font = pygame.font.Font(None, 40)
        self.start_game = start_game
        self.close_menu = close_menu
        self.change_volume = change_volume
        self.toggle_fullscreen = toggle_fullscreen
        self.exit_game = exit_game
        
        self.selected_option = 0
        self.game_started = False
        self.menu_options = SETTINGS_OPTIONS_START

    def move_up(self):
        self.selected_option = (self.selected_option - 1) % len(self.menu_options)

    def move_down(self):
        self.selected_option = (self.selected_option + 1) % len(self.menu_options)

    def select(self):
        match self.selected_option:
            case 0:
                if self.game_started:
                    self.close_menu()
                else:
                    self.menu_options = SETTINGS_OPTIONS_GAME
                    self.game_started = True
                    self.start_game()
            case 1:
                self.toggle_fullscreen()
            case 2:
                new_volume = 0.5
                self.change_volume(new_volume) #TODO
            case 3:
                self.exit_game()

    def draw(self, screen):
        pygame.draw.rect(screen, Color.GRAY, (MENU_X, MENU_Y, MENU_WIDTH, MENU_HEIGHT))

        for i, option in enumerate(self.menu_options):
            if i == self.selected_option:
                color = Color.BLACK
            else:
                color = Color.WHITE
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(MENU_X + MENU_WIDTH // 2, MENU_Y + 50 + i * 50))
            screen.blit(text, text_rect)