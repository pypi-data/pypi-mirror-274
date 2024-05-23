
import re

from eras.agents.simple_llm import SimpleLLM
from eras.config.config import config
from eras.services.shell_command_service import ShellCommandService
import openai

class UserCommandService:
    def __init__(self):
        self.openai_client = openai.OpenAI(
            # base_url=config.get_eras_base_url(),
            api_key=config.get_eras_open_ai_key()
            # api_key=config.get_open_ai_key()
        )
        self.shell_command_service = ShellCommandService(self.openai_client)
        self.simple_llm = SimpleLLM(self.openai_client)



    def handle_request(self, user_input: str):
        if user_input.startswith("/help" ):
            self.handle_help_request(user_input)
        elif user_input.startswith("/chat"):
            self.handle_chat_request(user_input)
        else:
            self.handle_shell_nli_request(user_input)

    def handle_help_request(self, user_input):
        print("Welcome to ERAS - Easily Runnable AI Shell")
        print("Commands: ==============================================")
        print("{defualt usage} - Natural Languge Interface for running commands. e.g. eras how do I list all files in a directory -> %ls")
        print("/help - get info about commands")
        print("/chat - ask the LLM a question about anything. e.g. /chat tell me about quantum physics")



    def handle_chat_request(self, user_input):
        match = re.match(r'^/chat\s+(.*)', user_input)
        prompt = match.group(1) if match else None

        def handle_text_received(text):
            print(text, end="")

        def handle_response_complete():
            print()

        self.simple_llm.stream_inference(prompt, handle_text_received, handle_response_complete)


    def handle_shell_nli_request(self, user_input):
        self.shell_command_service.handle_prompt(user_input)
