import os
from langsmith import Client
import streamlit as st
from Agentic_AI.Graphs.graph import Graph_Builder
from Agentic_AI.LLms.GROQ import GroqLLM
from Agentic_AI.LLms.Gemini import GeminiLLM
from Agentic_AI.LLms.Qwen import QwenLLM
from Agentic_AI.UserInterface.Streamlit_UI.Display_Result import DisplayResultStreamlit
from Agentic_AI.UserInterface.Streamlit_UI.Load_UI import LoadStreamlitUI
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase

def load_app():
    with st.sidebar:
            st.write("## LangSmith Configuration")
            langsmith_api_key = st.text_input("LangSmith API Key (Optional)", type="password")
            if langsmith_api_key:
                os.environ["LANGSMITH_API_KEY"] = langsmith_api_key
                os.environ["LANGSMITH_TRACING_V2"] = "true"
                os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
                os.environ["LANGSMITH_PROJECT"] = "agentic_chatbot"
                try:
                    Client()  # Test connection
                    st.success("✅ LangSmith connected!")
                except Exception as e:
                    st.error(f"❌ LangSmith Error: {str(e)}")

    ui = LoadStreamlitUI()
    user_control_input = ui.load_streamlit_ui()
    if not user_control_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    user_message = st.chat_input("Enter your message:")
    if user_message:
        try:
            llm_type = user_control_input.get("llm_type")
            if llm_type == "Groq":
                api_key = user_control_input.get("GROQ_API_KEY")
                if not api_key:
                    st.error("Please enter your GROQ API Key.")
                    return
                llm_object = GroqLLM(user_contols_input=user_control_input)
            elif llm_type == "Google Gemini":
                api_key = user_control_input.get("GOOGLE_API_KEY")
                if not api_key:
                    st.error("Please enter your Google Gemini API Key.")
                    return
                llm_object = GeminiLLM(user_contols_input=user_control_input)
            elif llm_type == "Qwen":
                api_key = user_control_input.get("HF_TOKEN")
                if not api_key:
                    st.error("Please enter your Hugging Face token.")
                    return
                llm_object = QwenLLM(user_contols_input=user_control_input)
            else:
                st.error("Please select a valid LLM.")
                return

            llm = llm_object.get_llm_model()
            usecase = user_control_input.get("selected_usecase")
            if usecase == "SQL Agent":
                DB_USER = user_control_input.get("DB_USER")
                DB_PASSWORD = user_control_input.get("DB_PASSWORD")
                DB_HOST = user_control_input.get("DB_HOST")
                DB_NAME = user_control_input.get("DB_NAME")

                if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
                    st.error("❌ Please enter all required database credentials.")
                    return

                try:
                    encoded_password = quote_plus(DB_PASSWORD)
                    engine = create_engine(f'mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}')
                    db = SQLDatabase(engine=engine)
                except Exception as e:
                    st.error(f"❌ Database connection failed: {e}")
                    return

                graph_builder = Graph_Builder(llm, db=db)
            else:
                graph_builder = Graph_Builder(llm)
            try:
                graph = graph_builder.setup_graph(usecase)
                print(user_message)
                DisplayResultStreamlit(usecase, graph, user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error: Graph set up failed- {e}")
                return
        except Exception as e:
             st.error(f"Error: Graph set up failed- {e}")
             return
