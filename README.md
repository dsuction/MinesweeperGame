# Minesweeper Console Game

## Project Overview
This is a console version of the Minesweeper game. It uses colors, tables built with special characters, and simple controls. The goal of the game is to find all mines.

## Features
*   Colored Interface: Game elements (numbers, mines, flags) are displayed in color.
*   Clear Board: The game board is created using ASCII tables and special characters.
*   Simple Controls: Commands for game interaction.
*   Flags: You can place and remove flags on cells.
*   Game States: Shows mine explosion or a victory message.

## Screenshots
Game display examples:

### Game Start
![Initial state of the game board.](https://raw.githubusercontent.com/dsuction/MinesweeperGame/main/images/image_1.png)
*Shows an empty game board at the beginning of the game.*

### Gameplay
![Game board with opened cells and flags.](https://raw.githubusercontent.com/dsuction/MinesweeperGame/main/images/image_2.png)
*Demonstrates cells with numbers and placed flags.*

### Game Over
![Game board after a loss with mines revealed.](https://raw.githubusercontent.com/dsuction/MinesweeperGame/main/images/image_4.png)
*Displays the exploded mine and the location of all mines.*

### Victory
![Victory screen.](https://raw.githubusercontent.com/dsuction/MinesweeperGame/main/images/image_3.png)
*Shows the win message and a fully revealed board.*

## How to Run The Project
Python (version 3.11 recommended) is required to run the game.

1. Clone the repository:
    ```bash
    git clone https://github.com/dsuction/MinesweeperGame.git
    ```
2. Navigate to the project directory:
    ```bash
    cd MinesweeperGame
    ```
3. Install dependencies (if any):
    ```bash
    pip -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
4. Run the game:
    ```bash
    python mines_weeper.py
    ```
    
## Technologies Used

*   Python 3.12
*   rich 14.0.0

## Contributing

You can create Issues or Pull Requests.

---

Dsuction

---
