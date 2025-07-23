import streamlit as st
from Agentic_AI.Graphs.graph import Graph_Builder
from Agentic_AI.LLms.GROQ import GroqLLM
from Agentic_AI.LLms.Gemini import GeminiLLM
from Agentic_AI.LLms.Qwen import QwenLLM
from Agentic_AI.UserInterface.Streamlit_UI.Display_Result import DisplayResultStreamlit
from Agentic_AI.UserInterface.Streamlit_UI.Load_UI import LoadStreamlitUI

def load_app():
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


