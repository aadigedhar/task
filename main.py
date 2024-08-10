from openai import OpenAI
import fitz

import torch
import gradio as gr
import requests
import json
import os
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")
# Load environment variables from a .env file
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

from QA_query import QAquery

if __name__=="__main__":                  
    # Gradio Interface
    llm_config = {'provider': 'openai', 'model': 'gpt-4o-mini'}
    embedder_config = {'provider': 'sentence-transformers', 'model': 'all-MiniLM-L6-v2'}
    api_key_input = "Open API key"
    slack_webhook_url = 'https://hooks.slack.com/services/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'


    ## Modules Import
    QAmodule = QAquery(slack_webhook_url, openai_api_key, llm_config, embedder_config)
    #SLmodule = SlackNotifier(slack_webhook_url)


    with gr.Blocks() as demo:
        pdf_input = gr.File(label="Upload PDF", file_types=['.pdf'])
        questions_input = gr.Textbox(label="Enter questions (one per line)", lines=5)
        
        output = gr.JSON(label="Answers")
        
        submit_button = gr.Button("Submit")
        submit_button.click(fn=QAmodule.answer_questions, inputs=[pdf_input, questions_input], outputs=output)

    # To launch the Gradio interface
    demo.launch(share=True)
