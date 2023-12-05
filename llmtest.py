from typing import List, Type
from exam import Exam, Scenario, GradeLog
from os import environ
import requests
import re
#import json
from dataclasses import dataclass

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

class LLMTest:
    def __init__(self, student_llm: Llm, ta_llm: Llm, exam: Exam):
        self.student_llm = student_llm
        self.ta_llm = ta_llm
        self.exam = exam

    def test(self) -> List[Type[GradeLog]]:
        student_responses = self.student_llm.prompt_sequence(self.exam.questions)
        graded_responses = self.ta_llm.prompt_sequence(self.format_grading_prompt_sequence(student_responses))
        standardized_responses = [self.process_ta_response(self.exam.questions[i], student_responses[i], graded_responses[i+1]) for i in range(len(self.exam.questions))]

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
       

    def process_ta_response(self, question, student_response, ta_response: str) -> Type[GradeLog]:
        # Process the TA's response and return it in the schema format
        # Placeholder implementation; this should be tailored to parse the actual TA's response
        def process_string(input_str: str):
            # Regex pattern to find 'Grade' followed by an integer
            pattern = r"Grade: (\d+)"

            # Search for the pattern in the input string
            match = re.search(pattern, input_str)

            if match:
                # Extract the grade
                grade = int(match.group(1))

                # Cut the 'Grade' portion out of the string
                notes = input_str.replace(match.group(0), '').strip()

                return notes, grade
            else:
                # Return the original string and a default grade if 'Grade' not found
                return input_str, None
        
        notes, grade = process_string(ta_response)

        return GradeLog(TA= self.ta_llm.model_identifier,
                                Student= self.student_llm.model_identifier,
                                Prompt=question,
                                Response=student_response, 
                                Notes=notes, 
                                Grade=grade)

#LLMtest works for Exam Class, we need a class LLMroleplay that works for Scenario class
class LLMRoleplay:
    def __init__(self, llm_agents: List[Llm], llm_umpire:Llm, scenario: Scenario):
        assert(len(llm_agents) == len(scenario.roles))
        self.llm_agents = llm_agents
        self.scenario = scenario
        self.llm_umpire = llm_umpire

    #since this is a roleplay, we need to have a play method instead of test method
    def play(self, force_stop_N: int = 100) -> List[Type[GradeLog]]:
        #notes:
        #for games with more than 2 roles, we need to have multiple communication channels
        #the set of communication channels is the power set of the set of llms (excluding the empty set)
        #situations can arise where the agents need to split into smaller groups or rejoin larger groups
        #the game ends when the scenario completion criteria occurs
        #the umpire is responsible for orchestrating the communication channels as well as determining when the game ends
        #the umpire is also responsible for evaluating the actions of the agents
        #the umpire is also responsible for providing feedback to the agents
        #the umpire is also responsible for providing a grade to each agent

        @dataclass
        class Agent:
            name: str
            llm: Llm
            context: str

        def speak(speaker, audience:List[Agent], message:str = "What do you say to them?") -> str:
            prompt = "Everything you know so far is:\n"+speaker.context+"\n the following agents can hear you: "+str([a.name for a in audience])+"\n"+message
            return self.llm.prompt(prompt)
        
        @dataclass
        class Storyline:
            channel: List[Agent] #list of llms that are present in the current communication channel
            speaker: List[Agent] #ordered list of speakers for each message in the current communication channel
            messages: List[str] #ordered list of messages in the current communication channel (must match the order of speakers)
        
        storytracker = True
        gametracker = True
        
        #initialize the agents
        #use regex to pull the names of the agents out of self.scenario.roles
        names = [re.search(r'@(\w+)', role).group(1) for role in self.scenario.roles]
        agents = [Agent(name=name, llm=self.llm_agents[i], context=self.scenario.dump_roles()[i]) for i, name in enumerate(names)]

        ump_role_brief = """\n You are roleplaying the umpire 
        the umpire is responsible for orchestrating the communication channels as well as determining when the game ends.
        You will be prompting the other agents, to indicate which agent should speak next,
        the names of the agents:"""+[str(agent) for agent in agents]+"""
        you can do one of 3 things:
        - prompt the next agent to speak by typing @name_of_agent: then a prompt for that agent
        - change the communication channel by typing #change_channel: then a list of agents in the new channel along with a text statement describing the circumstance of the new channel
        - end the game by typing #end_game: then a text statement describing the reason for ending the game"""

        ump = Agent(name = "umpire", llm = self.llm_umpire, context = self.scenario.dump_scenario()+ump_role_brief)

        # #method to parse the umpire's response using regex
        # def parse_umpire_response(response: str) -> str:
        #     # first check if the game is over
        #     if re.search(r'#end_game', response):
        #         return "game over"
        #     # next check if the communication channel is changing
        #     elif re.search(r'#change_channel', response):
        #         # if so, extract the new channel and update the storyline
        #         new_channel = re.search(r'#change_channel: (.*)', response).group(1)
        #         #update the storyline
        #         return "communication channel changed"
        #     # otherwise, prompt the next agent to speak
        #     else:
        #         next_agent = re.search(r'@(\w+)', response).group(1)
        #         return "prompting "+next_agent+" to speak"

        #method to evaluate a message from the umpire to determine if the game is over
        def evaluate_umpire_message_for_end_game(message: str) -> bool:
            if re.search(r'#end_game', message):
                return True
            else:
                return False
        
        def evaluate_umpire_message_for_channel_change(message: str) -> bool:
            if re.search(r'#change_channel', message):
                return True
            else:
                return False
            
        def extract_new_channel(message: str) -> List[Agent]:
            new_channel = re.search(r'#change_channel: (.*)', message).group(1)
            return new_channel
        
        def iterate_storyline(storyline:Storyline)->Storyline:
            #first check if the game is over
            if evaluate_umpire_message_for_end_game(storyline.messages[-1]):
                gametracker = False
                return storyline
            #next check if the communication channel is changing
            elif evaluate_umpire_message_for_channel_change(storyline.messages[-1]):
                #if so, extract the new channel and update the storyline
                new_channel = extract_new_channel(storyline.messages[-1])
                #update the storyline
                prompt = speak(ump, storyline.channel, "explain that the communication channel is changing to "+new_channel)
                storytracker = False
                return Storyline(channel = new_channel, speaker = storytracker.speaker+[ump], messages = storyline.messages+prompt)
            #otherwise, prompt the next agent to speak
            else:
                next_agent = re.search(r'@(\w+)', storyline.messages[-1]).group(1)
                return Storyline(channel = storyline.channel, speaker = next_agent, messages = speak(next_agent, storyline.channel))

        def narrate(history:List[Storyline], new_channel:List[Agent]= agents)->Storyline:

            if len(history)==0:
                prompt = speak(ump, new_channel, "Provide introductory narration to kick off the scenario. be sure to indicate who will speak first.")
                
            elif len(history)>force_stop_N:
                return Storyline(channel = agents, speaker = ump, messages = "#end_game: force stop")
            
            else:
                prompt = speak(ump, new_channel, "Provide narration to continue the scenario. be sure to indicate who will speak next.")
            
            #initialize new storyline
            s = Storyline(channel = new_channel, speaker = ump, messages = prompt)
            






        


