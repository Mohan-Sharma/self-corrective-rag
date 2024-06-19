from dependency_injector.wiring import inject
from langgraph.graph import END, StateGraph

from com.crack.snap.make.graph.components import route_question
from com.crack.snap.make.graph.components.decide_generation import \
	DecideGeneration
from com.crack.snap.make.graph.components.grade_generation import \
	GradeGeneration
from com.crack.snap.make.graph.components.route_question import RouteQuestion
from com.crack.snap.make.graph.nodes import web_search
from com.crack.snap.make.graph.nodes.generate_answer import GenerateAnswer
from com.crack.snap.make.graph.nodes.grade_document import GradeDocument
from com.crack.snap.make.graph.nodes.retrieve_document import RetrieveDocument
from com.crack.snap.make.graph.nodes.web_search import WebSearch
from com.crack.snap.make.model.graph_state import GraphState


class GraphService:
	
	@inject
	def __init__(self, grade_generation: GradeGeneration, web_search: WebSearch, retrieve_document: RetrieveDocument
		, grade_document: GradeDocument, generate_answer: GenerateAnswer, route_question: RouteQuestion, decide_generate: DecideGeneration):
		self.workflow = StateGraph(GraphState)
		self.grade_generation = grade_generation
		self.web_search = web_search
		self.retrieve_document = retrieve_document
		self.grade_document = grade_document
		self.generate_answer = generate_answer
		self.route_question = route_question
		self.decide_generate = decide_generate
		
	
	def create_graph(self):
		# Create the graph
		
		# Define the nodes
		self.workflow.add_node("websearch", self.web_search.web_search)  # web search
		self.workflow.add_node("retrieve", self.retrieve_document.retrieve)  # retrieve
		self.workflow.add_node("grade_documents", self.grade_document.grade_documents)  # grade documents
		self.workflow.add_node("generate", self.generate_answer.generate)  # generatae
		
		# Build graph
		self.workflow.set_conditional_entry_point(
			self.route_question.route_question,
			{
				"websearch": "websearch",
				"vectorstore": "retrieve",
			},
		)
		
		self.workflow.add_edge("retrieve", "grade_documents")
		self.workflow.add_conditional_edges(
			"grade_documents",
			self.decide_generate.decide_to_generate,
			{
				"websearch": "websearch",
				"generate": "generate",
			},
		)
		self.workflow.add_edge("websearch", "generate")
		self.workflow.add_conditional_edges(
			"generate",
			self.grade_generation.grade_generation_v_documents_and_question,
			{
				"not supported": "websearch",
				"useful": END,
				"not useful": "websearch",
			},
		)
		
		## Compile
		app = self.workflow.compile()
		
		return app
	


def export_to_mermaid(graph):
	mermaid_lines = ["graph TD"]
	
	# Add nodes
	for node in graph.nodes:
		mermaid_lines.append(f"{node}({node})")
	
	# Add edges
	for edge in graph.edges:
		source, target = edge
		mermaid_lines.append(f"{source} --> {target}")
	
	return "\n".join(mermaid_lines)


# Create the Mermaid graph definition
#mermaid_graph = export_to_mermaid(workflow)
#mermaid_file = "workflow_graph.mmd"
## Save the Mermaid definition to a file
#with open(mermaid_file, "w") as f:
#	f.write(mermaid_graph)


## Use the Mermaid CLI to generate a PNG image
#png_file = "workflow_graph.png"
#os.system(f"mmdc -i {mermaid_file} -o {png_file}")
#
## Display the image in Jupyter Notebook
#try:
#	display(Image(png_file))
#except Exception as e:
#	print(f"Failed to display image: {e}")
