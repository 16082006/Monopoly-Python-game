import gameboard
import gamesquare
import observer


class Player:
    """Player class to represent a player in the game"""

    def __init__(self, name, money):
        """Constructor for the Player class"""
        self.__name = name
        self.__money = money
        self.__properties = []
        self.__board_position = 0
        self.__doubles_count = 0
        self.__bankrupt_declared = False
        self.__utility_count = 0
        self.__railroad_count = 0
        # Jail-related attributes
        self.__turns_in_jail = 0
        self.__in_jail = False
        self.__jail_fine = 50
        self.__has_paid_fine = False
        self.__should_move_next_turn = False# NEW: Tracks if player should move after escaping
        self.__ready_to_move_after_escape = False
        self.__luck = 0
        self.__mortgaging_order = []

    def __str__(self):
        """String representation of the player"""
        return f"{self.__name} - {self.money} - {self.net_worth()} luck:{self.__luck:.1f}"

    # ===== JAIL-RELATED METHODS =====
    @property
    def in_jail(self):
        return self.__in_jail

    @property
    def turns_in_jail(self):
        return self.__turns_in_jail

    @property
    def should_move_next_turn(self):  # NEW: Getter for movement flag
        return self.__should_move_next_turn

    def go_to_jail(self):
        """Send to jail and pay fine immediately"""
        self.__board_position = 10
        self.__in_jail = True
        self.__turns_in_jail = 0
        self.__has_paid_fine = False
        self.__ready_to_move_after_escape = False
        self.__should_move_next_turn = False  # NEW: Reset movement flag
        self.__money -= self.__jail_fine
        if self.__money < 0:
            self.declare_bankrupt()
        observer.Event("update_state", f"{self.__name} pays ${self.__jail_fine} and goes to Jail!")

    def handle_jail_escape(self, dice_roll):
        """
        Handles jail escape attempts according to official Monopoly rules
        Returns True if player should move immediately (after paying fine),
        False if stays in jail or needs to wait for next turn (after doubles)
        """
        if not self.__in_jail:
            return True  # Not in jail, normal movement applies

        self.__turns_in_jail += 1
        dice_sum = dice_roll[0] + dice_roll[1]

        # Check for doubles
        if dice_roll[0] == dice_roll[1]:
            self.__in_jail = False
            self.__turns_in_jail = 0
            self.__ready_to_move_after_escape = True
            self.__should_move_next_turn = True
            observer.Event("update_state",
                           f"{self.__name} rolled doubles! {dice_roll[0]}+{dice_roll[1]}={dice_sum}. "
                           "Will move next turn.")
            return False

        # After 3 failed attempts
        if self.__turns_in_jail >= 3:
            if self.__money >= self.__jail_fine:
                self.__money -= self.__jail_fine
                self.__has_paid_fine = True
                self.__in_jail = False
                self.__turns_in_jail = 0
                self.__ready_to_move_after_escape = True
                self.__should_move_next_turn = True
                observer.Event("update_state",
                               f"{self.__name} paid ${self.__jail_fine} fine after 3 turns in jail. "
                               "Will move next turn.")
                return False
            else:
                # Player can't pay, must stay in jail
                observer.Event("update_state",
                               f"{self.__name} cannot pay ${self.__jail_fine} to leave jail! "
                               f"Turn {self.__turns_in_jail}/3. Rolled {dice_roll[0]}+{dice_roll[1]}={dice_sum}")
                return False

        # Still in jail, waiting for doubles or turn 3
        turns_left = 3 - self.__turns_in_jail
        observer.Event("update_state",
                       f"{self.__name} stays in jail ({turns_left} turn(s) left). "
                       f"Rolled {dice_roll[0]}+{dice_roll[1]}={dice_sum}")
        return False

    def move(self, spaces):
        """Move player with jail rules applying to both Jail (10) and Go to Jail (30)"""
        if self.__in_jail and not self.__should_move_next_turn:
            observer.Event("update_state", f"{self.__name} is in Jail and cannot move!")
            return False

        # Reset movement flag if escaping jail
        if self.__should_move_next_turn:
            self.__should_move_next_turn = False

        prior_position = self.__board_position
        self.__board_position += spaces
        passed_go = False

        # Handle board wrapping
        if self.__board_position >= 40:
            self.__board_position -= 40
            passed_go = True
            if not self.__in_jail:  # Only collect if not in jail
                self.__money += 200
                observer.Event("update_state", f"{self.__name} passed GO and collects $200!")

        # Update visual position
        observer.Event("update_player_position", {
            'player': self.__name,
            'from_position': prior_position,
            'to_position': self.__board_position
        })

        # Handle special squares - BOTH Jail (10) and Go to Jail (30) trigger jail
        if self.__board_position in [10, 30]:  # Both squares send to jail
            self.go_to_jail()
            observer.Event("update_state",
                           f"{self.__name} landed on {'Jail' if self.__board_position == 10 else 'Go to Jail'}!")
            return True

        elif self.__board_position == 20:  # Free Parking
            self.__money += 100
            observer.Event("update_state", f"{self.__name} landed on Free Parking! +$100")

        return True

    def buy_property(self, board_property):
        """Function to attempt to buy a property"""
        if not board_property.can_be_purchased():
            return False

        self.__properties.append(board_property)
        self.__money -= board_property.price
        board_property.owner = self
        if board_property.is_utility:
            self.__utility_count += 1
        if board_property.is_railroad:
            self.__railroad_count += 1
        return True

    def pay_rent(self, square, dice_sum):
        """Function to attempt to pay rent or tax on a square"""
        if square.owner is self:
            return 0
        rent = square.calculate_rent_or_tax(dice_sum)
        self.__money -= rent
        if square.owner is not None:
            square.owner.money += rent
        return rent

    def trade(self, other_player, offer, request):
        """Execute trade between players"""
        # Validate trade
        if not self._validate_trade(offer) or not other_player._validate_trade(request):
            return False

        # Exchange money
        self.money -= offer.get('money', 0)
        other_player.money -= request.get('money', 0)
        self.money += request.get('money', 0)
        other_player.money += offer.get('money', 0)

        # Exchange properties
        for prop in offer.get('properties', []):
            prop.owner = other_player

        for prop in request.get('properties', []):
            prop.owner = self

        return True

    def _validate_trade(self, trade_items):
        """Check if trade is valid"""
        # Check money
        if trade_items.get('money', 0) > self.money:
            return False

        # Check properties
        for prop in trade_items.get('properties', []):
            if prop.owner != self or prop.is_mortgaged:
                return False

        return True

    def mortgage_property(self, deed_name):
        """Function to mortgage a property"""
        for p in self.__properties:
            if p.name == deed_name:
                res = p.mortgage()
                if res:
                    self.__mortgaging_order.append(p)
                return True
        return False

    def unmortgage_property(self):
        """Function to unmortgage a property"""
        if len(self.__mortgaging_order) == 0:
            return ""
        p = self.__mortgaging_order.pop(0)
        res = p.unmortgage()
        if not res:
            return ""
        return p.name

    def net_worth(self):
        """Function to calculate the net worth of the player"""
        return self.money + sum(p.price for p in self.__properties)

    def collect(self, amount):
        """Function to collect money"""
        self.__money += amount


    @property
    def doubles_count(self):
        return self.__doubles_count

    @doubles_count.setter
    def doubles_count(self, doubles_count):
        self.__doubles_count = doubles_count

    @property
    def luck(self):
        return self.__luck

    @luck.setter
    def luck(self, luck):
        self.__luck = luck

    @property
    def money(self):
        return self.__money

    @money.setter
    def money(self, money):
        self.__money = money

    @property
    def name(self):
        return self.__name

    @property
    def position(self):
        return self.__board_position

    @property
    def bankrupt_declared(self):
        return self.__bankrupt_declared

    def declare_bankrupt(self):
        self.__bankrupt_declared = True

    @property
    def railroad_count(self):
        return self.__railroad_count

    @property
    def properties(self):
        return self.__properties

    @property
    def deed_names(self):
        return [p.name for p in self.__properties]

    @turns_in_jail.setter
    def turns_in_jail(self, value):
        self._turns_in_jail = value