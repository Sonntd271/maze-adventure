import yaml
from modules.core.upgrade import Upgrade

class Catalog:
    def __init__(self):
        self.__items = []
        self.__read_catalog()

    @property
    def items(self):
        return self.__items

    def __read_catalog(self):
        with open("assets/data/catalog.yaml") as catalog_info:
            catalog = yaml.safe_load(catalog_info)
            for upgrade in catalog["catalog"]:
                self.__items.append(
                    Upgrade(
                        name=upgrade["name"],
                        cost=upgrade["cost"],
                        target_attr=upgrade["stat"],
                        value=upgrade["value"]
                    )
                )

    def show_catalog(self):
        print("Showing available upgrades:\n")
        for idx, item in enumerate(self.__items):
            print(f"Upgrade ID: {idx + 1}\nName: {item.name}\nCost: {item.cost}\nTarget Status: {item.target_attr}\nValue: {item.value}\n")
