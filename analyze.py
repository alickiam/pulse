from openai import OpenAI
import os
from pydantic import BaseModel
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import math

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

# heartrate given in timestamps of heartrate

# gonna use min max scaler when i have it
def get_heartrate_score(heartrates):
    diff = []
    for i in range(1, len(heartrates)):
        diff.append(heartrates[i]-heartrates[i-1])
    rates = []
    num_beats = 0
    last_time = 0
    time = 0
    for i in diff:
        time += i
        num_beats = num_beats + 1
        if (time > last_time + 5):
            rates.append(num_beats*60/5)
            num_beats = 0
            last_time = time
    print(rates)
    rates.sort()
    n = len(rates)
    print(rates)
    score = rates[math.floor(n*.9)]-rates[math.floor(n*.1)]
    return score