# @author Mohan Sharma

from com.crack.snap.make.config import CommonSettings
from dependency_injector.wiring import inject
from rich.console import Console


class Utility:
	
	@inject
	def __init__(self, settings: CommonSettings):
		self.console = Console()
		self.settings = settings
		
	def console_rich_print(self, message, style) -> None:
		return self.console.print(message, style=style)
