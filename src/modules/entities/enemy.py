import pygame
from modules.core.character import Character
from modules.core.healthbar import Healthbar

class Enemy(Character):
    def __init__(self, x, y, speed, healthbar: Healthbar, size=32):
        super().__init__(x, y, speed, healthbar)
        self.__alive = True
        self.sprite_index = 0
        self.last_sprite_change = 0
        self.size = size
        self.__damage = 50
        self.images = {
            'up': pygame.image.load('assets/images/sprites/bomb_up.png').convert_alpha(),
            'down': pygame.image.load('assets/images/sprites/bomb_down.png').convert_alpha(),
            'left': pygame.image.load('assets/images/sprites/bomb_left.png').convert_alpha(),
            'right': pygame.image.load('assets/images/sprites/bomb_right.png').convert_alpha()
        }
        self.__scale_sprites()
        self.current_image = self.images['down']

    @property
    def alive(self):
        return self.__alive
    
    def __scale_sprites(self):
        for sprite in self.images.keys():
            self.images[sprite] = pygame.transform.scale(self.images[sprite], (self.size, self.size))

    def update(self, player, game_map, level, tile_size):
        if not self.__alive:
            return
        self.__move_toward_player(player, game_map, level, tile_size)

    def __can_see_player(self, player, game_map, level, tile_size):
        steps = 4
        x, y = self.position
        px, py = player.position
        dx = px - x
        dy = py - y
        dist = max(abs(dx), abs(dy))
        if dist == 0:
            return True
        step_x = dx / dist
        step_y = dy / dist

        for _ in range(0, int(dist), steps):
            x += step_x * steps
            y += step_y * steps
            tile_x = int(x // tile_size)
            tile_y = int(y // tile_size)
            if not game_map.is_walkable(level, tile_x, tile_y):
                return False
        return True

    def __move_toward_player(self, player, game_map, level, tile_size):
        now = pygame.time.get_ticks()
        x, y = self.position
        px, py = player.position

        if self.__can_see_player(player, game_map, level, tile_size):
            dx = 1 if px > x else -1 if px < x else 0
            dy = 1 if py > y else -1 if py < y else 0

            if abs(dx) > abs(dy):
                self.current_image = self.images['right'] if dx > 0 else self.images['left']
            elif abs(dy) > 0:
                self.current_image = self.images['down'] if dy > 0 else self.images['up']

            next_x = x + dx * self.speed
            next_y = y + dy * self.speed

            if game_map.is_walkable(level, int(next_x // tile_size), int(next_y // tile_size)):
                self.position = [next_x, next_y]
        else:
            if now - self.last_sprite_change > 2000:
                dirs = ['up', 'right', 'down', 'left']
                self.sprite_index = (self.sprite_index + 1) % 4
                self.current_image = self.images[dirs[self.sprite_index]]
                self.last_sprite_change = now

    def take_damage(self, damage):
        if self.is_alive():
            self.health.update_health(-damage)
            if not self.is_alive():
                self.__alive = False

    def check_collision_with_player(self, player):
        if not self.__alive:
            return
        rect_self = pygame.Rect(*self.position, self.size, self.size)
        rect_player = pygame.Rect(*player.position, player.size, player.size)
        if rect_self.colliderect(rect_player):
            player.take_damage(self.__damage)
            self.health.update_health(-9999)
            self.__alive = False

    def draw(self, surface, camera):
        if self.__alive:
            x = self.position[0] - camera.offset_x
            y = self.position[1] - camera.offset_y
            surface.blit(self.current_image, (x, y))

            if self.health.current_health < self.health.max_health:
                self.health.draw(
                    surface,
                    x,
                    y - 10
                )
