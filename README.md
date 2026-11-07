# Monopoly Board Game — Python & Tkinter

A desktop Monopoly-style board game developed in Python with a Tkinter graphical interface. I worked on the game in PyCharm, implementing interactive multiplayer gameplay, property transactions, player customization, and custom rules for jail, Free Parking, and rent.

The goal is to build wealth by buying properties, collecting rent, and making strategic trades while avoiding bankruptcy.

## Features

- Three-player game: Players take turns rolling two dice, moving around a 40-space board, and managing their money.
- Custom player names: Each player enters a name when the game starts (1–20 characters).
- Property management: Purchase available properties, collect rent, and mortgage or unmortgage owned properties.
- Property trading: Propose cash-and-property exchanges with another player.
- Custom rules: Jail fines, a Free Parking cash reward, and a double-rent bonus for complete color groups.
- Interactive desktop interface: Tkinter displays the board, player information, game messages, and trade controls.

## How to Play

1. Launch the application. Enter a name for each of the three players when prompted.
2. Take turns rolling the dice and moving around the board.
3. Buy available properties when you have sufficient funds.
4. Pay rent when you land on another player's eligible property.
5. Collect properties of the same color to qualify for the rent bonus.
6. Use the trading interface to offer money, eligible properties, or both.
7. Manage your balance and properties to stay in the game.

## Rules in This Version


### Starting Money and Passing Go

- Each player starts with $1,500.
- Passing Go through normal movement awards $200.
- Being sent directly to jail does not award $200 for passing Go.

### Jail

- Going to jail triggers an initial $50 fine.
- A jailed player can attempt to roll doubles on up to three turns.
- Rolling doubles releases the player without an additional fine; the initial $50 remains paid.
- After three unsuccessful attempts, the game charges an additional $50, for $100 total.
- Landing on Go To Jail sends the player to jail.
- Rolling doubles three times in a turn also triggers the game's jail-handling logic.

### Free Parking

- Landing on Free Parking awards $100 immediately.

### Property Ownership and Rent

- Unowned purchasable properties can be bought.
- Landing on an eligible property owned by another player triggers rent.
- Owning an entire color group gives a double-rent bonus on eligible unimproved properties.
- Mortgaged properties do not collect rent.
- Utilities and railroads use their own rent calculations rather than the color-group bonus.
- Mortgaging a property provides half its purchase price; unmortgaging requires that amount plus a 10% fee.

### Trading

- Players can propose exchanges involving cash, properties, or both.
- The game checks that a player owns each offered property and that the property is not mortgaged.
- The game also checks that each side has enough money for its proposed payment.
- When a valid trade is processed, the game transfers the agreed money and property ownership.

## Built With

| Technology | Purpose |
|---|---|
| Python | Game logic, players, turns, and transactions |
| Tkinter / ttk | Desktop GUI, player-name prompts, and trade controls |
| CSV | Board and property data |
| PyCharm | Development and debugging |


The code also uses an observer/event-notification pattern to communicate game updates to the interface.

## Project Structure

```text
monopoly1920/
├── view.py                 # Tkinter GUI and application entry point
├── controller.py           # Game flow, dice, turns, and trade coordination
├── player.py               # Player state, movement, money, and trades
├── gameboard.py            # Board setup and property-group logic
├── gamesquare.py           # Property details, mortgages, and rent
├── observer.py             # Event notifications
├── Gamelogger.py           # Game logging utility
├── resources/
│   ├── data/
│   │   └── board.csv       # Board data
│   └── images/             # Board and property images
└── text_docs/              # Additional project documentation
```

## Running the Game


### Requirements

- Python 3 with Tkinter support
- A desktop environment capable of displaying Tkinter windows
Tkinter is normally included with many Python installations; if import tkinter fails, install or enable Tkinter for your Python distribution.

### Steps

1. Download or clone this repository.
2. Open a terminal and navigate to the monopoly1920 folder (the folder containing view.py and resources).
3. Run:

   ```bash
   python view.py
   ```

   On systems where Python 3 is invoked as `python3`, use `python3 view.py` instead.
4. Enter the three player names in the prompts to begin.
PyCharm: Open the project and run view.py. Set the run configuration's working directory to monopoly1920 so the game can find resources/data/board.csv and the board images.

## Screenshots

Screenshots of the running game can be added here to demonstrate the board, player setup, and trading interface.
<!-- After adding real screenshots to a screenshots/ folder, uncomment and update these paths:
![Game board](screenshots/game-board.png)
![Player setup](screenshots/player-setup.png)
![Trading interface](screenshots/trading.png)
-->

## Technical Highlights

Working on this project involved:
- Implementing rule-based game logic for movement, fines, rent, and property transactions.
- Managing player state, cash balances, ownership, and jail status.
- Building interactive Tkinter dialogs and controls.
- Validating proposed trades before transferring money and properties.
- Organizing game functionality across separate Python modules.
- Connecting game events to GUI updates through observer-style notifications.
**Developer:** Anshul Kothiya  
**Project context:** Computer Science coursework  
**Development environment:** PyCharm