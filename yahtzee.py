#!/usr/bin/env python3

# GAME MODES:
# 1. Traditional: Players take turns and makes the optimal choice for the roll
# 2. Waterfall: Each player goes down the list one by one and attempts to score the best in each line
# 3. Head-2-Head: Each player goes down the list one by one but unlike Waterfall each line will be a
#                 competition where the player with more points scores the victory (unless tie)
# 4. One Roll: Each turn you will only get one roll before scoring
#    win/lose decision based on which player scores the highest.  Number of wins matters, not score.

from random import randint


def main():
    """
    Simple dumb Yahtzee! game
    """
    game_type = ""
    while True:
        print("\nWELCOME TO YAHTZEE!\n")

        print("Choose type of game:")
        print("1) Traditional")
        print("2) Top Down")
        print("3) Head-2-Head")
        print("4) One Roll")

        game_choice = int(input("\nChoice? ") or 1)

        if game_choice == 1 or game_choice == 2 or game_choice == 3 or game_choice == 4:
            if game_choice == 1:
                game_type = "Traditional"
            elif game_choice == 2:
                game_type = "Top Down"
            elif game_choice == 3:
                game_type = "Head-2-Head"
            elif game_choice == 4:
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
            for die, val in die_hand.items():
                print(f"{die}) {val}")

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

        while True:
            field = input("\nWhich field? ")

            # If selected field not in range continue prompting player
            if field:
                if 1 <= int(field) <= 13:
                    # If update operation failed continue prompting player
                    if player1.update_scoresheet(die_hand, field):
                        break

        turn = turn + 1

        player1.grand_total = 0
        if player1.grand_total is not None:
            break
    print("\nGame Over!")


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
        self.yahtzee_bonus = None
        self.lower_subtotal = None

        self.grand_total = None

    def display_scoresheet(self):
        """
        Display the current scoresheet details to stdout
        """
        print("~~SCORE SHEET~~")
        print("\nUpper\n")
        print(f"1) ONES: {self.ones}")
        print(f"2) TWOS: {self.twos}")
        print(f"3) THREES: {self.threes}")
        print(f"4) FOURS: {self.fours}")
        print(f"5) FIVES: {self.fives}")
        print(f"6) SIXES: {self.sixes}")
        print(f"\nUPPER SUBTOTAL: {self.upper_subtotal}")
        print(f"BONUS: {self.upper_bonus}")
        print(f"UPPER_TOTAL: {self.upper_total}")

        print("\nLower\n")
        print(f"7) Three of a kind: {self.three_of_kind}")
        print(f"8) Four of a kind: {self.four_of_kind}")
        print(f"9) Full House: {self.full_house}")
        print(f"10) Small Straight: {self.sm_straight}")
        print(f"11) Large Straight: {self.lg_straight}")
        print(f"12) Yahtzee!: {self.yahtzee}")
        print(f"Yahtzee! Bonus: {self.yahtzee_bonus}")
        print(f"\nLOWER SUBTOTAL: {self.lower_subtotal}")
        print(f"\nGRAND TOTAL: {self.grand_total}")

    def update_scoresheet(self, die_hand, field):
        """
        Perform validation and update scoresheet
        """
        print(f"DEBUG - DIE HAND: {die_hand}")
        print(f"DEBUG - FIELD: {field}")

        if field == "1":
            # Check to ensure this field is empty
            if not self.ones:
                # Validate there are actually values in the dice
                if 1 in die_hand.values():
                    # Add all ones together
                    self.ones = 0
                    for key, val in die_hand.items():
                        if die_hand[key] == 1:
                            self.ones = self.ones + die_hand[key]
                    print(f"Ones Updated ... {self.ones} points!")
                    return True
                else:
                    print("No ones found in hand")
            else:
                print("Field already filled")

        elif field == "2":
            # Check to ensure this field is empty
            if not self.twos:
                # Validate there are actually values in the dice
                if 2 in die_hand.values():
                    # Add all ones together
                    self.twos = 0
                    for key, val in die_hand.items():
                        if die_hand[key] == 2:
                            self.twos = self.twos + die_hand[key]
                    print(f"Twos Updated ... {self.twos} points!")
                    return True
                else:
                    print("No twos found in hand")
            else:
                print("Field already filled")

        elif field == "3":
            # Check to ensure this field is empty
            if not self.threes:
                # Validate there are actually values in the dice
                if 3 in die_hand.values():
                    # Add all ones together
                    self.threes = 0
                    for key, val in die_hand.items():
                        if die_hand[key] == 3:
                            self.threes = self.threes + die_hand[key]
                    print(f"Threes Updated ... {self.threes} points!")
                    return True
                else:
                    print("No threes found in hand")
            else:
                print("Field already filled")

        elif field == "4":
            # Check to ensure this field is empty
            if not self.fours:
                # Validate there are actually values in the dice
                if 4 in die_hand.values():
                    # Add all ones together
                    self.fours = 0
                    for key, val in die_hand.items():
                        if die_hand[key] == 4:
                            self.fours = self.fours + die_hand[key]
                    print(f"Fours Updated ... {self.fours} points!")
                    return True
                else:
                    print("No fours found in hand")
            else:
                print("Field already filled")

        elif field == "5":
            # Check to ensure this field is empty
            if not self.fives:
                # Validate there are actually values in the dice
                if 5 in die_hand.values():
                    # Add all ones together
                    self.fives = 0
                    for key, val in die_hand.items():
                        if die_hand[key] == 5:
                            self.fives = self.fives + die_hand[key]
                    print(f"Fives Updated ... {self.fives} points!")
                    return True
                else:
                    print("No fives found in hand")
            else:
                print("Field already filled")

        elif field == "6":
            # Check to ensure this field is empty
            if not self.sixes:
                # Validate there are actually values in the dice
                if 6 in die_hand.values():
                    # Add all ones together
                    self.sixes = 0
                    for key, val in die_hand.items():
                        if die_hand[key] == 6:
                            self.sixes = self.sixes + die_hand[key]
                    print(f"Sixes Updated ... {self.sixes} points!")
                    return True
                else:
                    print("No sixes found in hand")
            else:
                print("Field already filled")

        elif field == "7":
            print("Three of a kind!")

        elif field == "8":
            print("Four of a kind!")

        elif field == "9":
            print("Full House!")

        elif field == "10":
            print("Small Straight")

        elif field == "11":
            print("Large Straight")

        elif field == "12":
            print("Yahtzee!")

        return False
        # Check upper scorecard for completeness, if completed calculate total/bonus

        # Check lower scorecard for completeness, if completed calculate total/bonus


if __name__ == '__main__':
    main()
