import pygame
from classes.state_manager import state_manager
from classes.ui.button import Button
import classes.common.constants as c

if __name__ == "__main__":
    play_button = Button(300, 200, 200, 50, "Play", lambda: print("Play clicked"))
    store_button = Button(300, 300, 200, 50, "Store", lambda: print("Store clicked"))

    running = True
    while running:
        state_manager.screen.fill((255, 255, 255))

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
    
    pygame.quit()