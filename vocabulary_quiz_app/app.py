from __future__ import annotations

import random
import tkinter as tk

from tkinter import ttk, font

from vocabulary_quiz_app.quiz_logic import (
    QuizDirection,
    Word,
    check_answer,
    draw_word,
    expected_answer,
    prompt_for,
)


class VocabularyQuizApp:
    def __init__(self, root: tk.Tk, words: list[Word]) -> None:
        self.words = words
        self.rng = random.Random()
        self.current: Word | None = None
        self.checked = False
        self.score = 0
        self.total = 0
        self.direction = QuizDirection.TERM_TO_MEANING

        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="NanumGothic", size=12)

        root.title("Vocabulary Quiz")
        root.geometry("420x320")
        root.resizable(False, False)

        self.prompt_label_var = tk.StringVar(value="영단어")
        self.word_var = tk.StringVar(value="단어를 불러오는 중...")
        self.feedback_var = tk.StringVar(value="")
        self.score_var = tk.StringVar(value="Score: 0/0")
        self.direction_var = tk.StringVar(value="모드: 영어 → 뜻")

        ttk.Label(root, textvariable=self.prompt_label_var).pack(pady=(16, 4))
        ttk.Label(root, textvariable=self.word_var, font=("NanumGothic", 24)).pack()

        self.answer_entry = ttk.Entry(root, font=("NanumGothic", 14))
        self.answer_entry.pack(pady=12, ipadx=6, ipady=4)

        buttons = ttk.Frame(root)
        buttons.pack(pady=6)
        self.check_button = ttk.Button(buttons, text="채점", command=self.check_current)
        self.check_button.pack(side=tk.LEFT, padx=6)
        ttk.Button(buttons, text="다음", command=self.next_word).pack(
            side=tk.LEFT, padx=6
        )
        ttk.Button(buttons, text="모드 전환", command=self.toggle_direction).pack(
            side=tk.LEFT, padx=6
        )

        ttk.Label(root, textvariable=self.feedback_var).pack(pady=8)
        ttk.Label(root, textvariable=self.score_var).pack()
        ttk.Label(root, textvariable=self.direction_var).pack()

        self.next_word()

    def toggle_direction(self) -> None:
        if self.direction is QuizDirection.TERM_TO_MEANING:
            self.direction = QuizDirection.MEANING_TO_TERM
            self.prompt_label_var.set("뜻")
            self.direction_var.set("모드: 뜻 → 영어")
        else:
            self.direction = QuizDirection.TERM_TO_MEANING
            self.prompt_label_var.set("영단어")
            self.direction_var.set("모드: 영어 → 뜻")
        self.next_word()

    def next_word(self) -> None:
        self.current = draw_word(self.words, self.rng)
        self.word_var.set(prompt_for(self.current, self.direction))
        self.answer_entry.delete(0, tk.END)
        self.feedback_var.set("")
        self.checked = False
        self.check_button.state(["!disabled"])
        self.answer_entry.focus()

    def check_current(self) -> None:
        if self.current is None or self.checked:
            return
        self.checked = True
        self.total += 1
        user_input = self.answer_entry.get()
        if check_answer(self.current, user_input, self.direction):
            self.score += 1
            self.feedback_var.set("정답입니다!")
        else:
            answer = expected_answer(self.current, self.direction)
            self.feedback_var.set(f"오답입니다. 정답: {answer}")
        self.score_var.set(f"Score: {self.score}/{self.total}")
        self.check_button.state(["disabled"])
