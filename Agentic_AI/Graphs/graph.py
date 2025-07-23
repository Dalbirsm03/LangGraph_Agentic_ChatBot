from Agentic_AI.Nodes.Basic_ChatBot_Node import Basic_Node, State
from Agentic_AI.Nodes.Tool_node import ChatbotWithToolNode, State
from langgraph.graph import START,END,StateGraph
from langgraph.prebuilt import tools_condition , ToolNode
from Agentic_AI.Tools.Arxiv import the_tool_node, get_tools


class Graph_Builder:

    def __init__(self,llm):
        self.llm=llm
        self.graph_builder=StateGraph(State)
    
    def basic_chatbot_Graph(self):

        self.Basic_ChatBot_Node = Basic_Node(self.llm)
        self.graph_builder.add_node("ChatBot", self.Basic_ChatBot_Node.process)
        self .graph_builder.add_edge(START,"ChatBot")
        self.graph_builder.add_edge("ChatBot",END)

    def tool_graph(self):
         
         tools = get_tools()
         tool_node = the_tool_node(tools=tools)
         self.obj = ChatbotWithToolNode(self.llm)
         chatbot_node = self.obj.create_chatbot(tools)
         self.graph_builder.add_node("llm",chatbot_node)
         self.graph_builder.add_node("tools",tool_node)

         self.graph_builder.add_edge(START,"llm")
         self.graph_builder.add_conditional_edges("llm",tools_condition)
         self.graph_builder.add_edge("tools",END)

    def setup_graph(self, usecase: str):
            """
            Sets up the graph for the sel   ected use case.
            """
            if usecase == "Basic Chatbot":
                self.basic_chatbot_Graph()
            elif usecase == "Arxiv Search":
                 self.tool_graph()

            return self.graph_builder.compile()
