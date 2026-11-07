import os
import view
import random
import gameboard
import player as plr  # avoid naming conflict with the player module
import gamesquare
import observer


class Controller(observer.Observer):
    """Control the game flow"""

    def __init__(self, root):

        # for now we have references to the backend and frontend objects
        # tight coupling is not ideal, but we will refactor later
        super().__init__()
        self._view = view.View(root)

        csv_path = os.path.join("resources", "data", "board.csv")
        players = self._create_players(3)
        self._gameboard = gameboard.GameBoard(csv_path, players)

        self._add_listeners()

        self.__dice_rolled = False

        self.__roll_count = 0

        observer.Event("update_state", f"{self._gameboard.get_current_player().name}'s turn")
        observer.Event("update_state_box", str(self._gameboard))

        self._set_expected_val()


    def _add_listeners(self):
        """Add listeners to the view"""
        self.observe("roll", self._roll_action)
        self.observe("end_turn", self._end_player_turn)
        self.observe("purchase", self._buy_square)
        self.observe("mortgage", self._mortgage)
        self.observe("mortgage_specific", self._mortgage_specific)
        self.observe("unmortgage", self._unmortgage)

    def _test_observers(self, data):
        """Test the observer pattern"""
        print("observed event roll")

    def _create_players(self, num_players):
        players = []
        for i in range(num_players):
            while True:
                name = self._view.get_player_name(f"Player {i+1}")
                if name and 1 <= len(name) <= 20:  # Validate length
                    break
                # Optional: Show error in UI
                self._view.show_error("Name must be 1-20 characters")

            player = plr.Player(name, 1500)
            players.append(player)
            observer.Event("update_state", f"Player {i + 1}: {name} created")
        return players

    def _set_expected_val(self):
        ev = self._gameboard.calculate_expected_value(self._gameboard.get_current_player().position, 0)
        ev = round(ev, 2)
        observer.Event("update_state", f"Expected value: {ev}")

        player = self._gameboard.get_current_player()
        # add the expected value to the player's luck
        player.luck += ev

    def _roll_dice(self):
        """Simulate the rolling of two dice
            :return the sum of two random dice values
        """
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        dice_sum = dice1 + dice2

        self.__dice_rolled = True
        self.__roll_count += 1

        if dice1 == dice2:
            # double rolled
            observer.Event("update_state", f"Doubles rolled: {dice1}+{dice2} = {dice_sum}")
            self.__dice_rolled = False
        else:
            observer.Event("update_state", f"Dice rolled: {dice1} + {dice2} = {dice_sum}")
        return dice_sum  # Now returns tuple with individual values and sum

    def _handle_roll_dice(self):
        """Handle dice rolling with updated rules"""
        player = self._gameboard.get_current_player()

        # 1. Handle post-jail movement
        if getattr(player, '_Player__ready_to_move_after_escape', False):
            dice1, dice2 = random.randint(1, 6), random.randint(1, 6)
            dice_sum = dice1 + dice2

            if getattr(player, '_Player__entered_via_doubles', False):
                player._Player__entered_via_doubles = False
                observer.Event("update_state", f"{player._Player__name} moves freely from jail")

            player.move(dice_sum)
            player._Player__ready_to_move_after_escape = False
            player._Player__should_move_next_turn = False

            position = player._Player__board_position
            square = self._gameboard.get_square(position)

            if square.name == "Go to Jail":
                player.go_to_jail()
                observer.Event("update_state", f"{player._Player__name} landed on Go to Jail!")
                return True
            elif position == 10:  # Just visiting jail
                observer.Event("update_state", f"{player._Player__name} is visiting Jail")
                return True

            rent = player.pay_rent(square, dice_sum)
            if player._Player__money < 0:
                player.declare_bankrupt()
            return True

        # 2. Handle jail turns
        if player._Player__in_jail:
            if self.__dice_rolled:
                observer.Event("update_state", f"{player._Player__name} already rolled this turn in jail")
                return False

            dice1, dice2 = random.randint(1, 6), random.randint(1, 6)
            self.__dice_rolled = True
            self.__roll_count += 1

            if dice1 == dice2:  # Doubles rolled
                player._Player__in_jail = False
                player._Player__turns_in_jail = 0
                player._Player__ready_to_move_after_escape = True
                observer.Event("update_state", f"{player._Player__name} rolled doubles! Escapes paying only $50")
                return True
            else:
                player._Player__turns_in_jail += 1
                if player._Player__turns_in_jail >= 3:
                    player._Player__money -= 50  # Additional $50 (total $100)
                    player._Player__in_jail = False
                    player._Player__turns_in_jail = 0
                    player._Player__ready_to_move_after_escape = True
                    observer.Event("update_state", f"{player._Player__name} paid $100 total to leave jail")
                    return True
                else:
                    observer.Event("update_state",
                                   f"{player._Player__name} stays in jail (attempt {player._Player__turns_in_jail}/3)")
                    return False

        # 3. Normal turn handling
        if self.__dice_rolled and player._Player__doubles_count == 0:
            observer.Event("update_state", "Already rolled this turn")
            return False

        dice1, dice2 = random.randint(1, 6), random.randint(1, 6)
        dice_sum = dice1 + dice2
        self.__dice_rolled = True
        self.__roll_count += 1

        observer.Event("update_state", f"{player._Player__name} rolled {dice1} + {dice2} = {dice_sum}")

        # Handle doubles
        if dice1 == dice2:
            player._Player__doubles_count += 1
            if player._Player__doubles_count == 3:
                player._Player__entered_via_doubles = True
                player.go_to_jail()
                player._Player__doubles_count = 0
                observer.Event("update_state", f"Three doubles! {player._Player__name} goes to jail (no fine)")
                return True
            else:
                observer.Event("update_state", f"Doubles! {player._Player__name} gets another roll!")
                self.__dice_rolled = False
        else:
            player._Player__doubles_count = 0

        # Move player
        player.move(dice_sum)
        position = player._Player__board_position
        square = self._gameboard.get_square(position)

        # Check special squares
        if square.name == "Go to Jail":
            player.go_to_jail()
            observer.Event("update_state", f"{player._Player__name} goes to jail!")
            return True

        # Handle property landing
        if hasattr(square, 'owner') and square.owner != player and not square.is_mortgaged:
            rent = player.pay_rent(square, dice_sum)
            if rent > 0:
                observer.Event("update_state", f"Paid ${rent} to {square.owner._Player__name}")

        if player._Player__money < 0:
            player.declare_bankrupt()

        return not (dice1 == dice2)

    def initiate_trade(self, player1, player2, offer, request):
        """Handle trade between two players"""
        if player1.trade(player2, offer, request):
            observer.Event("update_state",
                           f"Trade completed between {player1.name} and {player2.name}!")
            return True
        else:
            observer.Event("update_state", "Trade failed - invalid terms")
            return False

    def _end_player_turn(self, callback):
        """End the current player's turn"""

        if not self.__dice_rolled:
            # player must roll the dice first
            observer.Event("update_state", "Roll the dice first")
            return
        self.__dice_rolled = False
        self.__roll_count = 0
        player_name = self._gameboard.next_turn()
        observer.Event("update_state_box", str(self._gameboard))
        observer.Event("update_card", self._gameboard.get_current_player().position)
        callback()
        observer.Event("update_state", f"{player_name}'s turn")

        self._set_expected_val()

    def _buy_square(self, data):
        """try to buy the square the active player is currently on"""

        if (self.__roll_count == 0):
            observer.Event("update_state", "Roll the dice first")
            return
        player = self._gameboard.get_current_player()
        position = player.position
        square = self._gameboard.get_square(position)
        buy = player.buy_property(square)
        if buy:
            print(f"Square bought {square}")
            observer.Event("update_state", f"Square bought: {square}")
        else:
            observer.Event("update_state", f"Square not bought: {square}")

        observer.Event("update_state_box", str(self._gameboard))

    def _mortgage(self, data):
        """Player has indicated an interest in mortgaging a property
        return their choices as a list of names"""
        player = self._gameboard.get_current_player()
        deeds = player.properties
        # only return the deeds that can be mortgaged
        observer.Event("choice", [d.name for d in deeds if not d.is_mortgaged])
        observer.Event("update_state_box", str(self._gameboard))

    def _mortgage_specific(self, deed_name):
        """Mortgage a specific property"""
        player = self._gameboard.get_current_player()
        res = player.mortgage_property(deed_name)
        print(deed_name)
        if res:
            observer.Event("update_state", f"{deed_name} mortgaged")
        else:
            observer.Event("update_state", f"attempt to mortgage {deed_name} failed")

    def _unmortgage(self, data):
        """Player has indicated an interest in unmortgaging a property
            they must unmortgage in a FIFO order
        """
        player = self._gameboard.get_current_player()
        deed_name = player.unmortgage_property()
        if deed_name != "":
            observer.Event("update_state", f"Unmortgaged: {deed_name}")
            observer.Event("update_state_box", str(self._gameboard))

    def button_clicked(self, button):
        """Handle View button click events"""
        print(f"Button clicked: {button}")
        self._roll_action(None)

    def _roll_action(self, data):
        player = self._gameboard.get_current_player()

        if not self._handle_roll_dice():
            return

        square = self._gameboard.get_square(player.position)
        money = player.money

        msg = f"{player.name} landed on {square}."

        observer.Event("update_state", msg)
        observer.Event("update_state_box", str(self._gameboard))
        observer.Event("update_card", player.position)