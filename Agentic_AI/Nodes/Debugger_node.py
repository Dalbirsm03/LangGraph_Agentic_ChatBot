from langchain_community.tools.stackexchange.tool import StackExchangeTool
from langchain_community.utilities.stackexchange import StackExchangeAPIWrapper
from langchain_tavily import TavilySearch
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from typing_extensions import TypedDict, List, Annotated
from langgraph.graph.message import add_messages
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from Agentic_AI.Tools.Tavily_Debug import get_tavily_tool_debug


# State Definition
class DState(TypedDict):
    messages: List[HumanMessage]
    question: str
    stack: str
    tavily: str
    aggregate: str

# Main Class
class DebuggerNode:
    def __init__(self, llm):
        self.llm = llm

    def process(self, state: DState):
        tavily_tool = get_tavily_tool_debug()
        query = state.get("question", "")
        search_result = tavily_tool.invoke({"query": query})
        print(search_result)
        return { "tavily":search_result}

        

    def stack_node(self, state: DState) -> dict:
        stack_api = StackExchangeAPIWrapper(max_results=2,query_type="all",result_separator="\n\n")
        stack_tool = StackExchangeTool(api_wrapper=stack_api)
        query = state.get("question", "")
        response = stack_tool.invoke({"query":query})
        print(response)
        return {"stack": response}
    

    def aggregator(self, state: DState) -> dict:
        tavily_result = state.get("tavily", "")
        stack_result = state.get("stack", "")
        if not isinstance(tavily_result, str):
            tavily_result = getattr(tavily_result, "content", str(tavily_result))

        if not isinstance(stack_result, str):
            stack_result = getattr(stack_result, "content", str(stack_result))

        combined_context = "\n\n".join(filter(None, [tavily_result, stack_result]))

        prompt = PromptTemplate.from_template("""
    You are a professional software debugging agent.  
    Your role is to help developers understand and resolve their programming issues efficiently.

    Below is a bug or error description along with search results. Provide:

    1. ✅ A **clear, concise solution**.
    2. 💡 A **brief explanation** of why this happens (if relevant).
    3. 🔗 If available, a **relevant helpful link** at the end like:  
    **Suggested Resource:** https://example.com

    ---
    🧩 **User Error/Question:**  
    {question}

    📚 **Search Results:**  
    {context}

    🧠 **Fix Summary:**
    """)

        chain = prompt | self.llm
        final_summary = chain.invoke({
            "question": state["question"],
            "context": combined_context
        })
        return {"aggregate": [final_summary.content if hasattr(final_summary, "content") else str(final_summary)]}
