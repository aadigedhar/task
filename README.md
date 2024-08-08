# PDF Search and Q&A Tool

## Overview

This project provides a tool for querying PDF documents using OpenAI's GPT model and Sentence Transformers for embedding. It features a Gradio interface for user interaction and sends results to a Slack channel.

## Requirements

To run this project, you'll need to install the following Python libraries:

- `openai`
- `fitz` (PyMuPDF)
- `sentence-transformers`
- `numpy`
- `torch`
- `gradio`
- `requests`
- `python-dotenv`

You can install these dependencies using pip:

```bash
pip install openai pymupdf sentence-transformers numpy torch gradio requests python-dotenv
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory of your project and add your OpenAI API key:

```plaintext
OPENAI_API_KEY=your_openai_api_key
```

Replace `your_openai_api_key` with your actual OpenAI API key.

### Slack Webhook URL

Update the `slack_webhook_url` variable in the script with your Slack webhook URL:

```python
slack_webhook_url = 'https://hooks.slack.com/services/your/webhook/url'
```

Replace `'https://hooks.slack.com/services/your/webhook/url'` with your actual Slack webhook URL.

## Code

### `PDFSearchTool` Class

This class handles PDF processing and querying using the OpenAI GPT model and Sentence Transformers.

- **Initialization**: `PDFSearchTool(pdf_path, openai_api_key, llm_config, embedder_config)`
  - `pdf_path`: Path to the PDF file.
  - `openai_api_key`: API key for OpenAI.
  - `llm_config`: Configuration for the language model.
  - `embedder_config`: Configuration for the sentence transformer model.

- **Methods**:
  - `process_pdf()`: Extracts text from the PDF and generates embeddings.
  - `query(query_text)`: Queries the PDF text based on the input query and retrieves an answer from the GPT model.

### `send_to_slack` Function

This function sends the answers to a specified Slack channel.

- **Parameters**:
  - `webhook_url`: URL of the Slack webhook.
  - `message`: JSON data containing the answers.

### `answer_questions` Function

This function uses the `PDFSearchTool` to answer questions based on the provided PDF and sends the results to Slack.

- **Parameters**:
  - `pdf`: The uploaded PDF file.
  - `questions`: Questions to be answered, one per line.
  - `openai_api_key`: API key for OpenAI.

### Gradio Interface

The Gradio interface allows users to upload a PDF, enter questions, and receive answers.

```python
with gr.Blocks() as demo:
    pdf_input = gr.File(label="Upload PDF", file_types=['.pdf'])
    questions_input = gr.Textbox(label="Enter questions (one per line)", lines=5)
    
    output = gr.JSON(label="Answers")
    
    submit_button = gr.Button("Submit")
    submit_button.click(fn=answer_questions, inputs=[pdf_input, questions_input], outputs=output)

# To launch the Gradio interface
demo.launch(share=True)
```

## Usage

1. **Run the Script**: Ensure that all required libraries are installed and execute the script to start the Gradio interface.
   
2. **Upload a PDF**: Use the Gradio interface to upload a PDF file.

3. **Enter Questions**: Input questions (one per line) and click "Submit".

4. **View Results**: The answers will be displayed in the Gradio interface and sent to the configured Slack channel.
