from ..agents.core import analyst_agent

class RAGService:
    def query(self, question: str):
        return analyst_agent.query(question)

rag_service = RAGService()