# @author Mohan Sharma
from dependency_injector.wiring import inject

from com.crack.snap.make.graph.chains.answer_generation import AnswerGeneration
from com.crack.snap.make.utils.utility import Utility


class GenerateAnswer:
	
	@inject
	def __init__(self, utility: Utility, answer_generation: AnswerGeneration):
		self.utility = utility
		self.answer_generation = answer_generation
	
	def generate(self, state):
		"""
		Generate answer using RAG on retrieved documents
	
		Args:
			state (dict): The current graph state
	
		Returns:
			state (dict): New key added to state, generation, that contains LLM generation
		"""
		self.utility.console_rich_print("---GENERATE---", "bold yellow")
		question = state["question"]
		documents = state["documents"]
		
		# RAG generation
		generation = self.answer_generation.generation().invoke({"context": documents, "question": question})
		
		return {"documents": documents, "question": question, "generation": generation}
