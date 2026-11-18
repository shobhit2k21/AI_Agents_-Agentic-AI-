from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv() # looks for .env file in the current directory and loads the environment variables
messages = [] # for temporary memory

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
      messages= messages
         )

    messages.append(
           {"role": "assistant", "content": response.choices[0].message.content}
       )


    print("Assistant: " + response.choices[0].message.content) # response from LLM 