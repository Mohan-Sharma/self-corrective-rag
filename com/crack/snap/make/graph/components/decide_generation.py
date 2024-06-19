# @author Mohan Sharma
from dependency_injector.wiring import inject

from com.crack.snap.make.utils.utility import Utility


class DecideGeneration:

	@inject
	def __init__(self, utility: Utility):
		self.utility = utility
	
	def decide_to_generate(self, state):
		"""
		Determines whether to generate an answer, or add web search
	
		Args:
			state (dict): The current graph state
	
		Returns:
			str: Binary decision for next node to call
		"""
		
		self.utility.console_rich_print("---ASSESS GRADED DOCUMENTS---", "bold yellow")
		question = state["question"]
		web_search = state["web_search"]
		filtered_documents = state["documents"]
		
		if web_search == "Yes":
			# All documents have been filtered check_relevance
			# We will re-generate a new query
			self.utility.console_rich_print("---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, INCLUDE WEB SEARCH---", "bold yellow")
			return "websearch"
		else:
			# We have relevant documents, so generate answer
			self.utility.console_rich_print("---DECISION: GENERATE---", "bold yellow")
			return "generate"

