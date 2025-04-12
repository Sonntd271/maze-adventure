class Currency:
    def __init__(self, initial_gold=0):
        self.gold = initial_gold

    def add(self, amount):
        self.gold += amount

    def spend(self, amount):
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False
