import streamlit as st
import os

from Agentic_AI.UserInterface.config import Config

class LoadStreamlitUI:
    
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        st.set_page_config(page_title="🤖 " + self.config.get_page_title(), layout="wide")
        st.header("🤖 " + self.config.get_page_title())

        with st.sidebar:
            llm_options = self.config.get_llms()
            usecase_options = self.config.get_usecase_options()
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)
            self.user_controls["llm_type"] = self.user_controls["selected_llm"]

            if self.user_controls["selected_llm"] == 'Groq':
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("API Key", type="password", key="groq_api_key")

                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("⚠️ Please enter your GROQ API key to proceed. Don't have? refer : https://console.groq.com/keys ")

            elif self.user_controls["selected_llm"] == 'Google Gemini':
                 model_options = self.config.get_gemini_llm()
                 self.user_controls["select_gemini_model"] = st.selectbox("Select Model", model_options)
                 self.user_controls["GOOGLE_API_KEY"] = st.session_state["GOOGLE_API_KEY"] = st.text_input("API Key", type="password", key="gemini_api_key")

                 if not self.user_controls["GOOGLE_API_KEY"]:
                    st.warning("⚠️ Please enter your Google Gemini API key to proceed. Don't have? refer : https://aistudio.google.com/")

            elif self.user_controls["selected_llm"] == 'Qwen':
                 model_options = self.config.get_qwen_llm()
                 self.user_controls["repo_id"] = st.selectbox("Select Model", model_options)
                 self.user_controls["HF_TOKEN"] = st.text_input("API Key", type="password", key="huggingfacehub_api_token")

                 if not self.user_controls["HF_TOKEN"]:
                    st.warning("⚠️ Please enter your Hugging Face token to proceed. Your token must have permission for 'Make calls to Inference Providers'. Don't have? refer : https://huggingface.co/settings/tokens")


            self.user_controls["selected_usecase"] = st.selectbox("Select Usecases", usecase_options)
            if self.user_controls["selected_usecase"] == "AI News Bot":
                os.environ["TAVILY_API_KEY"]=self.user_controls["TAVILY_API_KEY"]=st.session_state["TAVILY_API_KEY"]=st.text_input("TAVILY API KEY",type="password")
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("⚠️ Please enter your Tavily API key to proceed. Get one from: https://app.tavily.com/account/api-keys")

        return self.user_controls
