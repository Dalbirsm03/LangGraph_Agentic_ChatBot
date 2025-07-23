from langgraph.prebuilt import tools_condition , ToolNode
from langchain_community.tools import ArxivQueryRun
from langchain_community.utilities import ArxivAPIWrapper


def get_tools():
    api_wrapper = ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=500)
    arxiv_tool = ArxivQueryRun(api_wrapper=api_wrapper)
    tools = [arxiv_tool]
    return tools


def the_tool_node(tools):
    return ToolNode(tools=tools)
