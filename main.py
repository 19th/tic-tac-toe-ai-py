def render(board):
    print("\n")
    print(" - " * 3)

    # if the board is empty, display the numbers 1-9 to help choose a move
    if all([spot == " " for spot in board]):
        board = list("123456789")

    for i in range(3):
        print(" | ".join(board[i*3:i*3+3]))
        print(" - " * 3)

def check_win(board, player):
    # check rows
    for row in range(3):
        if all([spot == player for spot in board[row*3:row*3+3]]):
            return True

    # check columns
    for col in range(3):
        if all([spot == player for spot in board[slice(col, len(board), 3)]]):
            return True

    # check diagonals
    if all([spot == player for spot in board[slice(0, len(board), 4)]]) or all([spot == player for spot in board[slice(2, len(board) - 2, 2)]]):
        return True

    return False

def check_draw(board):
    return all([spot != " " for row in board for spot in row])

def get_move(board, player):
    while True:
        try:
            move_index = int(input(f"Player {player} turn, enter (1-9): ")) - 1
            if move_index < 0 or move_index > 8:
                print("Invalid move. Please enter a number between 1 and 9.")
                continue
            if board[move_index] != " ":
                print("Spot already taken. Please choose another.")
            return move_index
        except ValueError:
            print("Invalid input. Please enter a number.")

def play_game():
    board = list(" " * 9)
    print(board)
    current_player = "X"
    
    print("Welcome to Tic-Tac-Toe!")
    print("Player 1 is X, Player 2 is O")

    while True:
        render(board)
        move_index = get_move(board, current_player)
        board[move_index] = current_player
        
        if check_win(board, current_player):
            render(board)
            print(f"Player {current_player} wins!")
            break

        if check_draw(board):
            render(board)
            print("It's a draw!")
            break

        current_player = "O" if current_player == "X" else "X"

play_game()
