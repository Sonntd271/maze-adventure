import pygame

class Bullet:
    def __init__(self, x, y, dx, dy, speed=10, size=6):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.size = size
        self.active = True

    def update(self, game_map, level, tile_size):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        tile_x = int(self.x // tile_size)
        tile_y = int(self.y // tile_size)

        if not game_map.is_walkable(level, tile_x, tile_y):
            self.active = False

    def draw(self, surface, camera):
        if not self.active:
            return

        draw_x = self.x - camera.offset_x
        draw_y = self.y - camera.offset_y

        width = 20 if self.dx != 0 else 4
        height = 4 if self.dx != 0 else 20

        rect = pygame.Rect(draw_x, draw_y, width, height)
        pygame.draw.rect(surface, (255, 0, 0), rect)