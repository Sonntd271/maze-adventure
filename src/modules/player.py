import pygame
from modules.character import Character
from modules.bullet import Bullet

class Player(Character):
    def __init__(self, x, y, speed, healthbar):
        Character.__init__(self, x, y, speed, healthbar)
        self.bullets = []
        self.max_bullets = 1
        self.shoot_cooldown = 300  # milliseconds
        self.last_shot_time = 0

    def shoot(self, direction_vector):
        now = pygame.time.get_ticks()
        if (
            len(self.bullets) < self.max_bullets and
            now - self.last_shot_time >= self.shoot_cooldown
        ):
            x, y = self.position
            center_x = x + self.size // 2
            center_y = y + self.size // 2
            bullet = Bullet(center_x, center_y, *direction_vector)
            self.bullets.append(bullet)
            self.last_shot_time = now

    def update_bullets(self, game_map, level, tile_size):
        for bullet in self.bullets:
            bullet.update(game_map, level, tile_size)
        self.bullets = [b for b in self.bullets if b.active]

    def draw(self, surface, camera):
        super().draw(surface)  # draw self
        self.health.draw(surface, self.position[0] - camera.offset_x, self.position[1] - camera.offset_y - 10)
        for bullet in self.bullets:
            bullet.draw(surface, camera)