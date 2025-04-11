import pygame
from classes.resource_manager import resource_manager
import classes.common.constants as c
from classes.common.utilities import is_walkable, find_random_walkable_position
from classes.common.button import Button
from classes.game.player import Player
from classes.game.enemy import Enemy
from classes.game.camera import Camera
from classes.lobby.catalog import Catalog

def game():
    clock = pygame.time.Clock()
    
    player = Player(100, c.dimensions["screen_height"] // 2 + 50)
    camera = Camera(c.dimensions["map_width"], c.dimensions["map_height"])

    # Initialize enemies
    enemies = [Enemy(*find_random_walkable_position(resource_manager.maze_img)) for _ in range(3)]

    running = True
    while running and resource_manager.current_state == c.states["game"]:
        current_time = pygame.time.get_ticks()
        clock.tick(c.fps)
        resource_manager.screen.fill(c.colors["white"])

        keys = pygame.key.get_pressed()
        player.move(keys, resource_manager.maze_img)
        camera.update(player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                resource_manager.set_state(c.states["lobby"])
                return  # Return to the lobby

        # Draw game elements
        resource_manager.screen.blit(resource_manager.maze_img, (-camera.x_offset, -camera.y_offset))
        player.draw(camera)
        
        for projectile in player.projectiles[:]:
            projectile.move()
            
            if projectile.is_out_of_bounds() or projectile.hit_wall(resource_manager.maze_img):
                player.projectiles.remove(projectile)
                continue
            
            # Check for enemy hits
            for enemy in enemies[:]:
                if projectile.hit_enemy(enemy):
                    enemy.take_damage(projectile.damage)
                    player.projectiles.remove(projectile)
                    break  # Stop checking after first hit

        # Move enemies & check collisions
        for enemy in enemies[:]:
            if enemy.is_alive():
                enemy.move(player, resource_manager.maze_img)
                enemy.draw(camera)
                if enemy.collides_with_player(player):
                    player.take_damage(enemy.damage_amount, current_time)
            else:
                # Remove dead enemies and spawn new ones
                enemies.remove(enemy)
                
                # Ensure enemy spawns in a valid location
                for _ in range(5):  # Try 5 times to find a valid position
                    x, y = find_random_walkable_position(resource_manager.maze_img)
                    if is_walkable(x, y, resource_manager.maze_img):
                        enemies.append(Enemy(x, y))
                        break

        pygame.display.flip()


def store():
    catalog = Catalog()
    back_button = Button(300, 400, 200, 50, "Back to Lobby", lambda: resource_manager.set_state(c.states["lobby"]))
    
    buttons = []
    y_start = 150
    spacing = 60 

    # Generate item buttons
    for i, item in enumerate(catalog.items):
        item_text = resource_manager.font.render(f"{item.name} - {item.cost} Gold", True, (0, 0, 0))
        
        buy_button = Button(300, y_start + i * spacing, 150, 40, f"Buy {item.cost}g", lambda i=i: purchase_item(i, catalog))
        buttons.append((item_text, buy_button))

    running = True
    while running and resource_manager.current_state == c.states["store"]:
        resource_manager.screen.fill(c.colors["white"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if back_button.is_clicked(pos):
                    back_button.action()
                for _, button in buttons:
                    if button.is_clicked(pos):
                        button.action()

        # Draw items and buttons
        for i, (text, button) in enumerate(buttons):
            resource_manager.screen.blit(text, (100, y_start + i * spacing))
            button.draw()

        back_button.draw()
        pygame.display.flip()


def purchase_item(item_id, catalog):
    # TODO: Implement currency class to track money and use instead of player gold
    player = resource_manager.player
    if player and player.gold >= catalog.items[item_id].cost:
        catalog.purchase(player, item_id)
        print(f"✅ Purchased {catalog.items[item_id].name}!")
    else:
        print("❌ Not enough gold!")