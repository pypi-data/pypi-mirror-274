import keyboard
from dotenv import load_dotenv
load_dotenv()
from eras.agents.terminal_llama_agent import TerminalLlamaAgent
from eras.config.config import config
import subprocess
import os


class ShellCommandService:
    def __init__(self):
        # print('hi')
        import openai

        # self.openai_client = openai.OpenAI(
        #     base_url="http://192.168.0.209:8080/v1",  # "THIS MUST BE 127.0.0.1, not localhost
        #     api_key="sk-no-key-required"
        #     # api_key=config.get_open_ai_key()
        # )

        self.openai_client = openai.OpenAI(
            # base_url=config.get_eras_base_url(),
            api_key=config.get_eras_open_ai_key()
            # api_key=config.get_open_ai_key()
        )

        self.llm_functions_agent = TerminalLlamaAgent(openai_client=self.openai_client)

    def handle_prompt(self, prompt: str):
        response = self.llm_functions_agent.inference(prompt)
        if response == 'No shell command can facilitate your request':
            print(response)
            return
        # print(f"response is {response}")
        # self.run_shell_command(response)
        self.populate_terminal_with_shell_command(response)

    def populate_terminal_with_shell_command(self, command):
        keyboard.write(command)

    def run_shell_command(self, command: str):
        home_directory = os.path.expanduser("~")
        # # Execute the command
        # result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=home_directory)
        # # Print the output
        # print(result.stdout)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                   cwd=home_directory)

        # Stream the output line by line
        for line in process.stdout:
            print(line, end='')  # 'end' to avoid double newlines

        # Wait for the process to finish and get the return code
        return_code = process.wait()

        # Check if there were any errors
        if return_code != 0:
            for line in process.stderr:
                print(line, end='')