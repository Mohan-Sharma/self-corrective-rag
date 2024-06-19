# @author Mohan Sharma

from dependency_injector.wiring import inject
from langchain_community.tools.tavily_search import TavilySearchResults

from com.crack.snap.make.config import CommonSettings


class WebSearchTool:
	
	@inject
	def __init__(self, settings: CommonSettings):
		self.settings = settings

	def web_search_tool(self):
		return TavilySearchResults(k=5)

