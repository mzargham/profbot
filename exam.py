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
    
    def summarize_exam(self):
        print("Exam Guidelines:")
        for guideline in self.exam_guidelines:
            print(f"\t{guideline}")
        print("Questions:")
        for i, question in enumerate(self.questions):
            print(f"\t{i+1}. {question}")
            print(f"\t\t{self.question_guidelines[i]}")

    # Additional methods can be added here
