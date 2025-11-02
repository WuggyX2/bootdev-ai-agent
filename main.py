import argparse
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import available_functions, call_function

parser = argparse.ArgumentParser()
parser.add_argument("prompt")
parser.add_argument(
    "-v",
    "--verbose",
    dest="verbose",
    action="store_true",
    help="if the program should print verbose",
)

SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

MODEL = "gemini-2.0-flash-001"

def main():
    """
    Main entry function for the program
    """
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    args = parser.parse_args()

    if not args.prompt:
        print("prompt not provided ")
        sys.exit(1)

    prompt = sys.argv[1]
    print_verbose = args.verbose


    if print_verbose:
        print(f"User prompt: {prompt}")


    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    for _ in range(20):
        try:
            response = generate_content(client, messages, print_verbose)

            if response is not None:
                print("Final response:")
                print(response)
                break
        except Exception as e:
            print("Error " + e.__cause__)
            break


def generate_content(client, messages, print_verbose):
    generation_config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=SYSTEM_PROMPT
    )

    response = client.models.generate_content(
        model=MODEL,
        contents=messages,
        config=generation_config
    )

    for candidate in response.candidates:
        messages.append(candidate.content)

    if print_verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, print_verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if print_verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    messages.append(types.Content(role="user", parts=function_responses))

    return None

main()
