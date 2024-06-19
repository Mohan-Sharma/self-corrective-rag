# @author Mohan Sharma
import os
import sys

from dependency_injector import containers, providers

from com.crack.snap.make.config import get_settings
from com.crack.snap.make.graph.chains.answer_generation import AnswerGeneration
from com.crack.snap.make.graph.chains.answer_grader import AnswerGrader
from com.crack.snap.make.graph.chains.hallucination_grader import \
	HallucinationGrader
from com.crack.snap.make.graph.chains.retrieval_grader import RetrievalGrader
from com.crack.snap.make.graph.chains.router import Router
from com.crack.snap.make.graph.components.decide_generation import \
	DecideGeneration
from com.crack.snap.make.graph.components.grade_generation import \
	GradeGeneration
from com.crack.snap.make.graph.components.route_question import RouteQuestion
from com.crack.snap.make.graph.graph_service import GraphService
from com.crack.snap.make.graph.nodes.generate_answer import GenerateAnswer
from com.crack.snap.make.graph.nodes.grade_document import GradeDocument
from com.crack.snap.make.graph.nodes.retrieve_document import RetrieveDocument
from com.crack.snap.make.graph.nodes.web_search import WebSearch
from com.crack.snap.make.graph.tools.web_search_tool import WebSearchTool
from com.crack.snap.make.services.self_corrective_rag_service import \
	SelfCorrectiveRagService
from com.crack.snap.make.utils.utility import Utility


class Container(containers.DeclarativeContainer):
	
	@staticmethod
	def get_env():
		return os.environ.get("APP_ENV", "dev")
	
	env = providers.Callable(
		lambda: sys.argv[1] if len(sys.argv) > 1 else "dev"
	)
	
	settings = providers.Factory(get_settings, env=get_env())
	utility = providers.Factory(Utility, settings=settings)
	
	# tools
	web_search_tool = providers.Factory(WebSearchTool, settings=settings)
	
	# chain
	answer_generation = providers.Factory(AnswerGeneration)
	answer_grader = providers.Factory(AnswerGrader)
	hallucination_grader = providers.Factory(HallucinationGrader)
	retrieval_grader = providers.Factory(RetrievalGrader)
	router = providers.Factory(Router)
	
	# components
	decide_generation = providers.Factory(DecideGeneration, utility=utility)
	grade_generation = providers.Factory(GradeGeneration, utility=utility, hallucination_grader=hallucination_grader, answer_grader=answer_grader)
	route_question = providers.Factory(RouteQuestion, utility=utility)
	
	# nodes
	generate_answer = providers.Factory(GenerateAnswer, utility=utility, answer_generation=answer_generation)
	grade_document = providers.Factory(GradeDocument, utility=utility, retrieval_grader=retrieval_grader)
	retrieve_document = providers.Factory(RetrieveDocument, utility=utility)
	web_search = providers.Factory(WebSearch, utility=utility, web_search_tool=web_search_tool)
	
	# services
	graph_service = providers.Factory(GraphService, grade_generation=grade_generation, web_search=web_search, retrieve_document=retrieve_document, grade_document=grade_document, generate_answer=generate_answer, route_question=route_question, decide_generate=decide_generation)
	rag_service = providers.Factory(SelfCorrectiveRagService, settings=settings, utility=utility, graph_service=graph_service)

