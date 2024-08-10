from openai import OpenAI
from sentence_transformers import SentenceTransformer, util
import numpy as np
import fitz
import torch
import openai

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
        try:
            response = self.client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Based on the following text:\n{best_text}\nAnswer the query: {query_text}"}
                ],
                max_tokens=1000
            )
        

            return response.choices[0].message.content.strip()
        
        except openai.APIError as e:
            print(f"OpenAI API returned an API Error: {e}")
        
        except openai.APIConnectionError as e:
            print(f"Failed to connect to OpenAI API: {e}")
            
        except openai.RateLimitError as e:
            print(f"OpenAI API request exceeded rate limit: {e}")
            