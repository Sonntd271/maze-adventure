import pygame

class Healthbar:
    def __init__(self, max_health, starting_health):
        self.__max_health = max_health
        self.current_health = starting_health

    @property
    def max_health(self):
        return self.__max_health
    
    @max_health.setter
    def max_health(self, new_max_health):
        if new_max_health > self.max_health:
            self.__max_health = new_max_health
        else:
            raise ValueError("Max health should only be increased through upgrades")

    def update_health(self, value):
        self.current_health += value
        if self.current_health <= 0:
            self.current_health = 0
        
        return self.current_health

    def draw(self, surface, x, y):
        bar_width = 40
        bar_height = 6
        health_ratio = self.current_health / self.max_health

        pygame.draw.rect(surface, (200, 0, 0), pygame.Rect(x, y, bar_width, bar_height)) # Total health
        pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(x, y, bar_width * health_ratio, bar_height)) # Current health


if __name__ == "__main__":
    healthbar = Healthbar(100, 100)
    
    print("# ===== Testing max_health setter ===== #")
    print(f"Initial: {healthbar.max_health}")
    healthbar.max_health = 200
    print(f"After: {healthbar.max_health}")

    print("# ===== Testing update_health method ===== #")
    print(f"Initial: {healthbar.current_health}")
    healthbar.update_health(value=-50)
    print(f"After: {healthbar.current_health}")
    
