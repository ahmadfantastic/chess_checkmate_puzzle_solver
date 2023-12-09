from enum import Enum

import puzzleloader
import search
import state
from node import Node
from state import State
from state import Heuristic


class SearchAlgorithm(Enum):
    """
    Enumeration of Search Algorithms
    """
    MINIMAX = 1
    ALPHA_BETA_PRUNING = 2
    TRANSPOSITION = 3
    KILLER_MOVE_HEURISTIC = 4


def start_problem(initial_state: State, solution, search_type: SearchAlgorithm) -> None:
    """
    Start a new chess puzzle problem
    :param initial_state: The initial state to start with
    :param solution: The Actual solution of the problem
    :param search_type: The search algorithm to use
    """
    initial_node = Node(True, initial_state, 0)
    print("------------------------------------------------------------")
    print("Starting Chess Puzzle Problem: ")
    if search_type == SearchAlgorithm.MINIMAX:
        print("Search Algorithm: MiniMax")
        print("------------------------------------------------------------")
        terminal, expanded = search.minimax(initial_node)
    elif search_type == SearchAlgorithm.ALPHA_BETA_PRUNING:
        print("Search Algorithm: MiniMax with Alpha Beta Pruning")
        print("------------------------------------------------------------")
        terminal, expanded = search.alpha_beta_pruning(initial_node, -1, 1)
    elif search_type == SearchAlgorithm.TRANSPOSITION:
        search.transposition_table.clear()  # Ensure the transposition table is empty
        print("Search Algorithm: MiniMax with Alpha Beta Pruning and Transposition")
        print("------------------------------------------------------------")
        terminal, expanded = search.transposition(initial_node, -1, 1)
    elif search_type == SearchAlgorithm.KILLER_MOVE_HEURISTIC:
        search.transposition_table.clear()  # Ensure the transposition table is empty
        print("Search Algorithm: MiniMax with Alpha Beta Pruning, Transposition and Killer Move Heuristic")
        print("------------------------------------------------------------")
        terminal, expanded = search.killer_move_heuristic(initial_node, -1, 1, Heuristic.CHECK)
    else:
        print("Invalid Search Algorithm")
        return

    print("Number of States Expanded:", expanded)
    print("Utility:", terminal.state.utility())
    print("Initial Position:", state.position)
    print("Solution Path:", str(terminal))
    print("Actual Solution:", solution)
    print("------------------------------------------------------------")


if __name__ == '__main__':
    puzzles = puzzleloader.load_puzzle_file('puzzles/mate2.txt')

    for i in range(len(puzzles)):
        print("Test Case ", i + 1)
        puzzle = puzzles[i]
        state = State(puzzle['player'], puzzle['position'], puzzle['mate'])
        start_problem(state, puzzle['solution'], SearchAlgorithm.TRANSPOSITION)
