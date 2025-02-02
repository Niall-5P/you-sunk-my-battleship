from random import randint

scores = {"computer": 0, "player": 0}


class Board:
    """
    Main board class. Sets board size, the number of ships,
    the player's name and the board type (player board or computer).
    
    Attributes:
        size (int): The dimension of the board (size x size).
        num_ships (int): The total number of ships to place.
        name (str): Name of the board owner (player or computer).
        type (str): 'player' or 'computer'.
        guesses (list): List of all guesses made on this board.
        ships (list): List of all ship locations.
        board (list of lists): 2D grid representing the board.
    """
    def __init__(self, size, num_ships, name, board_type):
        self.size = size
        self.board = [["." for _ in range(size)] for _ in range(size)]
        self.num_ships = num_ships
        self.name = name
        self.type = board_type
        self.guesses = []
        self.ships = []

    def print(self):
        """
        Print the current state of the board. 
        For a 'player' board, ships are visible with '@'.
        For a 'computer' board, ships remain '.' until hit.
        """
        print(f"\n{self.name}'s Board:")
        for row in self.board:
            print(" ".join(row))
        print()

    def guess(self, x, y):
        """
        Mark a guess on this board at coordinates (x, y).
        Returns:
            str: "Hit" if the guess hits a ship, otherwise "Miss".
        """
        self.guesses.append((x, y))
        if (x, y) in self.ships:
            self.board[x][y] = "*"
            return "Hit"
        else:
            # Mark the miss with 'x' only if it wasn't already a '*'
            # (it shouldn't be, but let's be explicit).
            self.board[x][y] = "x"
            return "Miss"

    def add_ship(self, x, y):
        """
        Place a new ship at (x, y) if there's capacity.
        For the player's board, mark it with '@'.
        """
        if len(self.ships) >= self.num_ships:
            print("Error: cannot add more ships!")
        else:
            self.ships.append((x, y))
            if self.type == "player":
                self.board[x][y] = "@"


def random_point(size):
    """
    Return a random integer between 0 and size-1 (inclusive).
    """
    return randint(0, size - 1)


def valid_coordinates(x, y, board):
    """
    Check if the given (x, y) is valid:
      - Within the board bounds
      - The cell is '.'
    """
    if 0 <= x < board.size and 0 <= y < board.size:
        return board.board[x][y] == "."
    return False


def populate_board(board):
    """
    Randomly place ships on the board until the required
    number of ships is reached.
    """
    while len(board.ships) < board.num_ships:
        x = random_point(board.size)
        y = random_point(board.size)
        if valid_coordinates(x, y, board):
            board.add_ship(x, y)


def can_still_guess(board):
    """
    Returns True if there is at least one '.' on the board,
    meaning there's a valid guess remaining.
    """
    for row in board.board:
        if "." in row:
            return True
    return False


def check_for_stalemate(player_board, computer_board):
    """
    If both boards have no '.' squares left,
    neither side can make a valid guess anymore.
    
    Decide the outcome by comparing scores:
      - If player score > computer score => player wins
      - If computer score > player score => computer wins
      - Otherwise, it's a tie
    
    Returns:
        bool: True if a stalemate was detected and handled,
              False otherwise.
    """
    player_can_guess = can_still_guess(player_board)
    computer_can_guess = can_still_guess(computer_board)

    # If neither side has valid squares left
    if (not player_can_guess) and (not computer_can_guess):
        print("\nNo more valid moves left on either board!")
        print("Final Scores -> Player: {}, Computer: {}".format(
            scores['player'], scores['computer']))

        if scores["player"] > scores["computer"]:
            print("Stalemate, but you have more hits! You are the winner!")
        elif scores["computer"] > scores["player"]:
            print("Stalemate, but the computer has more hits! Computer wins!")
        else:
            print("Stalemate, and it's a tie!")

        return True

    return False


def make_guess(board):
    """
    Make a random guess for the computer on the given board,
    ensuring it's a valid coordinate that hasn't been tried.
    If no valid coordinates remain, return "No Moves".
    """
    if not can_still_guess(board):
        # No valid coordinates left at all
        return "No Moves"

    x = random_point(board.size)
    y = random_point(board.size)
    while not valid_coordinates(x, y, board):
        x = random_point(board.size)
        y = random_point(board.size)
    return board.guess(x, y)


def get_user_guess(board):
    """
    Continuously prompt the user for valid integer coordinates (x, y)
    within the board until a valid guess is obtained.
    
    Returns:
        tuple: (x, y) as integers within the board's range 
               and not already guessed.
    """
    while True:
        try:
            x = int(input("Guess a row (0-based): "))
            y = int(input("Guess a column (0-based): "))
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            continue

        # Check if in range and not already guessed
        if x < 0 or x >= board.size or y < 0 or y >= board.size:
            print(f"Coordinates out of range (0-{board.size-1}). Try again.")
            continue

        if board.board[x][y] != ".":
            print("You've already guessed that location. Try again.")
            continue

        return x, y


def play_game(computer_board, player_board):
    """
    Main function to play the game until either side sinks
    all of the opponent's ships or until a stalemate is detected.
    """
    while (scores["computer"] < computer_board.num_ships and
           scores["player"] < player_board.num_ships):

        # Check if there's a stalemate before the player's turn
        if check_for_stalemate(player_board, computer_board):
            return  # End the game loop if stalemate was handled

        # Player's turn
        player_board.print()
        computer_board.print()
        print("Player's Turn:")
        x, y = get_user_guess(computer_board)
        result = computer_board.guess(x, y)
        print(f"You guessed ({x}, {y}) and it was a {result}!")
        if result == "Hit":
            scores["player"] += 1

        # Check if the player sank all computer's ships
        if scores["player"] == computer_board.num_ships:
            print("Congratulations! You sank all the computer's ships!")
            return

        # Check stalemate again before the computer's turn
        if check_for_stalemate(player_board, computer_board):
            return

        # Computer's turn
        print("\nComputer's Turn:")
        comp_result = make_guess(player_board)

        if comp_result == "No Moves":
            # The computer can't make a valid guess -> stalemate scenario
            if check_for_stalemate(player_board, computer_board):
                return
        else:
            print(f"Computer guessed and it was a {comp_result}")
            if comp_result == "Hit":
                scores["computer"] += 1

            # Check if the computer sank all player's ships
            if scores["computer"] == player_board.num_ships:
                print(f"Sorry, {player_board.name}, "
                      "the computer sank all of your ships!")
                return

        print(f"\nScores -> Player: {scores['player']}, "
              f"Computer: {scores['computer']}\n")
        print("-" * 40)


def get_player_name():
    """
    Continuously prompt the user for a non-empty name.
    
    Returns:
        str: The player's validated name.
    """
    while True:
        name = input("Please enter your name: \n").strip()
        if name:
            return name
        else:
            print("Name cannot be blank. Please try again.")


def new_game():
    """
    Initiates a new game, setting up the board and starting play.
    """
    size = 5
    num_ships = 4

    # Reset global scores
    scores["computer"] = 0
    scores["player"] = 0

    print("-" * 35)
    print(" Welcome to YOU SUNK MY BATTLESHIP!!")
    print(f" Board Size: {size}. Number of ships: {num_ships}")
    print(" Top left corner is row: 0, col: 0")
    print("-" * 35)

    player_name = get_player_name()
    print("-" * 35)

    # Create boards
    player_board = Board(size, num_ships, player_name, "player")
    computer_board = Board(size, num_ships, "Computer", "computer")

    # Populate boards with ships
    populate_board(player_board)
    populate_board(computer_board)

    # Start the game loop
    play_game(computer_board, player_board)


# Entry point
if __name__ == "__main__":
    new_game()
