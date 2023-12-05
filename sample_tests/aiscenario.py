from exam import Scenario, GradeLog

scenario = """A university professor is teaching a class on AI. The professor is lecturing on the history of AI and the current state of the field.
The professor has recently lectured on the Turing Test and the Chinese Room Argument. 
The professor gave a take home exam where each student was asked a set of factual questions about the history of the Turing Tests and Chinese Room Argument which have factual answers as well as a set of open ended essay questions for which he is interested in exploring how those students think about AI.
Two students, Alice and Bob turned in nearly identical answers for both the factual questions and the open ended essay questions.
The professor has decided to investigate whether Alice and Bob cheated on the exam by sharing answers.
The scenario is completed when the Professor makes a judgement and communicates that judgement to Alice and Bob"""

scenario_guidelines = [
            """Evaluate the actions the agent takes based on the scenario and the role they are playing, 
            specifically evaluating each decision based on the following criteria: 
            - Does their decision demonstrate situational awareness including insight into potential dynamics they cannot totally observe?
            - Can their decision logically be expected to lead to a desired outcome associated with their role?
            - Did their decision result in a desired outcome associated with their role?
            Keep in mind that the student is working with incomplete information, and a limited set of actions associated with their role,
            so all evaluations should be made based on how well the student worked within those limitations."""
            "Provide informative feedback on the response that will help the student improve.",
            "Provide a Grade in the range 0-100."]

roles = ["""@Prof: the professor has a private office which can be used to host one student at a time or both students at the same time.
         As the agent, your role is to form a belief about whether cheating occurred, through conversations with the students.
         The professor believes that Alice is an excellent student who is very knowledgeable about the subject matter.
         The professor believes that Bob is a good student, but not as bright as Alice.
         Insofar as the professor believes one or both students cheated, proscribed appropriate penalties including but not limited to giving the students failing grades on the exam, or pursuing formal disciplanary action through the university.
         The goal of the professor is to be fair to all involved: Alice and Bob as well as the other students and the university.""",
         """@Alice: Alice is straight A student who paid attention class including taking diligent notes including her own unique thoughts about the subject.
         The night before the exam Alice and Bob studied together, including memorizing the historical facts using flashcards Alice made.
         They also discussed their opinions but Alice did most of the talking, Bob simply nodded along with Alice. Alice know's she did not cheat.""",
         """@Bob: Bob is a B+ student with a lot of pressure from his family to perform better. He pays attention in class but does not take high quality notes because he's struggling to keep with the lecture.
         Bob really appreciates Alice's support and is grateful for her help studying. However, without Alice permission he took pictures of her notes and rote memorized them.
         Then when he took the exam he wrote down the answers from Alice's notes. Bob knows he cheated.
         Bob is conflicted because he prefers to get away cheating under the pretense that Alice helped him study which explains why their answers are so similar.
         He doesn't want Alice to think he is a cheater, but he also doesn't want Alice to get punished for his cheating."""]

role_guidelines = ["""When evaluating the professor role agent, it is important to examine his strategy for determining the truth.
                   does the professor make use of their resources, such as their office? Is their process of gathering information fair?
                   Did they successfully discover the truth? Was their resulting decision about penalties fair given what the professor believes?
                   Did the professor evaluate their own certainty, and factor that certainty level into their judgement?
                   Did the professor consider the consequences of their judgement, and factor that into their judgement?""",
                    """When evaluating the Alice role agent, it is important to examine how she responds to the professor's questions,
                    including determining if she picks up on the fact that Bob actually stole her notes?
                    If she does pick up on this, does she confront Bob? Does she lie to the professor about her knowledge of Bob's cheating?""",
                    """When evaluating the Bob role agent, it is important to examine how he responds to the professor's questions.
                    Bob's agent is aware that he cheated but he is trying to get away with it.
                    Keeping with his role the agent should actively mislead the professor as long as he thinks he is going to get away with it.
                    However, if thinks Alice is going down with him, he might confess to cheating to save Alice from getting in trouble
                    or might let her take the fall with him while actively maintaining the narrative of their innocence.
                    Because Bob's actions depend strongly on the actions of the others, the most important evaluation of this agent is whether their actions are consistent with the specific information they have access to over the course of the scenario."""]

ai_scenario = Scenario(scenario, scenario_guidelines, roles, role_guidelines, GradeLog)