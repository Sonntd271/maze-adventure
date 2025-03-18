import yaml

CONFIG_FP = "assets/data/config.yaml"

with open(file=CONFIG_FP, mode="r") as config_file:
    config = yaml.safe_load(config_file)

constants = config["constants"]

# General
caption = constants["caption"]
fps = constants["fps"]

# Dictionaries
colors = constants["colors"]
font = constants["font"]
directions = constants["directions"]
states = constants["states"]
dimensions = constants["dimensions"]
