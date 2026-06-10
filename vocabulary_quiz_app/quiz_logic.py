from __future__ import annotations

import random

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Word:
    term: str
    meaning: str


class QuizDirection(str, Enum):
    """Which side of the word the user is asked to produce."""

    TERM_TO_MEANING = "term_to_meaning"  # show English term, answer Korean meaning
    MEANING_TO_TERM = "meaning_to_term"  # show Korean meaning, answer English term


def normalize_answer(text: str) -> str:
    return " ".join(text.strip().lower().split())


def prompt_for(word: Word, direction: QuizDirection) -> str:
    """Return the text shown to the user for the given direction."""
    if direction is QuizDirection.MEANING_TO_TERM:
        return word.meaning
    return word.term


def expected_answer(word: Word, direction: QuizDirection) -> str:
    """Return the answer the user is expected to type for the direction."""
    if direction is QuizDirection.MEANING_TO_TERM:
        return word.term
    return word.meaning


def check_answer(
    word: Word,
    user_input: str,
    direction: QuizDirection = QuizDirection.TERM_TO_MEANING,
) -> bool:
    target = expected_answer(word, direction)
    return normalize_answer(user_input) == normalize_answer(target)


def draw_word(words: list[Word], rng: random.Random | None = None) -> Word:
    if not words:
        raise ValueError("Word list is empty")
    chooser = rng if rng is not None else random
    return chooser.choice(words)
