# @author Mohan Sharma

from dependency_injector.wiring import inject
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

from com.crack.snap.make.vectorizer import get_llm


class Router:
	
	@inject
	def __init__(self):
		pass

	@staticmethod
	def question_router():
		question_router = PromptTemplate(
			template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an expert at routing a
	user question to a vectorstore or web search. Use the vectorstore for questions on system designs or anything related to software architecture or related semantics or work agreements. You do not need to be stringent with the keywords
	in the question related to these topics. Otherwise, use web-search. Give a binary choice 'web_search'
	or 'vectorstore' based on the question. Return the a JSON with a single key 'datasource' and
	no premable or explanation. Question to route: {question} <|eot_id|><|start_header_id|>assistant<|end_header_id>""",
			input_variables=["question"],
		)
		return question_router | get_llm() | JsonOutputParser()

