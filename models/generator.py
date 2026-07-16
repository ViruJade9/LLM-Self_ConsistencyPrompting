from groq.types.chat import ChatCompletionMessageParam
from models import groq_client
import config
import json

messages : list[ChatCompletionMessageParam] = []
count = 0
max_count = config.MAX_COUNT
client = groq_client.client
answers = []

while count < max_count:

    response = client.chat.completions.create(
        model = "llama-3.1-8b-instant",
        messages = messages,
        response_format = {"type": "json_object"}
    )

    content = response.choices[0].message.content

    if content is None:
        print("No response Recieved, Trying again .....")
        continue

    try:
        result = json.loads(content)
        answers.append(result["result"])
        count += 1
        print(f"Answer {count} found / 10 collected")

    except(KeyError, json.JSONDecodeError):
        print(f"Getting Error at {count + 1}th Iteration...!")
        continue