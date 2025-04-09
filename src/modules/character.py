import pygame
from healthbar import Healthbar

class Character:
    def __init__(self, x, y, speed, healthbar: Healthbar):
        self.__position = [x, y]
        self.__speed = speed
        self.__health = healthbar

    @property
    def position(self):
        return self.__position
    
    @position.setter
    def position(self, new_position):
        # TODO: Implement boundary checks
        self.__position = new_position

    @property
    def speed(self):
        return self.__speed
    
    @speed.setter
    def speed(self, new_speed):
        if new_speed > 0:
            self.__speed = new_speed
        else:
            raise ValueError("Speed has to be more than 0")

    @property
    def health(self):
        return self.__health
    
    def is_alive(self):
        return self.health.current_health > 0
    
    def take_damage(self, damage: int):
        return self.health.update_health(-damage)
    
    def move(self, direction):
        if direction == "up":
            self.__position[1] -= self.__speed
        elif direction == "down":
            self.__position[1] += self.__speed
        elif direction == "left":
            self.__position[0] -= self.__speed
        elif direction == "right":
            self.__position[0] += self.__speed

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            (0, 128, 255),
            pygame.Rect(self.__position[0], self.__position[1], 32, 32)
        )

        # Draw healthbar too
        character.health.draw(surface, self.__position[0], self.__position[1] - 15)

if __name__ == "__main__":
    character = Character(0, 0, 5, healthbar=Healthbar(100, 100))
    
    print("# ===== Testing negative speed ===== #")
    try:
        character.speed = -5
    except ValueError as e:
        print(e)
    
    print("# ===== Testing take_damage ===== #")
    print(f"Initial HP: {character.health.current_health}; Alive: {character.is_alive()}")
    character.take_damage(100)
    print(f"HP after: {character.health.current_health}; Alive: {character.is_alive()}")
    character.take_damage(50)
    print(f"HP after: {character.health.current_health}; Alive: {character.is_alive()}")
