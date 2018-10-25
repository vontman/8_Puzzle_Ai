from typing import List, Iterable

class PuzzleBoard:
    n: int
    arr: List[List[int]]
    def __init__(self, n: int) -> None:
        self.n = n
        self.arr = [[j for j in range(i, i + 3)] for i in range(0, 9, 3)]

def generate_random_puzzle_board(n: int) -> PuzzleBoard:
    from random import shuffle
    board: PuzzleBoard = PuzzleBoard(n)
    randomized_board_arr: List[int] = sum(board.arr, [])
    shuffle(randomized_board_arr)
    board.arr = [[randomized_board_arr[j] for j in range(i, i + 3)] for i in range(0, 9, 3)]
    return board

############################ Displaying the Board ############################
def _board_display_row(board: PuzzleBoard, row: int) -> str:
    if row == 0:
        return _board_display_top_row(board)
    if row == board.n:
        return _board_display_bottom_row(board)

    return _board_display_mid_row(board)

def _board_display_top_row(board: PuzzleBoard) -> str:
    return (
            "____" * board.n + "_\n" +
            "|   " * board.n + "|\n"
            )

def _board_display_mid_row(board: PuzzleBoard) -> str:
    return (
            "|___" * board.n + "|\n" +
            "|   " * board.n + "|\n"
            )

def _board_display_bottom_row(board: PuzzleBoard) -> str:
    return "|___" * board.n + "|\n"

def _board_display(board: PuzzleBoard, row: int) -> str:
    if row >= board.n:
        return _board_display_row(board, row)

    return _board_display_row(board, row) + ("| " + " | ".join(map(str, board.arr[row])) + " |\n" + _board_display(board, row + 1))


def board_display(board: PuzzleBoard) -> str:
    return _board_display(board, 0)

##############################################################################

board: PuzzleBoard = PuzzleBoard(3)
print(board_display(board))
print(board_display(generate_random_puzzle_board(3)))
print(board_display(generate_random_puzzle_board(3)))
print(board_display(generate_random_puzzle_board(3)))
print(board_display(generate_random_puzzle_board(3)))
