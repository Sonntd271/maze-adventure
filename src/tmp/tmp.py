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
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Adventure")

# Fonts
font = pygame.font.Font(None, 36)

# Directions (Up, Right, Down, Left)
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

# Game States
STATE_LOBBY = "lobby"
STATE_STORE = "store"
STATE_PLAY = "play"
current_state = STATE_LOBBY

# Button Class
class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
    
    def draw(self):
        pygame.draw.rect(screen, GRAY, self.rect)
        label = font.render(self.text, True, BLACK)
        screen.blit(label, (self.rect.x + 20, self.rect.y + 10))
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

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
        self.health = 100
        self.projectile_damage = 10
        self.gold = 50
    
    def move(self, dx, dy):
        new_x, new_y = self.x + dx, self.y + dy
        if maze[new_y][new_x] == 0:
            self.x, self.y = new_x, new_y
    
    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    
    def upgrade(self, stat, amount):
        if stat == "health":
            self.health += amount
        elif stat == "damage":
            self.projectile_damage += amount

# Upgrade item class
class UpgradeItem:
    def __init__(self, name, cost, effect, stat):
        self.name = name
        self.cost = cost
        self.effect = effect
        self.stat = stat

# Store class
class Store:
    def __init__(self):
        self.items = [
            UpgradeItem("Increase Health", 20, 20, "health"),
            UpgradeItem("Increase Damage", 30, 5, "damage")
        ]
    
    def purchase(self, player, item_index):
        if 0 <= item_index < len(self.items):
            item = self.items[item_index]
            if player.gold >= item.cost:
                player.gold -= item.cost
                player.upgrade(item.stat, item.effect)

player = Player(1, 1)
store = Store()

# UI Buttons
play_button = Button(300, 200, 200, 50, "Play", lambda: set_state(STATE_PLAY))
store_button = Button(300, 300, 200, 50, "Store", lambda: set_state(STATE_STORE))
back_button = Button(300, 500, 200, 50, "Back to Lobby", lambda: set_state(STATE_LOBBY))

# Set state function
def set_state(state):
    global current_state
    current_state = state

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if current_state == STATE_LOBBY:
                if play_button.is_clicked(pos):
                    play_button.action()
                elif store_button.is_clicked(pos):
                    store_button.action()
            elif current_state == STATE_STORE:
                if back_button.is_clicked(pos):
                    back_button.action()
    
    if current_state == STATE_LOBBY:
        play_button.draw()
        store_button.draw()
        gold_text = font.render(f"Gold: {player.gold}", True, BLACK)
        screen.blit(gold_text, (10, 10))
    elif current_state == STATE_STORE:
        gold_text = font.render(f"Gold: {player.gold}", True, BLACK)
        screen.blit(gold_text, (10, 10))
        y_offset = 100
        for i, item in enumerate(store.items):
            item_text = font.render(f"{i+1}. {item.name} - {item.cost} Gold", True, BLACK)
            screen.blit(item_text, (100, y_offset))
            y_offset += 40
        back_button.draw()
    elif current_state == STATE_PLAY:
        # Draw maze
        for y in range(ROWS):
            for x in range(COLS):
                if maze[y][x] == 1:
                    pygame.draw.rect(screen, BLACK, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        # Draw player
        player.draw()
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()