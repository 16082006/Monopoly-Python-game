Monopoly Board Game — Python & Tkinter
A desktop Monopoly-style board game developed in Python with a Tkinter graphical interface. I developed this game using PyCharm, implementing custom gameplay rules, player customization, and a property-trading system.

The goal is to manage money and properties, collect rent, make trades, and outlast other players. Alongside familiar Monopoly mechanics, this version has several custom rules that change how players move around the board and manage their money.
Features
- Multiplayer turns: Players roll dice, move around the board, and interact with properties and special spaces.
- Custom player names: Enter names when starting the game; they appear in the interface.
- Property ownership and rent: Buy properties and collect rent from opponents.
- Color-group bonus: Owning a complete color group can double rent on unimproved properties.
- Player trading: Exchange eligible properties, cash, or both with another active player.
- Custom jail system: Players pay an initial fine and can attempt to escape by rolling doubles.
- Free Parking reward: Landing on Free Parking awards cash.
- Live interface updates: Player position, money, and jail status update as the game progresses.
How to Play
1. Start the Python application and enter names for the players.
2. Take turns rolling the dice to move around the board.
3. Purchase available properties when permitted by the game.
4. Pay rent when you land on a property owned by another player.
5. Build up color groups to increase rent on eligible properties.
6. Use the trading interface to propose exchanges of properties and/or money.
7. Manage your cash carefully to avoid bankruptcy.
Rules in This Version
Passing Go
- Passing Go during normal movement awards $200.
- Being sent directly to jail does not award $200 for passing Go.
Jail
- A player sent to jail immediately pays $50.
- The player has up to three chances to roll doubles to escape.
- If the player rolls doubles, no additional fine is charged; the initial $50 still applies.
- If all three attempts fail, the player pays another $50 to leave jail, for a total of $100 in fines.
- Landing on Go To Jail moves the player directly to jail and applies these rules.
Free Parking
- Landing on Free Parking immediately adds $100 to the player's balance.
Rent and Property Groups
- When a player owns every property in a color group, rent is doubled on eligible properties without houses or hotels.
- Mortgaged properties do not receive this bonus.
- Utilities and railroads follow their own rent calculations rather than this color-group bonus.
Trading
- Active players can trade cash, unmortgaged properties, or a combination of both.
- A player must own any property they offer and have enough cash for the proposed payment.
- Mortgaged properties cannot be traded through this system.
- The interface provides player/property selectors, money controls, and a confirmation dialog.
- Once confirmed, a valid trade transfers ownership and funds immediately; trades are final.
Built With
- Python — game logic and application code
- Tkinter — desktop graphical user interface
- CSV — board/property data
- PyCharm — development and debugging environment
Project Structure
monopoly1920/
├── controller.py       # Turns, dice rolls, jail, and trade coordination
├── player.py           # Player state, movement, and transfers
├── gameboard.py        # Board and property-group logic
├── gamesquare.py       # Square behavior and rent rules
├── view.py             # Tkinter interface
├── observer.py         # Interface update notifications
└── resources/          # Board data and image assets
Running the Game
1. Install Python 3 on your computer.
2. Download or clone this repository.
3. Open the project in PyCharm (or another Python IDE).
4. Run the game's Tkinter entry-point script from the project directory. Ensure the resources folder remains in place so board data and images can load.
The exact launch command depends on how the repository is arranged; verify the entry-point file before adding a one-line command here.

## My Contributions and Implementation

I developed the Monopoly game using Python and Tkinter in PyCharm, focusing on implementing interactive gameplay, custom rules, property management, and player interactions.

### Key Features Implemented

- Jail System: Implemented jail penalties, including a $50 entry fine, three attempts to roll doubles to escape, and an additional penalty if unsuccessful.
- Free Parking: Added a custom rule that awards players $100 when they land on Free Parking.
- Player Movement: Implemented movement rules, including collecting $200 when passing Go and moving directly to jail when landing on Go To Jail.
- Player Customization: Added the ability for players to enter their names before starting the game.
- Property Management: Implemented property ownership tracking, rent calculations, and double rent when a player owns a complete color group.
- Trading System: Developed a system allowing players to exchange properties and money, with validation and confirmation before completing transactions.
- Graphical User Interface: Used Tkinter to support player interactions, display game information, and update the interface as gameplay progresses.

# Technical Skills Applied

- Python Programming
- Object-Oriented Programming (OOP)
- Graphical User Interface Development with Tkinter
- Event-Driven Programming
- Game Logic and Rule Implementation
- Debugging and Testing using PyCharm

Developer: Anshul Kothiya
Project: University Computer Science coursework