import pygame
import classes.common.constants as c
from classes.state_manager import state_manager


class Healthbar:
    def __init__(self, max_health, width=30, height=5):
        self.max_health = max_health
        self.current_health = max_health
        self.width = width
        self.height = height
    
    def update(self, health):
        self.current_health = max(0, min(health, self.max_health))
    
    def draw(self, x, y, camera):
        screen_x, screen_y = camera.apply(type("Entity", (object,), {"x": x, "y": y})()) 
        # Position the healthbar 15px above the character
        bar_x = screen_x + (c.dimensions["tile_size"] - self.width) // 2
        bar_y = screen_y - 15
        
        # Draw background (empty health)
        pygame.draw.rect(state_manager.screen, c.colors["black"], (bar_x - 1, bar_y - 1, self.width + 2, self.height + 2))
        pygame.draw.rect(state_manager.screen, c.colors["red"], (bar_x, bar_y, self.width, self.height))
        
        # Draw current health
        if self.current_health > 0:
            current_width = int((self.current_health / self.max_health) * self.width)
            pygame.draw.rect(state_manager.screen, c.colors["green"], (bar_x, bar_y, current_width, self.height))
