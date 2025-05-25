# Platformer Adventure

A 2D platformer game built with Pygame featuring player movement, enemies, platforms, coins, and multiple game states.


## Features

- Player character with jumping and movement mechanics
- Platforms (both static and moving)
- Patrolling enemies
- Collectible coins
- Score tracking and lives system
- Multiple game states (Menu, Playing, Game Over, Win)
- Sound effects and background music

## Requirements

- Python 3.6+
- Pygame

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/username/platformer-adventure.git
   cd platformer-adventure
   ```

2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install pygame
   ```

4. Run the game:
   ```bash
   python platformer_game.py
   ```

## How to Play

- **Arrow Keys**: Move left and right
- **Space** or **Up Arrow**: Jump
- **Enter**: Start game or return to menu
- **Escape**: Quit the game

## Game Objectives

- Collect all coins to win the level
- Avoid enemies and falling off platforms
- Try to achieve the highest score

## Project Structure

```
.
├── platformer_game.py    # Main game file
├── README.md             # This file
└── assets/               # Game assets directory
    ├── images/           # Images and sprites
    └── sounds/           # Sound effects and music
```

## Game Mechanics

- **Gravity**: The player is affected by gravity and will fall if not on a platform
- **Jumping**: The player can only jump when standing on a platform
- **Enemies**: Contact with enemies reduces player lives
- **Coins**: Collecting coins increases the score
- **Lives**: The player starts with 3 lives
- **Game Over**: Occurs when all lives are lost
- **Win**: Occurs when all coins are collected

## Code Structure

The game is organized into several key classes:

1. **Player Class**: Handles player movement, jumping, and collision detection  
2. **Platform Class**: Creates platforms for the player to stand on, including moving platforms  
3. **Enemy Class**: Implements patrolling enemies that can harm the player  
4. **Coin Class**: Collectible items that increase the player's score  
5. **Game Class**: Main class that manages the game loop, states, and all game objects  

## Future Improvements

- Add more levels with increasing difficulty
- Implement power-ups (double jump, speed boost, invincibility)
- Add animated sprites for player, enemies, and coins
- Implement a save/load system for progress
- Add different enemy types with unique behaviors
- Include boss battles at the end of each level
- Add parallax scrolling backgrounds for depth
- Implement a level editor for custom levels
- Add more sound effects and music tracks
- Include a high score system


## Acknowledgments

- Pygame community for their excellent documentation  
- Various online tutorials and resources that helped in understanding game development concepts
- Amazon's amazing AI powered chat agent - Amazon CLI Q
