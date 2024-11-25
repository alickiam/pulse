from openai import OpenAI
import os
from pydantic import BaseModel

class Compatibility(BaseModel):
    affection: int
    vulnerability: int
    kindness:int
    other: int
    negative: int
    explanation: str


def send_prompt(prompt):
    client = OpenAI()
    api_key = os.getenv("OPENAI_API_KEY")
    chat_completion = client.beta.chat.completions.parse(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o",
        response_format=Compatibility
    )
    return chat_completion.choices[0].message.parsed

def get_overall_conversation_score(score):
    return (score.affection + score.vulnerability + score.kindness + score.other - score.negative) / 4

def ask_match(conversation):
    prompt = open("conversation_prompt.txt", "r").read()
    return send_prompt(prompt + conversation)

def ask_advice(conversations):
    prompt = open("person_prompt.txt", "r").read()
    for i in conversations:
        prompt += "\n\nConversation:\n" + i
    return send_prompt(prompt)