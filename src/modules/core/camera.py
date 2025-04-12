import pygame

class Camera:
    def __init__(self, screen_width, screen_height, tile_size):
        self.__screen_width = screen_width
        self.__screen_height = screen_height
        self.__tile_size = tile_size
        self.__offset_x = 0
        self.__offset_y = 0

    @property
    def offset_x(self):
        return self.__offset_x

    @property
    def offset_y(self):
        return self.__offset_y

    @property
    def tile_size(self):
        return self.__tile_size

    def follow(self, target_pos, map_width, map_height):
        target_x, target_y = target_pos

        max_x = map_width * self.__tile_size - self.__screen_width
        max_y = map_height * self.__tile_size - self.__screen_height

        self.__offset_x = max(0, min(target_x - self.__screen_width // 2, max_x))
        self.__offset_y = max(0, min(target_y - self.__screen_height // 2, max_y))

    def draw_map(self, surface, layout, exit_tile):
        for y, row in enumerate(layout):
            for x, tile in enumerate(row):
                world_x = x * self.__tile_size
                world_y = y * self.__tile_size
                draw_x = world_x - self.__offset_x
                draw_y = world_y - self.__offset_y

                color = (100, 100, 100) if tile == 1 else (0, 0, 0)
                pygame.draw.rect(surface, color, (draw_x, draw_y, self.__tile_size, self.__tile_size))

        # Draw exit
        exit_x, exit_y = exit_tile
        pygame.draw.rect(surface, (0, 255, 0), (
            exit_x * self.__tile_size - self.__offset_x,
            exit_y * self.__tile_size - self.__offset_y,
            self.__tile_size,
            self.__tile_size
        ))
