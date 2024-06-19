# @author Mohan Sharma
from dependency_injector.wiring import inject

from com.crack.snap.make.graph.chains.retrieval_grader import RetrievalGrader
from com.crack.snap.make.utils.utility import Utility


class GradeDocument:
	
	@inject
	def __init__(self, utility: Utility, retrieval_grader: RetrievalGrader):
		self.utility = utility
		self.retrieve_grader = retrieval_grader
	
	def grade_documents(self, state):
		"""
		Determines whether the retrieved documents are relevant to the question
		If any document is not relevant, we will set a flag to run web search
		
		Args:
			state (dict): The current graph state
		
		Returns:
			state (dict): Filtered out irrelevant documents and updated web_search state
		"""
		
		self.utility.console_rich_print("---GRADE DOCUMENT---", "bold yellow")
		question = state["question"]
		documents = state["documents"]
		
		# Score each doc
		filtered_docs = []
		web_search = "No"
		for d in documents:
			score = self.retrieve_grader.retrieval_grader().invoke(
				{"question": question, "document": d.page_content}
			)
			grade = score["score"]
			# Document relevant
			if grade.lower() == "yes":
				self.utility.console_rich_print("---GRADE: DOCUMENT RELEVANT---", "bold yellow")
				filtered_docs.append(d)
			# Document not relevant
			else:
				self.utility.console_rich_print("---GRADE: DOCUMENT NOT RELEVANT---", "bold bright_red")
				# We do not include the document in filtered_docs
				# We set a flag to indicate that we want to run web search
				continue
		# if length of filtered_docs is not 0, we will run web search
		if len(filtered_docs) == 0:
			web_search = "Yes"
		
		return {"documents": filtered_docs, "question": question,
				"web_search": web_search}
