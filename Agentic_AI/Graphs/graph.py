from Agentic_AI.Nodes.Basic_ChatBot_Node import Basic_Node, State
from Agentic_AI.Nodes.Tool_node import ChatbotWithToolNode, State
from Agentic_AI.Nodes.AI_node import AINEWSWithToolNode , State
from langgraph.graph import START,END,StateGraph
from langgraph.prebuilt import tools_condition , ToolNode
from Agentic_AI.Tools.Arxiv import the_tool_node, get_tools
from Agentic_AI.Tools.Tavily import tavily_tool_node,get_tavily_tool


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

    def ai_news_builder_graph(self):
        tools = get_tavily_tool()
        tool_node = tavily_tool_node(tools=tools)
        self.obj = AINEWSWithToolNode(self.llm)
        ai_node = self.obj.ai_bot(tools)

        summary_node = self.obj.summarize_news_bot(self.llm)

        self.graph_builder.add_node("ai_node", ai_node)
        self.graph_builder.add_node("tools",tool_node)
        self.graph_builder.add_node("Summary",summary_node)
        self.graph_builder.add_edge(START,"ai_node")
        self.graph_builder.add_conditional_edges("ai_node", tools_condition)
        self.graph_builder.add_edge("tools","Summary")
        self.graph_builder.add_edge("Summary",END)


    def setup_graph(self, usecase: str):
            if usecase == "Basic Chatbot":
                self.basic_chatbot_Graph()
            elif usecase == "Arxiv Search":
                 self.tool_graph()
            elif usecase == "AI News Bot":
                 self.ai_news_builder_graph()

            return self.graph_builder.compile()
