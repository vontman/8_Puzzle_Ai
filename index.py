#TODO: Don't use classes or static methods, only use functions.
#TODO: Follow a consistent way of representing a game where it is abstracted from the algorithm


from typing import List, Any, Dict, Tuple
from time import time
from functools import reduce

import puzzle
from gamestate import GameState
from informed_search_algorithms import Bfs, Dfs_iter, Dfs
from uninformed_search_algorithms import AStar

def _find_pos(state: GameState, val: int) -> Tuple[int, int]:
    for i in range(puzzle.N):
        for j in range(puzzle.N):
            if state.board[i][j] == val:
                return (i, j)
    raise RuntimeError("Couldn't find val(", val, " in the board.")

def eucledianHeuristic(state: GameState) -> float:
    total_score: int = 0

    for i in range(puzzle.N):
        for j in range(puzzle.N):
            val:int = puzzle.GOAL_STATE.board[i][j]
            x, y = _find_pos(state, val)
            total_score += (x - i)**2 + (y - j)**2

    return total_score


def manhatanHeuristic(state: GameState) -> float:
    total_score: int = 0

    for i in range(len(puzzle.GOAL_STATE.board)):
        for j in range(len(puzzle.GOAL_STATE.board)):
            val:int = puzzle.GOAL_STATE.board[i][j]
            x, y = _find_pos(state, val)
            total_score += abs(x - i) + abs(y - j)

    return total_score


def evaluate(init_state: GameState, search_algorithm: Any, heuristicFn: Any = None) -> None:
    '''
    Evaluates the path to the goal state using the specified search_algorithm.
    Prints the full path along with cost, depth, expanded_nodes_cnt, time_elapsed.
    Args:
        init_state: the initial game state to be solved
        search_algorithm: could be anything of Bfs, Dfs, Dfs_iter, AStar
        heuristicFn(Optional): must be set when using AStar, could be either manhatanHeuristic or eucledianHeuristic
    '''
    print("Finding a path to goal using", search_algorithm, heuristicFn, "for board:")
    print(puzzle.display(init_state.board))
    curr_time = time()
    if heuristicFn is not None:
        found_sol, expanded_nodes_cnt, path_to_goal = search_algorithm.solve(
            init_state, puzzle.GOAL_STATE, puzzle.generate_neighbours, heuristicFn)
    else:
        found_sol, expanded_nodes_cnt, path_to_goal = search_algorithm.solve(
        init_state, puzzle.GOAL_STATE, puzzle.generate_neighbours)

    time_elapsed = time() - curr_time
    if not found_sol:
        print("Couldn't find a path to the goal.")
        print("Expanded nodes count:", expanded_nodes_cnt)
        print("Running time:", time_elapsed)
        return

    for state in path_to_goal[1:]:
        print("Move:", state.move)
        # print("man score", manhatanHeuristic(state))
        # print("euc score", eucledianHeuristic(state))
        print(puzzle.display(state.board))

    print("Result of using", search_algorithm, heuristicFn)
    print("Total path cost:", path_to_goal[-1].cost)
    print("Depth:", path_to_goal[-1].depth)
    print("Expanded nodes count:", expanded_nodes_cnt)
    print("Running time:", time_elapsed)



'''
some examples:

1 2 5
3 4 0
6 7 8
cost = 3

5 7 0
6 8 1
3 2 4
cost = 22

3 1 6
7 2 4
0 5 8
cost = 20
'''
board = puzzle.read_board_from_stdin()

evaluate(board, AStar, manhatanHeuristic)
evaluate(board, AStar, eucledianHeuristic)
evaluate(board, Bfs)
evaluate(board, Dfs)
