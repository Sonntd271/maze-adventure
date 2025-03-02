import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Explorer Prototype")

# Directions (Up, Right, Down, Left)
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

# Generate a random maze using recursive backtracking
def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    stack = [(1, 1)]
    maze[1][1] = 0  # Start position is open
    
    while stack:
        x, y = stack[-1]
        random.shuffle(DIRECTIONS)
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx * 2, y + dy * 2
            if 1 <= nx < cols - 1 and 1 <= ny < rows - 1 and maze[ny][nx] == 1:
                maze[ny][nx] = 0
                maze[y + dy][x + dx] = 0
                stack.append((nx, ny))
                break
        else:
            stack.pop()
    return maze

maze = generate_maze(ROWS, COLS)

# Player class
class Player:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.color = BLUE
        self.size = TILE_SIZE // 2
    
    def move(self, dx, dy):
        new_x, new_y = self.x + dx, self.y + dy
        if maze[new_y][new_x] == 0:
            self.x, self.y = new_x, new_y
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Enemy class
class Enemy:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.color = RED
    
    def move_random(self):
        dx, dy = random.choice(DIRECTIONS)
        new_x, new_y = self.x + dx, self.y + dy
        if maze[new_y][new_x] == 0:
            self.x, self.y = new_x, new_y
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Initialize player and enemy
player = Player(1, 1)
enemies = [Enemy(random.randint(2, COLS - 2), random.randint(2, ROWS - 2)) for _ in range(3)]

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.move(0, -1)
    if keys[pygame.K_s]:
        player.move(0, 1)
    if keys[pygame.K_a]:
        player.move(-1, 0)
    if keys[pygame.K_d]:
        player.move(1, 0)
    
    # Move enemies randomly
    for enemy in enemies:
        enemy.move_random()
    
    # Draw maze
    for y in range(ROWS):
        for x in range(COLS):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLACK, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    
    # Draw player and enemies
    player.draw()
    for enemy in enemies:
        enemy.draw()
    
    pygame.display.flip()
    clock.tick(10)

pygame.quit()