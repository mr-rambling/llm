import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import call_function, available_functions
from prompts import system_prompt
from config import ITERATIONS

def main(): 
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    verbose = '--verbose' in sys.argv
    prompts = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            prompts.append(arg)

    if not prompts:
        print("No prompt provided.")
        sys.exit(1)

    user_prompt = " ".join(prompts)

    if verbose:
        print(f"User prompt: {user_prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    
    for i in range(ITERATIONS):
        try:
            response, messages = generate_content(client, messages, verbose)
        except Exception as e:
            print(f"Error occurred: {e}")
        if not response.function_calls:
            if response.text:
                print(f"Final response: {response.text}")
                break

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
            )
    )

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    for candidate in response.candidates:
        messages.append(candidate.content)

    if not response.function_calls:
        return response, messages

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if not (function_call_result.parts or function_call_result.parts[0].function_response):
            raise Exception("Empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("No function responses generated, exiting.")

    messages.append(types.Content(role='tool', parts=function_responses))

    return response, messages

if __name__ == "__main__":
    main()
