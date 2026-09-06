from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from .tools import fetch_stock_price, technical_analysis_tool, analyze_financial_sentiment
from ..config import settings
from fastapi import HTTPException

# We use create_react_agent as a standard pre-built ReAct agent pattern in LangGraph

def get_agent():
    if not settings.OPENAI_API_KEY:
        return None
        
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key=settings.OPENAI_API_KEY)
    tools = [fetch_stock_price, technical_analysis_tool, analyze_financial_sentiment]
    
    agent_executor = create_react_agent(llm, tools)
    return agent_executor

def run_research_agent(query: str) -> str:
    agent = get_agent()
    if not agent:
        return "Error: OPENAI_API_KEY not configured. Cannot run AI Agent."
        
    try:
        result = agent.invoke({"messages": [("user", query)]})
        # The last message is the AI's response
        return result["messages"][-1].content
    except Exception as e:
         return f"Agent execution failed: {str(e)}"
