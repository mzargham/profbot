from typing import List, Type
from exam import Exam, Schema
from os import environ
import requests

class Llm:
    def __init__(self, model_identifier: str = "gpt-4-1106-preview", 
                 url: str = "https://api.openai.com/v1/chat/completions", 
                 role: str = "user",
                 auth: dict = {"Authorization": f"Bearer {environ.get('OPENAI_API_KEY')}"}):
        
        self.model_identifier = model_identifier
        self.url = url
        self.role = role
        self.auth = auth

    #add setters and getters for the above attributes
    # Getter for model_identifier
    @property
    def model_identifier(self):
        return self._model_identifier

    # Setter for model_identifier
    @model_identifier.setter
    def model_identifier(self, value):
        self._model_identifier = value

    # Getter for url
    @property
    def url(self):
        return self._url

    # Setter for url
    @url.setter
    def url(self, value):
        self._url = value

    # Getter for role
    @property
    def role(self):
        return self._role

    # Setter for role
    @role.setter
    def role(self, value):
        self._role = value

    # Getter for auth
    @property
    def auth(self):
        return self._auth

    # Setter for auth
    @auth.setter
    def auth(self, value):
        self._auth = value
        
    def prompt(self, text: str) -> str:
        # Method to send a prompt to the LLM and return its response
        url = self.url
        req = {
            "model": self.model_identifier,
            "messages":[
                {"role": self.role, "content": text}
            ]
        }
        print(req)
        response = requests.post(url, json=req, headers=self.auth)  # Use json parameter to send the request payload as JSON
        raw =  response.json()
        try:
            return f"{response.json()['choices'][0]['message']['content']}"
        except:
            return raw
        
    def prompt_sequence(self, prompts: List[str]) -> str:
        """
        Method to send a sequence of prompts to the LLM and return its response.
        Each prompt in the sequence is sent as a separate message in a single request.
        """
        url = self.url
        messages = [{"role": self.role, "content": prompt} for prompt in prompts]
        
        req = {
            "model": self.model_identifier,
            "messages": messages
        }
        print(req)
        response = requests.post(url, json=req, headers=self.auth)  # Use json parameter to send the request payload as JSON
        raw = response.json()
        try:
            return [resp['message']['content'] for resp in raw['choices']]
        except:
            return raw

#this is still full of dummy data (but it runs!)
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
