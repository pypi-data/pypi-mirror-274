import argparse
import sys
import os
from dotenv import load_dotenv
load_dotenv()

from eras.services.user_command_service import UserCommandService
from eras.config.post_install import ensure
# from eras.services.user_command_service import UserCommandService
def main():
    # print("main")
    ensure()
    parser = argparse.ArgumentParser(description="AI Natural Language Interface for running shell commands")
    parser.add_argument('question', nargs='+', help='question or instruction to turn into a shell command')
    args = parser.parse_args()
    user_input = ' '.join(args.question)
    user_command_service = UserCommandService()
    user_command_service.handle_request(user_input)


if __name__ == "__main__":
    main()
