# 🧠 Agentic AI System – Built with LangGrapg, Traced with LangSmith

A powerful, modular **Agentic AI System** built on top of [LangGraph](https://github.com/langchain-ai/langgraph), [LangChain](https://github.com/langchain-ai/langchain), and [Pydantic](https://docs.pydantic.dev/). This framework enables dynamic tool routing, LLM-based reasoning, and debugging capabilities using external APIs and custom logic, with **LangSmith observability** baked in.

---

## 🚀 Introduction

This project aims to solve real-world data & code intelligence tasks through a **graph-based agent architecture**. Using LangGraph's state machines and LangChain’s LLM binding APIs, it supports the seamless integration of:

- 🔁 Multiple **LLMs** (e.g., GPT-4, Claude, Gemini, Groq)
- 🧰 Multiple **external tools** (Tavily, StackExchange, Arxiv, SQL)
- 🔄 Dynamic multi-path graph flows for complex logic
- 🔍 Debugging via aggregation of StackOverflow + Web + AI summarization

All task logic is structured using **Pydantic TypedDicts** for type safety, and **LangSmith** integration enables full observability and traceability of graph execution, tool calls, and LLM steps.

---
