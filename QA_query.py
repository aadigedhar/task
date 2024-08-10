from pdftool import PDFSearchTool
from slackmesages import SlackNotifier

class QAquery:
    def __init__(self, slack_webhook_url, openai_api_key, llm_config, embedder_config):
        self.openai_api_key = openai_api_key
        self.llm_config = llm_config
        self.embedder_config = embedder_config
        self.slackpost = SlackNotifier(slack_webhook_url)

    def answer_questions(self, pdf, questions ):
        pdf_search_tool = PDFSearchTool(pdf.name, self.openai_api_key, self.llm_config, self.embedder_config)
        questions_list = questions.split('\n')
        answers = {}
        
        for question in questions_list:
            answer = pdf_search_tool.query(question)
            answers[question] = answer if answer else "Data Not Available"
        
        # Send the JSON output to Slack
        self.slackpost.send_message(answers)
        return answers