import queue
from enum import Enum

import chess


class Heuristic(Enum):
    """
    Heuristic Enumerations
    """
    NONE = 0
    CHECK = 1


class State:

    def __init__(self, player: bool, position: str, mate: int):
        """
        Initializes the State
        :param player: The current player, True for WHITE and False for BLACK
        :param position: FEN of a chess position
        :param mate: There is a checkmate in n moves
        """
        self.position = position
        self.player = player
        self.mate = mate
        self.board = chess.Board(position)  # Create a board from this position

    def terminal_test(self) -> bool:
        """
        Checks if this state has reached a terminal/goal state
        :return: True if the game is over based on chess rules mate is 0
        """
        return self.board.is_game_over() or self.mate == 0

    def utility(self) -> int:
        """
        Gets the utility value of a terminal state
        :return: +1 if player won the game, -1 if player lost the game or 0 if the game is draw or not over
        """
        outcome = self.board.outcome()
        if outcome and outcome.winner is not None:  # If white won
            return 1 if outcome.winner == self.player else -1
        else:
            return 0

    def __str__(self) -> str:
        """
        String representation of this state
        :return: The position of the state
        """
        return self.position

    def __eq__(self, __value) -> bool:
        """
        Comparing this state with another one
        :param __value: Another state
        :return: True only if they have the same position
        """
        return self.position == __value.position

    def find_successors(self, heuristic: Heuristic = Heuristic.NONE) -> queue.PriorityQueue:
        """
        Finds all successor states of these states
        :param heuristic: The move ordering heuristic to use, default is 0 to indicate no move ordering
        :return: A PriorityQueue of the successor states
        """
        successors = queue.PriorityQueue()  # It is just a simple list if heuristic=0
        for move in self.board.legal_moves:  # chess library helps with all legal moves
            action = self.board.san(move)  # Get string representation of the move
            self.board.push(move)  # Make a temporary move to get the new position
            new_position = self.board.fen()  # Get the FEN of the new position
            new_mate = self.mate if self.board.turn else self.mate - 1  # decrement mate only if Black moves
            state = State(self.player, new_position, new_mate)  # Create the successor State
            successors.put((self.h(heuristic), (action, state)))  # Add to the PriorityQueue
            self.board.pop()  # Undo the temporary move

        return successors

    def h(self, heuristic: Heuristic) -> int:
        """
        Gets the heuristic value of this state
        :param heuristic: The heuristic type to use, default is 0 to indicate no move ordering
        :return: The heuristic value of this state
        """

        if heuristic == Heuristic.NONE:  # No Heuristic
            return 0
        elif heuristic == Heuristic.CHECK:  # Killer Move Heuristic: Check move first
            if self.board.is_check():
                return 0
            else:
                return 1
