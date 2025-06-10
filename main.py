import argparse
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

parser = argparse.ArgumentParser()
parser.add_argument("prompt")
parser.add_argument(
    "-v",
    "--verbose",
    dest="verbose",
    action="store_true",
    help="if the program should print verbose",
)


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    args = parser.parse_args()

    if not args.prompt:
        print("prompt not provided ")
        sys.exit(1)

    prompt = sys.argv[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=messages
    )

    if args.verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print(response.text)


main()
