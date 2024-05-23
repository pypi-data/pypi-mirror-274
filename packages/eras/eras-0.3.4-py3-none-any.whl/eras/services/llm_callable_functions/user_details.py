import json
from eras.decorators.chatgpt_tool_data import chatgpt_tool_data
from eras.services.llm_callable_functions.callable_function_service_base import CallableFunctionServiceBase


# Demo service which provides ChatGPT the ability to call method get_user_details, which supplies a hard-coded result.
class UserDetails(CallableFunctionServiceBase):
    def __init__(self):
        super().__init__()

    @chatgpt_tool_data({
        "type": "function",
        "function": {
            "name": "get_user_details",
            "description": "Retrieves information for a user based on the combination of their first and last names.  "
                           "It returns information about the user's age, location, and profession.",
            "parameters": {
                "type": "object",
                "properties": {
                    "first_name": {
                        "type": "string",
                        "description": "First name of the user to get details of."
                    },
                    "last_name": {
                        "type": "string",
                        "description": "Last name of the user to get details of."
                    }
                },
                "required": ["first_name", "last_name"]
            }
        },
    })
    def get_user_details(self, args):
        arguments = json.loads(args)
        print(
            f"get_user_details function called with arguments first_name: {arguments['first_name']}, last_name: {arguments['last_name']}")
        response = {
            "age": 44,
            "location": {
                "state": "Utah"
            },
            "profession": "Software Engineer"
        }
        text_response = json.dumps(response)
        print(f"get_user_details is returning: {text_response}")
        return text_response
