import pygame
import classes.common.constants as c
from classes.common.utilities import is_walkable
from classes.game.healthbar import Healthbar
from classes.game.bullet import Bullet
from classes.resource_manager import resource_manager


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
            'up': resource_manager.player_up,
            'down': resource_manager.player_down,
            'left': resource_manager.player_left,
            'right': resource_manager.player_right
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
    
    def shoot(self):
        """Shoots a green laser in the last moved direction."""
        laser = Bullet(self.x + c.dimensions["tile_size"] // 2, self.y + c.dimensions["tile_size"] // 2, self.last_direction)
        self.projectiles.append(laser)

    def take_damage(self, amount, current_time):
        """Player takes damage from enemies"""
        # Only take damage once per second
        if current_time - self.last_damage_time >= 1000:  # 1000 ms = 1 second
            self.healthbar.update(self.healthbar.current_health - amount)
            self.last_damage_time = current_time
    
    def is_alive(self):
        """Check if player is still alive"""
        return self.healthbar.current_health > 0

    def draw(self, camera):
        # Draw current direction image instead of a static image
        resource_manager.screen.blit(self.current_image, camera.apply(self))
        
        # Draw health bar
        self.healthbar.draw(self.x, self.y, camera)
        
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(camera)