# @author Mohan Sharma
from dependency_injector.wiring import inject
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

from com.crack.snap.make.vectorizer import get_llm


class HallucinationGrader:
	
	@inject
	def __init__(self):
		pass

	@staticmethod
	def hallucination_grader():
		hallucination_prompt = ChatPromptTemplate.from_messages(
			[
				("system", "You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts. \n Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by the set of facts. Provide the binary score of 'yes' or 'no' as a JSON with a single key 'score' and no preamble or explanation or empty string."),
				("human", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}"),
			]
		)
		return hallucination_prompt | get_llm() | JsonOutputParser()

#hallucination_prompt = PromptTemplate(
#	template=""" <|begin_of_text|><|start_header_id|>system<|end_header_id|>
#	You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts.
#	Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by the set of facts.
#	Provide the binary score 'yes' or 'no' as a JSON with a single key 'score' and no preamble or explanation.
#	<|eot_id|><|start_header_id|>user<|end_header_id|>
#    Here are the facts:
#
#
#    {documents}
#
#
#    Here is the answer: {generation}  <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
#	input_variables=["generation", "documents"],
#)


