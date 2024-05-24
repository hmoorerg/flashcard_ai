# flashcard_ai
Quickly generate Flashcard decks for what *you* want to talk about

![image](https://github.com/hmoorerg/flashcard_ai/assets/5322865/e265daa9-8734-4d1b-95b4-29ca2fe6e581)

## Why was this created?
I wanted to be able to talk about my interests but words like "machine learning" won't be taught in a textbook. This LLM program fixes this issue by giving you flashcards for anything you want

## How does it work?
When you run the program, it will ask you for a topic. Type in a topic and the LLM will generate a list of flashcards.

Here are some examples of what you can ask:
- "Give me words for ordering at a coffee shop"
- "Teach me how to talk about cooking using sous vide"
- "Talking about my day where I went for a run and saw an otter"
  

## How do I make it generate flashcards in the correct format?
I force the LLM to output using valid json and provide it with a `create_flashcards` function to call that is annotated with the required information for each flashcard. This is then put into a pandas dataframe to make it easy to export in many different formats.
