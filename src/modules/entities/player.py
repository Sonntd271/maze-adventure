import pygame
from modules.core.character import Character
from modules.core.bullet import Bullet
from modules.core.upgrade import Upgrade

class Player(Character):
    def __init__(self, x, y, speed, healthbar, size=32):
        super().__init__(x, y, speed, healthbar)
        self.__bullets = []
        self.__max_bullets = 1
        self.__shoot_cooldown = 300 # milliseconds
        self.__last_shot_time = 0
        self.__bullet_damage = 10
        self.size = size
        self.images = {
            'up': pygame.image.load('assets/images/sprites/character_up.png').convert_alpha(),
            'down': pygame.image.load('assets/images/sprites/character_down.png').convert_alpha(),
            'left': pygame.image.load('assets/images/sprites/character_left.png').convert_alpha(),
            'right': pygame.image.load('assets/images/sprites/character_right.png').convert_alpha()
        }
        self.__scale_sprites()
        self.current_image = self.images['down']
        self.last_direction = 'down'

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

    def __scale_sprites(self):
        for sprite in self.images.keys():
            self.images[sprite] = pygame.transform.scale(self.images[sprite], (self.size, self.size))

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
        elif upgrade.target_attr == "damage":
            self.__bullet_damage += upgrade.value
        elif upgrade.target_attr == "health":
            self.health.max_health = self.health.max_health + upgrade.value
            self.health.current_health = self.health.max_health
        elif upgrade.target_attr == "max_bullets":
            self.max_bullets += upgrade.value
        upgrade.increment()

    def update_direction(self, dx, dy):
        if dx > 0:
            self.last_direction = 'right'
        elif dx < 0:
            self.last_direction = 'left'
        elif dy > 0:
            self.last_direction = 'down'
        elif dy < 0:
            self.last_direction = 'up'

        self.current_image = self.images[self.last_direction]

    def draw(self, surface, camera):
        # Character
        x = self.position[0] - camera.offset_x
        y = self.position[1] - camera.offset_y
        surface.blit(self.current_image, (x, y))

        # Healthbar
        self.health.draw(
            surface,
            self.position[0] - camera.offset_x,
            self.position[1] - camera.offset_y - 10
        )

        # Bullets
        for bullet in self.bullets:
            bullet.draw(surface, camera)
