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
        
    # def prompt_sequence(self, prompts: List[str]) -> List[str]:
    #     """
    #     Method to send a sequence of prompts to the LLM and return its response.
    #     Each prompt in the sequence is sent as a separate message in a single request.
    #     """
    #     url = self.url
    #     messages = [{"role": self.role, "content": prompt} for prompt in prompts]
        
    #     req = {
    #         "model": self.model_identifier,
    #         "messages": messages
    #     }
    #     print(req)
    #     response = requests.post(url, json=req, headers=self.auth)  # Use json parameter to send the request payload as JSON
    #     raw = response.json()
    #     print(raw)
    #     try:
    #         return [resp['message']['content'] for resp in raw['choices']]
    #     except:
    #         return raw
        
    def prompt_sequence(self, prompts: List[str]) -> List[str]:
        """
        Method to send a sequence of prompts to the LLM and return its responses.
        Each prompt is sent in a separate request, maintaining the conversation history.
        """
        conversation_history = []
        responses = []

        for prompt in prompts:
            # Concatenate all previous elements of the conversation for context
            full_prompt = " ".join(conversation_history + [prompt])

            # Create the request payload
            req = {
                "model": self.model_identifier,
                "messages": [{"role": self.role, "content": full_prompt}]
            }

            response = requests.post(self.url, json=req, headers=self.auth)
            raw = response.json()

            try:
                # Extract the response content
                content = raw['choices'][0]['message']['content']
                responses.append(content)
                # Update the conversation history
                conversation_history.append(prompt)
                conversation_history.append(content)
            except:
                # In case of an error, append the raw response for debugging
                responses.append(raw)

        return responses


#this is still full of dummy data (but it runs!)
class LLMTest:
    def __init__(self, student_llm: Llm, ta_llm: Llm, exam: Exam):
        self.student_llm = student_llm
        self.ta_llm = ta_llm
        self.exam = exam

    def test(self) -> List[Type[Schema]]:
        student_responses = self.student_llm.prompt_sequence(self.exam.questions)

        graded_responses = self.ta_llm.prompt_sequence(self.format_grading_prompt_sequence(student_responses))

        standardized_responses = [self.process_ta_response(response) for response in graded_responses]

        return standardized_responses

    
    def format_grading_prompt_sequence(self, responses: str) -> str:
        assert(len(self.exam.questions) == len(responses))
        # Format the grading prompt for the TA LLM
        context_str = """You are grading an exam. For each of the follow question:response pairs please provide a grade and notes for the student.
         the grade and the notes for every question should evaluated according to the following guidelines:"""
        context_str += "\n".join(self.exam.exam_guidelines)+"\n As the TA, the professor will be evaluating your evaluations as part of your teaching practicum; your PhD candidacy depends on this. Are you ready to begin?"

        def format_grading_prompt(question: str, response: str, guideline: str) -> str:
            prompt_str = "Question: "+question+"\n received the following response: "+response+"\n Please provide a grade and notes for the student, according to the following guidelines: "+guideline

            return prompt_str
        
        sequence = [context_str]+[format_grading_prompt(self.exam.questions[i], responses[i], self.exam.question_guidelines[i]) for i in range(len(self.exam.questions))]
        return sequence   
       

    def process_ta_response(self, ta_response: str) -> Type[Schema]:
        # Process the TA's response and return it in the schema format
        # Placeholder implementation; this should be tailored to parse the actual TA's response
        notes = "Extracted notes from TA's response"
        grade = 100  # Dummy value; extract the actual grade from the TA's response
        return self.exam.schema(Prompt="", Response="", Notes=notes, Grade=grade)
