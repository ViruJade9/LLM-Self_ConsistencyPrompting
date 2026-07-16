from models import generator
from models import groq_client
from prompts import summariser_prompt

answers = generator.answers
client = groq_client.client
messages = []

all_answers = "\n".join(
  [f"{index + 1}. {content}" for index, content in enumerate(answers)]
)

messages = [
    {
        
    }
]

summary_response = summary_response = client.chat.completions.create(
    model = "llama-3.3-70b-versatile",
    messages = messages,
    response_format = {"type": "json_object"}
)