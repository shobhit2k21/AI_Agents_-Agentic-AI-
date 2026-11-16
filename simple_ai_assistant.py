from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
print("Connecting to Ollama...")
response = client.chat.completions.create(
    model="qwen3:4b",
    messages=[
        {"role": "user", "content": "What is JAVA in CS?"}
    ]
)


print(response.choices[0].message.content)