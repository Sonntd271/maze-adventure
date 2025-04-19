import pygame
from modules.entities.enemy import Enemy
from modules.core.healthbar import Healthbar

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

    character.update_direction(dx, dy)

def spawn_enemies(num, layout, tile_size):
    enemies = []
    h, w = len(layout), len(layout[0])
    import random
    count = 0
    while count < num:
        x, y = random.randint(1, w - 2), random.randint(1, h - 2)
        if layout[y][x] == 0:
            ex, ey = x * tile_size, y * tile_size
            enemy = Enemy(ex, ey, speed=1, healthbar=Healthbar(50), size=tile_size // 1.5)
            enemies.append(enemy)
            count += 1
    return enemies

def lobby_screen(screen, player, currency, catalog, screen_width):
    font = pygame.font.SysFont(None, 28)

    while True:
        screen.fill((20, 20, 20))

        title = font.render("=== UPGRADE LOBBY ===", True, (255, 255, 255))
        screen.blit(title, (screen_width//2 - 100, 50))

        gold_display = font.render(f"Gold: {currency.gold}", True, (255, 215, 0))
        screen.blit(gold_display, (50, 100))

        for idx, upgrade in enumerate(catalog.items):
            u_text = f"{idx + 1}. {upgrade.name} (+{upgrade.value}) - {upgrade.cost} gold [x{upgrade.count}]"
            upgrade_surf = font.render(u_text, True, (255, 255, 255))
            screen.blit(upgrade_surf, (50, 150 + idx * 40))

        start_surf = font.render("Press ENTER to start", True, (180, 180, 180))
        screen.blit(start_surf, (50, 300))

        reset_msg = font.render("Press R to reset save", True, (255, 100, 100))
        screen.blit(reset_msg, (50, 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_4:
                    idx = event.key - pygame.K_1
                    if idx < len(catalog.items):
                        upgrade = catalog.items[idx]
                        if currency.spend(upgrade.cost):
                            player.apply_upgrade(upgrade)
                elif event.key == pygame.K_r:
                    currency.reset()
                    for _ in range(len(catalog.items)):
                        catalog.items[_].purchased = False
                elif event.key == pygame.K_RETURN:
                    return
        
    currency.save([u.name for u in catalog.items if u.purchased])
