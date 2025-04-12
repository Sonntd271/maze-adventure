import pygame

class Bullet:
    def __init__(self, x, y, dx, dy, speed=10):
        self.__x = x
        self.__y = y
        self.__dx = dx
        self.__dy = dy
        self.__speed = speed
        self.__active = True

    @property
    def position(self):
        return self.__x, self.__y

    @property
    def active(self):
        return self.__active

    def deactivate(self):
        self.__active = False

    def update(self, game_map, level, tile_size):
        self.__x += self.__dx * self.__speed
        self.__y += self.__dy * self.__speed

        tile_x = int(self.__x // tile_size)
        tile_y = int(self.__y // tile_size)

        if not game_map.is_walkable(level, tile_x, tile_y):
            self.__active = False

    def draw(self, surface, camera):
        if not self.__active:
            return

        draw_x = self.__x - camera.offset_x
        draw_y = self.__y - camera.offset_y

        width = 20 if self.__dx != 0 else 4
        height = 4 if self.__dx != 0 else 20

        rect = pygame.Rect(draw_x, draw_y, width, height)
        pygame.draw.rect(surface, (255, 0, 0), rect)
