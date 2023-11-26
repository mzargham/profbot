from dataclasses import dataclass
from typing import List, Type

@dataclass
class Schema:
    Prompt: str
    Response: str
    Notes: str
    Grade: int

class Exam:
    def __init__(self, questions: List[str], question_guidelines: List[str], exam_guidelines: List[str], schema: Type[Schema]):
        assert issubclass(schema, Schema), "Provided schema must be a subclass of Schema or Schema itself."

        self.questions = questions
        self.question_guidelines = question_guidelines
        self.exam_guidelines = exam_guidelines
        self.schema = schema

    # Additional methods can be added here
