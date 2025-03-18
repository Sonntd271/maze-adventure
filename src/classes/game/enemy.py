import pygame
import classes.common.constants as c
from classes.ui.healthbar import Healthbar
from classes.state_manager import state_manager


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
        self.healthbar = Healthbar(100)  # Enemy has 100 HP
        self.damage_amount = 20  # Damage to player per second
        self.last_sprite_change = pygame.time.get_ticks()
        self.sprite_index = 0

        # Store bomb images for different directions
        self.images = {
            'up': BOMB_UP,
            'down': BOMB_DOWN,
            'left': BOMB_LEFT,
            'right': BOMB_RIGHT
        }

        self.current_image = self.images['up']  # Default starting appearance
    
    def can_see_player(self, player, maze_image):
        """Check if there's a clear line of sight to the player (raycasting)."""
        steps = 50  
        x, y = self.x, self.y
        dx = player.x - x
        dy = player.y - y
        distance = max(abs(dx), abs(dy))
        step_x = dx / distance if distance != 0 else 0
        step_y = dy / distance if distance != 0 else 0

        for _ in range(0, distance, steps):
            x += step_x * steps
            y += step_y * steps
            if not is_walkable(int(x), int(y), maze_image):
                return False  

        return True  

    def move(self, player, maze_image):
        """Moves toward the player if visible; otherwise, stays in place and cycles sprite."""
        current_time = pygame.time.get_ticks()

        if self.can_see_player(player, maze_image):
            # Move towards player
            if self.x < player.x:
                new_x = self.x + self.speed
                self.current_image = self.images['right']
            elif self.x > player.x:
                new_x = self.x - self.speed
                self.current_image = self.images['left']
            else:
                new_x = self.x

            if self.y < player.y:
                new_y = self.y + self.speed
                self.current_image = self.images['down']
            elif self.y > player.y:
                new_y = self.y - self.speed
                self.current_image = self.images['up']
            else:
                new_y = self.y

            if is_walkable(new_x, new_y, maze_image):
                self.x = new_x
                self.y = new_y
        else:
            if current_time - self.last_sprite_change >= 2000:  
                sprite_order = ['up', 'right', 'down', 'left']
                self.sprite_index = (self.sprite_index + 1) % 4  
                self.current_image = self.images[sprite_order[self.sprite_index]]
                self.last_sprite_change = current_time  

    def take_damage(self, amount):
        """Enemy takes damage from projectiles"""
        self.healthbar.update(self.healthbar.current_health - amount)
    
    def is_alive(self):
        """Check if enemy is still alive"""
        return self.healthbar.current_health > 0
    
    def collides_with_player(self, player):
        """Check if enemy collides with player"""
        return (self.x < player.x + c.dimensions["tile_size"] and self.x + c.dimensions["tile_size"] > player.x and
                self.y < player.y + c.dimensions["tile_size"] and self.y + c.dimensions["tile_size"] > player.y)

    def draw(self, camera):
        state_manager.screen.blit(self.current_image, camera.apply(self))
        self.healthbar.draw(self.x, self.y, camera)
