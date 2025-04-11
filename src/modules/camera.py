import pygame

class Camera:
    def __init__(self, screen_width, screen_height, tile_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tile_size = tile_size
        self.offset_x = 0
        self.offset_y = 0

    def follow(self, target_pos, map_width, map_height):
        target_x, target_y = target_pos

        max_x = map_width * self.tile_size - self.screen_width
        max_y = map_height * self.tile_size - self.screen_height

        self.offset_x = max(0, min(target_x - self.screen_width // 2, max_x))
        self.offset_y = max(0, min(target_y - self.screen_height // 2, max_y))

    def draw_map(self, surface, layout, exit_tile):
        for y, row in enumerate(layout):
            for x, tile in enumerate(row):
                world_x = x * self.tile_size
                world_y = y * self.tile_size
                draw_x = world_x - self.offset_x
                draw_y = world_y - self.offset_y

                color = (100, 100, 100) if tile == 1 else (0, 0, 0)
                pygame.draw.rect(surface, color, (draw_x, draw_y, self.tile_size, self.tile_size))

        # Draw exit
        exit_x, exit_y = exit_tile
        pygame.draw.rect(surface, (0, 255, 0), (
            exit_x * self.tile_size - self.offset_x,
            exit_y * self.tile_size - self.offset_y,
            self.tile_size,
            self.tile_size
        ))