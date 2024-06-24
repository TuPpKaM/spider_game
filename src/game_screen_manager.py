
from settings import *


class GameScreenSizeManager:

    def __init__(self):
        self.screen_width, self.screen_height = START_WIDTH, START_HEIGHT

    def get_screen_size(self) -> int:
        return self.screen_width, self.screen_height
    
    def set_screen_size(self, width: int, height: int): #TODO::force redraw and resize
        self.screen_width, self.screen_height = width, height