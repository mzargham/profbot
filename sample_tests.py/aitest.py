from llmtest import Llm, LLMTest
from aiexam import ai_exam

# Create instances of the Llm class for both the student and the TA
student_llm = Llm("student_model_identifier")  # Replace with actual model identifier or configuration
ta_llm = Llm("ta_model_identifier")           # Replace with actual model identifier or configuration

# Create an instance of the LLMTest class with the student LLM, TA LLM, and the AI exam
llm_test = LLMTest(student_llm, ta_llm, ai_exam)

# Conduct the test
test_results = llm_test.test()

# Output the results
for result in test_results:
    print(result)
