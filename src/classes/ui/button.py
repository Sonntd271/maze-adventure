import pygame
from classes.state_manager import state_manager

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
    
    def draw(self):
        pygame.draw.rect(state_manager.screen, (200, 200, 200), self.rect)
        label = state_manager.font.render(self.text, True, (0, 0, 0))
        state_manager.screen.blit(label, (self.rect.x + 20, self.rect.y + 10))
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
