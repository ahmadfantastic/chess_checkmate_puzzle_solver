import math
from copy import deepcopy

from node import Node
from state import Heuristic


def minimax(node: Node) -> (Node, int):
    """
    Minimax algorithm
    :param node: The current Node
    :return: The best terminal node and number of states expanded to get there
    """
    if node.state.terminal_test():  # Terminal Node
        return node, 0
    elif node.is_max_node:  # Max Node
        total_expanded = 1
        best_val = -math.inf
        best_node = None

        successors = node.state.find_successors()
        while not successors.empty():  # Go through the successors
            (priority, (action, state)) = successors.get()
            successor = Node(False, state, node.depth + 1, node, action)
            terminal, expanded = minimax(successor)
            total_expanded += expanded
            if terminal.state.utility() > best_val:  # Update the best value and node
                best_val = terminal.state.utility()
                best_node = terminal

        return best_node, total_expanded

    else:  # Min Node
        total_expanded = 1
        best_val = math.inf
        best_node = None

        successors = node.state.find_successors()
        while not successors.empty():
            (priority, (action, state)) = successors.get()
            successor = Node(True, state, node.depth + 1, node, action)
            terminal, expanded = minimax(successor)
            total_expanded += expanded
            if terminal.state.utility() < best_val:  # Update the best value and node
                best_val = terminal.state.utility()
                best_node = terminal

        return best_node, total_expanded


def alpha_beta_pruning(node: Node, alpha, beta):
    """
    Minimax algorithm with Alpha-Beta Pruning
    :param node: The current Node
    :param alpha: The alpha value of the pruning
    :param beta: The beta value of the pruning
    :return: The best terminal node and number of states expanded to get there
    """
    if node.state.terminal_test():  # Terminal Node
        return node, 0
    elif node.is_max_node:  # Max Node
        total_expanded = 1
        best_val = -math.inf
        best_node = None

        successors = node.state.find_successors()
        while not successors.empty():
            (priority, (action, state)) = successors.get()
            successor = Node(False, state, node.depth + 1, node, action)
            terminal, expanded = alpha_beta_pruning(successor, alpha, beta)
            total_expanded += expanded

            if terminal.state.utility() > best_val:  # Update the best value and node
                best_val = terminal.state.utility()
                best_node = terminal
            elif terminal.state.utility() == best_val:  # If best value is the same, choose best node by depth
                if best_val > 0 and terminal.depth < best_node.depth:
                    # If we are winning, choose the smallest depth
                    best_node = terminal
                elif best_val < 0 and terminal.depth > best_node.depth:
                    # If we are losing, choose the biggest depth
                    best_node = terminal

            alpha = max(alpha, best_val)

            # Alpha Beta Pruning
            if beta <= alpha:
                break

        return best_node, total_expanded

    else:  # Min Node
        total_expanded = 1
        best_val = math.inf
        best_node = None

        successors = node.state.find_successors()
        while not successors.empty():
            (priority, (action, state)) = successors.get()
            successor = Node(True, state, node.depth + 1, node, action)
            terminal, expanded = alpha_beta_pruning(successor, alpha, beta)
            total_expanded += expanded

            if terminal.state.utility() < best_val:  # Update the best value and node
                best_val = terminal.state.utility()
                best_node = terminal
            elif terminal.state.utility() == best_val: # If best value is the same, choose best node by depth
                if best_val > 0 and terminal.depth > best_node.depth:
                    # If opponent is losing, choose the biggest depth
                    best_node = terminal
                elif best_val < 0 and terminal.depth < best_node.depth:
                    # If opponent is winning, choose the smallest depth
                    best_node = terminal

            beta = min(beta, best_val)

            # Alpha Beta Pruning
            if beta <= alpha:
                break

        return best_node, total_expanded


transposition_table: dict[str, Node] = {}


def transposition(node: Node, alpha, beta):
    """
    Minimax algorithm with Alpha-Beta Pruning and Transposition
    :param node: The current Node
    :param alpha: The alpha value of the pruning
    :param beta: The beta value of the pruning
    :return: The best terminal node and number of states expanded to get there
    """
    if node.state.position in transposition_table:
        best_node = deepcopy(transposition_table[node.state.position])
        pointer = best_node
        while node.state != pointer.state:
            pointer = pointer.parent
        pointer.parent = node.parent
        return best_node, 0
    elif node.state.terminal_test():  # Terminal Node
        return node, 0
    elif node.is_max_node:  # Max Node
        total_expanded = 1
        best_val = -math.inf
        best_node = None

        successors = node.state.find_successors()
        while not successors.empty():
            (priority, (action, state)) = successors.get()
            n = Node(False, state, node.depth + 1, node, action)
            terminal, expanded = transposition(n, alpha, beta)
            total_expanded += expanded

            if terminal.state.utility() > best_val: # Update the best value and node
                best_val = terminal.state.utility()
                best_node = terminal
            elif terminal.state.utility() == best_val:  # If best value is the same, choose best node by depth
                if best_val > 0 and terminal.depth < best_node.depth:
                    # If we are winning, choose the smallest depth
                    best_node = terminal
                elif best_val < 0 and terminal.depth > best_node.depth:
                    # If we are losing, choose the biggest depth
                    best_node = terminal

            alpha = max(alpha, best_val)

            # Alpha Beta Pruning
            if beta <= alpha:
                break

        transposition_table[node.state.position] = best_node
        return best_node, total_expanded

    else: # Min Node
        total_expanded = 1
        best_val = math.inf
        best_node = None

        successors = node.state.find_successors()
        while not successors.empty():
            (priority, (action, state)) = successors.get()
            successor = Node(True, state, node.depth + 1, node, action)
            terminal, expanded = transposition(successor, alpha, beta)
            total_expanded += expanded

            if terminal.state.utility() < best_val: # Update the best value and node
                best_val = terminal.state.utility()
                best_node = terminal
            elif terminal.state.utility() == best_val:  # If best value is the same, choose best node by depth
                if best_val > 0 and terminal.depth > best_node.depth:
                    # If opponent is losing, choose the biggest depth
                    best_node = terminal
                elif best_val < 0 and terminal.depth < best_node.depth:
                    # If opponent is winning, choose the smallest depth
                    best_node = terminal

            beta = min(beta, best_val)

            # Alpha Beta Pruning
            if beta <= alpha:
                break

        transposition_table[node.state.position] = best_node
        return best_node, total_expanded


def killer_move_heuristic(node: Node, alpha, beta, heuristic: Heuristic):
    """
    Minimax algorithm with Alpha-Beta Pruning
    :param node: The current Node
    :param alpha: The alpha value of the pruning
    :param beta: The beta value of the pruning
    :param heuristic: The type of heuristic to use
    :return: The best terminal node and number of states expanded to get there
    """
    if node.state.position in transposition_table:
        best_node = deepcopy(transposition_table[node.state.position])
        pointer = best_node
        while node.state != pointer.state:
            pointer = pointer.parent
        pointer.parent = node.parent
        return best_node, 0
    elif node.state.terminal_test():  # Terminal Node
        return node, 0
    elif node.is_max_node:  # Max Node
        total_expanded = 1
        best_val = -math.inf
        best_node = None

        successors = node.state.find_successors(heuristic)
        while not successors.empty():
            (priority, (action, state)) = successors.get()
            n = Node(False, state, node.depth + 1, node, action)
            terminal, expanded = killer_move_heuristic(n, alpha, beta, heuristic)
            total_expanded += expanded

            if terminal.state.utility() > best_val:  # Update the best value and node
                best_val = terminal.state.utility()
                best_node = terminal
            elif terminal.state.utility() == best_val:  # If best value is the same, choose best node by depth
                if best_val > 0 and terminal.depth < best_node.depth:
                    # If we are winning, choose the smallest depth
                    best_node = terminal
                elif best_val < 0 and terminal.depth > best_node.depth:
                    # If we are losing, choose the biggest depth
                    best_node = terminal

            alpha = max(alpha, best_val)

            # Alpha Beta Pruning
            if beta <= alpha:
                break

        transposition_table[node.state.position] = best_node
        return best_node, total_expanded

    else:  # Min Node
        total_expanded = 1
        best_val = math.inf
        best_node = None

        successors = node.state.find_successors(heuristic)
        while not successors.empty():
            (priority, (action, state)) = successors.get()
            successor = Node(True, state, node.depth + 1, node, action)
            terminal, expanded = killer_move_heuristic(successor, alpha, beta, heuristic)
            total_expanded += expanded

            if terminal.state.utility() < best_val:  # Update the best value and node
                best_val = terminal.state.utility()
                best_node = terminal
            elif terminal.state.utility() == best_val:  # If best value is the same, choose best node by depth
                if best_val > 0 and terminal.depth > best_node.depth:
                    # If opponent is losing, choose the biggest depth
                    best_node = terminal
                elif best_val < 0 and terminal.depth < best_node.depth:
                    # If opponent is winning, choose the smallest depth
                    best_node = terminal

            beta = min(beta, best_val)

            # Alpha Beta Pruning
            if beta <= alpha:
                break

        transposition_table[node.state.position] = best_node
        return best_node, total_expanded
