import os

import discord
import openai
from dotenv import load_dotenv

load_dotenv()

# Load environment variables (you can also hardcode these for testing purposes)
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_KEY')

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY

# Set up Discord client
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

# Jungian dream analysis template
JUNGIAN_ANALYSIS_PROMPT = """
You are a Jungian psychologist. A person has shared the following dream with you:

"{dream}"

Provide a detailed analysis of the dream using Carl Jung's concepts such as archetypes, the collective unconscious, the shadow, anima/animus, and symbols.

Dream analysis:
"""


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    print(f"received message {message}")  # TODO fix
    await message.channel.send("I am losing my sanity")
    # Ignore messages from the bot itself
    if message.author == client.user:
        return
    if message.channel.name != "dreams":
        print(f"channel name is {message.channel.name}")
        return

        # Check if the message contains a dream
    if "dream" in message.content.lower():
        dream_text = message.content

        # Create the prompt for GPT
        prompt = JUNGIAN_ANALYSIS_PROMPT.format(dream=dream_text)

        # Call OpenAI's GPT API to analyze the dream
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=500,
                temperature=0.7
            )

            # Get the response text (Jungian dream analysis)
            analysis = response['choices'][0]['text'].strip()

            # Send the analysis as a reply to the user's dream
            await message.channel.send(f"Jungian Dream Analysis:\n{analysis}")

        except Exception as e:
            await message.channel.send("Sorry, something went wrong with the dream analysis.")
            print(f"Error: {e}")


# Start the bot
client.run(DISCORD_TOKEN)
