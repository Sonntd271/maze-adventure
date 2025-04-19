import pygame
from modules.entities.player import Player
from modules.core.healthbar import Healthbar
from modules.core.map import Map
from modules.core.camera import Camera
from modules.core.currency import Currency
from modules.core.catalog import Catalog
from logic import *

pygame.init()

# Constants
CELL_SIZE = 50
TILE_SIZE = CELL_SIZE
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Adventure")
clock = pygame.time.Clock()

# Setup
level = 1
game_map = Map(rows=15 * CELL_SIZE, cols=15 * CELL_SIZE, cell_size=CELL_SIZE)
map_info = game_map.fetch_map_level(level)
layout = map_info["layout"]
start = map_info["start"]
exit_tile = map_info["exit"]
enemies = spawn_enemies(10, layout, TILE_SIZE)

healthbar = Healthbar(100)
player = Player(x=start[0] * TILE_SIZE, y=start[1] * TILE_SIZE, speed=5, healthbar=healthbar, size=TILE_SIZE // 1.5)
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE)
currency = Currency(initial_gold=0)
catalog = Catalog()

save_upgrades = currency.load()
for upgrade in catalog.items:
    times = save_upgrades.get(upgrade.name, 0)
    for _ in range(times):
        player.apply_upgrade(upgrade)

lobby_screen(screen, player, currency, catalog, SCREEN_WIDTH)

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    camera.follow(player.position, game_map.width, game_map.height)
    camera.draw_map(screen, layout, exit_tile)

    for enemy in enemies:
        enemy.update(player, game_map, level, TILE_SIZE)
        enemy.check_collision_with_player(player)
        enemy.draw(screen, camera)

    # Bullet collision
    for bullet in player.bullets:
        for enemy in enemies:
            if enemy.alive:
                bx, by = bullet.position
                rect = pygame.Rect(enemy.position[0], enemy.position[1], enemy.size, enemy.size)
                if rect.collidepoint(bx, by):
                    enemy.take_damage(player.bullet_damage)
                    if not enemy.alive:
                        currency.save_reward(10, catalog.items)
                    bullet.deactivate()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Movement keys (WASD)
    key_map = {
        "up": keys[pygame.K_w],
        "down": keys[pygame.K_s],
        "left": keys[pygame.K_a],
        "right": keys[pygame.K_d]
    }

    handle_movement(key_map, player, game_map, level, TILE_SIZE)

    # Shoot keys (arrows)
    if keys[pygame.K_UP]:
        player.shoot((0, -1))
    elif keys[pygame.K_DOWN]:
        player.shoot((0, 1))
    elif keys[pygame.K_LEFT]:
        player.shoot((-1, 0))
    elif keys[pygame.K_RIGHT]:
        player.shoot((1, 0))

    # Update and draw
    player.update_bullets(game_map, level, TILE_SIZE)
    player.draw(screen, camera)

    # Level end check
    player_tile = (player.position[0] // TILE_SIZE, player.position[1] // TILE_SIZE)
    if player_tile == exit_tile:
        level += 1
        map_info = game_map.fetch_map_level(level)
        if map_info:
            currency.save_reward(50, catalog.items)
            layout = map_info["layout"]
            start = map_info["start"]
            exit_tile = map_info["exit"]
            player.position = [start[0] * TILE_SIZE, start[1] * TILE_SIZE]
            enemies = spawn_enemies(num=10, layout=layout, tile_size=TILE_SIZE)
            player.bullets.clear()
        else:
            print("You win!")
            running = False
    
    if not player.is_alive():
        print("Game Over")
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()