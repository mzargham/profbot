from typing import List, Type
from exam import Exam, Schema
from os import environ
import requests
class Llm:
    def __init__(self, model_identifier: str):
        self.model_identifier = model_identifier
        # Initialize other necessary attributes and connect to the LLM if needed

    def prompt(self, text: str) -> str:
        # Method to send a prompt to the LLM and return its response
        url = 'https://api.openai.com/v1/chat/completions'
        req = {
            "model": "gpt-4-1106-preview",
            "messages":[
                {"role": "user", "content": text}
            ]
        }
        response = requests.post(url, req, headers={"Authorization": f"Bearer {environ.get('OPENAI_API_KEY')}"})
        return f"Response to: {response.json()['choices'][0]['message']['content']}"

class LLMTest:
    def __init__(self, student_llm: Llm, ta_llm: Llm, exam: Exam):
        self.student_llm = student_llm
        self.ta_llm = ta_llm
        self.exam = exam

    def test(self) -> List[Type[Schema]]:
        student_responses = [self.student_llm.prompt(question) for question in self.exam.questions]
        graded_responses = []

        for question, student_response in zip(self.exam.questions, student_responses):
            grading_prompt = self.format_grading_prompt(question, student_response)
            ta_response = self.ta_llm.prompt(grading_prompt)
            graded_responses.append(self.process_ta_response(ta_response))

        return graded_responses

    def format_grading_prompt(self, question: str, response: str) -> str:
        # Format the grading prompt for the TA LLM
        return f"Question: {question}\nResponse: {response}\nGuidelines: {self.exam.exam_guidelines}"

    def process_ta_response(self, ta_response: str) -> Type[Schema]:
        # Process the TA's response and return it in the schema format
        # Placeholder implementation; this should be tailored to parse the actual TA's response
        notes = "Extracted notes from TA's response"
        grade = 100  # Dummy value; extract the actual grade from the TA's response
        return self.exam.schema(Prompt="", Response="", Notes=notes, Grade=grade)

# Example usage (pseudo-code, adjust as per actual implementation)
# student_llm = Llm("student_model_identifier")
# ta_llm = Llm("ta_model_identifier")
# llm_test = LLMTest(student_llm, ta_llm, some_exam_instance)
# test_results = llm_test.test()
