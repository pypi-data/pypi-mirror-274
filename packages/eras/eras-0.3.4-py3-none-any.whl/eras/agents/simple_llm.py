import time

from eras.config.config import config
from eras.models.simple_stream_inference_callable import (SimpleStreamInferenceCallable, LLMTextReceivedCallable,
                                                          LLMResponseCompletedCallable)


class SimpleLLM:
    def __init__(self, openai_client):

        self.client = openai_client

    def stream_inference(self, prompt: str, handle_on_text_received: LLMTextReceivedCallable,
                         handle_response_complete: LLMResponseCompletedCallable) -> None:
        # start_time_seconds = time.time()
        system_message = f"""
        You are friendly AI assistant that runs in a terminal.  Format all responses you provide for the terminal for the operating system {config.get_user_operating_system()}.
        Your responses are streamed to the terminal via python print statements.
        """
        completion = self.client.chat.completions.create(
            model=config.get_model_name(),
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            stream=True,  # Whether to stream the response or return the full response at once
        )

        for chunk in completion:
            text = chunk.choices[0].delta.content
            if text is not None:
                handle_on_text_received(text)

        handle_response_complete()
        # print()
        # print(f"answer received in {time.time() - start_time_seconds} seconds.")

    def get_simple_stream_inference_callable(self) -> SimpleStreamInferenceCallable:
        return lambda prompt, handle_on_text_received, handle_response_complete: (
            self.stream_inference(prompt, handle_on_text_received, handle_response_complete))
