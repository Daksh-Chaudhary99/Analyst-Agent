import os
import logging
from llama_index.core.agent import ReActAgent
from llama_index.llms.nebius import NebiusLLM
from ..tools.financial_tools import ratio_tool, stock_price_tool
from ..tools.rag_tool import query_engine_tool

# --- Constants ---
AGENT_LLM_MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct"

class AnalystAgent:
    # Singleton Design Pattern
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AnalystAgent, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance


    def __init__(self):
        if self._initialized: 
            return
        logging.info("Initializing AnalystAgent...")
        self.agent = self._create_agent() # Agent is initialized only once in the beginning
        self._initialized = True
        logging.info("AnalystAgent initialized successfully.")


    def _create_agent(self):
        # Assemble all tools
        tools = [query_engine_tool, ratio_tool, stock_price_tool]

        # Initialize the Agent LLM
        llm = NebiusLLM(
            api_key=os.environ["NEBIUS_API_KEY"],
            model_name=AGENT_LLM_MODEL,
            api_base="https://api.studio.nebius.com/v1/",
            temperature=0.0
        )

        # Create and return the ReAct Agent
        return ReActAgent.from_tools(tools=tools, llm=llm, verbose=True)

    def query(self, question: str):
        return self.agent.chat(question)

# --- Singleton Instance ---
analyst_agent = AnalystAgent()