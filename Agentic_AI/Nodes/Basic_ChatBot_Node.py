from typing_extensions import TypedDict,List
from langchain_community.tools import ArxivQueryRun
from langchain_community.utilities import ArxivAPIWrapper
from langgraph.graph.message import add_messages
from typing import Annotated


class State(TypedDict):
    """
    Represent the structure of the state used in graph
    """
    messages: Annotated[List,add_messages]

class Basic_Node:

    def __init__(self,llm,db = None):
        self.llm = llm
        self.db = db
    
    def process(self,state: State)-> dict:
        return {"messages": self.llm.invoke(state['messages'])}
    




            