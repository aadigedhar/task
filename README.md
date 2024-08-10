
# PDF Q&A Bot

This project is a PDF Question-Answering (Q&A) system that allows users to upload a PDF and ask questions about its content. The system processes the PDF, extracts relevant information, and returns structured answers. The answers are also sent to a specified Slack channel via a webhook.

## Features

- **PDF Content Processing**: Extracts and processes text from uploaded PDFs.
- **Question-Answering**: Uses a language model to answer user-provided questions based on the PDF content.
- **Slack Notifications**: Sends the results to a specified Slack channel for easy access.

## Installation

1. **Clone the repository**:

    ```bash
    git clone  https://github.com/aadigedhar/task.git
    cd task
    ```

2. **Create a virtual environment** (optional but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - Create a `.env` file in the project root.
    - Add your OpenAI API key and other necessary environment variables:

    ```plaintext
    OPENAI_API_KEY=your-openai-api-key
    SLACK_WEBHOOK_URL=your-slack-webhook-url
    ```

## Usage

1. **Run the Application**:

    ```bash
    python main.py
    ```

2. **Upload PDF and Ask Questions**:
    - Open the Gradio interface in your browser (the URL will be shown in the terminal).
    - Upload your PDF and enter your questions.
    - The answers will be displayed on the screen and sent to the Slack channel.

## File Descriptions

- **main.py**: The entry point of the application. It sets up the Gradio interface and handles user inputs, calling the `QAquery` class to process the PDF and answer questions.
  
- **pdftool.py**: Contains the `PDFSearchTool` class, which is responsible for processing the PDF, extracting text, and generating embeddings for efficient search.
  
- **QA_query.py**: Defines the `QAquery` class, which handles the overall question-answering workflow, including PDF processing and calling the language model for answers.
  
- **slackmesages.py**: Implements the `SlackNotifier` class, which sends messages to a Slack channel using a webhook.

## Dependencies

- `openai`: For interacting with OpenAI's GPT models.
- `fitz` (PyMuPDF): For PDF processing.
- `sentence-transformers`: For creating and handling embeddings.
- `gradio`: For building the user interface.
- `requests`: For sending HTTP requests to Slack.

## Configuration

- **OpenAI API Key**: Required to interact with the GPT model.
- **Slack Webhook URL**: Required to send the results to Slack.

Ensure these are set up in your `.env` file as shown in the installation steps.
