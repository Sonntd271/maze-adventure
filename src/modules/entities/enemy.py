import pygame
from modules.core.character import Character

class Enemy(Character):
    def __init__(self, x, y, speed, healthbar):
        super().__init__(x, y, speed, healthbar)
        self.__color = (200, 0, 0)
        self.__alive = True

    @property
    def alive(self):
        return self.__alive

    def update(self, player, game_map, level, tile_size):
        if not self.__alive:
            return

        px, py = player.position
        ex, ey = self.position

        if not self._has_clear_path(ex, ey, px, py, game_map, level, tile_size):
            return

        dx = 1 if px > ex else -1 if px < ex else 0
        dy = 1 if py > ey else -1 if py < ey else 0

        if abs(px - ex) > abs(py - ey):
            self.__move_towards(dx, 0, game_map, level, tile_size)
        else:
            self.__move_towards(0, dy, game_map, level, tile_size)

    def _has_clear_path(self, ex, ey, px, py, game_map, level, tile_size):
        if int(ex // tile_size) == int(px // tile_size):
            x = int(ex // tile_size)
            y1, y2 = sorted([int(ey // tile_size), int(py // tile_size)])
            for y in range(y1 + 1, y2):
                if not game_map.is_walkable(level, x, y):
                    return False
            return True

        elif int(ey // tile_size) == int(py // tile_size):
            y = int(ey // tile_size)
            x1, x2 = sorted([int(ex // tile_size), int(px // tile_size)])
            for x in range(x1 + 1, x2):
                if not game_map.is_walkable(level, x, y):
                    return False
            return True

        return False

    def __move_towards(self, dx, dy, game_map, level, tile_size):
        next_x = self.position[0] + dx * self.speed
        next_y = self.position[1] + dy * self.speed

        if abs(next_x % tile_size) < 1:
            next_x = round(next_x / tile_size) * tile_size
        if abs(next_y % tile_size) < 1:
            next_y = round(next_y / tile_size) * tile_size

        # Check corners
        corners = [
            (next_x, next_y),
            (next_x + self.size - 1, next_y),
            (next_x, next_y + self.size - 1),
            (next_x + self.size - 1, next_y + self.size - 1),
        ]

        if all(game_map.is_walkable(level, int(cx // tile_size), int(cy // tile_size)) for cx, cy in corners):
            self.position = [next_x, next_y]

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
            player.take_damage(25)
            self.health.update_health(-9999)
            self.__alive = False

    def draw(self, surface, camera):
        if self.__alive:
            pygame.draw.rect(surface, self.__color, (
                self.position[0] - camera.offset_x,
                self.position[1] - camera.offset_y,
                self.size,
                self.size
            ))
