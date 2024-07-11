import discord
import json
import os
from flask import Flask 

intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)

# Load config file (if needed)
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    print("config.json file not found")
    exit()
except json.JSONDecodeError as e:
    print(f"Error decoding JSON from config.json: {e}")
    exit()

# Fetch bot token from Replit secrets
token = os.getenv('DISCORD_TOKEN')

if not token:
    raise ValueError("Bot token not found in Replit secrets")

responses = config.get('responses', {})

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Check if bot was mentioned
    if client.user.mentioned_in(message):
        msg_content = message.content.strip().lower()
        print(f"Received message: '{msg_content}'")

        trigger_found = False
        for trigger, response in responses.items():
            print(f"Checking if trigger '{trigger}' is in message '{msg_content}'")
            if trigger in msg_content:
                print(f"Trigger found: '{trigger}' -> Responding with: '{response}'")
                # Send response
                sent_message = await message.channel.send(response)
                # Delete the user's message
                await message.delete()
                trigger_found = True
                break

        if not trigger_found:
            print(f"No trigger found in: '{msg_content}'")
            print("Available triggers:", list(responses.keys()))
# Create a Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

# Run the Flask app in a separate thread
def run_flask():
    app.run(host='0.0.0.0', port=5000)

# Start the bot and Flask app
if __name__ == "__main__":
    from threading import Thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
client.run(token)
