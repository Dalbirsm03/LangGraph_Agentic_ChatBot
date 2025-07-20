from Agentic_AI.Nodes.Basic_ChatBot_Node import Basic_Node, State
from langgraph.graph import START,END,StateGraph

class Graph_Builder:

    def __init__(self,llm):
        self.llm=llm
        self.graph_builder=StateGraph(State)
    
    def basic_chatbot_Graph(self):

        self.Basic_ChatBot_Node = Basic_Node(self.llm)
        self.graph_builder.add_node("ChatBot", self.Basic_ChatBot_Node.process)
        self .graph_builder.add_edge(START,"ChatBot")
        self.graph_builder.add_edge("ChatBot",END)

    def setup_graph(self, usecase: str):
            """
            Sets up the graph for the selected use case.
            """
            if usecase == "Basic Chatbot":
                self.basic_chatbot_Graph()

            return self.graph_builder.compile()
