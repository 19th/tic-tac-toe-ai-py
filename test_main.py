import pytest
from main import check_draw, check_win

def test_win_rows():
    possible_wins = [
        ["X", "X", "X", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", "X", "X", "X", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", "X", "X", "X"],
    ]
    for board in possible_wins:
        assert check_win(board, "X") == True
        assert check_win(board, "O") == False

def test_not_win_rows():
    possible_not_wins = [
        ["X", "X", "O", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", "X", "O", "X", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", "O", "X", "X"],
    ]
    for board in possible_not_wins:
        assert check_win(board, "X") == False
        assert check_win(board, "O") == False

def test_win_columns():
    possible_wins = [
        ["X", " ", " ", "X", " ", " ", "X", " ", " "],
        [" ", "X", " ", " ", "X", " ", " ", "X", " "],
        [" ", " ", "X", " ", " ", "X", " ", " ", "X"],
    ]
    for board in possible_wins:
        assert check_win(board, "X") == True
        assert check_win(board, "O") == False

def test_not_win_columns():
    possible_not_wins = [
        ["X", " ", " ", " ", " ", " ", "X", " ", " "],
        [" ", "X", " ", " ", "O", " ", " ", "X", " "],
        [" ", " ", "X", " ", " ", "O", " ", " ", "X"],
    ]
    for board in possible_not_wins:
        assert check_win(board, "X") == False
        assert check_win(board, "O") == False

def test_win_diagonals():
    possible_wins = [
        ["X", " ", " ", " ", "X", " ", " ", " ", "X"],
        [" ", " ", "X", " ", "X", " ", "X", " ", " "],
    ]
    for board in possible_wins:
        assert check_win(board, "X") == True
        assert check_win(board, "O") == False

    possible_wins = [
        ["O", " ", " ", " ", "O", " ", " ", " ", "O"],
        [" ", " ", "O", " ", "O", " ", "O", " ", " "],
    ]
    for board in possible_wins:
        assert check_win(board, "O") == True
        assert check_win(board, "X") == False

def test_draw():
    board = ["X", "O", "X", "O", "X", "O", "O", "X", "O" ]
    assert(check_draw(board)) == True


    board = ["X", "O", "X", "O", "X", "O", "O", "X", " "]
    assert(check_draw(board)) == False

