from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict, Literal, Annotated
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langchain_community.tools import QuerySQLCheckerTool
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field


class EState(TypedDict):
    question: str
    query: str
    result: str
    answer: str
    correct_or_not: str


class SQLNodes:
    class QueryOutput(TypedDict):
        query: Annotated[str, ..., "Syntactically valid SQL query."]

    class Routes(BaseModel):
        route: Literal["Generate", "Execute"] = Field(
            description="Decide whether to rewrite query by generating again or execute it"
        )

    def __init__(self, llm, db):
        self.llm = llm
        self.db = db

        # Routing model setup
        self.router = self.llm.with_structured_output(self.Routes)

        system_message = """
        Given an input question, create a syntactically correct {dialect} query to
        run to help find the answer. Unless the user specifies in his question a
        specific number of examples they wish to obtain, always limit your query to
        at most {top_k} results. You can order the results by a relevant column to
        return the most interesting examples in the database.

        Never query for all the columns from a specific table, only ask for the
        few relevant columns given the question.
        Pay attention to use only the column names that you can see in the schema
        description. Be careful to not query for columns that do not exist. Also,
        pay attention to which column is in which table.
        Only use the following tables:
        {table_info}
        """

        user_prompt = "Question: {input}"

        self.query_prompt_template = ChatPromptTemplate.from_messages(
            [("system", system_message), ("user", user_prompt)]
        )

    def generate(self, state: EState):
        prompt = self.query_prompt_template.invoke({
            "dialect": self.db.dialect,
            "top_k": 10,
            "table_info": self.db.get_table_info(),
            "input": state["question"],
        })
        structured_llm = self.llm.with_structured_output(self.QueryOutput)
        result = structured_llm.invoke(prompt)
        print("✅ Generated Query:", result["query"])
        return {"query": result["query"]}

    def check(self, state: EState):
        checker_tool = QuerySQLCheckerTool(db=self.db, llm=self.llm)
        checked_result = checker_tool.invoke({"query": state["query"]})
        print("🧠 Checker Output:\n", checked_result)

        routing = self.router.invoke([
            SystemMessage(content="Decide whether to Generate or Execute the SQL based on the following checker output.If  The original query is correct and does not contain any common mistakes. Therefore, the rewritten query is the same as the original query: then go to execute"),
            HumanMessage(content=checked_result)
        ])
        print("🔁 Routing Decision:", routing.route)
        return {"correct_or_not": routing.route}

    def next_route(self, state: EState):
        if state["correct_or_not"].lower() == "generate":
            return "Generate"
        return "Execute"

    def execute(self, state: EState):
        tool = QuerySQLDatabaseTool(db=self.db)
        result = tool.invoke(state["query"])
        print("✅ Executed SQL.")
        return {"result": result}

    def answer(self, state: EState):
        prompt = (
            "Given the following user question, corresponding SQL query, "
            "and SQL result, answer the user question.\n\n"
            f"Question: {state['question']}\n"
            f"SQL Query: {state['query']}\n"
            f"SQL Result: {state['result']}"
        )
        response = self.llm.invoke(prompt)
        return {"answer": response.content}
    