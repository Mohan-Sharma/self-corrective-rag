# @author Mohan Sharma

from dependency_injector.wiring import inject
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

from com.crack.snap.make.vectorizer import get_llm


class AnswerGrader:
	
	@inject
	def __init__(self):
		pass

	@staticmethod
	def answer_grader():
		answer_grader_prompt = PromptTemplate(
			template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
			You are a grader assessing whether an answer addresses / resolves a question.
			Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question.
			Provide the binary score as a JSON with a single key 'score' and no preamble or explanation.
			<|eot_id|><|start_header_id|>user<|end_header_id|> Here is the answer:
			
			
			{generation}
			
			
			Here is the question: {question}
			
			<|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
			input_variables=["generation", "question"],
		)
		return answer_grader_prompt | get_llm() | JsonOutputParser()
