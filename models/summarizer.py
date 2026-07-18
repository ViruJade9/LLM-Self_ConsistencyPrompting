import json
import config
from models.groq_client import client
from prompts.summarizer_prompt import SUMMARY_PROMPT

def summarizer_answers(answers: list[str]) -> str:
  """
    Summarize all generated responses into one final answer.

    Args:
        answers (list[str]):
            List of generated responses.

    Returns:
        str:
            Final summarized answer.
    """

  all_answers = "\n".join(
    [
      f"{index + 1}. {content}" 
      for index, content in enumerate(answers)
    ]
  )

  messages = [
    {
      "role": "system",
      "content": SUMMARY_PROMPT
    },
    {
      "role": "user",
      "content": 
      f"""
      {all_answers}
      """
    }
  ]

  response = client.chat.completions.create(
      model = config.SUMMARY_MODEL,
      messages = messages,
      response_format = {"type": "json_object"}
  )

  content = response.choices[0].message.content

  if content is None:
    raise Exception("Summary response is empty")
  
  result = json.loads(content)

  return result["final_answer"]