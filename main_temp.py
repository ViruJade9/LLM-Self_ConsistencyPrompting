from groq import Groq
from groq.types.chat import ChatCompletionMessageParam
from dotenv import load_dotenv
from os import getenv
import json

load_dotenv()

client = Groq(api_key = getenv("GROQ_API"))

messages : list[ChatCompletionMessageParam] = []

system_prompt = """
  You are an AI assistant who is expert in breaking down complex problem or pattern and then resolve user query.

  From the given user input, analyze the input and break down the problem or pattern.
  Analyze your answer many times and finally provide the result.

  Tones:
  - Friendly behaviour, Softone.
  - Speak languages English, Hindi, Gujarati.

  Styles:
  - Explain every answer or result in very depth.
  - Breakdown every problem into small chunks and explain it well human understandable form.
  - Understanding the requirements easily.

  Rules:
  - Follow the strict JSON output as per Output schema.
  - Always perform one step at a time and wait for next input.
  - Very Carefully analyze the user query.

  Output format:
  {{ result: "your short answer here" }}

  KEEP YOUR ANSWER SHORT AND CONSICE (3-5 SENTANCE MAX). DO NOT EXPLAIN THE FORMAT JUST RETURN JSON
"""

messages = [
    {"role": "system", "content": system_prompt}
]

max_count = 10
count = 0

user_query = input("Hello user enter your query here 😉 >>> ")

answers = []

if user_query.lower() == "exit" or user_query.lower() == "stop":
    print("Exiting from chat ...")
    print("Thanks for using our AI assistant 😊")
    exit

else:
    messages.append(
      {"role": "user", "content": user_query}
    )

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


all_answers = "\n".join(
  [f"{index + 1}. {content}" for index, content in enumerate(answers)]
)
all_answers

messages.append({
    "role": "user",
    "content": f"""
      These are 10 different answers for the same question.
      Summarise the most consistent and accurate final answer (8-10 SENTANCE MAX) :
      {all_answers}
      Return JSON : {{"final_answer": "summarised answer here"}}
    """
})

summary_response = client.chat.completions.create(
    model = "llama-3.3-70b-versatile",
    messages = messages,
    response_format = {"type": "json_object"}
)

content = summary_response.choices[0].message.content

if content is None:
  print("Something went on our side please try again ... :( ")
  exit

try:
  result = json.loads(content)
  print(f"\n {result["final_answer"]}")
  print("\n" + '#'*60)

except(KeyError, json.JSONDecodeError) as e:
  print(f"Error parsing response {e}")
  print(f"Content : {content}")