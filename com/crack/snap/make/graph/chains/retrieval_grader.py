# @author Mohan Sharma

from dependency_injector.wiring import inject
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

from com.crack.snap.make.vectorizer import get_llm


class RetrievalGrader:
	
	@inject
	def __init__(self):
		pass

	@staticmethod
	def retrieval_grader():
		retrieval_prompt = PromptTemplate(
			template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
			You are a grader assessing relevance of a retrieved document to a user question.
			If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant.
			Give a binary score of 'yes' or 'no'. 'Yes' means the document is relevant to the question.
			Provide the binary score as a JSON with a single key 'score' and no preamble or explanation
			<|eot_id|><|start_header_id|>Human<|end_header_id|>
			Retrieved document:
			
			{document}
			
			
			User question: {question}
			
			
			<|eot_id|><|start_header_id|>assistant<|end_header_id>
			""",
			input_variables=["question", "document"],
		)
		return retrieval_prompt | get_llm() | JsonOutputParser()
