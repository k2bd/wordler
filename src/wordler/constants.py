import os

#: Location of the wordle API
WORDLE_API_URL = os.environ.get("INPUT_WORDLEAPIURL", "")

#: Puzzle size to solve
PUZZLE_SIZE = int(os.environ.get("INPUT_PUZZLESIZE", "5"))
