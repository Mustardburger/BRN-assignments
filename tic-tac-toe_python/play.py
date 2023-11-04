import os
import numpy as np

class TicTacToe:

    def __init__(self, player_symbol, computer_symbol, board_size=3):
        self.board_size = board_size
        self.board = np.zeros(shape=(self.board_size, self.board_size))
        self.player_symbol = player_symbol
        self.computer_symbol = computer_symbol
        self.mapping = {
            1: self.player_symbol,
            0: ".",
            -1: self.computer_symbol
        }
        self.reverse_mapping = {
            self.player_symbol: 1,
            ".": 0,
            self.computer_symbol: -1
        }

    def check_legal(self, piece: str, loc: tuple):
        """
        Code to check whether the move is legal
        """
        # Convert
        piece = self.reverse_mapping[piece]

        # If the move is anything different from 1 and -1
        if piece != -1 and piece != 1: return False

        # If the loc is illegal
        row, col = loc
        try:
            row, col = int(row), int(col)
        except: return False
        if 0 > row or row > self.board_size - 1: return False
        if 0 > col or col > self.board_size - 1: return False

        # If the move is already occupied by a different piece
        if self.board[row, col] != 0: return False

        return True

    def make_move(self, piece: str, loc: tuple):
        """
        Make a move for a player
        """
        row, col = loc
        if not self.check_legal(piece, loc): return False
        self.board[int(row), int(col)] = self.reverse_mapping[piece]

    def avail_move(self):
        """
        Returns a list of (row, col) specifying valid moves for both players.
        More useful for computer agents
        """
        non_zero_coords = np.argwhere(self.board == 0)
        coord_tuples = [tuple(coord) for coord in non_zero_coords]
        return coord_tuples

    def check_win(self):
        """
        Check whether there is a player winning. If there is, return their piece. If not, return 0
        """
        sum_cols = np.sum(self.board, axis=0)
        sum_rows = np.sum(self.board, axis=1)
        sum_left_diag = np.sum(self.board.diagonal())
        sum_right_diag = np.sum(np.fliplr(self.board).diagonal())

        # Player 1 wins
        if np.any(sum_cols == self.board_size) or np.any(sum_rows == self.board_size) \
            or self.board_size == sum_left_diag or self.board_size == sum_right_diag: return 1
        
        # Player 2 wins
        if np.any(sum_cols == -self.board_size) or np.any(sum_rows == -self.board_size) \
            or -self.board_size == sum_left_diag or -self.board_size == sum_right_diag: return -1
        
        else: return 0

    def check_draw(self):
        """
        Returns True if the game ends in a draw. Return False otherwise
        """
        if np.any(self.board == 0): return False
        else:
            if self.check_win() != 0: return False
            else: return True

    def check_game_finished(self):
        """
        Check whether the game is done.
        Returns 1 or -1 if there is a winner, 0 if it's a draw, and 2 if the game has not finished
        """
        if self.check_draw(): return 0
        player = self.check_win()
        if player != 0: return player
        else: return 2

    def print_board(self):
        """
        Print the board to the terminal
        """
        print("Current board:\n")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

        # Map from the numerical table to the symbol table
        printable_board = [[self.mapping[self.board[i, j]] for j in range(self.board_size)] for i in range(self.board_size)]

        # Print the first row of the table
        inds = [str(i) for i in list(range(self.board_size))]
        inds = " ".join(inds)
        print(f"  {inds}")

        # Then print the table itself
        for r in range(self.board_size):
            row = " ".join(printable_board[r])
            print(f"{r} {row}")

        print()


class RandomComputer:

    def __init__(self, computer_symbol: str):
        """
        The computer agent. Only makes random moves have been initiated
        """
        self.computer_symbol = computer_symbol

    def make_moves(self, game: TicTacToe):
        """
        Given a list of available moves, make a random move
        """
        avail_moves = game.avail_move()
        ind = np.random.randint(len(avail_moves))
        move = avail_moves[ind]
        return move


class PlayTicTacToe:

    def __init__(self):

        # Get user's input
        self.player_symbol = input("X or O? ")
        while self.player_symbol != "X" and self.player_symbol != "O":
            self.player_symbol = input("Please enter again: X or O? ")

        # Assign accordingly which symbol is used in the game
        if self.player_symbol == "X": self.computer_symbol = "O"
        else: self.computer_symbol = "X"
        self.board_size = 3

        # Initiate the game
        self.game = TicTacToe(
            player_symbol=self.player_symbol, 
            computer_symbol=self.computer_symbol,
            board_size=self.board_size
        )
        self.history = []

        # Initiate computer agent
        self.computer = RandomComputer(computer_symbol=self.computer_symbol) 


    def play(self):
        """
        Main loop to play the game
        """
        # Main loop of the game. The game only ends when one of these conditions is satisfied
        game_round = 0

        while self.game.check_win() == 0 and not self.game.check_draw():

            # Set game round
            game_round += 1

            # Print round display
            print("#################################\n")
            print(f"############ Round {game_round} ############\n")
            print("#################################\n")

            # Print current board
            self.game.print_board()

            # Ask for a move, then check whether the move is valid
            print(f"Player {self.player_symbol} turn\n")
            confirm, row, col = "n", -1, -1
            while not self.game.check_legal(self.player_symbol, (row, col)) or confirm == "n": 

                # Get the input from the user
                row = input("What row? ")
                col = input("What col? ")
                confirm = input(f" Place {self.player_symbol} at row={row} and col={col} [y/n]? ")
                while confirm not in ["y", "n"]:
                    confirm = input(f" Enter again [y/n]? ")

                # If the player enters n, continue
                if confirm == "n":
                    print(f"Re-enter move to play...")
                    continue
                
                # If the move is invalid, continue
                if not self.game.check_legal(self.player_symbol, (row, col)):
                    print(f"Invalid value. Row and col should be between 0 and {self.board_size - 1} and should not occupy already placed squares")

            # After the move is valid, enter the move, then print the board
            self.game.make_move(piece=self.player_symbol, loc=(row, col))
            print(" Move placed!\n")
            self.game.print_board()

            # Check if the game is over
            result = self.game.check_game_finished()
            if result != 2: break                

            # If not, update board to computer to make a move
            computer_row, computer_col = self.computer.make_moves(self.game)
            self.game.make_move(piece=self.computer_symbol, loc=(computer_row, computer_col))
            print(" Computer move registered")
            self.game.print_board()

            # Check if the game is over one more time
            result = self.game.check_game_finished()
            if result != 2: break

        # Check result
        if result == 1:
            print("Player wins!")
        elif result == -1:
            print("Computer wins!")
        else:
            print("Game ends in a draw")


def main():

    # Initiate the main components of the game
    gameplay = PlayTicTacToe()
    gameplay.play()



if __name__ == "__main__":
    main()