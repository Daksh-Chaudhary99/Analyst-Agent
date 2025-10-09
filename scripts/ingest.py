import os
import chromadb
import logging
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.nebius import NebiusEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- 1. Configuration ---
DOCUMENTS_PATH = "./documents"
VECTOR_STORE_PATH = "./vector_store"
EMBED_MODEL_NAME = "BAAI/bge-en-icl"
CHROMA_COLLECTION_NAME = "sedar_filings"


def load_documents(path: str):
    """Loads documents from the specified directory."""
    logging.info(f"Loading documents from '{path}'...")
    reader = SimpleDirectoryReader(path)
    documents = reader.load_data()
    logging.info(f"Loaded {len(documents)} document(s).")
    return documents


def initialize_embedding_model():
    """Initializes and returns the Nebius embedding model."""
    logging.info("Initializing embedding model...")
    if "NEBIUS_API_KEY" not in os.environ:
        logging.critical("NEBIUS_API_KEY environment variable not set.")
        raise ValueError("NEBIUS_API_KEY environment variable not set.")

    try:
        embed_model = NebiusEmbedding(
            api_key=os.environ["NEBIUS_API_KEY"],
            model_name=EMBED_MODEL_NAME,
            api_base="https://api.studio.nebius.com/v1/"
        )
        logging.info(f"Nebius AI Embedding Model ('{EMBED_MODEL_NAME}') initialized successfully.")
        return embed_model
    except Exception as e:
        logging.critical(f"UNRECOVERABLE ERROR during embedding model initialization: {e}")
        raise


def setup_vector_store(path: str, collection_name: str):
    """Sets up and returns the ChromaDB vector store and storage context."""
    logging.info(f"Setting up ChromaDB vector store at '{path}'...")
    db = chromadb.PersistentClient(path=path)
    chroma_collection = db.get_or_create_collection(collection_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return storage_context


def main():
    """Main function to run the ingestion pipeline."""
    documents = load_documents(DOCUMENTS_PATH)
    embed_model = initialize_embedding_model()
    storage_context = setup_vector_store(VECTOR_STORE_PATH, CHROMA_COLLECTION_NAME)

    splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=20)

    logging.info("Creating vector index... (This may take a few minutes)")
    index = VectorStoreIndex.from_documents(
        documents,
        transformations=[splitter],
        embed_model=embed_model,
        storage_context=storage_context,
        show_progress=True
    )

    logging.info("✅ Ingestion complete! Vector index is persisted in ChromaDB.")
    logging.info(f"✅ Vector store location: {os.path.abspath(VECTOR_STORE_PATH)}")

if __name__ == "__main__":
    main()