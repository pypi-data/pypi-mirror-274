import argparse
import sys
import os

from eras.services.shell_command_service import ShellCommandService
from eras.config.post_install import ensure

def main():
    # print("main")
    ensure()
    parser = argparse.ArgumentParser(description="AI Natural Language Interface for running shell commands")
    parser.add_argument('question', nargs='+', help='question or instruction to turn into a shell command')
    args = parser.parse_args()
    question = ' '.join(args.question)

    # print(f'received question: {question}')
    shell_command_service = ShellCommandService()
    shell_command_service.handle_prompt(question)


if __name__ == "__main__":
    main()
