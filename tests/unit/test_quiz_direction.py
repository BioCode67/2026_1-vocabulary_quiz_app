from vocabulary_quiz_app.quiz_logic import (
    QuizDirection,
    Word,
    check_answer,
    expected_answer,
    prompt_for,
)


def test_prompt_and_expected_term_to_meaning() -> None:
    word = Word(term="apple", meaning="사과")
    direction = QuizDirection.TERM_TO_MEANING

    assert prompt_for(word, direction) == "apple"
    assert expected_answer(word, direction) == "사과"


def test_prompt_and_expected_meaning_to_term() -> None:
    word = Word(term="apple", meaning="사과")
    direction = QuizDirection.MEANING_TO_TERM

    assert prompt_for(word, direction) == "사과"
    assert expected_answer(word, direction) == "apple"


def test_check_answer_meaning_to_term() -> None:
    word = Word(term="book", meaning="책")

    assert check_answer(word, "book", QuizDirection.MEANING_TO_TERM)
    assert check_answer(word, "  BOOK ", QuizDirection.MEANING_TO_TERM)
    assert not check_answer(word, "책", QuizDirection.MEANING_TO_TERM)


def test_check_answer_default_is_term_to_meaning() -> None:
    word = Word(term="chair", meaning="의자")

    # Default direction keeps original behaviour intact.
    assert check_answer(word, "의자")
    assert not check_answer(word, "chair")
