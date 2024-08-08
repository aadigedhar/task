from openai import OpenAI
import fitz
from sentence_transformers import SentenceTransformer, util
import numpy as np
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

class PDFSearchTool:
    def __init__(self, pdf_path, openai_api_key, llm_config, embedder_config):
        self.pdf_path = pdf_path
        self.llm_model = llm_config['model']
        self.client = OpenAI(api_key=openai_api_key)
        self.embedder = SentenceTransformer(embedder_config['model'])
        self.pdf_texts, self.embeddings = self.process_pdf()

    def process_pdf(self):
        pdf_document = fitz.open(self.pdf_path)
        pdf_texts = []
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            pdf_texts.append(page.get_text())
        embeddings = self.embedder.encode(pdf_texts, convert_to_tensor=True)
        return pdf_texts, embeddings

    def query(self, query_text):
        query_embedding = self.embedder.encode(query_text, convert_to_tensor=True)

        # Ensure the embeddings are on the CPU
        if query_embedding.is_cuda:
            query_embedding = query_embedding.cpu()
        if self.embeddings.is_cuda:
            self.embeddings = self.embeddings.cpu()

        # Compute cosine similarities
        scores = util.pytorch_cos_sim(query_embedding, self.embeddings)[0]

        # Convert the tensor to a numpy array
        scores_np = scores.numpy()

        best_score_idx = np.argmax(scores_np)
        best_text = self.pdf_texts[best_score_idx]

        response = self.client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Based on the following text:\n{best_text}\nAnswer the query: {query_text}"}
            ],
            max_tokens=1000
        )
        print(response)
        return response.choices[0].message.content.strip()

def send_to_slack(webhook_url, message):
    data = {
        "username": "Q&A-Bot",
        "icon_emoji": ":robot_face:",
        "text": "Here are the answers:",
        "attachments": [
            {
                "color": "#36a64f",
                "type": "mrkdwn",
                "text": json.dumps(message, indent=4)
            }
        ]
    }

    response = requests.post(
        webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'}
        )
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")

def answer_questions(pdf, questions, openai_api_key):
    pdf_search_tool = PDFSearchTool(pdf.name, openai_api_key, llm_config, embedder_config)
    questions_list = questions.split('\n')
    answers = {}
    
    for question in questions_list:
        answer = pdf_search_tool.query(question)
        answers[question] = answer if answer else "Data Not Available"
    
    # Send the JSON output to Slack
    print("this is last answaer : ", answers)
    send_to_slack(slack_webhook_url, answers)
    return answers

llm_config = {'provider': 'openai', 'model': 'gpt-4o-mini'}
embedder_config = {'provider': 'sentence-transformers', 'model': 'all-MiniLM-L6-v2'}
api_key_input = "Your API Key"
slack_webhook_url = 'slack web hook URL'

                      
# Gradio Interface

with gr.Blocks() as demo:
    pdf_input = gr.File(label="Upload PDF", file_types=['.pdf'])
    questions_input = gr.Textbox(label="Enter questions (one per line)", lines=5)
    
    output = gr.JSON(label="Answers")
    
    submit_button = gr.Button("Submit")
    submit_button.click(fn=answer_questions, inputs=[pdf_input, questions_input], outputs=output)

# To launch the Gradio interface
demo.launch(share=True)
