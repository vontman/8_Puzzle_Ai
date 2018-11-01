from abc import ABCMeta, abstractmethod
from typing import Any, TypeVar, NamedTuple, Generic, Iterable, Tuple, Callable, List


class GameState(NamedTuple):
    '''
    Represents the current game state.
    board: The current board configuration
    depth: The depth of the current solution
    cost: The cost to reach this state from parent.
    move: The last move resulting in this state.
    '''
    board: Any
    depth: int = 0
    cost: int = 0
    move: Any = "No Moves"

    def __hash__(self) -> Any:
        return self.board.__hash__()

    def __eq__(self, other: Any) -> Any:
        return self.board.__eq__(other.board)


GetNeighboursFn = Callable[[GameState], List[GameState]]
IsValidStateFn = Callable[[GameState], Tuple[bool, str]]
GenerateRandomBoardFn = Callable[[], GameState]
ReadBoardFromStdin = Callable[[], GameState]

