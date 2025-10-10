import os
import logging
import chromadb
from llama_index.core.tools import QueryEngineTool
from llama_index.embeddings.nebius import NebiusEmbedding
from llama_index.llms.nebius import NebiusLLM
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex

# --- Constants ---
VECTOR_STORE_PATH = "./vector_store"
CHROMA_COLLECTION_NAME = "sedar_filings"
EMBED_MODEL_NAME = "BAAI/bge-en-icl"
SYNTHESIS_LLM_MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct"

def _create_rag_tool():
    """
    Private function to initialize and return the RAG tool.
    This heavy initialization should only happen once.
    """
    logging.info("Initializing RAG tool...")
    
    # Initialize models and load index
    llm = NebiusLLM(
        api_key=os.environ["NEBIUS_API_KEY"],
        model=SYNTHESIS_LLM_MODEL,
        api_base="https://api.studio.nebius.com/v1/",
    )

    embed_model = NebiusEmbedding(
        api_key=os.environ["NEBIUS_API_KEY"], model_name=EMBED_MODEL_NAME, api_base="https://api.studio.nebius.com/v1/"
    )
    
    db = chromadb.PersistentClient(path=VECTOR_STORE_PATH)
    chroma_collection = db.get_collection(CHROMA_COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)
    query_engine = index.as_query_engine(llm=llm, similarity_top_k=5)

    # Create and return the RAG tool
    tool = QueryEngineTool.from_defaults(
        query_engine=query_engine,
        name="sedar_filing_retriever",
        description="Use this tool to retrieve specific information and answer questions about a company's SEDAR+ financial filing."
    )
    logging.info("RAG tool initialized successfully.")
    return tool

# --- Singleton Instance ---
query_engine_tool = _create_rag_tool()