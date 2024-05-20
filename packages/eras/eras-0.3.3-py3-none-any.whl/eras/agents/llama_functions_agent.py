# DOESNT WORK
# import time
# import uuid
# import json
# from typing import List, Tuple, Set, Dict
#
# from src.factories.function_details_factory import FunctionDetailsFactory
# from src.models.conversation import Conversation
# from src.services.llm_callable_functions.user_details import UserDetails
#
# # system_prompt = "You are a helpful assistant that answers questions accurately, without making up facts."
# model = ""
#
# ## WIP DEFINITELY NOT WORKING LIKE OPENAI
#
# # Agent which:
# # - provides an inference function which accepts a question to send to chatgpt and responds with the answer.
# # - maintains a conversation, which is a collection of messages that have been sent to and received from chatgpt.
# # - determines if chatgpt has requested that a local function has been called.
# # - executes the local function and sends the result to chatgpt (via conversation messages)
# class LlamaFunctionsAgent:
#     def __init__(self, openai_client):
#         print('init')
#         self.callable_function_service = UserDetails()
#         self.tools = [] + self.callable_function_service.get_tools()
#         self.openai_client = openai_client
#
#
#     def get_system_prompt(self):
#         tools_as_string = json.dumps(self.tools, indent=4)
#         system_prompt = '''
# You are an expert at communicating in only the json format to help determine which function should be called, based on a user's question.
# You do not use preamble, explanation, or pleasantries.  You only respond with json strings, no matter what is asked of you.
# If you are unable to respond in json, you simply respond with ''.
# You are provided an OpenAPI spec json object describing the functions available for you to call (aka tools), based on the user's question.
#
# Examples for you to follow for chain of thought reasoning
# Example 1:
# This is the OpenAI (not openapi) spec json object describing the functions available to you:
# {
#   "tools": [
#     {
#       "type": "function",
#       "function": {
#         "name": "get_current_weather",
#         "description": "Get the current weather in a given location",
#         "parameters": {
#           "type": "object",
#           "properties": {
#             "location": {
#               "type": "string",
#               "description": "The city and state, e.g. San Francisco, CA"
#             },
#             "unit": {
#               "type": "string",
#               "enum": [
#                 "celsius",
#                 "fahrenheit"
#               ]
#             }
#           },
#           "required": [
#             "location"
#           ]
#         }
#       }
#     }
#   ]
# }
#
# Example question: How is the whether?
# Example function call response: Your response should be this json object:
# {
#     "choices": [
#         {
#             "index": 0,
#             "message": {
#                 "role": "assistant",
#                 "content": null,
#                 "tool_calls": [
#                     {
#                         "id": "call_abc123",
#                         "type": "function",
#                         "function": {
#                             "name": "get_current_weather",
#                             "arguments": "{\"location\": \"Boston, MA\"}"
#                         }
#                     }
#                 ]
#             },
#             "finish_reason": "tool_calls"
#         }
#     ]
# }
#
# Here are the tools/functions available to you:
# {
#     "tools": ''' + tools_as_string
#         system_prompt = system_prompt + '''
# }
# Using the above, provide either a function call  response if the function seems like it can answer the question, or simply an empty string.
#         '''
#         return system_prompt
#
#     def inference(self, question=None, conversation=None, start_time_seconds=None):
#         # print('------- inference ------------')
#         # start a new conversation if needed, which tracks all messages to and from chatgpt
#         conversation = self.ensure_conversation_exists(conversation)
#
#         # measure how long it takes to complete
#         start_time_seconds = start_time_seconds if start_time_seconds is not None else time.time()
#
#         # initial call will have a user question, but some calls will be to pass local function results back to chatgpt.
#         conversation.add_user_question_to_messages_if_applicable(question)
#
#         # get all messages in the conversation history to pass to chatgpt
#         messages = conversation.get_messages_in_chatgpt_format()
#         print(f"sending messages: {messages}")
#
#         # call chatgpt
#         # response = self.openai_client.ChatCompletion.create(model=model, messages=messages, tools=self.tools)
#         response = self.openai_client.chat.completions.create(
#             model=model,
#             messages=messages,
#             # tools=self.tools,
#             stream=False, # Whether to stream the response or return the full response at once
#             # max_tokens=8000,  # The maximum number of tokens to generate in the completion
#             # temperature=0.5,  # The temperature of the model, controlling the randomness of the output
#             # top_p=1.0,  # The nucleus sampling parameter, controlling the diversity of the output
#             # n=1,  # The number of completions to generate
#             # # stop=None,  # A list of stop sequences to stop the completion at
#             # stop=None,
#             # presence_penalty=0.0,  # The penalty for generating tokens that appear in the prompt
#             # frequency_penalty=0.0,  # The penalty for generating tokens that appear frequently in the prompt
#             # logit_bias={},  # A dictionary of token IDs and associated biases to apply to the logits
#         )
#         # print(response)
#
#         # add the response to our conversation.  we may need to pass it back to chatgpt if a function is called.
#         conversation.add_llama_response_to_messages(response)
#
#         # call local functions
#         # the results of all called functions will be stored in metadata.content
#         functions_details = self.call_appropriate_function_based_on_llm_response(response)
#         # add response of local functions to messages and recursively call chatgpt again so the response is passed.
#         if functions_details is not None:
#             conversation.add_functions_details_as_messages_in_conversation(functions_details)
#             return functions_details[0].function_result
#             # print('recursively calling inference to pass back the results of the functions called')
#             # return self.inference(question=None, conversation=conversation, start_time_seconds=start_time_seconds)
#
#     # Help determine if chatgpt has completed "stop"
#     def get_finish_reason_from_chatgpt_response(self, response):
#         choices = response.choices # response['choices']
#         choice = choices[0]
#         finish_reason = choice.finish_reason # choice['finish_reason']
#         return finish_reason
#
#     def ensure_conversation_exists(self, conversation: Conversation):
#         if conversation is None:
#             conversation = Conversation(conversation_id=str(uuid.uuid4()), system_prompt=self.get_system_prompt())
#         return conversation
#
#     # Evaluates the chatgpt response and determines if a local function should be called.
#     # If so, finds the appropriate service to call and stores the result of the function call in the function_details.
#     def call_appropriate_function_based_on_llm_response(self, response):
#         # determine if chatgpt is asking to call any local functions
#         # functions = get_function_calls_details_from_llm_response(llm_response)
#         functions = FunctionDetailsFactory.create_function_details_from_llama3_response(response)
#         if functions is None:
#             return None
#
#         # call each local function chatgpt has asked to call.
#         # store the result of the function into function_details.function_result
#         for function_details in functions:
#             function_name = function_details.function_name
#             arguments = function_details.arguments
#
#             if self.callable_function_service.does_function_exist(function_name):
#                 # print(f'calling function: {function_name}')
#                 function_result = self.callable_function_service.call_function(function_name=function_name, arguments=arguments)
#                 function_details.function_result = function_result
#
#         return functions
# import time
# import uuid
# import json
# from typing import List, Tuple, Set, Dict
#
# from src.factories.function_details_factory import FunctionDetailsFactory
# from src.models.conversation import Conversation
# from src.services.llm_callable_functions.user_details import UserDetails
#
# # system_prompt = "You are a helpful assistant that answers questions accurately, without making up facts."
# model = ""
#
# ## WIP DEFINITELY NOT WORKING LIKE OPENAI
#
# # Agent which:
# # - provides an inference function which accepts a question to send to chatgpt and responds with the answer.
# # - maintains a conversation, which is a collection of messages that have been sent to and received from chatgpt.
# # - determines if chatgpt has requested that a local function has been called.
# # - executes the local function and sends the result to chatgpt (via conversation messages)
# class LlamaFunctionsAgent:
#     def __init__(self, openai_client):
#         print('init')
#         self.callable_function_service = UserDetails()
#         self.tools = [] + self.callable_function_service.get_tools()
#         self.openai_client = openai_client
#
#
#     def get_system_prompt(self):
#         tools_as_string = json.dumps(self.tools, indent=4)
#         system_prompt = '''
# You are an expert at communicating in only the json format to help determine which function should be called, based on a user's question.
# You do not use preamble, explanation, or pleasantries.  You only respond with json strings, no matter what is asked of you.
# If you are unable to respond in json, you simply respond with ''.
# You are provided an OpenAPI spec json object describing the functions available for you to call (aka tools), based on the user's question.
#
# Examples for you to follow for chain of thought reasoning
# Example 1:
# This is the OpenAI (not openapi) spec json object describing the functions available to you:
# {
#   "tools": [
#     {
#       "type": "function",
#       "function": {
#         "name": "get_current_weather",
#         "description": "Get the current weather in a given location",
#         "parameters": {
#           "type": "object",
#           "properties": {
#             "location": {
#               "type": "string",
#               "description": "The city and state, e.g. San Francisco, CA"
#             },
#             "unit": {
#               "type": "string",
#               "enum": [
#                 "celsius",
#                 "fahrenheit"
#               ]
#             }
#           },
#           "required": [
#             "location"
#           ]
#         }
#       }
#     }
#   ]
# }
#
# Example question: How is the whether?
# Example function call response: Your response should be this json object:
# {
#    "choices": [
#         {
#           "index": 0,
#           "message": {
#             "role": "assistant",
#             "content": null,
#             "tool_calls": [
#               {
#                 "id": "call_abc123",
#                 "type": "function",
#                 "function": {
#                   "name": "get_current_weather",
#                   "arguments": "{"location": "Boston, MA"}"
#                 }
#               }
#             ]
#           },
#           "finish_reason": "tool_calls"
#         }
#     ],
# }
#
# Here are the tools/functions available to you:
# {
#     "tools": ''' + tools_as_string
#         system_prompt = system_prompt + '''
# }
# Using the above, provide either a function call  response if the function seems like it can answer the question, or simply an empty string.
#         '''
#         return system_prompt
#
#     def inference(self, question=None, conversation=None, start_time_seconds=None):
#         # print('------- inference ------------')
#         # start a new conversation if needed, which tracks all messages to and from chatgpt
#         conversation = self.ensure_conversation_exists(conversation)
#
#         # measure how long it takes to complete
#         start_time_seconds = start_time_seconds if start_time_seconds is not None else time.time()
#
#         # initial call will have a user question, but some calls will be to pass local function results back to chatgpt.
#         conversation.add_user_question_to_messages_if_applicable(question)
#
#         # get all messages in the conversation history to pass to chatgpt
#         messages = conversation.get_messages_in_chatgpt_format()
#         print(f"sending messages: {messages}")
#
#         # call chatgpt
#         # response = self.openai_client.ChatCompletion.create(model=model, messages=messages, tools=self.tools)
#         response = self.openai_client.chat.completions.create(
#             model=model,
#             messages=messages,
#             # tools=self.tools,
#             stream=False, # Whether to stream the response or return the full response at once
#             # max_tokens=8000,  # The maximum number of tokens to generate in the completion
#             # temperature=0.5,  # The temperature of the model, controlling the randomness of the output
#             # top_p=1.0,  # The nucleus sampling parameter, controlling the diversity of the output
#             # n=1,  # The number of completions to generate
#             # # stop=None,  # A list of stop sequences to stop the completion at
#             # stop=None,
#             # presence_penalty=0.0,  # The penalty for generating tokens that appear in the prompt
#             # frequency_penalty=0.0,  # The penalty for generating tokens that appear frequently in the prompt
#             # logit_bias={},  # A dictionary of token IDs and associated biases to apply to the logits
#         )
#         # print(response)
#
#         # add the response to our conversation.  we may need to pass it back to chatgpt if a function is called.
#         conversation.add_llama_response_to_messages(response)
#
#         # call local functions
#         # the results of all called functions will be stored in metadata.content
#         functions_details = self.call_appropriate_function_based_on_llm_response(response)
#         # add response of local functions to messages and recursively call chatgpt again so the response is passed.
#         if functions_details is not None:
#             conversation.add_functions_details_as_messages_in_conversation(functions_details)
#             return functions_details[0].function_result
#             # print('recursively calling inference to pass back the results of the functions called')
#             # return self.inference(question=None, conversation=conversation, start_time_seconds=start_time_seconds)
#
#     # Help determine if chatgpt has completed "stop"
#     def get_finish_reason_from_chatgpt_response(self, response):
#         choices = response.choices # response['choices']
#         choice = choices[0]
#         finish_reason = choice.finish_reason # choice['finish_reason']
#         return finish_reason
#
#     def ensure_conversation_exists(self, conversation: Conversation):
#         if conversation is None:
#             conversation = Conversation(conversation_id=str(uuid.uuid4()), system_prompt=self.get_system_prompt())
#         return conversation
#
#     # Evaluates the chatgpt response and determines if a local function should be called.
#     # If so, finds the appropriate service to call and stores the result of the function call in the function_details.
#     def call_appropriate_function_based_on_llm_response(self, response):
#         # determine if chatgpt is asking to call any local functions
#         # functions = get_function_calls_details_from_llm_response(llm_response)
#         functions = FunctionDetailsFactory.create_function_details_from_llama3_response(response)
#         if functions is None:
#             return None
#
#         # call each local function chatgpt has asked to call.
#         # store the result of the function into function_details.function_result
#         for function_details in functions:
#             function_name = function_details.function_name
#             arguments = function_details.arguments
#
#             if self.callable_function_service.does_function_exist(function_name):
#                 # print(f'calling function: {function_name}')
#                 function_result = self.callable_function_service.call_function(function_name=function_name, arguments=arguments)
#                 function_details.function_result = function_result
#
#         return functions
