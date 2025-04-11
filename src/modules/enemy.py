import pygame
from modules.character import Character

class Enemy(Character):
    def __init__(self, x, y, speed, healthbar):
        Character.__init__(self, x, y, speed, healthbar)
        self.__color = (200, 0, 0)
        self.alive = True

    def update(self, player, game_map, level, tile_size):
        if not self.alive:
            return

        px, py = player.position
        ex, ey = self.position

        # Check line of sight (same row or col with clear path)
        if abs(px - ex) < tile_size:  # same column
            step = tile_size if py > ey else -tile_size
            for y in range(int(ey), int(py), step):
                if not game_map.is_walkable(level, ex // tile_size, y // tile_size):
                    return
            self.__move_towards(0, step // abs(step))
        elif abs(py - ey) < tile_size:  # same row
            step = tile_size if px > ex else -tile_size
            for x in range(int(ex), int(px), step):
                if not game_map.is_walkable(level, x // tile_size, ey // tile_size):
                    return
            self.__move_towards(step // abs(step), 0)

    def __move_towards(self, dx, dy):
        self.position[0] += dx * self.speed
        self.position[1] += dy * self.speed

    def take_damage(self, damage):
        if self.is_alive():
            self.health.update_health(-damage)
            if not self.is_alive():
                self.alive = False

    def check_collision_with_player(self, player):
        if not self.alive:
            return
        rect_self = pygame.Rect(*self.position, self.size, self.size)
        rect_player = pygame.Rect(*player.position, player.size, player.size)
        if rect_self.colliderect(rect_player):
            player.take_damage(25)  # Damage value
            self.health.update_health(-9999)
            self.alive = False

    def draw(self, surface, camera):
        if self.alive:
            pygame.draw.rect(surface, self.__color, (
                self.position[0] - camera.offset_x,
                self.position[1] - camera.offset_y,
                self.size,
                self.size
            ))