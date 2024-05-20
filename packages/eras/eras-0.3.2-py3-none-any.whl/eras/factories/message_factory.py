from eras.models.message import Message
import json

class MessageFactory:
    @staticmethod
    def create_message_from_chatgpt_response(response):
        choices = response.choices
        choice = choices[0]
        gpt_message = choice.message  # choice['message']
        role = gpt_message.role  # gpt_message['role']
        message_text = gpt_message.content  # gpt_message['content']
        tool_calls = gpt_message.tool_calls
        finish_reason = choice.finish_reason
        # if 'tool_calls' in gpt_message:
        #     tool_calls = gpt_message.tool_calls  # gpt_message['tool_calls']
        # if 'finish_reason' in choice:
        #     finish_reason = choice.finish_reason  # choice['finish_reason']
        message = Message(message_text=message_text, role=role, raw_chatgpt_chat_completion_response=response,
                          tool_calls=tool_calls)
        return message

    @staticmethod
    def create_message_from_llama_response(response):
        choices = response.choices
        choice = choices[0]
        gpt_message = choice.message  # choice['message']
        role = gpt_message.role  # gpt_message['role']
        message_text = gpt_message.content  # gpt_message['content']
        tool_calls = MessageFactory.parse_potential_tool_calls_from_llama(message_text)
        finish_reason = choice.finish_reason
        # if 'tool_calls' in gpt_message:
        #     tool_calls = gpt_message.tool_calls  # gpt_message['tool_calls']
        # if 'finish_reason' in choice:
        #     finish_reason = choice.finish_reason  # choice['finish_reason']
        message = Message(message_text=message_text, role=role, raw_chatgpt_chat_completion_response=response,
                          tool_calls=tool_calls)
        return message

    @staticmethod
    def parse_potential_tool_calls_from_llama(json_string: str):
        try:
            json_obj = json.loads(json_string)

            # Check if 'tool_calls' exists in the JSON object
            choices = json_obj.get("choices", [])
            if choices:
                first_choice = choices[0]
                message = first_choice.get("message", {})
                tool_calls = message.get("tool_calls", None)
                if tool_calls:
                    return tool_calls

        except json.JSONDecodeError as e:
            x = 1
            # print("Invalid JSON:", e)
            # print(json_string)

    @staticmethod
    def create_message_from_user_question(question: str):
        return Message(role="user", message_text=question)

    @staticmethod
    def create_system_prompt_message(system_prompt: str):
        return Message(role="system", message_text=system_prompt)
