from Agentic_AI.Nodes.Basic_ChatBot_Node import Basic_Node, State as BasicState
from Agentic_AI.Nodes.Tool_node import ChatbotWithToolNode, State as ToolState
from Agentic_AI.Nodes.AI_node import AINEWSWithToolNode, State as AINewsState
from Agentic_AI.Nodes.SQL_node import EState as SQLState, SQLNodes
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import tools_condition
from Agentic_AI.Tools.Arxiv import the_tool_node, get_tools
from Agentic_AI.Tools.Tavily import tavily_tool_node, get_tavily_tool


class Graph_Builder:

    def __init__(self, llm, db=None):
        self.db = db
        self.llm = llm
        self.graph_builder = None
        
    def basic_chatbot_Graph(self):
        self.graph_builder = StateGraph(BasicState)
        basic_node = Basic_Node(self.llm)
        self.graph_builder.add_node("ChatBot", basic_node.process)
        self.graph_builder.add_edge(START, "ChatBot")
        self.graph_builder.add_edge("ChatBot", END)

    def tool_graph(self):
        self.graph_builder = StateGraph(ToolState)
        tools = get_tools()
        tool_node = the_tool_node(tools=tools)
        chatbot_node = ChatbotWithToolNode(self.llm).create_chatbot(tools)

        self.graph_builder.add_node("llm", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)
        self.graph_builder.add_edge(START, "llm")
        self.graph_builder.add_conditional_edges("llm", tools_condition)
        self.graph_builder.add_edge("tools", END)

    def ai_news_builder_graph(self):
        self.graph_builder = StateGraph(AINewsState)
        tools = get_tavily_tool()
        tool_node = tavily_tool_node(tools=tools)
        ai_node_obj = AINEWSWithToolNode(self.llm)
        ai_node = ai_node_obj.ai_bot(tools)
        summary_node = ai_node_obj.summarize_news_bot(self.llm)

        self.graph_builder.add_node("ai_node", ai_node)
        self.graph_builder.add_node("tools", tool_node)
        self.graph_builder.add_node("Summary", summary_node)
        self.graph_builder.add_edge(START, "ai_node")
        self.graph_builder.add_conditional_edges("ai_node", tools_condition)
        self.graph_builder.add_edge("tools", "Summary")
        self.graph_builder.add_edge("Summary", END)

    def sql_graph(self):
        self.graph_builder = StateGraph(SQLState)
        sql_nodes = SQLNodes(self.llm, self.db)
        self.graph_builder.add_node("Generate", sql_nodes.generate)
        self.graph_builder.add_node("Check", sql_nodes.check)
        self.graph_builder.add_node("Execute", sql_nodes.execute)
        self.graph_builder.add_node("Answer", sql_nodes.answer)

        self.graph_builder.add_edge(START, "Generate")
        self.graph_builder.add_edge("Generate", "Check")
        self.graph_builder.add_conditional_edges("Check", sql_nodes.next_route, {
            "Generate": "Generate",
            "Execute": "Execute"
        })
        self.graph_builder.add_edge("Execute", "Answer")
        self.graph_builder.add_edge("Answer", END)

    def setup_graph(self, usecase: str):
        if usecase == "Basic Chatbot":
            self.basic_chatbot_Graph()
        elif usecase == "Arxiv Search":
            self.tool_graph()
        elif usecase == "AI News Agent":
            self.ai_news_builder_graph()
        elif usecase == "SQL Agent":
            if not self.db:
                raise ValueError("SQL Agent requires a database connection.")
            self.sql_graph()
        else:
            raise ValueError(f"Unknown usecase: {usecase}")

        return self.graph_builder.compile()
