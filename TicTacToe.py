class TicTacToe:
    def __init__(self):
        """
        Initialize a TicTacToe game with an empty board, starting player 'X', and an empty list to store moves.
        """
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.moves = []
    
    def display_board(self):
        """
        Display the current state of the TicTacToe board.
        """
        for i in range(0, 9, 3):
            print(" | ".join(self.board[i:i+3]))
            if i < 6:
                print("-" * 9)
    
    def make_move(self, move):
        """
        Make a move on the TicTacToe board.

        Parameters:
        - move (int): The index where the current player wants to place their mark.

        Raises:
        - IndexError: If the move is outside the valid range [0, 8].
        """
        try:
            if self.board[move] == ' ':
                self.board[move] = self.current_player
                store = self.current_player+":"+str(move)
                self.moves.append(store)
                self.current_player = 'X' if self.current_player == 'O' else 'O'
            else:
                print("Invalid move. Cell already occupied")
        except IndexError:
            print("Invalid move. Please enter a number between 0 and 8")

    def save_moves_to_file(self, move):
        """
        Save the list of moves to a file named 'tictactoe.txt'
        """
        with open('tictactoe.txt', 'w') as f:
            f.write(' '.join(map(str, self.moves)))

    def is_winner(self, player):
        """
        Check if the specified player has won.

        Parameters:
        - player (str): The player to check for a win('X' or 'O').

        Returns:
        -bool: True if the player has won, False otherwise.
        """
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combination in winning_combinations:
            all_match = True
            for i in combination:
                if self.board[i] != player:
                    all_match = False
                    break
            if all_match:
                return True
        return False
        
    def is_board_full(self):
        """
        Check if the TicTacToe board is full (no empty spaces remaining).

        Returns:
        -bool: True if the board is full, False otherwise.
        """
        for i in self.board:
            if ' ' in i:
                return False
        return True
    
    def get_possible_moves(self):
        """
        Get a list of possible moves (indices of empty spaces) on the current board.

        Returns:
        -list: A list of possible moves.
        """
        possible_moves = []
        for i in range(9):
            if self.board[i] == ' ':
                possible_moves.append(i)
        return possible_moves
    
    def get_best_move(self):
        """
        Find the best move for the AI player ('O') using the minimax algorithm.

        Returns:
        -int: The index of the best move.
        """
        best_Score = float('-inf')
        best_move = None
        for move in self.get_possible_moves():
            self.board[move] = 'O'
            score = self.minimax(self.board, 0, False)
            self.board[move] = ' '
            if score > best_Score:
                best_Score = score
                best_move = move
        return best_move
    
    def minimax(self, board, depth, is_maximizing_player):
        """
        The minimax algorithm to determine the best move for the AI player ('O').

        Parameters:
        - board (list): The current state of the TicTacToe board.
        - depth (int): The depth of recursion in the minimax algorithm.
        - is_maximizing_player (bool): True if maximizing player, False if minimizing player.

        Returns:
        - int: The score associated with the current board state.
        """
        scores = {'X': -1, 'O': 1, 'tie': 0}

        # Check for terminal states
        if self.is_winner('X'):
            return scores['X']
        if self.is_winner('O'):
            return scores['O']
        if self.is_board_full():
            return scores['tie']
        
        if is_maximizing_player:
            # Maximizing player ('O')
            max_score = float('-inf')
            for move in self.get_possible_moves():
                board[move] = 'O'
                score = self.minimax(board, depth+1, False)
                board[move] = ' '
                max_score = max(score, max_score)
            return max_score
        
        else:
            # Minimizing player ('X')
            min_score = float('inf')
            for move in self.get_possible_moves():
                board[move] = 'X'
                score = self.minimax(board, depth+1, True)
                board[move] = ' '
                min_score = min(score, min_score)
            return min_score

    def play_game(self):
        """
        Play a complete TicTacToe game, alternating between player and AI moves.
        """
        while True:
            try:
                self.display_board()
                move = int(input("Enter value: (0-8): "))
                while move > 8:
                    move = int(input("Please enter a number between 0 and 8: "))
                while self.board[move] != ' ':
                    move = int(input("Invalid move. Cell already occupied. Please enter a number between 0 and 8: "))
                self.make_move(move)
                self.save_moves_to_file(move)

                if self.is_winner('X'):
                    self.display_board()
                    print('X wins!')
                    break
                if self.is_board_full():
                    self.display_board()
                    print("It's a tie!")
                    break
                if self.is_winner('O'):
                    self.display_board()
                    print('O wins!')
                    break
                
                best_move = self.get_best_move()
                self.make_move(best_move)
                self.save_moves_to_file(move)

                if self.is_winner('X'):
                    self.display_board()
                    print('X wins!')
                    break
                if self.is_board_full():
                    self.display_board()
                    print("It's a tie!")
                    break
                if self.is_winner('O'):
                    self.display_board()
                    print('O wins!')
                    break

            except ValueError:
                print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    game = TicTacToe()
    game.play_game()