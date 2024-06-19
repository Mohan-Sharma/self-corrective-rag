# @author Mohan Sharma
from dependency_injector.wiring import inject
from langchain_core.documents import Document

from com.crack.snap.make.graph.tools.web_search_tool import WebSearchTool
from com.crack.snap.make.utils.utility import Utility


class WebSearch:
	
	@inject
	def __init__(self, utility: Utility, web_search_tool: WebSearchTool):
		self.web_search_tool = web_search_tool
		self.utility = utility
	
	def web_search(self, state):
		"""
		Web search based based on the question
	
		Args:
			state (dict): The current graph state
	
		Returns:
			state (dict): Appended web results to documents
		"""
		
		print("---WEB SEARCH---")
		question = state["question"]
		documents = state["documents"]
		
		# Web search
		docs = self.web_search_tool.web_search_tool().invoke({"query": question})
		web_results = "\n".join([d["content"] for d in docs])
		web_results = Document(page_content=web_results)
		if documents is not None:
			documents.append(web_results)
		else:
			documents = [web_results]
		return {"documents": documents, "question": question}

