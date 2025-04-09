import pygame
from classes.resource_manager import resource_manager
from classes.common.button import Button
import classes.common.constants as c
from classes.stage_manager import game, store

def lobby():
    play_button = Button(300, 200, 200, 50, "Play", lambda: resource_manager.set_state(c.states["game"]))
    store_button = Button(300, 300, 200, 50, "Store", lambda: resource_manager.set_state(c.states["store"]))

    running = True
    while running and resource_manager.current_state == c.states["lobby"]:
        resource_manager.screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if play_button.is_clicked(pos):
                    play_button.action()
                elif store_button.is_clicked(pos):
                    store_button.action()
        
        play_button.draw()
        store_button.draw()
        
        pygame.display.flip()

        # Transition to the next state
        if resource_manager.current_state == c.states["game"]:
            game()
        elif resource_manager.current_state == c.states["store"]:
            store()

    pygame.quit()

if __name__ == "__main__":
    lobby()
