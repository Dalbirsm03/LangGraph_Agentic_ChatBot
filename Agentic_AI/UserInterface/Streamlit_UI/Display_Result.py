import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import json


class DisplayResultStreamlit:
    def __init__(self,usecase,graph,user_message):
        self.usecase= usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase= self.usecase
        graph = self.graph
        user_message = self.user_message
        print(user_message)
        if usecase =="Basic Chatbot":
                for event in graph.stream({'messages':("user",user_message)}):
                    print(event.values())
                    for value in event.values():
                        print(value['messages'])
                        with st.chat_message("user"):
                            st.write(user_message)
                        with st.chat_message("assistant"):
                            st.write(value["messages"].content)
        if usecase == "Arxiv Search":
            with st.chat_message("user"):
                st.write(user_message)

            final_response = ""

            for event in graph.stream({'messages': ("user", user_message)}):
                for value in event.values():
                    for msg in value["messages"]:
                        if hasattr(msg, "content") and msg.content:
                            final_response = msg.content

            with st.chat_message("assistant"):
                st.write(final_response if final_response else "No relevant results found.")
        if usecase == "AI News Agent":
            with st.chat_message("user"):
                st.write(user_message)

            final_response = ""

            for event in graph.stream({'messages': ("user", user_message)}):
                for value in event.values():
                    for msg in value["messages"]:
                        if hasattr(msg, "content") and msg.content:
                            final_response = msg.content

            with st.chat_message("assistant"):
                st.write(final_response if final_response else "No relevant results found.")

        elif usecase == "SQL Agent":
            state = {"question": user_message}
            with st.chat_message("user"):
                st.write(user_message)

            final_answer = None

            for step in graph.stream(state, stream_mode="values"):
                if "answer" in step:
                    final_answer = step["answer"]

            if final_answer:
                with st.chat_message("assistant"):
                    st.markdown("🧠 **Final Answer:**")
                    st.write(final_answer)
            else:
                with st.chat_message("assistant"):
                    st.write("⚠️ No answer was generated.")

        elif usecase == "Debugger Agent":
            state = {"question": user_message}
            with st.chat_message("user"):
                st.write(user_message)

            final_answer = None

            for step in graph.stream(state, stream_mode="values"):
                if "aggregate" in step:
                    final_answer = step["aggregate"]

            if final_answer:
                with st.chat_message("assistant"):
                    st.markdown("🧠 **Final Answer:**")
                    st.write(final_answer[0] if isinstance(final_answer, list) else final_answer)
            else:
                with st.chat_message("assistant"):
                    st.write("⚠️ No answer was generated.")