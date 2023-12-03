from exam import Exam, GradeLog
from dataclasses import dataclass
from typing import List
    
# Define the AI exam specific questions and guidelines
questions = ["What is AI?", "Explain deep learning."]
question_guidelines = [
    "At minimum, must address the following: AI stands for Artificial Intelligence, which is a broad field of computer science encompassing machine learning, deep learning, expert systems, and many other techniques.",
    "At minimum, must address the following: Deep learning is a subset of machine learning which emphasizes the use of neural networks with many layers; since deep learning is a subset of machine learning, it is also a subset of AI."
]

exam_guidelines = [
    "Evaluate based on clarity, accuracy, and depth; higher marks for more depth without loss of accuracy.",
    "Provide informative feedback on the response that will help the student improve.",
    "Provide a Grade in the range 0-100."
]
#print(Schema.__annotations__)

# Create an instance of the Exam class using the AISchema
ai_exam = Exam(questions, question_guidelines, exam_guidelines, GradeLog)



