from ollama._client import AsyncClient
import os
import sys

async def character_generator():
    character = sys.argv[1]
    print(f"You are creating a character for {character}.")

    foldername = ''.join(character.split()).lower()
    directory = os.path.join(os.path.dirname(__file__), foldername)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    client = AsyncClient()  # Initialized the AsyncClient
    bio = await client.generate(
        model="llama3:8b-instruct-q8_0",
        prompt=(
            f"create a bio of {character} in a single long paragraph. Instead of saying '{character} is...' or "
            f"'{character} was...' use language like 'You are...' or 'You were...'. Then create a paragraph describing the "
            f"speaking mannerisms and style of {character}. Don't include anything about how {character} looked or what they "
            f"sounded like, just focus on the words they said. Instead of saying '{character} would say...' use language like "
            f"'You should say...'. If you use quotes, always use single quotes instead of double quotes. If there are any "
            f"specific words or phrases you used a lot, show how you used them."
        )
    )

    content = f"FROM llama3\nSYSTEM \"\"\"\n{bio['response'].replace('\n', ' ')} All answers to questions should be related back to what you are most known for.\n\"\"\""
    
    with open(os.path.join(directory, 'Modelfile'), 'w') as file:
        file.write(content)
    print('The file has been saved!')

if __name__ == "__main__":
    import asyncio
    asyncio.run(character_generator())
