import yaml
from upgrade import Upgrade

CATALOG_FP = "assets/data/catalog.yaml"


class Catalog:
    def __init__(self):
        with open(file=CATALOG_FP, mode="r") as catalog_file:
            catalog = yaml.safe_load(catalog_file)

        self.items = [
            Upgrade(
                item["name"],
                item["cost"],
                item["effect"],
                item["stat"]
            ) for item in catalog["catalog"]
        ]

    def purchase(self, player, item_id):
        if 0 <= item_id < len(self.items):
            item = self.items[item_id]
            # If player has enough gold
            if player.gold >= item.cost:
                player.gold -= item.cost
                player.upgrade(item.stat, item.effect)


if __name__ == "__main__":
    catalog = Catalog()
    print(catalog.items)
    print(catalog.items[0].name)
