import time

from tabulate import tabulate

from chatgpt_player import get_gpt_move
from db import get_history, get_steps, save_game, save_step, update_game
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

def player_move(board, player, game_id):
    move_index = get_player_move(board, player)
    board[move_index] = player
    render(board)
    
    save_step(game_id, player, 0, move_index + 1)

    if check_win(board, player):
        update_game(game_id, player, True)
        print(f"Player {player} wins!")
        return True

    if check_draw(board):
        update_game(game_id, "draw", True)
        print("It's a draw!")
        return True

    return False

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
    game_id = save_game("player 1", "player 2", None)

    render(board)

    while True:
        is_finished = player_move(board, current_player, game_id)
        if is_finished:
            break

        current_player = "O" if current_player == "X" else "X"

def play_game_with_ai():
    board = list(" " * 9)

    print("Welcome to Tic-Tac-Toe!")
    print("Player is X, AI is O")
    game_id = save_game("player 1", "AI", None)

    current_player = "X"
    ai_player = "O"

    render(board)

    while True:
        is_finished = player_move(board, current_player, game_id)
        if is_finished:
            break

        time.sleep(1)
        print("AI move")
        move_index = get_ai_move(board, "O")
        board[move_index] = "O"
        render(board)
        save_step(game_id, "O", 0, move_index + 1)
        
        if check_win(board, ai_player):
            save_game("player", "AI", "AI")
            print(f"AI wins!")
            break

        if check_draw(board):
            save_game("player", "AI", "draw")
            print("It's a draw!")
            break
        time.sleep(1)

def play_game_with_chatgpt():
    board = list(" " * 9)

    print("Welcome to Tic-Tac-Toe!")
    game_id = save_game("player 1", "ChatGPT", None)

    render(board)

    current_player = "X"
    ai_player = "O"

    print(f"Player is {current_player}, AI is {ai_player}")

    while True:
        is_finished = player_move(board, current_player, game_id)
        if is_finished:
            break

        print("AI move")

        # Get the AI move from ChatGPT with 3 retries
        retry = 0
        while retry < 3:
            try:
                move_index = get_gpt_move(board, ai_player)
                if board[move_index] != " ":
                    print("Spot already taken. Please choose another.")
                    retry += 1
                    continue
            except Exception as e:
                print("Error requesting ChatGPT: ", e)
                print("Retrying...")
                retry += 1
                continue
            break
        else:
            print("Failed to get AI move. Exiting...")
            exit(1)
            break

        board[move_index] = "O"
        render(board)
        save_step(game_id, "O", 0, move_index + 1)
        
        if check_win(board, ai_player):
            save_game("player", "AI", "AI")
            print(f"AI wins!")
            break

        if check_draw(board):
            save_game("player", "AI", "draw")
            print("It's a draw!")
            break
        time.sleep(1)

def choose_side():
    side = input("Choose your side (X or O): ")
    if side not in ["X", "O"]:
        print("Invalid choice. Please choose X or O.")
        return choose_side()
    return side

def choose_game():
    game_id = input("Choose game (id): ")
    if not game_id.isdigit():
        print("Bad ID number")
        return choose_game()
    return game_id

def main():
    while True:
        print("\n======")
        mode = input("Choose a mode:\n1. Play with a friend\n2. Play with AI\n3. Play with ChatGPT\n4. Show history\n5. Show game steps\n6. Exit\n")
        match mode:
            case "1":
                play_with_friend()
            case "2":
                play_game_with_ai()
            case "3":
                play_game_with_chatgpt()
            case "4":
                print("Show history\n")
                print(tabulate(get_history(), headers=["Game #", "Player 1", "Player 2", "Winner", "Finished"], tablefmt='orgtbl'))
                        
            case "5":
                print("Show game steps")
                game_id = choose_game()
                steps = get_steps(game_id)
                board = list(" " * 9)
                print("\n")
                for step in steps:
                    print(f"Player: {step[2]}, Position: {step[4]}")
                    board[step[4] - 1] = step[2]
                    render(board)
                print("======")

            case "6":
                print("Exit")
                break
            case _:
                print("Invalid choice")
                

# if the script is run directly, call the main function, 
# otherwise, the functions will be imported into other scripts
if __name__ == "__main__":
    main()