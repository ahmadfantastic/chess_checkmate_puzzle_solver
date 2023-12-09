from state import State


class Node:
    def __init__(self, is_max_node: bool, state: State, depth: int, parent: 'Node' = None, action: str = None):
        """
        Initialise the Node
        :param is_max_node: Whether the node is a max node or min mode
        :param state: The state of the node
        :param depth: The depth of the node i.e., number of moves that leads to the chess position
        :param parent: The parent of the node
        :param action: The move that leads to the creation of this node
        """
        self.is_max_node = is_max_node
        self.state = state
        self.depth = depth
        self.parent = parent
        self.action = action

    def __str__(self):
        """
        The string representation of the Node
        :return: The path from the initial node to this node
        """
        if self.parent is None:
            return ""
        return str(self.parent) + " -> " + self.action

