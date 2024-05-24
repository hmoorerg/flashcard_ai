import json
from openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
import argparse
from rich.console import Console
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.output import ColorDepth
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import Frame, TextArea


class Flashcard:
    def __init__(self, english, hanzi, pinyin, example_sentence, character_meanings = None, usage_notes = None):
        self.english = english
        self.hanzi = hanzi
        self.pinyin = pinyin
        self.example_sentence = example_sentence
        self.character_meanings = character_meanings
        self.usage_notes = usage_notes

    def __repr__(self):
        return f"Flashcard(English={self.english}, Hanzi={self.hanzi}, Pinyin={self.pinyin}, Example_sentence={self.example_sentence}, Character_meanings={self.character_meanings}, usage_notes={self.usage_notes})"


def create_flashcards(flashcards):
    """
    Adds the specified flashcards to the user's Anki deck.

    :param flashcards: List of dictionaries, each representing a flashcard.
                       Each flashcard contains 'English', 'Pinyin', 
                       'Example sentence', and 'Character meanings'.
    """
    df = pd.DataFrame([vars(flashcard) for flashcard in flashcards])
    print(df)


load_dotenv()

client = OpenAI()
language = os.getenv("LANGUAGE")

def _generate_prompt(language: str, topic: str) -> str:
    return f"Give me a {language} flashcard deck about '{topic}'."

def _request_deck(topic: str) -> pd.DataFrame:
    instructions = f"""You are a flashcard creating bot that creates flashcard decks based off of a topic that help the user learn {language}. Try to create at least 15 flashcards if you can. Return your output as JSON. Do not include any newline characters like '\n'"""

    tools = [
        {
            "type": "function",
            "function": {
                "name": "create_flashcards",
                "description": "Adds the specified flashcards to the user's Anki deck",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "flashcards": {
                            "type": "array",
                            "description": "The flashcards to add to the user's deck",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "english": {
                                        "type": "string",
                                        "description": "English translation of the word."
                                    },
                                    "hanzi": {
                                        "type": "string",
                                        "description": "Chinese translation of the word. (in hanzi, not Pinyin)."
                                    },
                                    "pinyin": {
                                        "type": "string",
                                        "description": "Pinyin representation of the word using tone marks, like 'hóngsè' for the word '红色'."
                                    },
                                    "example_sentence": {
                                        "type": "string",
                                        "description": "A sentence using the word in context with 汉字.",
                                    },
                                    "character_meanings": {
                                        "type": "string",
                                        "description": "Meanings for multi-character terms to help remember the whole word, formatted as '(hanzi)=(meaning);(hanzi)=(meaning);...' or an empty string"
                                    },
                                    "usage_notes": {
                                        "type": "string",
                                        "description": "Additional notes for cases where an extra explanation might be helpful (for example, maybe a word is used frequently with a grammar rule like '了')"
                                    }
                                    
                                },
                                "required": ["english", "hanzi", "pinyin", "example_sentence"]
                            }
                        }
                    },
                    "required": ["flashcards"]
                }
            }
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": _generate_prompt(language=language, topic=topic)},
        ],
        tools=tools,
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        available_functions = {
            "create_flashcards": create_flashcards,
        }
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            
            flashcards_to_add = [Flashcard(**fc) for fc in function_args.get("flashcards", [])]
            
            # Todo: make this a pure function
            function_to_call(
                flashcards=flashcards_to_add,
            )

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
