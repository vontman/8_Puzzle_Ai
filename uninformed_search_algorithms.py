from typing import List, Tuple, Dict, Set, Any, Callable
from gamestate import GameState, GetNeighboursFn
from queue import PriorityQueue
from math import sqrt
import puzzle


class GameStateWrapper():
    gameState: GameState
    heuristic: Any

    def __init__(self, gameState: GameState, heuristic: Any) -> None:
        self.gameState = gameState
        self.heuristic = heuristic

    def __lt__(self, other):
        return self.heuristic(self.gameState) + self.gameState.cost < self.heuristic(
                other.gameState) + other.gameState.cost

    def __eq__(self, other):
        return self.gameState.__eq__(other.gameState)

    def __hash__(self):
        return self.gameState.__hash__()


class AStar():
    @staticmethod
    def trace(parents: Dict[GameStateWrapper, GameStateWrapper],
              current_state: GameStateWrapper,
              init_parent: GameStateWrapper) -> List[GameState]:
        states: List[GameState] = []
        while current_state is not init_parent:
            states.append(current_state.gameState)
            current_state = parents[current_state]
        states.reverse()
        return states

    @staticmethod
    def solve(init_state: GameState, goal_state: GameState,
              get_neighbours_fn: GetNeighboursFn,
              heuristicFn: Callable[[GameState], float]
              ) -> Tuple[bool, int, List[GameState]]:
        '''
        Using the A* search algorithm to find the fullpath from the given state to the goal.
        The performance of the algorithm relies on the given hearistic function.
        If the heuristic function is admissible then surely it will find the optimal solution.
        Usually uses less memory than BFS as it is more information about the states.
        Args:
            init_state: The initial game state.
            goal_state: The goal state to determine when a solution is found.
            get_neighbours_fn: Used to generate the successor states for any given state.
            heuristicFn: The heuristic function used to estimate the cost to the solution from any game state.
        Ret:
            (is_solution_found,
            number of expanded nodes,
            full path to solution)
        '''

        mark_init_state = GameStateWrapper(GameState(board=None), heuristicFn)
        parents: Dict[GameStateWrapper, GameStateWrapper] = {}
        queue: PriorityQueue[
            Tuple[GameStateWrapper, GameStateWrapper]] = PriorityQueue()
        queue.put((mark_init_state, GameStateWrapper(init_state, heuristicFn)))
        expanded_nodes_cnt: int = 0
        while not queue.empty():
            parent_state, current_state = queue.get()

            if current_state in parents:
                continue

            expanded_nodes_cnt += 1
            parents[current_state] = parent_state

            if current_state.gameState == goal_state:
                return (True, expanded_nodes_cnt,
                        AStar.trace(parents, current_state, mark_init_state))

            for neighbour_state in get_neighbours_fn(current_state.gameState):
                queue.put((current_state,
                           GameStateWrapper(neighbour_state, heuristicFn)))

        return (False, expanded_nodes_cnt, [])
