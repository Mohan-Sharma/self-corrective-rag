# @author Mohan Sharma
from com.crack.snap.make.config import CommonSettings
from com.crack.snap.make.graph.graph_service import GraphService
from com.crack.snap.make.utils.utility import Utility
from dependency_injector.wiring import inject
from rich.console import Console


class SelfCorrectiveRagService:
	
	@inject
	def __init__(self, settings: CommonSettings, utility: Utility, graph_service: GraphService):
		self.settings = settings
		self.console = Console()
		self.utility = utility
		self.graph_service = graph_service
		
	def generate(self, user_message: str) -> str:
		try:
			inputs = {"question": user_message}
			state_graph = self.graph_service.create_graph()
			for output in state_graph.stream(inputs):  # type: ignore
				for key, value in output.items():
					self.utility.console_rich_print(f"Finished running: {key}:", "bold green")
			# Final generation
			generation_ = value["generation"]
			self.utility.console_rich_print(generation_, "bold green")
			return f"{generation_}"
		except Exception as e:
			self.utility.console_rich_print(f"Error: {e}", "bold red")
			return "Sorry I am unable to generate the answer for you..."
