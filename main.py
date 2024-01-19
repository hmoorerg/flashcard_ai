import openai
from dotenv import load_dotenv
import os
import pandas as pd
import io
import argparse # Import the argparse module

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
language = os.getenv("LANGUAGE")

def _generate_prompt(language: str, topic: str) -> str:
    return f"Give me a {language} flashcard deck about '{topic}'"

def _request_deck(topic: str) -> pd.DataFrame:
    instructions = f"""You are a flashcard creating bot that creates flashcard decks based off of a topic that help the user learn {language}. Try to create at least 15 flashcards if you can. 
    
    # Your task:
    Output a TSV file with these headers: 'English', '{language}', 'Pinyin', 'Example sentence', 'Example sentence (English)', 'Character meanings'.
    
    # Column-specific instrutions:
    - The 'English' column should include the English translation of the word.
    - The 'Pinyin' column should include pinyin like 'hóngsè' for the word '红色'.
    - The 'Example sentence' column should include a sentence that uses the word in context. Only use 汉字, not 拼音.
    - The 'Character meanings' is a place to write meanings for multi-character terms that might help me remember the whole word (For example, for '服务员' it would be helpful to know that '服务" means "to serve"). Do not provide a definition for the whole word because that is already provided in the 'English' column, just leave the field empty. The format should be either "" or "(hanzi)=(meaning);(hanzi)=(meaning);..." (not including the quotes).
    
    # Important notes:
    Do not break the TSV format! If you do then I will not be able to import the deck into Anki.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": _generate_prompt(language=language, topic=topic)},
        ]
    )

    text = response["choices"][0]["message"]["content"]

    return pd.read_csv(io.StringIO(text), sep="\t")

# Create an argument parser object
parser = argparse.ArgumentParser(description="A flashcard creating bot")

# Add a --csv argument that takes a boolean value
parser.add_argument("--csv", action="store_true", help="Write to a csv file")


# Parse the arguments
args = parser.parse_args()

while True:
    topic = input("What is your topic?\n> ")
    try:
        df = _request_deck(topic)
        print(df)
        print()
        print()
        # If the --csv argument is True, write the dataframe to a csv file with the topic name
        if args.csv:
            df.to_csv(f"{topic}.csv", index=False)
            print(f"Saved to {topic}.csv")
    except Exception as e:
        print(e)
