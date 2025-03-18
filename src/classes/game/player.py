import pygame
import classes.common.constants as c
from classes.ui.healthbar import Healthbar
from classes.state_manager import state_manager


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.projectiles = []  # List to store lasers
        self.last_direction = 'right'  # Default direction (starting with right)
        self.healthbar = Healthbar(500)  # Player has 500 HP
        self.last_damage_time = 0  # To track when damage was last taken
        
        # Dictionary to store player images for each direction
        self.images = {
            'up': PLAYER_UP,
            'down': PLAYER_DOWN,
            'left': PLAYER_LEFT,
            'right': PLAYER_RIGHT
        }
        
        # Current image based on last direction (start with right)
        self.current_image = self.images['right']

    def move(self, keys, maze_image):
        dx, dy = 0, 0
        direction_changed = False
        
        if keys[pygame.K_LEFT]: 
            dx = -self.speed
            self.last_direction = 'left'
            direction_changed = True
        if keys[pygame.K_RIGHT]: 
            dx = self.speed
            self.last_direction = 'right'
            direction_changed = True
        if keys[pygame.K_UP]: 
            dy = -self.speed
            self.last_direction = 'up'
            direction_changed = True
        if keys[pygame.K_DOWN]: 
            dy = self.speed
            self.last_direction = 'down'
            direction_changed = True

        # Update player image if direction changed
        if direction_changed:
            self.current_image = self.images[self.last_direction]

        new_x, new_y = self.x + dx, self.y + dy

        # Check if the new position is on a transparent pixel
        if is_walkable(new_x, new_y, maze_image):
            self.x, self.y = new_x, new_y
