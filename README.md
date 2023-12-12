# Chess Checkmate Puzzle Solver
This program uses simple AI search techniques to solve chess checkmate puzzles.

### Techniques used include
- MiniMax Algorithm
- Alpha-Beta Pruning
- Transposition
- Killer Move Heuristic (for Move Ordering)

## About the Project
This project was completed as a course project on `Artificial Intelligence` at `Clarkson University` taught by `Prof. Christopher Lynch`.

### Project Completed by:
- Ahmad Suleiman: https://github.com/ahmadfantastic
- Nowreen Ahsan
- Katie Bonk

### Project Documents
- [Project Proposal](https://docs.google.com/document/d/10mtiBX_XN--wOmkSw8E3o_NwrYxPUMSmiF1g2fk72Yg/edit)
- [Project Final Presentation](https://docs.google.com/presentation/d/1bbWk2Nlo_cc15aLFTWp-yFizXrhnfXdoygoRPycCst8/edit#slide=id.g2a41824c8cb_0_68)
- [Project Final Report](https://docs.google.com/document/d/1OtrkMxc-68UzHX5k0Kzr06oLgI7htZGAWVLjB4ryj4Y/edit#heading=h.pwelozedd80i)

## Running

### Prerequisite
The prerequisites needed to run this program are
- `Python 3.*`:  https://www.python.org/downloads/
- `pip`: Package installer for Python https://pypi.org/project/pip/
- `IDE`: To edit the code and decide which puzzle problem to run, you need an IDE. This project is configured with `PyCharm`

### Installation
1. The only package needed to install this program is `python-chess`. To install it, run the command `pip install chess`
2. Clone this reposition using: `git clone https://github.com/ahmadfantastic/chess_checkmate_puzzle_solver.git`
3. Open the project using your IDE.

### Available Puzzle Problems
There are some chess checkmate puzzles in the [/puzzles](puzzles) folder, with even more in the [/puzzles_full](puzzles_full) folder.
These puzzles are fetched from: https://wtharvey.com/.

### Running an Example
Here is a sample code snippet to run the checkmate in 2 puzzles in [/puzzles](puzzles/mate2.txt) 
```python
if __name__ == '__main__':
    puzzles = puzzleloader.load_puzzle_file('puzzles/mate2.txt')

    for i in range(len(puzzles)):
        print("Test Case ", i + 1)
        puzzle = puzzles[i]
        state = State(puzzle['player'], puzzle['position'], puzzle['mate'])
        start_problem(state, puzzle['solution'], SearchAlgorithm.TRANSPOSITION)
```
