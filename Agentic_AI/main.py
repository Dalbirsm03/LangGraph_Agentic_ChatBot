import streamlit as st
from Agentic_AI.Graphs.graph import Graph_Builder
from Agentic_AI.LLms.GROQ import GroqLLM
from Agentic_AI.UserInterface.Streamlit_UI.Display_Result import DisplayResultStreamlit
from Agentic_AI.UserInterface.Streamlit_UI.Load_UI import LoadStreamlitUI

def load_app():
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()
    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    user_message = st.chat_input("Enter your message:")
    if user_message:
        try:
            
            llm_object = GroqLLM(user_contols_input = user_input)
            llm = llm_object.get_llm_model()
            usecase = user_input.get("selected_usecase")

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


