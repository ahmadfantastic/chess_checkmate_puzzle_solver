import re


def load_puzzle_file(filename: str) -> list:
    """
    Loads puzzles from a file
    :param filename: The puzzle filename
    :return: A list of the puzzles
    """

    f = open(filename, "r")

    puzzles = []

    next_line = f.readline().rstrip('\n')
    while next_line:
        puzzles.append(
            format_puzzle(
                next_line,
                f.readline().rstrip('\n'),
                f.readline().rstrip('\n')
            )
        )
        #  Ignore two empty white space
        f.readline()
        f.readline()

        next_line = f.readline().rstrip('\n')

    return puzzles


def format_puzzle(meta_line: str, position_line: str, solution_line: str):
    """
    Formats puzzle lines to a dictionary
    :param meta_line: Line of puzzle metadata
    :param position_line: : Line of chess puzzle position
    :param solution_line: Line of chess puzzle solution
    :return: A dictionary of the puzzle
    """

    # Formatting meta
    meta_line = meta_line.split(',')
    meta = {
        'players': meta_line[0],
        'location': meta_line[1],
        'date': meta_line[2]
    }

    # Formatting FEN position
    position = position_line

    # Formatting solution
    solution_line = re.split(r'(\d+\.)', solution_line)
    solution = []
    i = 2  # Ignore the first empty item and number item
    player = True  # True to indicate white
    while i < len(solution_line):
        moves = solution_line[i].split()
        if len(moves) == 2:
            solution.append({
                'w': moves[0],
                'b': moves[1]
            })
        elif i == 2:  # The first move is black
            player = False  # False to indicate black
            solution.append({
                'b': moves[0]
            })
        else:  # The last move is white
            solution.append({
                'w': moves[0]
            })

        i += 2  # Skip to the next 2 items

    return {
        'meta': meta,
        'player': player,  # True for White, False for Black
        'position': position,
        'mate': len(solution),
        'solution': solution
    }
