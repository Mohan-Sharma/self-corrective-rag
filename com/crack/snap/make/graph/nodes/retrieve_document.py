# @author Mohan Sharma
import logging

from dependency_injector.wiring import inject

from com.crack.snap.make.utils.utility import Utility
from com.crack.snap.make.vectorizer import get_retriever


class RetrieveDocument:
	
	@inject
	def __init__(self, utility: Utility):
		self.utility = utility
	
	def retrieve(self, state):
		"""
		Retrieve documents from vectorstore
	
		Args:
			state (dict): The current graph state
	
		Returns:
			state (dict): New key added to state, documents, that contains retrieved documents
		"""
		self.utility.console_rich_print("---RETRIEVE---", "bold yellow")
		question = state["question"]
		
		# Retrieval
		#multi_query_retriever = MultiQueryRetriever(retriever=get_retriever(), llm_chain=llm_chain, parser_key="lines")
		#logging.basicConfig()
		#logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)
		logging.getLogger("langchain.output_parsers").setLevel(logging.INFO)
		documents = get_retriever().invoke(question)
		return {"documents": documents, "question": question}
