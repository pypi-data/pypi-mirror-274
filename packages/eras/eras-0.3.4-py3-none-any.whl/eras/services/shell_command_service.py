import keyboard
from eras.agents.terminal_llama_agent import TerminalLlamaAgent
from eras.config.config import config
import subprocess
import os


class ShellCommandService:
    def __init__(self, openai_client):
        # print('hi')
        self.openai_client = openai_client
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