# Maze Adventure

## Objectives
Clear a dynamically generated maze (get to the last level) while eliminating enemy that will move towards you and self-destruct

## Classes: In-game

**Player**
- Has health
- Able to shoot projectiles (upgradable in lobby)

**Enemy**
- Stationary but turn in cardinal directions randomly
- Once player spotted, close in to self-destruct, removing itself from map and dealing damage to the player

**Map**
- Handles dynamic generation of the map
    - Pending decision: Pre-load or on-view generation
    - Has to be randomized -- playthroughs will have different obstacle / enemy locations
- Map has areas of increasing difficulties

**Camera**
- Maintains the current view of the map in a 2d array
- Keeps track of the current "stage" the player is in

## Classes: Lobby

**Currency**
- Maintains the golds acquired within the maze

**Store**
- Upgrade player attributes e.g. health, projectile damage

## Ties to course content
- Pygame - Game has to be built using python library "pygame"
- Concurrency - Map and enemy have to be independent from player-controlled components
