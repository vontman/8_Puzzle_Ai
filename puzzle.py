from typing import List, Tuple, Iterable
from gamestate import GameState

N: int = 3

PuzzleBoard = Tuple[Tuple[int, ...], ...]
Move = Tuple[int, int, str]
State = Tuple[PuzzleBoard, str]

GOAL_STATE: GameState = GameState(board=((0, 1, 2), (3, 4, 5), (6, 7, 8)))

class InvalidPuzzleError(Exception):
    '''
    Error that indicated an invalid board.
    The error message includes the reason of invalidity and the invalid board.
    '''

    def __init__(self, msg: str, invalid_board: PuzzleBoard) -> None:
        super(InvalidPuzzleError, self).__init__(msg + "\nInvalid board: \n" +
                                                 display(invalid_board))

def is_valid(board: PuzzleBoard) -> Tuple[bool, str]:
    '''
    Checks that:
    - The board dimensions are N * N.
    - The board has unique values from 1 to N.
    - There is an empty space.
    '''
    if len(board) != N or len(board[0]) != N:
        return (False, "Invalid board dimensions")
    flattened_board: List[int] = [board[i // N][i % N] for i in range(N * N)]
    if not 0 in flattened_board:
        return (False, "Empty space not found in board.")
    if not all([i in flattened_board for i in range(1, N * N)]):
        return (False,
                "The board doesn't contain all elements from 1 to " + str(N))
    return (True, "")


def generate_random_state() -> GameState:
    '''
    Generate a random valid puzzle state.
    Ret: PuzzleBoard
    '''
    from random import shuffle
    randomized_board_arr: List[int] = [i for i in range(N * N)]
    shuffle(randomized_board_arr)
    return GameState(
        board=tuple([
            tuple([randomized_board_arr[j] for j in range(i, i + N)])
            for i in range(0, N * N, N)
        ]))


def read_board_from_stdin() -> GameState:
    print("Please enter the elements row by row separated by spaces.")
    print("Use 0 to represent the empty space.")
    board = tuple([tuple([int(x) for x in input().split()]) for i in range(N)])
    res: Tuple[bool, str] = is_valid(board)
    if not res[0]:
        raise InvalidPuzzleError(res[1], board)
    return GameState(board = board)


def _get_empty_space_pos(board: PuzzleBoard) -> Tuple[int, int]:
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                return (i, j)
    raise RuntimeError(
        "This Shouldn't happen as is_valid() should be called before calling this fn"
    )


def _generate_valid_moves(board: PuzzleBoard) -> Iterable[Move]:
    possible_moves: List[Move] = [(-1, 0, "Left"), (1, 0, "Right"),
                                  (0, -1, "Up"), (0, 1, "Down")]

    empty_space_pos: Tuple[int, int] = _get_empty_space_pos(board)

    return filter(
        lambda move: (0 <= empty_space_pos[0] + move[0] < N and 0 <= empty_space_pos[1] + move[1] < N),
        possible_moves)


def _transition_get_item(board: PuzzleBoard, move: Move,
                         empty_space_pos: Tuple[int, int], row: int,
                         col: int) -> int:
    if (row, col) == empty_space_pos:
        return board[empty_space_pos[0] + move[0]][empty_space_pos[1] +
                                                   move[1]]
    elif (row, col) == (empty_space_pos[0] + move[0],
                        empty_space_pos[1] + move[1]):
        return 0
    else:
        return board[row][col]


def _transition(board: PuzzleBoard, move: Move,
                empty_space_pos: Tuple[int, int]) -> PuzzleBoard:
    return tuple([
        tuple([
            _transition_get_item(board, move, empty_space_pos, row, col)
            for col in range(N)
        ]) for row in range(N)
    ])


def generate_neighbours(state: GameState) -> List[GameState]:
    res = is_valid(state.board)
    if not res[0]:
        raise InvalidPuzzleError(res[1], state.board)
    empty_space_pos: Tuple[int, int] = _get_empty_space_pos(state.board)
    return [
        GameState(
            board=_transition(state.board, move, empty_space_pos),
            cost=state.cost + 1,
            depth=state.depth + 1,
            move=move[2]) for move in _generate_valid_moves(state.board)
    ]


############################ Displaying the Board ############################
def _display_row(board: PuzzleBoard, row: int) -> str:
    if row == 0:
        '''
        A top row
        ______________
        |   |   |    |

        '''
        return ("____" * len(board) + "_\n" + "|   " * len(board) + "|\n")

    elif row == len(board):
        '''
        A bottom row

        |___|___|____|

        '''
        return "|___" * len(board) + "|\n"

    else:
        '''
        A middle row

        |___|___|___|
        |   |   |   |

        '''
        return ("|___" * len(board) + "|\n" + "|   " * len(board) + "|\n")


def _display(board: PuzzleBoard, row: int) -> str:
    if row >= len(board):
        return _display_row(board, row)

    return (_display_row(board, row) + "| " + " | ".join(
        [str(i) if i != 0 else ' '
         for i in board[row]]) + " |\n" + _display(board, row + 1))


def display(board: PuzzleBoard) -> str:
    '''
    Display the puzzle board
    Args:
        board: PuzzleBoard
    Ret:
        str: representation of board.
    '''
    return _display(board, 0)


##############################################################################
