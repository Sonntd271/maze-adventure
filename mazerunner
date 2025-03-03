import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720  # Visible game window size
MAP_WIDTH, MAP_HEIGHT = 2000, 2000  # Full map size
TILE_SIZE = 40
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Adventure")

# Load images
MAZE_IMAGE = pygame.image.load(r'C:\Users\bounc\Downloads\mazerunner\images\realmaze_1.png').convert_alpha()

# Load bomb images
BOMB_UP = pygame.image.load(r'C:\Users\bounc\Downloads\mazerunner\images\bomb_up.png')
BOMB_DOWN = pygame.image.load(r'C:\Users\bounc\Downloads\mazerunner\images\bomb_down.png')
BOMB_LEFT = pygame.image.load(r'C:\Users\bounc\Downloads\mazerunner\images\bomb_left.png')
BOMB_RIGHT = pygame.image.load(r'C:\Users\bounc\Downloads\mazerunner\images\bomb_right.png')

# Load player directional images
PLAYER_UP = pygame.image.load(r'C:\Users\bounc\Downloads\mazerunner\images\character_up.png')
PLAYER_DOWN = pygame.image.load(r'C:\Users\bounc\Downloads\mazerunner\images\character_down.png')
PLAYER_LEFT = pygame.image.load(r'C:\Users\bounc\Downloads\mazerunner\images\character_left.png')
PLAYER_RIGHT = pygame.image.load(r'C:\Users\bounc\Downloads\mazerunner\images\character_right.png')

# Scale images
PLAYER_UP = pygame.transform.scale(PLAYER_UP, (TILE_SIZE, TILE_SIZE))
PLAYER_DOWN = pygame.transform.scale(PLAYER_DOWN, (TILE_SIZE, TILE_SIZE))
PLAYER_LEFT = pygame.transform.scale(PLAYER_LEFT, (TILE_SIZE, TILE_SIZE))
PLAYER_RIGHT = pygame.transform.scale(PLAYER_RIGHT, (TILE_SIZE, TILE_SIZE))

BOMB_UP = pygame.transform.scale(BOMB_UP, (TILE_SIZE, TILE_SIZE))
BOMB_DOWN = pygame.transform.scale(BOMB_DOWN, (TILE_SIZE, TILE_SIZE))
BOMB_LEFT = pygame.transform.scale(BOMB_LEFT, (TILE_SIZE, TILE_SIZE))
BOMB_RIGHT = pygame.transform.scale(BOMB_RIGHT, (TILE_SIZE, TILE_SIZE))

# Clock
clock = pygame.time.Clock()

class Camera:
    def __init__(self, width, height):
        self.width = width  # Map width
        self.height = height  # Map height
        self.x_offset = 0  # Camera position
        self.y_offset = 0

    def update(self, player):
        """Keeps the player centered while keeping the camera inside map bounds."""
        self.x_offset = player.x - SCREEN_WIDTH  // 2
        self.y_offset = player.y - SCREEN_HEIGHT  // 2

        # Prevent the camera from going beyond the map edges
        self.x_offset = max(0, min(self.x_offset, self.width - SCREEN_WIDTH))
        self.y_offset = max(0, min(self.y_offset, self.height - SCREEN_HEIGHT))

    def apply(self, entity):
        """Shifts entities based on the camera offset so they move relative to the player."""
        return entity.x - self.x_offset, entity.y - self.y_offset


class Healthbar:
    def __init__(self, max_health, width=30, height=5):
        self.max_health = max_health
        self.current_health = max_health
        self.width = width
        self.height = height
    
    def update(self, health):
        self.current_health = max(0, min(health, self.max_health))
    
    def draw(self, x, y, camera):
        screen_x, screen_y = camera.apply(type("Entity", (object,), {"x": x, "y": y})()) 
        # Position the healthbar 15px above the character
        bar_x = screen_x  + (TILE_SIZE - self.width) // 2
        bar_y = screen_y  - 15
        
        # Draw background (empty health)
        pygame.draw.rect(screen, BLACK, (bar_x - 1, bar_y - 1, self.width + 2, self.height + 2))
        pygame.draw.rect(screen, RED, (bar_x, bar_y, self.width, self.height))
        
        # Draw current health
        if self.current_health > 0:
            current_width = int((self.current_health / self.max_health) * self.width)
            pygame.draw.rect(screen, GREEN, (bar_x, bar_y, current_width, self.height))

class Projectile:
    def __init__(self, x, y, direction, speed=10):
        self.x = x
        self.y = y
        self.direction = direction  # ('up', 'down', 'left', 'right')
        self.speed = speed
        self.color = GREEN
        self.width = 3
        self.height = 10
        self.damage = 50  # Damage per hit

    def move(self):
        if self.direction == 'up':
            self.y -= self.speed
        elif self.direction == 'down':
            self.y += self.speed
        elif self.direction == 'left':
            self.x -= self.speed
        elif self.direction == 'right':
            self.x += self.speed

    def draw(self, camera):
        screen_x, screen_y = camera.apply(self)
        if self.direction in ['up', 'down']:
            pygame.draw.line(screen, self.color, (screen_x, screen_y), (screen_x, screen_y - self.height), self.width)
        else:  # Left or Right
            pygame.draw.line(screen, self.color, (screen_x, screen_y), (screen_x + self.height, screen_y), self.width)

    def is_out_of_bounds(self):
        return self.x < 0 or self.x > MAP_WIDTH  or self.y < 0 or self.y > MAP_HEIGHT

    def hit_wall(self, maze_image):
        """Checks if the laser hits a non-walkable area in the maze."""
        return not is_walkable(self.x, self.y, maze_image)
    
    def hit_enemy(self, enemy):
        """Check if the projectile hits an enemy."""
        return (self.x >= enemy.x and self.x <= enemy.x + TILE_SIZE and
                self.y >= enemy.y and self.y <= enemy.y + TILE_SIZE)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.projectiles = []  # List to store lasers
        self.last_direction = 'right'  # Default direction (starting with right)
        self.healthbar = Healthbar(500)  # Player has 500 HP
        self.last_damage_time = 0  # To track when damage was last taken
        
        # Dictionary to store player images for each direction
        self.images = {
            'up': PLAYER_UP,
            'down': PLAYER_DOWN,
            'left': PLAYER_LEFT,
            'right': PLAYER_RIGHT
        }
        
        # Current image based on last direction (start with right)
        self.current_image = self.images['right']

    def move(self, keys, maze_image):
        dx, dy = 0, 0
        direction_changed = False
        
        if keys[pygame.K_LEFT]: 
            dx = -self.speed
            self.last_direction = 'left'
            direction_changed = True
        if keys[pygame.K_RIGHT]: 
            dx = self.speed
            self.last_direction = 'right'
            direction_changed = True
        if keys[pygame.K_UP]: 
            dy = -self.speed
            self.last_direction = 'up'
            direction_changed = True
        if keys[pygame.K_DOWN]: 
            dy = self.speed
            self.last_direction = 'down'
            direction_changed = True

        # Update player image if direction changed
        if direction_changed:
            self.current_image = self.images[self.last_direction]

        new_x, new_y = self.x + dx, self.y + dy

        # Check if the new position is on a transparent pixel
        if is_walkable(new_x, new_y, maze_image):
            self.x, self.y = new_x, new_y

    def shoot(self):
        """Shoots a green laser in the last moved direction."""
        laser = Projectile(self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2, self.last_direction)
        self.projectiles.append(laser)

    def take_damage(self, amount, current_time):
        """Player takes damage from enemies"""
        # Only take damage once per second
        if current_time - self.last_damage_time >= 1000:  # 1000 ms = 1 second
            self.healthbar.update(self.healthbar.current_health - amount)
            self.last_damage_time = current_time
    
    def is_alive(self):
        """Check if player is still alive"""
        return self.healthbar.current_health > 0

    def draw(self, camera):
        # Draw current direction image instead of a static image
        screen.blit(self.current_image, camera.apply(self))
        
        # Draw health bar
        self.healthbar.draw(self.x, self.y, camera)
        
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(camera)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
        self.healthbar = Healthbar(100)  # Enemy has 100 HP
        self.damage_amount = 20  # Damage to player per second
        self.last_sprite_change = pygame.time.get_ticks()
        self.sprite_index = 0

        # Store bomb images for different directions
        self.images = {
            'up': BOMB_UP,
            'down': BOMB_DOWN,
            'left': BOMB_LEFT,
            'right': BOMB_RIGHT
        }

        self.current_image = self.images['up']  # Default starting appearance
    
    def can_see_player(self, player, maze_image):
        """Check if there's a clear line of sight to the player (raycasting)."""
        steps = 50  
        x, y = self.x, self.y
        dx = player.x - x
        dy = player.y - y
        distance = max(abs(dx), abs(dy))
        step_x = dx / distance if distance != 0 else 0
        step_y = dy / distance if distance != 0 else 0

        for _ in range(0, distance, steps):
            x += step_x * steps
            y += step_y * steps
            if not is_walkable(int(x), int(y), maze_image):
                return False  

        return True  

    def move(self, player, maze_image):
        """Moves toward the player if visible; otherwise, stays in place and cycles sprite."""
        current_time = pygame.time.get_ticks()

        if self.can_see_player(player, maze_image):
            # Move towards player
            if self.x < player.x:
                new_x = self.x + self.speed
                self.current_image = self.images['right']
            elif self.x > player.x:
                new_x = self.x - self.speed
                self.current_image = self.images['left']
            else:
                new_x = self.x

            if self.y < player.y:
                new_y = self.y + self.speed
                self.current_image = self.images['down']
            elif self.y > player.y:
                new_y = self.y - self.speed
                self.current_image = self.images['up']
            else:
                new_y = self.y

            if is_walkable(new_x, new_y, maze_image):
                self.x = new_x
                self.y = new_y
        else:
            if current_time - self.last_sprite_change >= 2000:  
                sprite_order = ['up', 'right', 'down', 'left']
                self.sprite_index = (self.sprite_index + 1) % 4  
                self.current_image = self.images[sprite_order[self.sprite_index]]
                self.last_sprite_change = current_time  

    def take_damage(self, amount):
        """Enemy takes damage from projectiles"""
        self.healthbar.update(self.healthbar.current_health - amount)
    
    def is_alive(self):
        """Check if enemy is still alive"""
        return self.healthbar.current_health > 0
    
    def collides_with_player(self, player):
        """Check if enemy collides with player"""
        return (self.x < player.x + TILE_SIZE and self.x + TILE_SIZE > player.x and
                self.y < player.y + TILE_SIZE and self.y + TILE_SIZE > player.y)

    def draw(self, camera):
        screen.blit(self.current_image, camera.apply(self))
        self.healthbar.draw(self.x, self.y, camera)

def is_walkable(x, y, maze_image):
    """Ensures the entire player sprite is on a walkable area by checking multiple points."""
    if 0 <= x < MAP_WIDTH  - TILE_SIZE and 0 <= y < MAP_HEIGHT  - TILE_SIZE:
        # Check four corners of the player to ensure full-body collision detection
        corners = [
            (x, y),  # Top-left
            (x + TILE_SIZE - 1, y),  # Top-right
            (x, y + TILE_SIZE - 1),  # Bottom-left
            (x + TILE_SIZE - 1, y + TILE_SIZE - 1)  # Bottom-right
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
    player_start_x, player_start_y = 100, SCREEN_HEIGHT // 2 + 50
    
    max_attempts = 1000
    attempts = 0
    
    while attempts < max_attempts:
        # Generate random coordinates
        x = random.randint(TILE_SIZE, MAP_WIDTH  - TILE_SIZE)
        y = random.randint(TILE_SIZE, MAP_HEIGHT  - TILE_SIZE)
        
        # Check distance from player's starting position
        distance = ((x - player_start_x) ** 2 + (y - player_start_y) ** 2) ** 0.5
        
        # Check if position is walkable and far enough from player start
        if is_walkable(x, y, maze_image) and distance >= min_distance:
            # Make sure the entire enemy sprite would be on walkable area
            if (is_walkable(x + TILE_SIZE, y, maze_image) and
                is_walkable(x, y + TILE_SIZE, maze_image) and
                is_walkable(x + TILE_SIZE, y + TILE_SIZE, maze_image)):
                return x, y
        
        attempts += 1
    
    # Fallback to a default position if we couldn't find a good one
    return 300, 300  # This should be a walkable position in most mazes

# Initialize player
player = Player(100, SCREEN_HEIGHT  // 2 + 50)
camera = Camera(MAP_WIDTH, MAP_HEIGHT)

# Initialize enemies at random walkable positions
enemies = []
num_enemies = 3  # Number of enemies to spawn

for _ in range(num_enemies):
    x, y = find_random_walkable_position(MAZE_IMAGE)
    enemies.append(Enemy(x, y))

# Main game loop
camera = Camera(2000, 2000)
running = True
while running:
    current_time = pygame.time.get_ticks()
    clock.tick(30)  # 30 FPS
    screen.fill(WHITE)
    

    # Get input
    keys = pygame.key.get_pressed()
    player.move(keys, MAZE_IMAGE)
    camera.update(player)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    screen.blit(MAZE_IMAGE, (-camera.x_offset, -camera.y_offset))
    player.draw(camera)



    # Move projectiles and check for collisions
    for projectile in player.projectiles[:]:
        projectile.move()
        
        # Check for wall hits or out of bounds
        if projectile.is_out_of_bounds() or projectile.hit_wall(MAZE_IMAGE):
            player.projectiles.remove(projectile)
            continue
        
        # Check for enemy hits
        for enemy in enemies[:]:
            if projectile.hit_enemy(enemy):
                enemy.take_damage(projectile.damage)
                player.projectiles.remove(projectile)
                break

    # Move enemies and check for player collisions
    for enemy in enemies[:]:
        if enemy.is_alive():
            enemy.move(player, MAZE_IMAGE)
            
            # Check for collision with player
            if enemy.collides_with_player(player):
                player.take_damage(enemy.damage_amount, current_time)
        else:
            # Remove dead enemies
            enemies.remove(enemy)
            
            # Spawn a new enemy when one dies
            x, y = find_random_walkable_position(MAZE_IMAGE)
            enemies.append(Enemy(x, y))

    # Check if player is still alive
    if not player.is_alive():
        # Game over handling (you can add more logic here)
        print("Game Over!")
        running = False
    
    # Draw elements if they are alive
    player.draw(camera)
    for enemy in enemies:
        enemy.draw(camera)

    pygame.display.flip()

pygame.quit()
