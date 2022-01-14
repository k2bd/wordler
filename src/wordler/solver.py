from string import ascii_lowercase
from typing import Any, Dict, List

import requests
from pydantic import BaseModel
from wordle_api.wordle import GuessResult, ResultKind
from wordle_api.words import candidate_words

from wordler.constants import WORDLE_API_URL

DAILY = "daily"


def valid_words(size: int, guesses: List[GuessResult]) -> List[str]:
    """
    Words that match the list of guesses that have been made
    """

    def word_valid(word):
        for guess in guesses:
            if guess.result == ResultKind.CORRENT:
                if word[guess.slot] != guess.guess:
                    return False
            if guess.result == ResultKind.PRESENT:
                if guess.guess not in word:
                    return False
            if guess.result == ResultKind.ABSENT:
                if word[guess.slot] == guess.guess:
                    return False
        return True

    return [word for word in candidate_words(size=size) if word_valid(word)]


def get_slot_letter_counts(available_words: List[str]):
    return {
        slot: {
            letter: len([w for w in available_words if w[slot] == letter])
            for letter in ascii_lowercase
        }
        for slot in range(len(available_words[0]))
    }


def score_word(
    word: str,
    scorer: Dict[int, Dict[str, int]],
) -> int:
    return sum(scorer[slot][word[slot]] for slot in range(len(word)))


def best_word(size: int, guesses: List[GuessResult]):
    available = valid_words(size=size, guesses=guesses)
    scorer = get_slot_letter_counts(available)
    word_scores = {word: score_word(word, scorer) for word in available}
    return sorted(
        word_scores.keys(),
        key=lambda word: word_scores[word],
        reverse=True,
    )[0]


class Result(BaseModel):
    guesses: List[str]
    emojis: List[str]


def solve(size: int, url: str, base_query: Dict[str, Any]):
    """
    Generic solve
    """
    guessed_words: List[str] = []
    guess_results: List[GuessResult] = []
    result_emojis: List[str] = []

    while True:
        guess = best_word(size=size, guesses=guess_results)

        response = requests.get(url, params={**base_query, "guess": guess})
        response.raise_for_status()

        guessed_words.append(guess)
        guess_result = [GuessResult.parse_obj(result) for result in response.json()]
        guess_results.extend(guess_result)

        result_emojis.append("".join(r.result.square() for r in guess_result))

        if all(r.result == ResultKind.CORRENT for r in guess_result):
            # Success
            break

    return Result(guesses=guessed_words, emojis=result_emojis)


def solve_daily(size: int = 5):
    """
    Solve the daily puzzle
    """
    url = WORDLE_API_URL + "/daily"
    base_query = {"size": size}
    return solve(size=size, url=url, base_query=base_query)


def solve_seed(seed: int, size: int = 5):
    """
    Solve a puzzle given a random seed
    """
    url = WORDLE_API_URL + "/random"
    base_query = {"size": size, "seed": seed}
    return solve(size=size, url=url, base_query=base_query)


def solve_word(word: str):
    """
    Solve a puzzle with a given solution
    """
    url = WORDLE_API_URL + f"/word/{word}"
    return solve(size=len(word), url=url, base_query={})
