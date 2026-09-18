from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from .tools import fetch_stock_price, technical_analysis_tool, analyze_financial_sentiment, fundamental_analysis_tool, options_analysis_tool
from ..config import settings
from fastapi import HTTPException

# We use create_react_agent as a standard pre-built ReAct agent pattern in LangGraph

def get_agent():
    if not settings.OPENAI_API_KEY:
        return None
        
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key=settings.OPENAI_API_KEY)
    tools = [fetch_stock_price, technical_analysis_tool, analyze_financial_sentiment, fundamental_analysis_tool, options_analysis_tool]
    
    system_prompt = """You are a highly advanced Financial Research AI Agent. 
    Your goal is to provide comprehensive, accurate, and structured financial reports.
    When asked to research a stock or asset, utilize the tools available to you to gather:
    1. Current Price and Basic Info
    2. Fundamental Data (P/E, Growth, Debt, etc.)
    3. Technical Indicators (RSI, Moving Averages)
    4. Options Chain / Derivatives sentiment
    5. News Sentiment
    
    Format your response in Markdown with clear headers for each section. Provide a final conclusive summary with an actionable insight based on the gathered data.
    """
    
    agent_executor = create_react_agent(llm, tools, messages_modifier=system_prompt)
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
