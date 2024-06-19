# @author Mohan Sharma

from dependency_injector.wiring import inject
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from com.crack.snap.make.vectorizer import get_llm


class AnswerGeneration:
	
	@inject
	def __init__(self):
		pass

	@staticmethod
	def generation():
		generation_prompt = PromptTemplate(
			template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
			You are an assistant for question-answering tasks.
			Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know.
			<|eot_id|><|start_header_id|>user<|end_header_id|>
			Question: {question}


			Context:  {context}


			Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id>""",
			input_variables=["question", "context"],
		)
		return generation_prompt | get_llm() | StrOutputParser()


#
# rag_prompt = ChatPromptTemplate.from_messages([
# 	("human",
# 	 """You are an assistant for question-answering tasks.
# 		Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know.
#
# 	    Question: {question}
#     	Context: {context}
# 	 	Answer:"""),
# ])

