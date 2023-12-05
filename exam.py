from dataclasses import dataclass
from typing import List, Type
import json

@dataclass
class GradeLog:
    TA: str
    Student: str
    Prompt: str
    Response: str
    Notes: str
    Grade: int

class Exam:
    def __init__(self, questions: List[str], question_guidelines: List[str], exam_guidelines: List[str], schema: GradeLog):
        assert issubclass(schema, GradeLog), "Provided schema must be a subclass of Schema or Schema itself."

        self.questions = questions
        self.question_guidelines = question_guidelines
        self.exam_guidelines = exam_guidelines
        self.schema = GradeLog
    
    def summarize_exam(self):
        print("Exam Guidelines:")
        for guideline in self.exam_guidelines:
            print(f"\t{guideline}")
        print("Questions:")
        for i, question in enumerate(self.questions):
            print(f"\t{i+1}. {question}")
            print(f"\t\t{self.question_guidelines[i]}")
    
    def dump_exam(self):
        """Returns a string representation of the exam packages as json"""
        return json.dumps(self.__dict__)

    # Additional methods can be added here
class Scenario:
    """This class is used to create an examination where the TA and Student's interact in a simulated Scenario."""
    def __init__(self, scenario: str, scenario_guidelines: List[str], roles: List[str],role_guidelines:List[str], schema: GradeLog):
        self.roles = roles #List of roles each with private backstory
        self.scenario = scenario #Public Backstory available to all roles
        self.scenario_guidelines = scenario_guidelines  
        self.role_guidelines = role_guidelines #Role specific guidelines for evaluating the actions
        self.schema = schema

    def summarize_scenario(self):
        print("Scenario Guidelines:")
        for guideline in self.scenario_guidelines:
            print(f"\t{guideline}")
        print("Roles:")
        for i, role in enumerate(self.roles):
            print(f"\t{i+1}. {role}")
            print(f"\t\t{self.role_guidelines[i]}")
    
    def dump_scenario(self):
        """Returns a string representation of the scenario packages as json"""
        return json.dumps(self.__dict__)

    def dump_roles(self):
        """Returns a list of strings, each string is a role with the scenario and role context appended"""
        return [self.dump_scenario+"\n You are roleplaying the following character: \n"+role for role in self.roles]
        