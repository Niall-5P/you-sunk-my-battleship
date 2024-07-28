from random import randint

scores = {"computer": 0, "player": 0}


class Board:
    """
    Main board class. Sets board size, the number of ships,
    the player's name and the board type (player board or computer)
    Has methods for adding ships and guesses and printing the board
    """
    def __init__(self, size, num_ships, name, type):
        self.size = size
        self.board = [["." for x in range(size)] for y in range(size)]
        self.num_ships = num_ships
        self.name = name
        self.type = type
        self.guesses = []
        self.ships = []

    def print(self):
        for row in self.board:
            print(" ".join(row))

    def guess(self, x, y):
        self.guesses.append((x, y))
        self.board[x][y] = "x"

        if (x, y) in self.ships:
            self.board[x][y] = "*"
            return "Hit"
        else:
            return "Miss"

    def add_ship(self, x, y, type="computer"):
        if len(self.ships) >= self.num_ships:
            print("Error: you cannot add any more ships!")
        else:
            self.ships.append((x, y))
            if self.type == "player":
                self.board[x][y] = "@"


def random_point(size):
    """
    Helper function to return a random integer between 0 and size
    """
    return randint(0, size - 1)


def valid_coordinates(x, y, board):
    """
    Helper function to check if the coordinates are valid (i.e., within the board and not already taken).
    """
    return 0 <= x < board.size and 0 <= y < board.size and board.board[x][y] == "."


def populate_board(board):
    """
    Function to randomly place ships on the board.
    """
    while len(board.ships) < board.num_ships:
        x, y = random_point(board.size), random_point(board.size)
        if valid_coordinates(x, y, board):
            board.add_ship(x, y, board.type)


def make_guess(board):
    """
    Function to make a guess on the board.
    """
    x, y = random_point(board.size), random_point(board.size)
    while not valid_coordinates(x, y, board):
        x, y = random_point(board.size), random_point(board.size)
    return board.guess(x, y)


def play_game(computer_board, player_board):
    """
    Main function to play the game.
    """
    while scores["computer"] < computer_board.num_ships and scores["player"] < player_board.num_ships:
        player_board.print()
        computer_board.print()
        
        x, y = int(input("Guess a row: ")), int(input("Guess a column: "))
        result = computer_board.guess(x, y)
        print(f"Player guessed ({x}, {y}) and it was a {result}")

        if result == "Hit":
            scores["player"] += 1

        comp_result = make_guess(player_board)
        print(f"Computer guessed and it was a {comp_result}")

        if comp_result == "Hit":
            scores["computer"] += 1
        
        print(f"Scores - Player: {scores['player']}, Computer: {scores['computer']}")


def new_game():
    """
    Starts a new game. Sets the board size and number of ships, resets the scores and initialises the boards.
    """
    size = 5
    num_ships = 4
    scores["computer"] = 0
    scores["player"] = 0
    print("-" * 35)
    print(" Welcome to YOU SUNK MY BATTLESHIP!!")
    print(f" Board Size: {size}. Number of ships: {num_ships}")
    print(" Top left corner is row: 0, col: 0")
    print("-" * 35)
    player_name = input("Please enter your name: \n")
    print("-" * 35)
    player_board = Board(size, num_ships, player_name, "player")
    computer_board = Board(size, num_ships, "Computer", "computer")
    populate_board(player_board)
    populate_board(computer_board)
    play_game(computer_board, player_board)
new_game()