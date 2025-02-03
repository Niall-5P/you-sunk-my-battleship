from random import randint

# Global scores
scores = {"computer": 0, "player": 0}


class Board:
    """
    Represents a Battleship board of given size and number of ships.
    Ships are tracked in self.ships (as a list of (x, y) tuples).
    The board grid (self.board) starts with '.', and guesses become 'x' or '*'.
    """
    def __init__(self, size, num_ships, name):
        self.size = size
        self.num_ships = num_ships
        self.name = name
        # The visible board: '.' = unguessed, 'x' = miss, '*' = hit
        self.board = [["." for _ in range(size)] for _ in range(size)]
        self.ships = []     # list of (x, y) ship positions
        self.guesses = []   # list of (x, y) guesses made on this board

    def print_board(self):
        """Print the current board state to the console."""
        print(f"\n{self.name}'s Board:")
        for row in self.board:
            print(" ".join(row))
        print()

    def add_ship(self, x, y):
        """Add a ship at (x, y)."""
        if len(self.ships) < self.num_ships:
            self.ships.append((x, y))

    def guess(self, x, y):
        """
        Process a guess at (x, y). 
        Returns "Hit" or "Miss".
        """
        self.guesses.append((x, y))

        if (x, y) in self.ships:
            self.board[x][y] = "*"
            return "Hit"
        else:
            self.board[x][y] = "x"
            return "Miss"


def random_coord(size):
    """Return a random coordinate within 0..size-1."""
    return randint(0, size - 1)


def valid_guess(x, y, board):
    """
    A guess is valid if:
      - It's inside the board
      - The cell isn't already guessed ('x' or '*')
    """
    if 0 <= x < board.size and 0 <= y < board.size:
        return board.board[x][y] == "."
    return False


def populate_board(board):
    """
    Randomly place ships on the board (board.ships)
    until we have num_ships ships.
    We do NOT mark them visually so the computer can guess them!
    """
    while len(board.ships) < board.num_ships:
        x = random_coord(board.size)
        y = random_coord(board.size)
        # Check that we haven't placed a ship here already
        if (x, y) not in board.ships:
            board.add_ship(x, y)


def make_guess(board):
    """
    The computer picks random coords until it finds
    a valid cell to guess ('.'). Returns "Hit" or "Miss".
    """
    while True:
        x = random_coord(board.size)
        y = random_coord(board.size)
        if valid_guess(x, y, board):
            return board.guess(x, y)


def get_user_guess(board):
    """
    Repeatedly prompt for row/column input until we get a valid guess.
    Returns (x, y) as integers.
    """
    while True:
        try:
            x = int(input("Guess a row (0-based): "))
            y = int(input("Guess a column (0-based): "))
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            continue

        if not valid_guess(x, y, board):
            print("That coordinate is either out of range or already guessed. Try again.")
            continue

        return x, y


def play_game(player_board, computer_board):
    """
    Main game loop: 
    - The user guesses on the computer's board.
    - The computer guesses on the player's board.
    - First to sink all opponent's ships (== num_ships hits) wins.
    """
    global scores

    while scores["player"] < computer_board.num_ships and scores["computer"] < player_board.num_ships:
        # Print boards (the player's board shows hits/misses, computer's board shows your guesses on it)
        player_board.print_board()
        computer_board.print_board()

        # Player turn
        print("Player's Turn:")
        x, y = get_user_guess(computer_board)
        result = computer_board.guess(x, y)
        print(f"You guessed ({x}, {y}) - {result}!")
        if result == "Hit":
            scores["player"] += 1
            if scores["player"] == computer_board.num_ships:
                print("Congratulations! You sank all the computer's ships!")
                break

        # Computer turn
        if scores["player"] < computer_board.num_ships:  # only if game not ended
            print("\nComputer's Turn:")
            comp_result = make_guess(player_board)
            print(f"Computer guessed and it was a {comp_result}")
            if comp_result == "Hit":
                scores["computer"] += 1
                if scores["computer"] == player_board.num_ships:
                    print(f"Sorry, {player_board.name}, the computer sank all your ships!")
                    break

        # Print scoreboard
        print(f"\nScores => Player: {scores['player']}, Computer: {scores['computer']}")
        print("-" * 40)


def get_player_name():
    """Prompt until user gives a non-empty name."""
    while True:
        name = input("Please enter your name: ").strip()
        if name:
            return name
        print("Name cannot be blank. Please try again.")


def new_game():
    """Set up and start a new game."""
    size = 5
    num_ships = 4

    # Reset global scores
    scores["player"] = 0
    scores["computer"] = 0

    print("-" * 35)
    print(" Welcome to YOU SUNK MY BATTLESHIP!! ")
    print(f" Board Size: {size}. Number of ships: {num_ships}")
    print(" Top-left corner is row: 0, col: 0")
    print("-" * 35)

    player_name = get_player_name()
    print("-" * 35)

    # Create boards
    player_board = Board(size, num_ships, player_name)
    computer_board = Board(size, num_ships, "Computer")

    # Randomly place ships on each board
    populate_board(player_board)
    populate_board(computer_board)

    # Start the game
    play_game(player_board, computer_board)


if __name__ == "__main__":
    new_game()
