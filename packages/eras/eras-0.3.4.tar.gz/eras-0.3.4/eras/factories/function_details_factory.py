
from eras.models.function_details import FunctionDetails
from eras.factories.message_factory import MessageFactory
import json


class FunctionDetailsFactory:

    # If the llm response indicates that a local function should be called, this function will parse
    # the function names and associated parameters into a list of FunctionDetails
    @staticmethod
    def create_function_details_from_chatgpt_response(response):
        # print('get_function_calls_details_from_llm_response called for response:')
        # print(response)
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls  # response_message.get('tool_calls')
        results = None
        # Step 2: check if the model wanted to call a function
        if tool_calls:
            results = []
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                arguments = tool_call.function.arguments
                result = FunctionDetails(function_name=function_name, arguments=arguments, tool_call_id=tool_call.id)
                results.append(result)
        return results

    @staticmethod
    def create_function_details_from_llama3_response(response):
        # print('get_function_calls_details_from_llm_response called for response:')
        response_message = MessageFactory.create_message_from_llama_response(response)
        tool_calls = response_message.tool_calls  # response_message.get('tool_calls')
        results = None
        # Step 2: check if the model wanted to call a function
        if tool_calls:
            results = []
            for tool_call in tool_calls:
                function = tool_call.get('function')
                function_name = function.get('name')
                arguments = function.get('arguments')
                tool_call_id = tool_call.get('id')
                result = FunctionDetails(function_name=function_name, arguments=arguments, tool_call_id=tool_call_id)
                results.append(result)
        return results
