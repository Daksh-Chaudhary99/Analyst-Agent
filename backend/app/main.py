# Entry point for the FastAPI server
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv  
load_dotenv()
from .services.rag_service import rag_service

class QueryRequest(BaseModel):
    question: str
class QueryResponse(BaseModel):
    response: str

app = FastAPI(
    title="SEDAR+ Analyst Agent API",
    description="An API for querying financial documents using an AI agent.",
    version="1.0.0"
)

# @app.post("/query", response_model=QueryResponse)
# def handle_query(request: QueryRequest):
#     agent_response = rag_service.query(request.question)
#     return QueryResponse(response=str(agent_response))

@app.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    agent_response = await rag_service.query(request.question)
    return QueryResponse(response=str(agent_response))

@app.get("/")
def read_root():
    return {"status": "API is running"}