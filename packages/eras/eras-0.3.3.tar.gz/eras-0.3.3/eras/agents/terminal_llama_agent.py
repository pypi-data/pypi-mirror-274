import time
import uuid

from eras.models.conversation import Conversation

# system_prompt = "You are a helpful assistant that answers questions accurately, without making up facts."
model = "gpt-3.5-turbo"


# Agent which:
# - provides an inference function which accepts a question to send to chatgpt and responds with the answer.
# - maintains a conversation, which is a collection of messages that have been sent to and received from chatgpt.
# - determines if chatgpt has requested that a local function has been called.
# - executes the local function and sends the result to chatgpt (via conversation messages)
class TerminalLlamaAgent:
    def __init__(self, openai_client):

        self.openai_client = openai_client


    def get_system_prompt(self):
        user_os = "System: Mac , macOS: Monterey, osVersion: 12.4"
        system_prompt = '''
You are an expert in providing a Natural Language Interface that converts questions and/or instructions into terminal commands.        
You are renowned for your ability to take a user's question or instruction and create a valid terminal command that works every time.
You do not use preamble, explanation, or pleasantries.  You only respond with valid terminal commands that work with the user's operating system.
If there is no way to create a valid terminal command, simply say 'No shell command can facilitate your request'.
Do not surround the terminal command with any string indicators, like `, ', or ".
Here are some example question/command and what your response should look like:

Mac OS Example 1:
Question/Command: Show me the contents of my Documents folder.
Response: ls ~/Documents

Mac OS Example 2:
Question/Command: Create a new directory called 'Projects' in my home folder.
Response: mkdir ~/Projects

Mac OS Example 3:
Question/Command: Delete the file named 'old_report.pdf' from my Desktop.
Response: rm ~/Desktop/old_report.pdf

Mac OS Example 4:
Question/Command: Find all files containing the word 'budget' in my Documents folder.
Response: grep -r "budget" ~/Documents

The user's Operating System is: 
        ''' + user_os
        return system_prompt

    def inference(self, question=None, conversation=None, start_time_seconds=None):
        # print('------- inference ------------')
        # start a new conversation if needed, which tracks all messages to and from chatgpt
        conversation = self.ensure_conversation_exists(conversation)

        # measure how long it takes to complete
        start_time_seconds = start_time_seconds if start_time_seconds is not None else time.time()

        # initial call will have a user question, but some calls will be to pass local function results back to chatgpt.
        conversation.add_user_question_to_messages_if_applicable(question)

        # get all messages in the conversation history to pass to chatgpt
        messages = conversation.get_messages_in_chatgpt_format()
        # print(f"sending messages: {messages}")

        # call chatgpt
        # response = self.openai_client.ChatCompletion.create(model=model, messages=messages, tools=self.tools)
        response = self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            # tools=self.tools,
            stream=False, # Whether to stream the response or return the full response at once
            # max_tokens=8000,  # The maximum number of tokens to generate in the completion
            # temperature=0.5,  # The temperature of the model, controlling the randomness of the output
            # top_p=1.0,  # The nucleus sampling parameter, controlling the diversity of the output
            # n=1,  # The number of completions to generate
            # # stop=None,  # A list of stop sequences to stop the completion at
            # stop=None,
            # presence_penalty=0.0,  # The penalty for generating tokens that appear in the prompt
            # frequency_penalty=0.0,  # The penalty for generating tokens that appear frequently in the prompt
            # logit_bias={},  # A dictionary of token IDs and associated biases to apply to the logits
        )
        # print(response)

        # add the response to our conversation.  we may need to pass it back to chatgpt if a function is called.
        conversation.add_llama_response_to_messages(response)

        response_message = conversation.get_last_message()
        # print(response_message.message_text)
        return response_message.message_text

    def ensure_conversation_exists(self, conversation: Conversation):
        if conversation is None:
            conversation = Conversation(conversation_id=str(uuid.uuid4()), system_prompt=self.get_system_prompt())
        return conversation

