# @author Mohan Sharma
import argparse
import os
import shutil
import sys

from com.crack.snap.make.utils.utility import Utility
from com.crack.snap.make.config import DevSettings
from langchain.schema.document import Document
from langchain_community.chat_models import ChatOllama
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter

__EMBEDDING_MODEL = 'nomic-embed-text'
__CHROMA_PATH = "./.chroma"
__local_llm = "llama3"


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("--clear", action="store_true",
						help="Reset the database.")
	parser.add_argument("pdf_folder_path", type=str, nargs='?',
						help="Path of the pdf folder")
	args = parser.parse_args()
	
	if not args.pdf_folder_path and not args.clear:
		parser.error(
			'No action requested, upload-pdfs | [-h] | [--clear] | pdf_folder_path')
	
	if args.clear:
		utility.console_rich_print("✨ Clearing Database", "bold yellow")
		clear_database()
		sys.exit(0)
	
	pdf_folder = args.pdf_folder_path
	utility.console_rich_print(f"📄 Loading PDFs from: {pdf_folder}", "bold cyan")
	documents = load_documents(pdf_folder)
	chunks = split_documents(documents)
	add_to_chroma(chunks)


def load_documents(pdf_folder: str) -> list[Document]:
	document_loader = PyPDFDirectoryLoader(pdf_folder)
	return document_loader.load()


def split_documents(documents: list[Document]):
	__chunk_size = 500
	__overlap = 80
	
	text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
		chunk_size=__chunk_size,
		chunk_overlap=__overlap,
	)
	
	chunks: list[Document] = text_splitter.split_documents(documents)
	utility.console_rich_print(f"Number of chunks: {len(chunks)}", "bold yellow")
	
	return chunks


def add_to_chroma(chunks: list[Document]):
	# Load the existing database.
	db: Chroma = get_db()
	
	# Calculate Page IDs.
	chunks_with_ids = calculate_chunk_ids(chunks)
	
	utility.console_rich_print(f"chunks: {chunks_with_ids}", "bold cyan")
	
	# Add or Update the documents.
	existing_items = db.get(include=[])  # IDs are always included by default
	existing_ids = set(existing_items["ids"])
	utility.console_rich_print(f"Number of existing documents in DB: {len(existing_ids)}", "bold green")
	
	# Only add documents that don't exist in the DB.
	new_chunks = []
	for chunk in chunks_with_ids:
		if chunk.metadata["id"] not in existing_ids:
			new_chunks.append(chunk)
	
	if len(new_chunks):
		utility.console_rich_print(f"👉 Adding new documents: {len(new_chunks)}", "bold green")
		new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
		db.add_documents(new_chunks, ids=new_chunk_ids)
	else:
		utility.console_rich_print("✅ No new documents to add", "bold green")


def calculate_chunk_ids(chunks):
	# Page Source : Page Number : Chunk Index
	
	last_page_id = None
	current_chunk_index = 0
	
	for chunk in chunks:
		source = chunk.metadata.get("source")
		page = chunk.metadata.get("page")
		current_page_id = f"{source}:{page}"
		
		# If the page ID is the same as the last one, increment the index.
		if current_page_id == last_page_id:
			current_chunk_index += 1
		else:
			current_chunk_index = 0
		
		# Calculate the chunk ID.
		chunk_id = f"{current_page_id}:{current_chunk_index}"
		last_page_id = current_page_id
		
		# Add it to the page meta-data.
		chunk.metadata["id"] = chunk_id
	
	return chunks


def clear_database() -> None:
	if os.path.exists(__CHROMA_PATH):
		shutil.rmtree(__CHROMA_PATH)


def get_embeddings() -> OllamaEmbeddings:
	return OllamaEmbeddings(model=__EMBEDDING_MODEL)


def get_db() -> Chroma:
	embeddings = get_embeddings()
	return Chroma(persist_directory=__CHROMA_PATH, embedding_function=embeddings)


def get_retriever() -> VectorStoreRetriever:
	return get_db().as_retriever(search_kwargs={"k": 1})


def get_llm() -> Ollama:
	return ChatOllama(model=__local_llm, format="json", temperature=0)


if __name__ == "__main__":
	utility = Utility(DevSettings())
	main()
