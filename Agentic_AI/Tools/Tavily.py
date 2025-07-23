from tavily import TavilyClient
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode

def get_tavily_tool():    
    tools = TavilySearch(
        query="Top Artificial Intelligence (AI) technology",
        topic="news",           
        max_results=5,           
        search_depth="advanced",    
    )
    tools = [tools]
    return tools

def tavily_tool_node(tools):
    return ToolNode(tools = tools)



