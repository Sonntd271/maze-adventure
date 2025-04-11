import pygame
import classes.common.constants as c


class Camera:
    def __init__(self, width, height):
        self.width = width  # Map width
        self.height = height  # Map height
        self.x_offset = 0  # Camera position
        self.y_offset = 0

    def update(self, player):
        """Keeps the player centered while keeping the camera inside map bounds."""
        self.x_offset = player.x - c.dimensions["screen_width"]  // 2
        self.y_offset = player.y - c.dimensions["screen_height"]  // 2

        # Prevent the camera from going beyond the map edges
        self.x_offset = max(0, min(self.x_offset, self.width - c.dimensions["screen_width"]))
        self.y_offset = max(0, min(self.y_offset, self.height - c.dimensions["screen_height"]))

    def apply(self, entity):
        """Shifts entities based on the camera offset so they move relative to the player."""
        return entity.x - self.x_offset, entity.y - self.y_offset
