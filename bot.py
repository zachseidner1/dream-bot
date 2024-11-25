import os

import discord
import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Load environment variables (you can also hardcode these for testing purposes)
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_KEY')

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY
openai_client = OpenAI(
    api_key=OPENAI_API_KEY
)

# Set up Discord client
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

# Jungian dream analysis template
JUNGIAN_ANALYSIS_PROMPT = """
You are a Jungian psychologist. A person will share their dream with you.

Provide a concise but impactful analysis of the dream. The analysis should reveal things about the user that they may not initially expect.
Remember to make the analysis concise, but impactful. Concision is important though. 
"""


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    print(f"received message {message}")
    # Ignore messages from the bot itself
    if message.author == client.user:
        return
    if message.channel.name != "dreams":
        print(f"channel name is {message.channel.name}")
        return

        # Check if the message contains a dream
    if "dream" in message.content.lower():
        dream_text = message.content

        # Call OpenAI's GPT API to analyze the dream
        try:
            response = openai_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": JUNGIAN_ANALYSIS_PROMPT
                            }
                        ]
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": dream_text
                            }
                        ]
                    }
                ],
                model="gpt-4o-mini"
            )

            # Get the response text (Jungian dream analysis)
            analysis = response.choices[0].message.content

            # Send the analysis as a reply to the user's dream
            await message.channel.send(f"Dream Analysis:\n{analysis}")

        except Exception as e:
            await message.channel.send("Sorry, something went wrong with the dream analysis.")
            print(f"Error: {e}")
    else:
        print(f"message lower: {message.content.lower()}")

    # Start the bot


client.run(DISCORD_TOKEN)
