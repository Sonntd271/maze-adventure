import pygame
from modules.character import Character
from modules.healthbar import Healthbar

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Adventure")
clock = pygame.time.Clock()

# Initialize character and healthbar
healthbar = Healthbar(max_health=100, starting_health=75)
character = Character(x=100, y=100, speed=5, healthbar=healthbar)

running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        character.move("up")
    if keys[pygame.K_s]:
        character.move("down")
    if keys[pygame.K_a]:
        character.move("left")
    if keys[pygame.K_d]:
        character.move("right")

    # Draw character
    character.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
