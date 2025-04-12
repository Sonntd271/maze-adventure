import pygame
from modules.core.character import Character
from modules.core.bullet import Bullet
from modules.core.upgrade import Upgrade

class Player(Character):
    def __init__(self, x, y, speed, healthbar):
        super().__init__(x, y, speed, healthbar)
        self.__bullets = []
        self.__max_bullets = 1
        self.__shoot_cooldown = 300  # milliseconds
        self.__last_shot_time = 0
        self.__bullet_damage = 10

    @property
    def bullets(self):
        return self.__bullets

    @property
    def bullet_damage(self):
        return self.__bullet_damage

    @property
    def max_bullets(self):
        return self.__max_bullets

    @max_bullets.setter
    def max_bullets(self, value):
        self.__max_bullets = value

    def shoot(self, direction_vector):
        now = pygame.time.get_ticks()
        if (
            len(self.__bullets) < self.__max_bullets and
            now - self.__last_shot_time >= self.__shoot_cooldown
        ):
            x, y = self.position
            center_x = x + self.size // 2
            center_y = y + self.size // 2
            bullet = Bullet(center_x, center_y, *direction_vector)
            self.__bullets.append(bullet)
            self.__last_shot_time = now

    def update_bullets(self, game_map, level, tile_size):
        for bullet in self.__bullets:
            bullet.update(game_map, level, tile_size)
        self.__bullets = [b for b in self.__bullets if b.active]

    def apply_upgrade(self, upgrade: Upgrade):
        print(f"Applied: {upgrade.name}")
        if upgrade.target_attr == "speed":
            self.speed += upgrade.value
            print(f"Speed upgraded by {upgrade.value}")
        elif upgrade.target_attr == "damage":
            self.__bullet_damage += upgrade.value
            print(f"Bullet damage upgraded by {upgrade.value}")
        elif upgrade.target_attr == "health":
            self.health.max_health = self.health.max_health + upgrade.value
            self.health.current_health = self.health.max_health
            print(f"Health upgraded by {upgrade.value}")

    def draw(self, surface, camera):
        super().draw(surface)
        self.health.draw(surface, self.position[0] - camera.offset_x, self.position[1] - camera.offset_y - 10)
        for bullet in self.__bullets:
            bullet.draw(surface, camera)
