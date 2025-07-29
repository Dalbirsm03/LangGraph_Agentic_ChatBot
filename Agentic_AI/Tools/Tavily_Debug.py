# Tavily_Debug.py
from langchain_tavily import TavilySearch
import os

def get_tavily_tool_debug():    
    try:
        if not os.getenv("TAVILY_API_KEY"):
            raise ValueError("TAVILY_API_KEY not found in environment variables")
            
        tavily_search = TavilySearch(
            max_results=5,
            search_depth="advanced"
        )
        return tavily_search
    except Exception as e:
        print(f"Error setting up Tavily search: {e}")
        return None
