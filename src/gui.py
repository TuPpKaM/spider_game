
import pygame


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

    