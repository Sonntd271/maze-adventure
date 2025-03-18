import pygame
import classes.common.constants as c
from classes.state_manager import state_manager

class Bullet:
    def __init__(self, x, y, direction, speed=10):
        self.x = x
        self.y = y
        self.direction = direction  # ('up', 'down', 'left', 'right')
        self.speed = speed
        self.color = c.colors["green"]
        self.width = 3
        self.height = 10
        self.damage = 50  # Damage per hit

    def move(self):
        if self.direction == 'up':
            self.y -= self.speed
        elif self.direction == 'down':
            self.y += self.speed
        elif self.direction == 'left':
            self.x -= self.speed
        elif self.direction == 'right':
            self.x += self.speed

    def draw(self, camera):
        screen_x, screen_y = camera.apply(self)
        if self.direction in ['up', 'down']:
            pygame.draw.line(state_manager.screen, self.color, (screen_x, screen_y), (screen_x, screen_y - self.height), self.width)
        else:  # Left or Right
            pygame.draw.line(state_manager.screen, self.color, (screen_x, screen_y), (screen_x + self.height, screen_y), self.width)

    def is_out_of_bounds(self):
        return self.x < 0 or self.x > c.dimensions["map_width"]  or self.y < 0 or self.y > c.dimensions["map_height"]

    def hit_wall(self, maze_image):
        return not is_walkable(self.x, self.y, maze_image)
    
    def hit_enemy(self, enemy):
        return (self.x >= enemy.x and self.x <= enemy.x + c.dimensions["tile_size"] and
                self.y >= enemy.y and self.y <= enemy.y + c.dimensions["tile_size"])

