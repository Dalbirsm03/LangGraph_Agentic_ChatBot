from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
import os
import streamlit as st
class QwenLLM:
    def __init__(self,user_contols_input):
        self.user_controls_input=user_contols_input

    def get_llm_model(self):
        try:
            huggingfacehub_api_token=self.user_controls_input["HF_TOKEN"]
            repo_id=self.user_controls_input["repo_id"]
            if huggingfacehub_api_token=='' and os.environ["HF_TOKEN"] =='':
                st.error("Please Enter the Hugging Face")

            llmm = HuggingFaceEndpoint(
                repo_id=repo_id,
                task="text-generation",
                max_new_tokens=512,
                do_sample=False,
                repetition_penalty=1.03,
                huggingfacehub_api_token=huggingfacehub_api_token 
            )
            llm = ChatHuggingFace(llm=llmm)

        except Exception as e:
            raise ValueError(f"Error Ocuured With Exception : {e}")
        return llm