import json

from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOLS, FUNCTION_MAP
import os

load_dotenv() # looks for .env file in the current directory and loads the environment variables
messages = [] # for temporary memory
messages.append({"role": "system", "content": "You are a helpful assistant who explains concepts simply under 20 words."}) # system message

while True:
    user_input = input("\nAsk: ")  # user questions
    if user_input.lower() in ["exit", "quit", "bye"]:
        break

    messages.append({"role": "user", "content": user_input})

    client = OpenAI(
     base_url=os.getenv("BASE_URL"),
     api_key=os.getenv("API_KEY")
       )

    print("Connecting to Ollama...")

    response = client.chat.completions.create(
      model=os.getenv("MODEL"),
      messages= messages,
      tools=TOOLS
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        messages.append(msg)

        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments or "{}")

            fn = FUNCTION_MAP[func_name]
            result = fn(**func_args)

            messages.append(
                {
                    "role": "tool",
                    "tool_id": tool_call.id,
                    "content": str(result)
                }
            )

        #2nd call
        response = client.chat.completions.create(
          model=os.getenv("MODEL"),
          messages=messages
        )     

        msg = response.choices[0].message

    messages.append(
           {"role": "assistant", "content": msg.content}
       )


    print("Assistant: " + msg.content) # response from LLM 