import pygame
import classes.common.constants as c

# Centralized resources are managed here
class StateManager:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        self.screen = pygame.display.set_mode((c.dimensions["screen_width"], c.dimensions["screen_height"]))
        pygame.display.set_caption(c.caption)
        self.font = pygame.font.Font(c.font["family"], c.font["size"])
        
        self.current_state = c.states["lobby"]


# Use this instance to perform setup
state_manager = StateManager()
