import player
import gamesquare

class GameBoard:

    __boardCSV = {
        "name": 0,
        "space": 1,
        "color": 2,
        "position": 3,
        "price": 4,
        "build": 5,
        "rent": 6,
        "rent1": 7,
        "rent2": 8,
        "rent3": 9,
        "rent4": 10,
        "rent5": 11,
        "hotelcost": 12,
        "owner": 13,
        "houses": 14,
        "groupmembers": 15
    }

    def __init__(self, properties_path, players ):
        self.__properties = self._load_game_board(properties_path)

        self.__players = players

        self.__total_turns = 0

        # set the current player
        self.__current_player = self.__players.pop(0)

    def next_turn(self):
        #add the prior player to the end of the queue
        if not self.__current_player.bankrupt_declared:
            self.__players.append(self.__current_player)

        self.__total_turns += 1

        #set the current player to the next player in the queue
        self.__current_player = self.__players.pop(0)

        return self.__current_player.name

    def calculate_expected_value(self, pos, doubles_count):
        """calculate the expected outcome of the next turn"""
        expected_value = 0
        for i in range(1,7):
            for j in range(1,7):
                new_pos = (pos + i + j) % 40
                #base case calculate the outcome of landing on the square
                if doubles_count == 2 and i == j:
                    continue #go to jail

                expected_value += (self.get_board_square(new_pos).calculate_rent_or_tax(i+j) / 36)
                if i == j:
                    #recursive case roll again don't forget this must be multiplied by
                    # the probability of rolling a double (1/36)
                    expected_value += (self.calculate_expected_value(new_pos, doubles_count+1) / 36)
        return expected_value

    def get_current_player(self):
        """return the current player"""
        return self.__current_player

    def get_all_squares(self):
        return self.__properties

    def get_square(self, index):
        return self.__properties[index]

    def get_board_square(self, index):
        """Function to return the board square at the given index
            @:param game_board: an ordered list of Properties
            @:param index: the index of the space on the board
            @:return square: the square at the given index
        """
        square = self.__properties[index]
        return square

    def _load_game_board(self, csv_path):
        """Load game board with color groups for monopoly tracking"""
        properties = []
        color_groups = {}  # Temporary storage for grouping properties by color

        f = open(csv_path, "r")
        next(f)  # Skip header row

        # First pass - create properties and group by color
        for line in f:
            line = line.strip().split(",")

            utility = line[self.__boardCSV["space"]] == "Utility"
            railroad = line[self.__boardCSV["space"]] == "Railroad"
            color = line[self.__boardCSV["color"]]

            sq = gamesquare.GameSquare(
                name=line[self.__boardCSV["name"]],
                price=int(line[self.__boardCSV["price"]]),
                rent=int(line[self.__boardCSV["rent"]]),
                color=color,
                is_utility=utility,
                is_railroad=railroad,
                space=line[self.__boardCSV["space"]]
            )

            properties.append(sq)

            # Skip grouping for special spaces and railroads/utilities
            if not utility and not railroad and color:  # Only group colored properties
                if color not in color_groups:
                    color_groups[color] = []
                color_groups[color].append(sq)

        f.close()

        # Second pass - assign color groups to each property
        for color, group in color_groups.items():
            for property in group:
                # Assign all other properties of same color to each property's group
                property._GameSquare__color_group = [p for p in group if p != property]

        return properties

    def __str__(self):
        board_str = "player - cash - net worth - position\n"
        board_str += f"{self.__current_player} "
        board_str += f"{self.get_board_square(self.__current_player.position).name}\n"
        for player in self.__players:
            if player.bankrupt_declared:
                board_str += f"{player.name} declared bankruptcy\n"
                continue
            board_str += f"{player} "
            board_str += f"{self.get_board_square(player.position).name}\n"

        return board_str

