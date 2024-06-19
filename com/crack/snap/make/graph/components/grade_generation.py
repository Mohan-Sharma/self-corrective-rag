# @author Mohan Sharma
from dependency_injector.wiring import inject

from com.crack.snap.make.graph.chains.answer_grader import AnswerGrader
from com.crack.snap.make.graph.chains.hallucination_grader import \
	HallucinationGrader
from com.crack.snap.make.utils.utility import Utility


class GradeGeneration:
	
	@inject
	def __init__(self, utility: Utility, hallucination_grader: HallucinationGrader, answer_grader: AnswerGrader):
		self.utility = utility
		self.hallucination_grader = hallucination_grader
		self.answer_grader = answer_grader
		
	def grade_generation_v_documents_and_question(self, state):
		"""
		Determines whether the generation is grounded in the document and answers question.
	
		Args:
			state (dict): The current graph state
	
		Returns:
			str: Decision for next node to call
		"""
		
		self.utility.console_rich_print("---CHECK HALLUCINATIONS---", "bold yellow")
		question = state["question"]
		documents = state["documents"]
		generation = state["generation"]
		
		score = self.hallucination_grader.hallucination_grader().invoke(
			{"documents": documents, "generation": generation}
		)
		grade = score["score"]
		
		# Check hallucination
		if grade == "yes":
			self.utility.console_rich_print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---", "bold yellow")
			# Check question-answering
			score = self.answer_grader.answer_grader().invoke(
				{"question": question, "generation": generation})
			grade = score["score"]
			if grade == "yes":
				self.utility.console_rich_print("---DECISION: GENERATION ADDRESSES QUESTION---", "bold yellow")
				return "useful"
			else:
				self.utility.console_rich_print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---", "bold yellow")
				return "not useful"
		else:
			self.utility.console_rich_print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---", "bold yellow")
			return "not supported"
