# flashcard_ai

A project to automatically generate flashcards for learning Chinese.

## How does it work?
When you run the program, it will ask you for a topic. Type in a topic and the LLM will generate a list of flashcards.

## How do I make it generate flashcards in the correct format?
I force the LLM to output using valid json and provide it with a `create_flashcards` function to call that is annotated with the required information for each flashcard.
