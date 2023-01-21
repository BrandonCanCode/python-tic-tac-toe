import random
import time
SIZE = 3

# This class manages the game board as a 2D character array
class GameBoard:
    def __init__(self):
        self.new_board()

    def new_board(self):
        self.board = [
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
        ]

    def update_board(self, r, c, val):
        self.board[r][c] = val

    def __str__(self):
        out_str =  "           column\n"
        out_str += "row |    1    2    3\n"
        out_str += "----|-----------------\n"
                    
        for r in range(SIZE):
            out_str += f" {r+1}  |  "
            for c in range(SIZE):
                if self.board[r][c] == 'o':
                    out_str += " ⭕ "
                elif self.board[r][c] == 'x':
                    out_str += " ❌ "
                else:
                    out_str += "    "

                if c != 2:
                    out_str += "|"
            if r != 2:
                out_str += "\n    |  ----+----+----\n"
        return out_str + '\n'


# Must pass the 2D board as the argument
def check_win_lose(board):
    # Check rows
    for row in board:
        if all(cell == 'x' for cell in row):
            return 'x'
        elif all(cell == 'o' for cell in row):
            return 'o'

    # Check columns
    for col in zip(*board):
        if all(cell == 'x' for cell in col):
            return 'x'
        elif all(cell == 'o' for cell in col):
            return 'o'

    # Check diagonals
    diag1 = [board[i][i] for i in range(SIZE)]
    diag2 = [board[i][2-i] for i in range(SIZE)]
    if all(cell == 'x' for cell in diag1) or all(cell == 'c' for cell in diag2):
        return 'x'
    elif all(cell == 'o' for cell in diag1) or all(cell == 'o' for cell in diag2):
        return 'o'

    # Check for empty slots
    for row in board:
        for cell in row:
            if cell == '':
                return
    # Assume board is full
    return 'Tie'


# Gets user input and validates it for correctness
def get_input(board):
    is_valid = False
    user_input = ""

    # Run loop until input is valid or until user quits
    while is_valid == False:
        user_input = input(
            "Your move. Input coordinates 'row, col' e.g. '1 3': ")

        # Quit condition
        if any(x in user_input for x in ('q', 'quit')):
            quit(0)

        values = user_input.split()
        try:
            r = int(values[0])
            c = int(values[1])

            if 0 < r <= SIZE and 0 < c <= SIZE:
                if board[r-1][c-1] != '':
                    print("This location is already marked...")
                else:
                    is_valid = True
            else:
                print("Input not within the range (1-3)!")
        except:
            print("Invalid input...")

    return r-1, c-1


# AI player algorithm
def minimax(board, depth, isMaximizing):
    result = check_win_lose(board)
    if result == "x":
        return 1
    elif result == "o":
        return -1
    elif result == "Tie":
        return 0

    bestMove = (-1, -1, '')
    bestScore = -float('inf')
    bestMoves = []
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == '':
                board[i][j] = ('x' if isMaximizing else 'o')
                score = minimax(board, depth+1, isMaximizing)
                board[i][j] = ''
                if isinstance(score, int) == False:
                    return score
                elif score == bestScore:
                    bestMoves.append((i, j))
                elif score > bestScore:
                    bestScore = score
                    bestMoves = [(i, j)]
    if len(bestMoves) > 0:
        # Add randomness by randomly choosing among the best moves
        randomMove = random.choice(bestMoves)
        bestMove = (randomMove[0], randomMove[1],
                    ('x' if isMaximizing else 'o'))
        board[randomMove[0]][randomMove[1]] = ('x' if isMaximizing else 'o')
        return bestMove



# Welcome message
print('''
<>=====================================<>
    Welcome to Brandon's Tic-Tac-Toe!
    
    Input coordinates to make a move
    like '1 2' where 1 is the first
    row and 2 is the second column
    starting from top-left corner.

    Coordinates range from 1 to 3

    Input q to quit  
<>=====================================<>
''')

# Game variables and setup
is_quit = False
user_turn = True
user_icon = 'x'
AI_icon = 'o'
game_board = GameBoard()
print(game_board)

# Game Loop
while is_quit == False:
    
    #Get user input for user's turn
    if user_turn:
        user_in = get_input(game_board.board)
        game_board.update_board(*user_in, user_icon)
        user_turn = False
    #Get AI input for AI's turn
    else:
        AI_is_x = (True if AI_icon == 'x' else False)
        AI_in = minimax(game_board.board, 0, AI_is_x)
        
        # Validate AI output
        if isinstance(AI_in, int):
            print('AI broke! Restart application.')
            quit(1)
        
        time.sleep(0.5)
        game_board.update_board(*AI_in)
        user_turn = True
        print("AI Turn Over:")
    print(game_board)

    # Check win and lose conditions
    result = check_win_lose(game_board.board)
    if result != None:
        if (result == 'Tie'):
            print("Tie! Game over!")
        elif result == 'x':
            print("X wins!")
        elif result == 'o':
            print("o wins!")

        # Game is over, create a new board for new game
        print("Play again(Y/n)?")
        again = input("> ")
        if again == 'n' or again == 'N':
            is_quit = True
        else:
            print("New game!")
            game_board.new_board()
            print(game_board)
            if user_turn:
                user_icon = 'x'
                AI_icon = 'o'
                print("You are ❌")
            else:
                user_icon = 'o'
                AI_icon = 'x'
                print("You are ⭕")

print("Program exiting...")