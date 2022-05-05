import time
import random

""" Remaining tasks:
    AI goes for easy win
    AI prevents easy lose
    Unbeatable AI
    """


class bcolors:
    USERX = "\033[95m"
    USER0 = "\033[94m"
    WINNERGREEN = "\033[92m"
    WRONG = "\033[93m"
    ENDC = "\033[0m"


# -----  constant global variables ----
current_player = "X"
max_turn = 9


def init_board():
    """Returns an empty 3-by-3 board (with .)."""
    board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
    return board


def want_quit(move):
    if move == "quit":
        exit()


def get_move(board, player):
    """Returns the coordinates of a valid move for player on board."""
    rows = {"A": 0, "B": 1, "C": 2}
    cols = {"1": 0, "2": 1, "3": 2}

    move = input("\nPlease give me a coordinate! ")
    want_quit(move)

    if len(move) == 2 and (move[0] in rows.keys() and move[1] in cols.keys()):
        row, col = rows[move[0]], cols[move[1]]
        if board[row][col] == ".":
            return (row, col)
        else:
            print(bcolors.WRONG + "This coordinate is already taken!" + bcolors.ENDC)
            return get_move(board, player)
    else:
        print(
            bcolors.WRONG
            + "Give me valid coordinate!!! Combine (A, B, C) with (1, 2, 3)"
            + bcolors.ENDC
        )
        return get_move(board, player)


def easy_win_row(board, player):
    row, col = "a", "a"
    for i in range(len(board)):
        if board[i].count(".") == 1 and (board[i].count(player) == 2):
            col = board[i].index(".")
            row = i
    return row, col


def easy_win_col(board, player):
    trans_board = [[], [], []]
    for i in range(len(trans_board)):
        for row in board:
            trans_board[i].append(row[i])

    row, col = easy_win_row(trans_board, player)
    board_col = row
    board_row = col
    return board_row, board_col


def easy_win_diagonal(board, player):
    a_diagonal = [[board[0][0], board[1][1], board[2][2]]]
    b_diagonal = [[board[0][2], board[1][1], board[2][0]]]
    row, col = easy_win_row(a_diagonal, player)
    board_row = board_col = col
    if board_col == "a":
        row, col = easy_win_row(b_diagonal, player)
        if col != "a":
            board_row = col
            board_col = 2 - col
    return board_row, board_col


def get_ai_move(board, player):
    """Returns the coordinates of a valid move for player on board."""
    flat_board = [item for sublist in board for item in sublist]

    if flat_board.count(".") == 9:
        row, col = 1, 1  # coord = 1, 1
    else:
        row, col = "a", "a"  # None

    easy_list = [easy_win_diagonal, easy_win_col, easy_win_row]
    for player_for in [player, current_user(player)]:  #!!!
        i = 0
        while (row, col) == ("a", "a") and i < 3:  # while coord is None and i < 3:
            row, col = easy_list[i](board, player_for)
            i += 1

    if (row, col) == ("a", "a"):
        row, col = random.randrange(3), random.randrange(3)

    if board[row][col] == ".":
        return (row, col)
    else:
        return get_ai_move(board, player)


def mark(board, current_player, row, col):
    """Marks the element at row & col on the board for player."""
    board[row][col] = current_player
    return board


def win_row(board):
    for row in board:
        if row[0] == row[1] == row[2] and "." not in row:
            return True
    return False


def win_col(board):
    board = [item for sublist in board for item in sublist]
    x = "X"
    o = "0"
    if board[0:7:3] == [x, x, x] or board[0:7:3] == [o, o, o]:
        return True
    elif board[1:8:3] == [x, x, x] or board[0:7:3] == [o, o, o]:
        return True
    elif board[2::3] == [x, x, x] or board[0:7:3] == [o, o, o]:
        return True
    else:
        return False


def win_diagonal(board, current_player):
    if (
        board[0][0] == current_player
        and board[1][1] == current_player
        and board[2][2] == current_player
    ):
        return True
    elif (
        board[0][2] == current_player
        and board[1][1] == current_player
        and board[2][0] == current_player
    ):
        return True
    else:
        return False


def has_won(board, current_player):
    """Returns True if player has won the game."""
    if win_row(board) or win_col(board) or win_diagonal(board, current_player):
        return True
    else:
        return False


def is_full(board):
    """Returns True if board is full."""
    flat_board = [item for sublist in board for item in sublist]
    return "." not in flat_board


def print_board(board, current_player):
    """Prints a 3-by-3 board on the screen with borders."""
    colored_board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
    for rowi in range(len(board)):
        for itemi in range(len(board[rowi])):
            if board[rowi][itemi] == "X":
                colored_board[rowi][itemi] = bcolors.USERX + "X" + bcolors.ENDC
            elif board[rowi][itemi] == "0":
                colored_board[rowi][itemi] = bcolors.USER0 + "0" + bcolors.ENDC

    print("  1   2   3")
    print(f"A {colored_board[0][0]} | {colored_board[0][1]} | {colored_board[0][2]}")
    print(" ---+---+---")
    print(f"B {colored_board[1][0]} | {colored_board[1][1]} | {colored_board[1][2]}")
    print(" ---+---+---")
    print(f"C {colored_board[2][0]} | {colored_board[2][1]} | {colored_board[2][2]}")


def print_result(winner):
    """Congratulates winner or proclaims tie (if winner equals zero)."""
    return print(f"{winner}")


def current_user(current_player):
    if current_player == "X":
        return "0"
    else:
        return "X"


def change_AI(is_AI):
    if is_AI:
        return False
    else:
        return True


def is_end(board, current_player, turn, winner):
    if is_full(board):
        winner = bcolors.WINNERGREEN + "It's a tie!" + bcolors.ENDC
        turn = max_turn
    if has_won(board, current_player):
        winner = bcolors.WINNERGREEN + "The winner is: " + current_player + bcolors.ENDC
        turn = max_turn
    return turn, winner


def step(board, current_player, turn, winner, is_AI):
    print_board(board, current_player)
    if is_AI:
        messageX = bcolors.USERX + "\nNow AI is thinking!" + bcolors.ENDC
        message0 = bcolors.USER0 + "\nNow AI is thinking!" + bcolors.ENDC
        message = messageX if current_player == "X" else message0
        # time.sleep(1)
        print(message)
        time.sleep(1)
        (row, col) = get_ai_move(board, current_player)
    else:
        (row, col) = get_move(board, current_player)
    board = mark(board, current_player, row, col)
    turn, winner = is_end(board, current_player, turn, winner)
    current_player = current_user(current_player)
    turn += 1
    time.sleep(1)

    return turn, winner, board, current_player


def tictactoe_game(mode, current_player):
    board = init_board()
    turn = 0
    winner = ""
    is_AI_start = {
        "HUMAN-HUMAN": False,
        "AI-HUMAN": True,
        "HUMAN-AI": False,
        "AI-AI": True,
    }
    is_AI = is_AI_start[mode]
    while turn < max_turn:
        messageX = bcolors.USERX + "\n  X's turn!" + bcolors.ENDC
        message0 = bcolors.USER0 + "\n  0's turn" + bcolors.ENDC
        message = messageX if current_player == "X" else message0
        print(message)
        turn, winner, board, current_player = step(
            board, current_player, turn, winner, is_AI
        )
        if mode == "AI-HUMAN" or mode == "HUMAN-AI":
            is_AI = change_AI(is_AI)

    print("\n")
    print_board(board, current_player)
    print_result(f"\n{winner}")
    if "tie" not in winner:
        if not is_AI:
            print(
                """
{\__/}
( ●_●) CONGRATULATION
( > 🍪 You won this cookie! \n"""
            )
        else:
            print(
                """
{\__/}
( ●_●) CONGRATULATION
( > ⚡ You won this energy! \n"""
            )
    else:
        print(
            """
{\__/}
( ●_●) NOT YET
( 🎁< Nobody won this gift yet! \n"""
        )


def main_menu():
    mode = input(
        "Please choose a game mode (1 = HUMAN-HUMAN, 2 = AI-HUMAN, 3 = HUMAN-AI, 4 = AI-AI): "
    )
    levels = {"1": "HUMAN-HUMAN", "2": "AI-HUMAN", "3": "HUMAN-AI", "4": "AI-AI"}

    try:
        mode = levels[mode]
        tictactoe_game(mode, current_player)
    except KeyError:
        print("The choosed mode is invalid!")
        return main_menu()


if __name__ == "__main__":
    main_menu()