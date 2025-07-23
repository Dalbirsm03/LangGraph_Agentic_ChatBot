from tavily import TavilyClient
from typing_extensions import TypedDict, List
from langgraph.graph.message import add_messages
from typing import Annotated
from langchain_core.prompts import ChatPromptTemplate
import json

class State(TypedDict):
    """
    Represent the structure of the state used in graph
    """
    messages: Annotated[List, add_messages]

class AINEWSWithToolNode:
    """
    Chatbot logic enhanced with tool integration.
    """
    def __init__(self, model):
        self.llm = model

    def ai_bot(self, tools):
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State) -> State:
            return {"messages": [llm_with_tools.invoke(state["messages"])]}

        return chatbot_node

    def summarize_news_bot(self, llm):  # Like ai_bot, binds llm and returns node
        self.llm = llm

        def summary_node(state: State) -> State:
                """
                Node that summarizes tool-generated news results.
                """
                tool_msg = state["messages"][-1]

                try:
                    content = tool_msg.content
                    if isinstance(content, str):
                        content = json.loads(content)

                    articles = content.get("results", [])
                    if not articles:
                        return {"messages": ["No news results to summarize."]}

                    prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an AI news summarizer. Given a list of AI news articles, return a clean, readable **markdown** list.

For each article, include:
1. The **title** in bold
2. A clickable URL link labeled `Read Article`
3. A human-friendly publish date like "17 February 2024"
4. Sort the articles by latest first

Format like this:
**TITLE**  
🔗 [Read Article](URL)  
🗓️ Published: DD Month YYYY

If content is missing, skip that article. Only return markdown — no intro, no extra text."""),

    ("user", "Articles:\n{articles}")
])

                    articles_str = "\n\n".join([
                        f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
                        for item in articles
                    ])

                    response = llm.invoke(prompt.format(articles=articles_str))
                    return {"messages": [response]}

                except Exception as e:
                    return {"messages": [f"⚠️ Error summarizing news: {str(e)}"]}

        return summary_node