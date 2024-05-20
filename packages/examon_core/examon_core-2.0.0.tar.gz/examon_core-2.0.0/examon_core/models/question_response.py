from dataclasses import dataclass

from .question import Question


@dataclass
class QuestionResponse:
    question: Question = None
    response: str = None
    correct: bool = None
