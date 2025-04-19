import yaml
import os

class Currency:
    SAVE_PATH = "assets/data/save_data.yaml"

    def __init__(self, initial_gold=0):
        self.__gold = initial_gold

    @property
    def gold(self):
        return self.__gold

    def add(self, amount):
        self.__gold += amount

    def spend(self, amount):
        if self.__gold >= amount:
            self.__gold -= amount
            return True
        return False

    def save(self, upgrades: list):
        data = {
            "gold": self.__gold,
            "upgrades": {u.name: u.count for u in upgrades}
        }
        with open(self.SAVE_PATH, "w") as f:
            yaml.dump(data, f)

    def load(self):
        if os.path.exists(self.SAVE_PATH):
            with open(self.SAVE_PATH, "r") as f:
                data = yaml.safe_load(f) or {}
                self.__gold = data.get("gold", 0)
                return data.get("upgrades", {})
        return {}
    
    def save_reward(self, amount, upgrades):
        self.add(amount)
        self.save(upgrades)

    def reset(self):
        self.__gold = 0
        with open(self.SAVE_PATH, "w") as f:
            yaml.dump({"gold": 0, "upgrades": []}, f)
