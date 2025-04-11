import pygame
from modules.enemy import Enemy
from modules.healthbar import Healthbar

def draw_character(screen, character, camera):
    x, y = character.position
    offset_x, offset_y = camera.offset_x, camera.offset_y
    character_rect = pygame.Rect(x - offset_x, y - offset_y, character.size, character.size)
    pygame.draw.rect(screen, character.color, character_rect)
    character.health.draw(screen, x - offset_x, y - offset_y - 10)

def handle_movement(keys, character, game_map, level, tile_size):
    x, y = character.position
    speed = character.speed
    size = character.size

    dx = dy = 0
    if keys["up"]: dy -= speed
    if keys["down"]: dy += speed
    if keys["left"]: dx -= speed
    if keys["right"]: dx += speed

    # Normalize diagonal speed
    if dx != 0 and dy != 0:
        dx *= 0.7071
        dy *= 0.7071

    next_x = x + dx
    next_y = y + dy

    # Check all corners of the new bounding box
    corners = [
        (next_x, next_y),
        (next_x + size - 1, next_y),
        (next_x, next_y + size - 1),
        (next_x + size - 1, next_y + size - 1),
    ]

    can_move = all(
        game_map.is_walkable(level, int(cx // tile_size), int(cy // tile_size))
        for cx, cy in corners
    )

    if can_move:
        character.position = [next_x, next_y]

def spawn_enemies(num, layout, tile_size):
    enemies = []
    h, w = len(layout), len(layout[0])
    import random
    count = 0
    while count < num:
        x, y = random.randint(1, w - 2), random.randint(1, h - 2)
        if layout[y][x] == 0:
            ex, ey = x * tile_size, y * tile_size
            enemy = Enemy(ex, ey, speed=2, healthbar=Healthbar(50, 50))
            enemies.append(enemy)
            count += 1
    return enemies
