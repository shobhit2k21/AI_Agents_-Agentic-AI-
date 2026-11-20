#standard library imports
import os

#third party impots
from openai import OpenAI
from dotenv import load_dotenv

#local modules
from Utilities.utilities import log
from tools import TOOLS, run_tools

load_dotenv() # looks for .env file in the current directory and loads the environment variables
messages = [] # for temporary memory

messages.append({"role": "system", "content": "You are a helpful assistant who explains concepts simply under 20 words."}) # system message
MAX_CALLS = 5 # maximum number of tool calls allowed per user input

client = OpenAI(
     base_url=os.getenv("BASE_URL"),
     api_key=os.getenv("API_KEY")
    )


# Chained Tool_Calling
while True:
    user_input = input("\nAsk: ")  # user questions
    if user_input.lower() in ["exit", "quit", "bye"]:
        break

    messages.append({"role": "user", "content": user_input})
    

    for steps in range(MAX_CALLS):
         response = client.chat.completions.create(
              model=os.getenv("MODEL"),
              messages= messages,
              tools=TOOLS
            )
         
         msg = response.choices[0].message   

         if not msg.tool_calls:
            break

         log(f"Step {steps + 1}: model requested: {len(msg.tool_calls)} tool call(s).")
         
         for tool_call in msg.tool_calls:
            result = run_tools(tool_call)

            messages.append(
                 {
                    "role": "tool",
                    "tool_id": tool_call.id,
                    "content": str(result)
                }
             )

    else :
      fallback = "Maximum tool calls reached. Sorry I can't help with that."
      messages.append({"role": "assistant", "content": fallback})
      continue


    messages.append(
           {"role": "assistant", "content": msg.content}
       )


    print("Assistant: " + (msg.content or "")) # response from LLM 