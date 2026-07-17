import json
import config
from models.groq_client import client
from prompts.system_prompt import SYSTEM_PROMPT

def generate_answer(user_query:str) -> list[str]:
    """
    Generate multiple answers for the same question
    """

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_query
        }
    ]

    answers = []
    count = 0

    while count < config.MAX_COUNT:

        response = client.chat.completions.create(
            model = config.GENERATOR_MODEL,
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
            print(f"Answer {count} found / {config.MAX_COUNT} collected")

        except(KeyError, json.JSONDecodeError):
            print(f"Getting Error at {count + 1}th Iteration...!")
            continue
    
    return answers