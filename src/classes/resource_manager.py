import pygame
import classes.common.constants as c
from classes.common.utilities import load_images


class ResourceManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((c.dimensions["screen_width"], c.dimensions["screen_height"]))
        pygame.display.set_caption(c.caption)
        self.font = pygame.font.Font(c.font["family"], c.font["size"])
        
        self.current_state = c.states["lobby"]
        self.maze_img, self.bomb_up, self.bomb_down, self.bomb_left, self.bomb_right, self.player_up, self.player_down, self.player_left, self.player_right = load_images()

    def set_state(self, new_state):
        self.current_state = new_state

# Global instance
resource_manager = ResourceManager()
