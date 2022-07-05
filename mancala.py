"""An implementation of the game mancala."""

from argparse import ArgumentParser
from cgi import print_arguments
#from ast import Store
#from importlib.metadata import distribution
#from tkinter.font import names
from blessed import Terminal
import sys
from time import sleep

#####
# Board setup
#####

TERM = Terminal()

NEUT = TERM.gray33      # 33% gray
P0DK = TERM.cyan4       # dark color for player 0
P0LT = TERM.cyan3       # light color for player 0
P1DK = TERM.violetred4  # dark color for player 1
P1LT = TERM.violetred1  # light color for player 1

# this template gets populated in Mancala.print_board
SLOT = "{:>2}"
TEMPLATE = f"""{TERM.home+TERM.clear}\
<SP>  {P0DK}\u2193  f  e  d  c  b  a  \u2190  <NAME0>
<SP> {P0LT}{SLOT} {SLOT} {SLOT} {SLOT} {SLOT} {SLOT} {SLOT}
<SP> {NEUT}------------------------
<SP> {P1LT}   {SLOT} {SLOT} {SLOT} {SLOT} {SLOT} {SLOT} {SLOT}
{P1DK}<NAME1>  \u2192  g  h  i  j  k  l  \u2191{TERM.normal}"""

PAUSE = 0.3             # used to help animate moves

PITS = "abcdef.ghijkl"  # helps convert between pit indexes and letters in UI
STORES = [6, 13]        # indexes of the stores

#####
# Helper function
#####

def get_move(game, player):
    """Get player's selection of a pit to play from.
    
    The player will select a letter corresponding to one of their pits. This
    function will translate their selection into an index of game.board. The
    function will ask repeatedly until the user provides valid input.
    
    Args:
        game (Mancala): the current game.
        player (int): index of the player (0 or 1).
    
    Returns:
        int: the pit selected by the user, expressed as an index of game.board.
    
    Side effects:
        Displays information in the terminal.
        May cause the program to exit.
    """
    while True:
        print()
        selection = (input(f"{game.names[player]}, select one of your pits that"
                          " is not empty (or enter q to quit): ")
                     .lower()
                     .strip())
        if selection == "q":
            sys.exit(0)
        try:
            if len(selection) != 1 or not selection.isalpha():
                raise ValueError("Please enter a single letter.")
            pit = PITS.find(selection)
            if pit == -1:
                raise ValueError("Please enter a letter corresponding to one of"
                                 " your non-empty pits.")
            game.validate_move(pit, player)
        except ValueError as e:
            print(e)
        else:
            return pit

######################################################################################################################
# Mancala class
#####

class Mancala:
    # replace this comment with your class docstring and implementations of the
    # __init__(), validate_move(), check_capture(), distribute_seeds(), and
    # play_round() methods
    def __init__(self, p0, p1, func0 = get_move, func1 = get_move):
        """This method initializes three attributes
        Args:
            p0 (str): the name of player 0
            p1 (str): the name of player 1
            func0(function): to call player 0's turn
            func1(function): to call player 1's turn

        Side effects:
            Calling the functions will leave the terminal changed
        
        """
        self.names = [p0, p1]
        self.turn_funcs = [func0, func1]
        self.board = []
        
    
    def validate_move(self, pit_index, p_index):
        """Determines if a player can play from a particular pit
        Args:
            pit_index (integer): The index of the player
            p_index (integer): The value of the player's index 0 or 1
        Raises: z
            ValueError: if specified index is a store
            ValueError: if the specified pit index does not belong to the player
            ValueError: if the specified pit has nothing in it
        Side Effects:
            The ValueErrors will print to the terminal
        """
        
        if pit_index in STORES:
            raise ValueError("Sorry, you can't select the store.")

        own_pit = self.is_own_pit(pit_index, p_index)
        if own_pit == False: 
            raise ValueError("Sorry, you don't control that pit")

        if self.board[pit_index] == 0:
            raise ValueError("Sorry that pit is empty")

    def check_capture(self, pit_index, p_index):
        """Determines whether a player has qualified to capture seeds and proceeds with capture if conditions is met 
        Args:
            pit_index (int): The index of the player
            p_index (int): The value of the player's index 0 or 1
        Side Effects:
                It prints to a message to the terminal which notifies that one player has captured the contents of the opponent's pits.
        """
        if self.is_own_pit(pit_index, p_index) and pit_index not in STORES and self.board[pit_index] ==1:
            if p_index == 0:
                p_store = STORES[0]               
            elif p_index ==1:
                p_store = STORES[1]
            index_opp = 12 - pit_index
            self.board[p_store] += self.board[pit_index] + self.board[index_opp]
            self.board[pit_index] = 0
            self.board[index_opp] = 0
            self.print_board()
            print(f"{p_index} captured the contents of pits {PITS} and {PITS}")

    def distribute_seeds(self, notempty_pit, p_index):
        """distributes seeds that were in a specified pit to the subsequent pits and the player's store
        Args:
            notempty_pit (int): index of a non-empty pit belonging to the player
            p_index (int): The value of the player's index 0 or 1
        Side Effects:
            It modifies attributes and displays information on the terminal
        Returns: 
            we return the index of the last pit into which seed was placed
        """
        captured = self.board[notempty_pit]
        self.board[notempty_pit] = 0
        self.print_board()
        while captured > 0: 
            notempty_pit = (notempty_pit + 1) % 14
            if notempty_pit != STORES[1 - p_index]:
                self.print_board()
                self.board[notempty_pit] += 1
                captured -= 1

        return notempty_pit

    
    def play_round(self): 
        """this method manages one round of game play
        Side Effects:
            this method will print who gets an extra turn to the terminal
        """
        self.board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self.print_board()
        p_index = 0
        while self.game_over() == False:
            notempty_pit = self.turn_funcs[p_index](self, p_index)
            distSeed = self.distribute_seeds(notempty_pit, p_index)
            self.check_capture(distSeed, p_index)
            

            if distSeed in STORES:
                print(f"s{self.names} gets an extra turn!")
            else:
                p_index = (1 - p_index)
        self.print_winner()



######################################################################################################################################################
            



    



        
        
    
    def game_over(self):
        """Determine whether a round is over.
        
        A round is considered over when one player's pits are all empty.
        
        Returns:
            bool: True if the game is over, otherwise False.
        """
        return sum(self.board[0:6]) == 0 or sum(self.board[7:13]) == 0
    
    def score(self, player):
        """Calculate a player's score.
        
        Args:
            player (int): player's index (0 or 1).
        
        Returns:
            int: the requested player's score.
        """
        start = 0 if player == 0 else 7
        end = start + 7
        return sum(self.board[start:end])
    
    def is_own_pit(self, pit, player):
        """Determine if pit belongs to player.
        
        Args:
            pit (int): index into self.board.
            player (int): player's index (0 or 1).
        
        Returns:
            bool: True if pit belongs to player.
        """
        first_pit = 0 if player == 0 else 7
        store = first_pit + 6
        return first_pit <= int(pit) <= store
    
    def play(self):
        """Manage game play.
        
        After each round, ask players if they would like to play again.
        
        Side effects:
            Displays information in the terminal.
            Calls methods that modify self.board.
        """
        with TERM.fullscreen():
            while True:
                try:
                    self.play_round()
                    if not self.play_again():
                        sys.exit(0)
                except SystemExit:
                    print("Thanks for playing!")
                    sleep(PAUSE*3)
                    raise
        
    def play_again(self):
        """Ask players if they would like to play another round.

        Returns:
            bool: True if players choose to keep playing, otherwise False.
        
        Side effects:
            Displays information in the terminal.
        """
        print()
        while True:
            response = (input("Would you like to play again (y/n)? ")
                        .strip()
                        .lower()[0])
            if response not in "ny":
                print("Please type 'y' or 'n'.")
                continue
            return response == "y"
    
    def print_board(self, pause=PAUSE):
        """Displays the board in the terminal and pauses momentarily.

        Args:
            pause (float, optional): duration to pause before allowing the
                program to continue. Expressed in seconds. Defaults to PAUSE.
        
        Side effects:
            Displays information in the terminal.
            Delays program execution for a brief amount of time.
        """
        template = (TEMPLATE
                    .replace("<NAME0>", self.names[0])
                    .replace("<NAME1>", self.names[1])
                    .replace("<SP>", " "*len(self.names[1])))
        print(template.format(*(self.board[6::-1]+self.board[7:])))
        sleep(pause)

    def print_winner(self):
        """Display information about the winner of a round.
        
        Side effects:
            Displays information in the terminal.
        """
        self.print_board()
        print()
        score0 = self.score(0)
        score1 = self.score(1)
        if score0 == score1:
            print("Tie game!")
        else:
            winner = 0 if score0 > score1 else 1
            winner_score = max(score0, score1)
            loser_score = min(score0, score1)
            print(f"{self.names[winner]} wins {winner_score} to {loser_score}.")


#####
# Code to run the program
#####

def parse_args(arglist):
    """Parse command-line arguments.
    
    Expect two required arguments (the names of two players).
    
    Returns:
        namespace: a namespace with two attributes: name0 and name1, both
        strings.
    """
    parser = ArgumentParser()
    parser.add_argument("name0", help="the first player's name")
    parser.add_argument("name1", help="the second player's name")
    return parser.parse_args(arglist)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    game = Mancala(args.name0, args.name1)
    game.play()