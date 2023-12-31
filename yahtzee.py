#!/usr/bin/env python3

# GAME MODES:
# 1. Traditional: Players take turns and makes the optimal choice for the roll
# 2. Waterfall: Each player goes down the list one by one and attempts to score the best in each line
# 3. One Roll: Each turn you will only get one roll before scoring
#    win/lose decision based on which player scores the highest.  Number of wins matters, not score.
# 4. Head-2-Head: Each player goes down the list one by one but unlike Waterfall each line will be a
#                 competition where the player with more points scores the victory (unless tie)


from random import randint
import os


def main():
    """
    Simple dumb Yahtzee! game
    """

    os.system('cls' if os.name == 'nt' else 'clear')

    _display_title()

    game_type = ""
    while True:
        print("Choose type of game:\n")
        print("1) Traditional")
        print("2) Waterfall")
        print("3) One Roll")

        game_choice = int(input("\nChoice? ") or 1)

        if game_choice == 1 or game_choice == 2 or game_choice == 3:
            if game_choice == 1:
                game_type = "Traditional"
            elif game_choice == 2:
                game_type = "Top Down"
            elif game_choice == 3:
                game_type = "One Roll"

            break

    print(f"\nBeginning {game_type} game.")

    player1 = ScoreSheet()

    turn = 1
    die_hand = {"1": None, "2": None, "3": None, "4": None, "5": None}

    # Turns continue until win condition of full scorecard
    while True:
        roll = 1
        # Loop for each of 3 rolls
        for r in range(1, 4):
            print(f"\nTurn {turn} roll {roll}\n")

            # Populate the die hand with the die rolls
            die_hand = _roll(die_hand)

            # Display die roll to player
            print(f"    (1)         (2)         (3)         (4)         (5)")

            # Loop the 5 lines of the list containing the dice display
            for die_image_line in range(0, 5):
                # Loop through each die to display the correct image
                for die_number in range(1, 6):
                    # Will print out each display line on one line, at the end it'll conclude with a newline
                    if die_number < 5:
                        print(f"{_display_dice(die_hand[str(die_number)])[die_image_line]}", end=" ")
                    else:
                        print(f"{_display_dice(die_hand[str(die_number)])[die_image_line]}")

            # print(f"{_display_dice(die_hand['1'])[0]}  {_display_dice(die_hand['2'])[0]}  {_display_dice(die_hand['3'])[0]}  {_display_dice(die_hand['4'])[0]}  {_display_dice(die_hand['5'])[0]}")
            # print(f"{_display_dice(die_hand['1'])[1]}  {_display_dice(die_hand['2'])[1]}  {_display_dice(die_hand['3'])[1]}  {_display_dice(die_hand['4'])[1]}  {_display_dice(die_hand['5'])[1]}")
            # print(f"{_display_dice(die_hand['1'])[2]}  {_display_dice(die_hand['2'])[2]}  {_display_dice(die_hand['3'])[2]}  {_display_dice(die_hand['4'])[2]}  {_display_dice(die_hand['5'])[2]}")
            # print(f"{_display_dice(die_hand['1'])[3]}  {_display_dice(die_hand['2'])[3]}  {_display_dice(die_hand['3'])[3]}  {_display_dice(die_hand['4'])[3]}  {_display_dice(die_hand['5'])[3]}")
            # print(f"{_display_dice(die_hand['1'])[4]}  {_display_dice(die_hand['2'])[4]}  {_display_dice(die_hand['3'])[4]}  {_display_dice(die_hand['4'])[4]}  {_display_dice(die_hand['5'])[4]}")

            # One Roll game mode.  Just short circuit after the first roll
            if game_choice == 3:
                break

            if r < 3:
                player_hold = input("\nHold? ")

            # Remove die values that are not being held so they will be re-rolled
            # On last turn don't purge values from non-held dice
            if roll != 3:
                for d in range(1, 6):
                    if str(d) not in player_hold:
                        die_hand[str(d)] = None
            roll = roll + 1

        input("\nAny Key to Continue: ")

        player1.display_scoresheet()

        # Traditional game mode and One Roll game mode
        if game_choice == 1 or game_choice == 3:
            while True:
                field = input("\nWhich field? ")

                # If selected field not in range continue prompting player
                if field:
                    if 1 <= int(field) <= 13:
                        # If update operation failed continue prompting player
                        if player1.update_scoresheet(die_hand, field):
                            break
        # Waterfall Game Mode
        elif game_choice == 2:
            player1.update_scoresheet(die_hand, str(player1.get_next_available_field()))

        turn = turn + 1
        # Re-initialize die hand to get a fresh roll
        die_hand = {"1": None, "2": None, "3": None, "4": None, "5": None}

        # If section is completed calculate totals
        player1.validate_scoresheet()

        # Reset Yahtzee! Bonus cheat preventer
        player1.bonus_this_turn = True

        # End game scenario is when grand total has been calculated
        if player1.grand_total is not None:
            break
    print("\nGame Over!")

    print("\nFINAL SCORE")
    player1.display_scoresheet()


def _display_title():
    title_art = (
        ",   .     |    |                    |",
        "|   |,---.|---.|--- ,---,,---.,---. |",
        "`---',---||   ||     .-' |---'|---' |",
        "  |  `---^`   '`---''---'`---'`---' o",
        "  `                                 ",
    )

    for line in title_art:
        print(line)


def _display_dice(die_number):
    dice_art = {
        1: (
            "┌─────────┐",
            "│         │",
            "│    ●    │",
            "│         │",
            "└─────────┘",
        ),
        2: (
            "┌─────────┐",
            "│  ●      │",
            "│         │",
            "│      ●  │",
            "└─────────┘",
        ),
        3: (
            "┌─────────┐",
            "│  ●      │",
            "│    ●    │",
            "│      ●  │",
            "└─────────┘",
        ),
        4: (
            "┌─────────┐",
            "│  ●   ●  │",
            "│         │",
            "│  ●   ●  │",
            "└─────────┘",
        ),
        5: (
            "┌─────────┐",
            "│  ●   ●  │",
            "│    ●    │",
            "│  ●   ●  │",
            "└─────────┘",
        ),
        6: (
            "┌─────────┐",
            "│  ●   ●  │",
            "│  ●   ●  │",
            "│  ●   ●  │",
            "└─────────┘",
        ),
    }

    return dice_art[die_number]


def _roll(die_hand):
    """
    Perform one "roll".  Roll all 6 dies less any dies being held
    """
    for die, val in die_hand.items():
        if not val:
            die_hand[die] = _roll_die()

    return die_hand


def _roll_die():
    """
    Perform roll of one die and return result
    """
    return randint(1, 6)


class ScoreSheet:

    def __init__(self):
        """
        Initialize new score sheet to blank
        """
        self.ones = None
        self.twos = None
        self.threes = None
        self.fours = None
        self.fives = None
        self.sixes = None
        self.upper_subtotal = None
        self.upper_bonus = None
        self.upper_total = None

        self.three_of_kind = None
        self.four_of_kind = None
        self.full_house = None
        self.sm_straight = None
        self.lg_straight = None
        self.yahtzee = None
        self.chance = None
        self.yahtzee_bonus = 0
        self.lower_subtotal = None

        self.grand_total = None

        self.bonus_this_turn = True

    def display_scoresheet(self):
        score_sheet = (
            f"┌───────────────────────────────┐",
            f"│          SCORE SHEET          │",
            f"└───────────────────────────────┘",
            f"┌───────────────────────────────┐",
            f"│ Select │ UPPER SECTION │ Score│",
            f"│───────────────────────────────│",
            f"│  (1)   │ Ones          │ {self._padded_output(self.ones)} │",
            f"│  (2)   │ Twos          │ {self._padded_output(self.twos)} │",
            f"│  (3)   │ Threes        │ {self._padded_output(self.threes)} │",
            f"│  (4)   │ Fours         │ {self._padded_output(self.fours)} │",
            f"│  (5)   │ Fives         │ {self._padded_output(self.fives)} │",
            f"│  (6)   │ Sixes         │ {self._padded_output(self.sixes)} │",
            f"│───────────────────────────────│",
            f"│        │ TOTAL SCORE   │ {self._padded_output(self.upper_subtotal)} │",
            f"│        │ BONUS         │ {self._padded_output(self.upper_bonus)} │",
            f"│        │ TOTAL UPPER   │ {self._padded_output(self.upper_total)} │",
            f"│───────────────────────────────│",
            f"│        │ LOWER SECTION │      │",
            f"│───────────────────────────────│",
            f"│  (7)   │ 3 of a kind   │ {self._padded_output(self.three_of_kind)} │",
            f"│  (8)   │ 4 of a kind   │ {self._padded_output(self.four_of_kind)} │",
            f"│  (9)   │ Full House    │ {self._padded_output(self.full_house)} │",
            f"│  (10)  │ Sm. Straight  │ {self._padded_output(self.sm_straight)} │",
            f"│  (11)  │ Lg. Straight  │ {self._padded_output(self.lg_straight)} │",
            f"│  (12)  │ YAHTZEE!      │ {self._padded_output(self.yahtzee)} │",
            f"│  (13)  │ Chance        │ {self._padded_output(self.chance)} │",
            f"│        │ Yahtzee! Bonus│ {self._padded_output(self.yahtzee_bonus)} │",
            f"│───────────────────────────────│",
            f"│        │ TOTAL LOWER   │ {self._padded_output(self.lower_subtotal)} │",
            f"│        │ TOTAL UPPER   │ {self._padded_output(self.upper_total)} │",
            f"│        │ GRAND TOTAL   │ {self._padded_output(self.grand_total)} │",
            f"└───────────────────────────────┘",
        )

        for line in score_sheet:
            print(line)

    def get_next_available_field(self):
        next_available = 1
        ordered_fields = [self.ones, self.twos, self.threes, self.fours, self.fives, self.sixes, self.three_of_kind,
                          self.four_of_kind, self.full_house, self.sm_straight, self.lg_straight, self.yahtzee,
                          self.chance]
        for field in ordered_fields:
            if isinstance(field, int):
                # Field does exist so check the next
                next_available = next_available + 1

        return next_available

    def _padded_output(self, value, max_positions=4):

        num_spaces = max_positions - len(str(value))

        disp_string = str(value)
        for x in range(0, num_spaces):
            disp_string = disp_string + " "

        return disp_string

    def update_scoresheet(self, die_hand, field):
        """
        Perform validation and update scoresheet
        """
        # print(f"DEBUG - DIE HAND: {die_hand}")
        # print(f"DEBUG - FIELD: {field}")
        print("\n")
        if field == "1":
            # Check to ensure this field is empty
            if not isinstance(self.ones, int):
                self.ones = 0
                # Validate there are actually values in the dice
                if 1 in die_hand.values():
                    # Add all ones together
                    for key, val in die_hand.items():
                        if die_hand[key] == 1:
                            self.ones = self.ones + die_hand[key]
                print(f"Ones Updated ... {self.ones} points!")
                return True
            else:
                print("You already have ones")

        elif field == "2":
            # Check to ensure this field is empty
            if not isinstance(self.twos, int):
                self.twos = 0
                # Validate there are actually values in the dice
                if 2 in die_hand.values():
                    # Add all ones together
                    for key, val in die_hand.items():
                        if die_hand[key] == 2:
                            self.twos = self.twos + die_hand[key]
                print(f"Twos Updated ... {self.twos} points!")
                return True
            else:
                print("You already have twos")

        elif field == "3":
            # Check to ensure this field is empty
            if not isinstance(self.threes, int):
                self.threes = 0
                # Validate there are actually values in the dice
                if 3 in die_hand.values():
                    # Add all ones together
                    for key, val in die_hand.items():
                        if die_hand[key] == 3:
                            self.threes = self.threes + die_hand[key]
                print(f"Threes Updated ... {self.threes} points!")
                return True
            else:
                print("You already have threes")

        elif field == "4":
            # Check to ensure this field is empty
            if not isinstance(self.fours, int):
                self.fours = 0
                # Validate there are actually values in the dice
                if 4 in die_hand.values():
                    # Add all ones together
                    for key, val in die_hand.items():
                        if die_hand[key] == 4:
                            self.fours = self.fours + die_hand[key]
                print(f"Fours Updated ... {self.fours} points!")
                return True
            else:
                print("You already have fours")

        elif field == "5":
            # Check to ensure this field is empty
            if not isinstance(self.fives, int):
                self.fives = 0
                # Validate there are actually values in the dice
                if 5 in die_hand.values():
                    # Add all ones together
                    for key, val in die_hand.items():
                        if die_hand[key] == 5:
                            self.fives = self.fives + die_hand[key]
                print(f"Fives Updated ... {self.fives} points!")
                return True
            else:
                print("You already have fives")

        elif field == "6":
            # Check to ensure this field is empty
            if not isinstance(self.sixes, int):
                self.sixes = 0
                # Validate there are actually values in the dice
                if 6 in die_hand.values():
                    # Add all ones together
                    for key, val in die_hand.items():
                        if die_hand[key] == 6:
                            self.sixes = self.sixes + die_hand[key]
                print(f"Sixes Updated ... {self.sixes} points!")
                return True
            else:
                print("You already have sixes")

        elif field == "7":
            # Check to ensure this field is empty
            if not isinstance(self.three_of_kind, int):
                num_val = {
                    1: 0,
                    2: 0,
                    3: 0,
                    4: 0,
                    5: 0,
                    6: 0,
                }
                # Populate dict of values
                total_value = 0
                for key, val in die_hand.items():
                    num_val[val] = num_val[val] + val
                    total_value = total_value + val

                # Validate there are actually values in the dice
                self.three_of_kind = 0
                for key, val in num_val.items():
                    if val / key >= 3:
                        self.three_of_kind = total_value
                print(f"Three of a kind updated ... {self.three_of_kind} points!")
                return True
            else:
                print("You already have three of a kind")

        elif field == "8":
            # Check to ensure this field is empty
            if not isinstance(self.four_of_kind, int):
                num_val = {
                    1: 0,
                    2: 0,
                    3: 0,
                    4: 0,
                    5: 0,
                    6: 0,
                }
                # Populate dict of values
                total_value = 0
                for key, val in die_hand.items():
                    num_val[val] = num_val[val] + val
                    total_value = total_value + val

                # Validate there are actually values in the dice
                self.four_of_kind = 0
                for key, val in num_val.items():
                    if val / key >= 4:
                        self.four_of_kind = total_value
                print(f"Four of a kind updated ... {self.four_of_kind} points!")
                return True
            else:
                print("You already have four of a kind")

        elif field == "9":
            if not isinstance(self.full_house, int):
                num_val = {
                    1: 0,
                    2: 0,
                    3: 0,
                    4: 0,
                    5: 0,
                    6: 0,
                }
                # Populate dict of values
                for key, val in die_hand.items():
                    num_val[val] = num_val[val] + val

                # Validate there are actually values in the dice
                self.full_house = 0
                for key, val in num_val.items():
                    if val / key == 3:
                        for key, val in num_val.items():
                            if val / key == 2:
                                self.full_house = 25
                print(f"Full house updated ... {self.full_house} points!")
                return True
            else:
                print("You already have a full house")

        elif field == "10":
            if not isinstance(self.sm_straight, int):
                self.sm_straight = 0
                die_values = []
                for key, val in die_hand.items():
                    die_values.append(val)
                if self._has_sequence(sorted(die_values), 3):
                    self.sm_straight = 30
                print(f"Small straight updated ... {self.sm_straight} points!")
                return True
            else:
                print("You already have a small straight")

        elif field == "11":
            if not isinstance(self.lg_straight, int):
                self.lg_straight = 0
                die_values = []
                for key, val in die_hand.items():
                    die_values.append(val)
                if self._has_sequence(sorted(die_values), 4):
                    self.lg_straight = 40
                print(f"Large straight updated ... {self.lg_straight} points!")
                return True
            else:
                print("You already have a large straight")

        elif field == "12":
            if not isinstance(self.yahtzee, int):
                num_val = {
                    1: 0,
                    2: 0,
                    3: 0,
                    4: 0,
                    5: 0,
                    6: 0,
                }
                # Populate dict of values
                for key, val in die_hand.items():
                    num_val[val] = num_val[val] + val

                # Validate there are actually values in the dice
                self.yahtzee = 0
                for key, val in num_val.items():
                    if val / key >= 5:
                        self.yahtzee = 50
                print(f"Yahtzee! updated ... {self.yahtzee} points!")
                return True
            else:
                # If there is already a Yahtzee! then add a Yahtzee! Bonus
                # Will still return false because with a bonus you still need
                # to select another field to fill in.
                if self.bonus_this_turn:
                    self.yahtzee_bonus = self.yahtzee_bonus + 100
                    print(f"Another Yahtzee!11!  Yahtzee! Bonus: {self.yahtzee_bonus}")

                    # Set flag that Yahtzee! Bonus was awarded so player can't cheat
                    self.bonus_this_turn = False
                else:
                    print(f"Yahtzee! Bonus already awarded")

        elif field == "13":
            if not isinstance(self.chance, int):
                self.chance = 0
                for key, val in die_hand.items():
                    self.chance = self.chance + val

                print(f"Chance updated ... {self.chance} points!")
                return True
            else:
                print("You already have chance")
        return False

    def validate_scoresheet(self):
        # Check upper scorecard for completeness, if completed calculate total/bonus
        if not isinstance(self.upper_subtotal, int):
            if isinstance(self.ones, int) and isinstance(self.twos, int) and isinstance(self.threes,
                                                                                        int) and isinstance(self.fours,
                                                                                                            int) and isinstance(
                    self.fives, int) and isinstance(self.sixes, int):
                self.upper_subtotal = self.ones + self.twos + self.threes + self.fours + self.fives + self.sixes
                if self.upper_subtotal >= 63:
                    self.upper_bonus = 35
                else:
                    self.upper_bonus = 0

                self.upper_total = self.upper_subtotal + self.upper_bonus

                print(f"\nUpper Section Complete!")
                print(f"───────────────────────")
                print(f"Subtotal: {self.upper_subtotal}")
                if self.upper_bonus > 0:
                    print(f"You got a bonus.  Extra 35 points.")
                else:
                    print(f"No bonus.  Subtotal of upper section < 63")
                print(f"Upper Total: {self.upper_total}")

        # Check lower scorecard for completeness, if completed calculate total/bonus
        if not isinstance(self.lower_subtotal, int):
            if isinstance(self.three_of_kind, int) and isinstance(self.four_of_kind, int) and isinstance(
                    self.full_house, int) and isinstance(self.sm_straight, int) and isinstance(self.lg_straight,
                                                                                               int) and isinstance(
                    self.yahtzee, int) and isinstance(self.chance, int):
                self.lower_subtotal = self.three_of_kind + self.four_of_kind + self.full_house + self.sm_straight + self.lg_straight + self.yahtzee + self.chance

                print(f"\nLower Section Complete!")
                print(f"───────────────────────")
                print(f"Subtotal: {self.lower_subtotal}")

        # Check both section subtotals, if complete calculate grand total which ends the game
        if isinstance(self.upper_total, int) and isinstance(self.lower_subtotal, int):
            self.grand_total = self.upper_total + self.lower_subtotal

            print(f"\nGRAND TOTAL: {self.grand_total}")

    def _has_sequence(self, check_list, seq_length):
        return any(list(check_list[i:i + seq_length]) == list(range(check_list[i], check_list[i] + seq_length))
                   for i in range(len(check_list) - seq_length + 1))


if __name__ == '__main__':
    main()
