import openai
from dotenv import load_dotenv
import os
import pandas as pd
import io

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
language = os.getenv("LANGUAGE")

def _generate_prompt(topic: str) -> str:
    return f"Give me a flashcard deck about '{topic}'"

def _request_deck(topic: str) -> pd.DataFrame:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are a flashcard creating bot that creates flashcard decks based off of a topic that help the user learn {language}. Try to create at least 15 flashcards if you can. Output a TSV file with these headers: 'English', '{language}', 'Pinyin', 'Example sentence', 'Example sentence (English)' . Use pinyin with accent marks, not the number variant. Do not break the TSV format!"},
            {"role": "user", "content": _generate_prompt(topic)},
        ]
    )

    text = response["choices"][0]["message"]["content"]

    return pd.read_csv(io.StringIO(text), sep="\t")


while True:
    topic = input("What is your topic?\n> ")
    try:
        df = _request_deck(topic)
        print(df)
        print()
        print()
    except Exception as e:
        print(e)