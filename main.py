import time

time.sleep(3)

def render(board):
    print("\n")
    print(" - " * 3)

    # if the board is empty, display the numbers 1-9 to help choose a move
    if all([spot == " " for spot in board]):
        board = list("123456789")

    for i in range(3):
        print(" | ".join(board[i*3:i*3+3]))
        print(" - " * 3)

    print("\n")

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

def get_player_move(board, player):
    while True:
        try:
            move_index = int(input(f"Player {player} turn, enter (1-9): ")) - 1
            if move_index < 0 or move_index > 8:
                print("Invalid move. Please enter a number between 1 and 9.")
                continue
            if board[move_index] != " ":
                print("Spot already taken. Please choose another.")
                continue
            return move_index
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_ai_move(board, player):
    possible_win_board = board.copy()

    # check for center move
    if possible_win_board[4] == " ":
        return 4

    # check for winning move
    for i in range(9):
        if possible_win_board[i] == " ":
            possible_win_board[i] = player
            if check_win(possible_win_board, player):
                return i
            possible_win_board[i] = " "

    # check for blocking move
    opponent = "X" if player == "O" else "O"
    for i in range(9):
        if possible_win_board[i] == " ":
            possible_win_board[i] = opponent
            if check_win(possible_win_board, opponent):
                return i
            possible_win_board[i] = " "

    # check for corner move
    for i in [0, 2, 6, 8]:
        if board[i] == " ":
            return i

    # check for side move
    for i in [1, 3, 5, 7]:
        if board[i] == " ":
            return i

    return -1

def play_with_friend():
    board = list(" " * 9)
    current_player = "X"
    
    print("Welcome to Tic-Tac-Toe!")
    print("Player 1 is X, Player 2 is O")

    while True:
        render(board)
        move_index = get_player_move(board, current_player)
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

def play_game_with_ai():
    board = list(" " * 9)

    print("Welcome to Tic-Tac-Toe!")
    print("Player is X, AI is O")

    current_player = "X"
    ai_player = "O"

    while True:
        render(board)
        move_index = get_player_move(board, current_player)
        board[move_index] = current_player
        
        if check_win(board, current_player):
            render(board)
            print(f"Player {current_player} wins!")
            break

        if check_draw(board):
            render(board)
            print("It's a draw!")
            break

        render(board)
        time.sleep(1)
        print("AI move")
        move_index = get_ai_move(board, "O")
        board[move_index] = "O"
        
        if check_win(board, ai_player):
            render(board)
            print(f"AI wins!")
            break

        if check_draw(board):
            render(board)
            print("It's a draw!")
            break
        time.sleep(1)

def play_game_with_chatgpt():
    pass

def main():
    mode = input("Choose a mode:\n1. Play with a friend\n2. Play with AI\n3. Play with ChatGPT\n4. Show history\n5. Show game steps\n6. Exit\n")
    match mode:
        case "1":
            play_with_friend()
        case "2":
            play_game_with_ai()
        case "3":
            play_game_with_chatgpt()
        case "4":
            print("Show history")
        case "5":
            print("Show game steps")
        case "6":
            print("Exit")
        case _:
            print("Invalid choice. Exiting...")

# if the script is run directly, call the main function, 
# otherwise, the functions will be imported into other scripts
if __name__ == "__main__":
    main()