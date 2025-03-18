import pygame
import random
import classes.common.constants as c

def is_walkable(x, y, maze_image):
    """Ensures the entire player sprite is on a walkable area by checking multiple points."""
    if 0 <= x < c.dimensions["map_width"]  - c.dimensions["tile_size"] and 0 <= y < c.dimensions["map_height"]  - c.dimensions["tile_size"]:
        # Check four corners of the player to ensure full-body collision detection
        corners = [
            (x, y),  # Top-left
            (x + c.dimensions["tile_size"] - 1, y),  # Top-right
            (x, y + c.dimensions["tile_size"] - 1),  # Bottom-left
            (x + c.dimensions["tile_size"] - 1, y + c.dimensions["tile_size"] - 1)  # Bottom-right
        ]

        # If any corner is NOT transparent (not walkable), return False
        for corner_x, corner_y in corners:
            if maze_image.get_at((corner_x, corner_y)).a != 0:
                return False  # It's a wall

        return True  # Fully walkable
    return False  # Out of bounds

def find_random_walkable_position(maze_image, min_distance=300):
    """
    Find a random walkable position in the maze that is at least min_distance 
    away from the player's starting position.
    """
    player_start_x, player_start_y = 100, c.dimensions["screen_height"] // 2 + 50
    
    max_attempts = 1000
    attempts = 0
    
    while attempts < max_attempts:
        # Generate random coordinates
        x = random.randint(c.dimensions["tile_size"], c.dimensions["map_width"]  - c.dimensions["tile_size"])
        y = random.randint(c.dimensions["tile_size"], c.dimensions["map_height"]  - c.dimensions["tile_size"])
        
        # Check distance from player's starting position
        distance = ((x - player_start_x) ** 2 + (y - player_start_y) ** 2) ** 0.5
        
        # Check if position is walkable and far enough from player start
        if is_walkable(x, y, maze_image) and distance >= min_distance:
            # Make sure the entire enemy sprite would be on walkable area
            if (is_walkable(x + c.dimensions["tile_size"], y, maze_image) and
                is_walkable(x, y + c.dimensions["tile_size"], maze_image) and
                is_walkable(x + c.dimensions["tile_size"], y + c.dimensions["tile_size"], maze_image)):
                return x, y
        
        attempts += 1
    
    # Fallback to a default position if we couldn't find a good one
    return 300, 300  # This should be a walkable position in most mazes

def load_images():
    # Screen has to be initialized before calling
    maze_img = pygame.image.load(c.images["maze"]).convert_alpha()

    # Enemy
    bomb_up = pygame.image.load(c.images["bomb"]["up"])
    bomb_down = pygame.image.load(c.images["bomb"]["down"])
    bomb_left = pygame.image.load(c.images["bomb"]["left"])
    bomb_right = pygame.image.load(c.images["bomb"]["right"])

    bomb_up = pygame.transform.scale(bomb_up, (c.dimensions["tile_size"], c.dimensions["tile_size"]))
    bomb_down = pygame.transform.scale(bomb_down, (c.dimensions["tile_size"], c.dimensions["tile_size"]))
    bomb_left = pygame.transform.scale(bomb_left, (c.dimensions["tile_size"], c.dimensions["tile_size"]))
    bomb_right = pygame.transform.scale(bomb_right, (c.dimensions["tile_size"], c.dimensions["tile_size"]))

    # Player
    player_up = pygame.image.load(c.images["player"]["up"])
    player_down = pygame.image.load(c.images["player"]["down"])
    player_left = pygame.image.load(c.images["player"]["left"])
    player_right = pygame.image.load(c.images["player"]["right"])

    player_up = pygame.transform.scale(player_up, (c.dimensions["tile_size"], c.dimensions["tile_size"]))
    player_down = pygame.transform.scale(player_down, (c.dimensions["tile_size"], c.dimensions["tile_size"]))
    player_left = pygame.transform.scale(player_left, (c.dimensions["tile_size"], c.dimensions["tile_size"]))
    player_right = pygame.transform.scale(player_right, (c.dimensions["tile_size"], c.dimensions["tile_size"]))

    return maze_img, bomb_up, bomb_down, bomb_left, bomb_right, player_up, player_down, player_left, player_right
