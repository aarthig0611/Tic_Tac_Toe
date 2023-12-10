import os
import random

class TicTacToeGame:
    BOARD_SIZE = 5
    FILE_NAME = "tictactoe.txt"

    def __init__(self):
        self.is_new_game = True

    def clear_old_console_output(self):
        """
        clear the old console outputs to
        print upto date output and keep
        a clean game view.
        :return:
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def format_gameboard_view(self, board):
        for i in range(self.BOARD_SIZE):
            row_str = " | ".join(board[i])
            print(row_str)
            if i < self.BOARD_SIZE - 1:
                print("-" * (4 * self.BOARD_SIZE - 1))

    def print_game_board(self, board):
        if self.is_new_game:
            self.is_new_game = False
        else:
            self.clear_old_console_output()
            print("\nAI just made a move.\nYour turn\n")

        self.format_gameboard_view(board)

    def get_file_length(self, file_name):
        word_count = 0
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                data = file.read()
                lines = data.split()
                word_count = len(lines)
        else:
            print("File not found")
        return word_count

    def clean_file(self, file_to_clean):
        """
        When the game begins the text file storing
        game moves deletes moves from the previous
        game
        :return:
        """
        file_length = self.get_file_length(file_to_clean)
        if file_length > 0:
            with open(file_to_clean, "w") as moves_file:
                pass

    def store_move_in_file(self, move_value, move_type):
        """
        :param move_index:
        :param move_type:
        :return:
        store the move value X or O followed by the index
        of the position of the move. Example 2:X
        """
        move_value_and_type = f"{move_type}:{move_value}"
        file_length = self.get_file_length(self.FILE_NAME)
        try:
            with open(self.FILE_NAME, 'a') as file_name:
                if file_length > 0:
                    file_name.write(", ")
                file_name.write(move_value_and_type)
        except Exception as e:
            print("Error:", e)

    def who_will_go_first(self):
        return 'player' if random.randint(0, 1) == 0 else 'AI'

    def make_move(self, board, letter, move):
        row, col = move
        board[row][col] = letter

    def check_winner(self, board, mark):
        for i in range(self.BOARD_SIZE):
            if all(board[i][j] == mark for j in range(self.BOARD_SIZE)) or all(board[j][i] == mark for j in range(self.BOARD_SIZE)):
                return True
        if all(board[i][i] == mark for i in range(self.BOARD_SIZE)) or all(board[i][self.BOARD_SIZE - 1 - i] == mark for i in range(self.BOARD_SIZE)):
            return True
        return False

    def is_space_free(self, board, move):
        row, col = move
        return board[row][col] == ' '

    def player_move(self, board):
        while True:
            try:
                move = int(input('Enter your move (1-25): '))
                if 1 <= move <= self.BOARD_SIZE ** 2:
                    move_row = (move - 1) // self.BOARD_SIZE
                    move_col = (move - 1) % self.BOARD_SIZE
                    if self.is_space_free(board, (move_row, move_col)):
                        self.store_move_in_file(move, 'O')
                        return move_row, move_col
                    else:
                        print('That position has already been occupied!')
                else:
                    print(f'Please input a number within the range of 1 to {self.BOARD_SIZE ** 2}')
            except ValueError:
                print('Please enter a valid number!')

    def ai_move(self, board):
        while True:
            row = random.randint(0, self.BOARD_SIZE - 1)
            col = random.randint(0, self.BOARD_SIZE - 1)
            if self.is_space_free(board, (row, col)):
                self.get_AI_move_value(row, col)
                return row, col

    def get_AI_move_value(self, row_value, column_value):
        position = row_value * self.BOARD_SIZE + column_value + 1
        self.store_move_in_file(position, 'X')

    def is_board_full(self, board):
        return all(board[i][j] != ' ' for i in range(self.BOARD_SIZE) for j in range(self.BOARD_SIZE))

    def play_game(self):
        game = TicTacToeGame()
        board = [[' ' for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]

        while True:
            player = 'O'
            AI = 'X'
            turn = game.who_will_go_first()

            print("\nWelcome to the 5x5 Tic Tac Toe game!\n")
            print(f'The {turn} will go first.')

            while True:
                if turn == 'player':
                    game.print_game_board(board)
                    move_row, move_col = game.player_move(board)
                    game.make_move(board, player, (move_row, move_col))
                else:
                    move_row, move_col = game.ai_move(board)
                    game.make_move(board, AI, (move_row, move_col))

                game.print_game_board(board)

                if game.check_winner(board, player if turn == 'player' else AI):
                    print("Congratulations! You've won!" if turn == 'player' else "The AI has won!")
                    return
                elif game.is_board_full(board):
                    print('The game is a tie!')
                    return
                else:
                    turn = 'AI' if turn == 'player' else 'player'

if __name__ == "__main__":
    start_game = TicTacToeGame()
    start_game.clean_file(start_game.FILE_NAME)
    start_game.clear_old_console_output()
    start_game.play_game()