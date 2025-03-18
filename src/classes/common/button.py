import pygame
from classes.resource_manager import resource_manager

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
    
    def draw(self):
        pygame.draw.rect(resource_manager.screen, (200, 200, 200), self.rect)
        label = resource_manager.font.render(self.text, True, (0, 0, 0))
        resource_manager.screen.blit(label, (self.rect.x + 20, self.rect.y + 10))
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
