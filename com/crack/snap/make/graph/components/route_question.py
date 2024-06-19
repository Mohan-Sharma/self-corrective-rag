# @author Mohan Sharma

from dependency_injector.wiring import inject

from com.crack.snap.make.utils.utility import Utility


class RouteQuestion:
	
	@inject
	def __init__(self, utility: Utility):
		self.utility = utility
	
	def route_question(self, state):
		"""
		Route question to web search or RAG.
	
		Args:
			state (dict): The current graph state
	
		Returns:
			str: Next node to call
		"""
		
		self.utility.console_rich_print("---ROUTE QUESTION---", "bold yellow")
		question = state["question"]
		self.utility.console_rich_print(question, "bold green")
		return "vectorstore"


#source = question_router.invoke({"question": question})
#print(source)
#print(source["datasource"])
#if source["datasource"] == "web_search":
#	print("---ROUTE QUESTION TO WEB SEARCH---")
#	return "websearch"
#elif source["datasource"] == "vectorstore":
#	print("---ROUTE QUESTION TO RAG---")
#	return "vectorstore"
