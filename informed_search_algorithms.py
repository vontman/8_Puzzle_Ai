from typing import List, Tuple, Dict, Set
from gamestate import GameState, GetNeighboursFn
from queue import Queue


class Bfs():

    @staticmethod
    def trace(parents: Dict[GameState, GameState], current_state: GameState,
              init_parent: GameState) -> List[GameState]:
        states: List[GameState] = []
        while current_state is not init_parent:
            states.append(current_state)
            current_state = parents[current_state]
        states.reverse()
        return states

    @staticmethod
    def solve(init_state: GameState, goal_state: GameState,
              get_neighbours_fn: GetNeighboursFn
              ) -> Tuple[bool, int, List[GameState]]:
        '''
        Using the BFS search algorithm to find the fullpath from the given state to the goal.
        BFS will always find the optimal solution.
        Uses a lot of memory when the solution is deep.
        Args:
            init_state: The initial game state.
            goal_state: The goal state to determine when a solution is found.
            get_neighbours_fn: Used to generate the successor states for any given state.
        Ret:
            (is_solution_found,
            number of expanded nodes,
            full path to solution)
        '''
        mark_init_state = GameState(board=None)
        parents: Dict[GameState, GameState] = {}
        queue: Queue[Tuple[GameState, GameState]] = Queue()
        queue.put((mark_init_state, init_state))
        expanded_nodes_cnt: int = 0
        while not queue.empty():
            parent_state, current_state = queue.get()

            if current_state in parents:
                continue
            expanded_nodes_cnt += 1
            parents[current_state] = parent_state

            if current_state == goal_state:
                return (True, expanded_nodes_cnt, Bfs.trace(parents, current_state,
                                        mark_init_state))

            for neighbour_state in get_neighbours_fn(current_state):
                queue.put((current_state, neighbour_state))

        return (False, expanded_nodes_cnt, [])


class Dfs():
    @staticmethod
    def _solve(goal_state: GameState,
               get_neighbours_fn: GetNeighboursFn, current_state: GameState,
               vis: Set[GameState],
               parents: List[GameState], expanded_nodes_cnt: int) -> Tuple[bool, int, List[GameState]]:
        if current_state in vis:
            return (False, expanded_nodes_cnt, [])
        vis.add(current_state)
        parents.append(current_state)
        expanded_nodes_cnt += 1

        if current_state == goal_state:
            return (True, expanded_nodes_cnt, parents)

        for neighbour in reversed(get_neighbours_fn(current_state)):
            found_sol, expanded_nodes, states = Dfs._solve(goal_state,
                                           get_neighbours_fn, neighbour, vis,
                                           parents, expanded_nodes_cnt)
            if found_sol:
                return (True, expanded_nodes, states)

        parents.pop()
        return (False, expanded_nodes_cnt, [])

    @staticmethod
    def solve(init_state: GameState, goal_state: GameState,
              get_neighbours_fn: GetNeighboursFn
              ) -> Tuple[bool, int, List[GameState]]:
        '''
        Using the DFS search algorithm to find the fullpath from the given state to the goal.
        DFS will always any solution not caring about the path cost => not optimal.
        Uses a lot of memory when the solution is deep.
        Mostly goes to stack overflow.
        Args:
            init_state: The initial game state.
            goal_state: The goal state to determine when a solution is found.
            get_neighbours_fn: Used to generate the successor states for any given state.
        Ret:
            (is_solution_found,
            number of expanded nodes,
            full path to solution)
        '''
        return Dfs._solve(goal_state, get_neighbours_fn, init_state,
                          set(), [], 0)


class Dfs_iter():
    @staticmethod
    def _solve(goal_state: GameState,
               get_neighbours_fn: GetNeighboursFn, current_state: GameState,
               vis: Set[GameState],
               parents: List[GameState]) -> Tuple[bool, int, List[GameState]]:

        expanded_nodes_cnt:int = 0
        stack: List[List[GameState]] = [[current_state]]

        while len(stack) > 0:
            current_states = stack.pop()
            current_state = current_states[-1]

            if current_state in vis:
                continue

            expanded_nodes_cnt += 1

            vis.add(current_state)

            if current_state == goal_state:
                return (True, expanded_nodes_cnt, current_states)

            for neighbour in get_neighbours_fn(current_state):
                stack.append(current_states + [neighbour])
        return (False, expanded_nodes_cnt, [])

    @staticmethod
    def solve(init_state: GameState, goal_state: GameState,
              get_neighbours_fn: GetNeighboursFn
              ) -> Tuple[bool, int, List[GameState]]:
        '''
        Same as above except it doesn't use recursion to avoid stack overflows.

        Args:
            init_state: The initial game state.
            goal_state: The goal state to determine when a solution is found.
            get_neighbours_fn: Used to generate the successor states for any given state.
        Ret:
            (is_solution_found,
            number of expanded nodes,
            full path to solution)
        '''
        return Dfs_iter._solve(goal_state, get_neighbours_fn,
                               init_state, set(), [])
