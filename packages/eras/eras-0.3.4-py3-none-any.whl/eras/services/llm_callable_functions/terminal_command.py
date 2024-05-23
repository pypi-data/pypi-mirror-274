import json
from eras.decorators.chatgpt_tool_data import chatgpt_tool_data
from eras.services.llm_callable_functions.callable_function_service_base import CallableFunctionServiceBase


# Demo service which provides ChatGPT the ability to call method get_user_details, which supplies a hard-coded result.
class TerminalCommand(CallableFunctionServiceBase):
    def __init__(self):
        super().__init__()

    @chatgpt_tool_data({
        "type": "function",
        "function": {
            "name": "execute_terminal_command",
            "description": "Executes a terminal command",
            "parameters": {
                "type": "object",
                "properties": {
                    "command_to_run": {
                        "type": "string",
                        "description": "A string of the command to run in the terminal"
                    },
                },
                "required": ["command_to_run"]
            }
        },
    })
    def execute_terminal_command(self, args):
        arguments = json.loads(args)
        print(
            f"execute_terminal_command function called with arguments first_name: {arguments['command_to_run']}")

