import pygame


class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (219, 7, 61)
    ORANGE = (219, 165, 7)
    LIGHT_BLUE = (142, 199, 210)
    MEDIUM_BLUE = (12, 105, 134)
    DARK_BLUE = (7, 72, 91)

def split_sprite(path, cols, rows = 1, scale = 1) -> list:
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
                sprites.append(scale_sprite(sprite, scale))
            else:
                sprites.append(sprite)

    return sprites

def scale_sprite(original_sprite: pygame.Surface, scale_factor) -> pygame.Surface:
    original_width, original_height = original_sprite.get_size()

    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)

    return pygame.transform.scale(original_sprite, (new_width, new_height))