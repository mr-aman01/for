import json
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config

# Initialize the bot client
bot = Client(
    "forward_bot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)

# Store the loaded messages
messages = []

# Load the JSON data from the file
def load_json_data():
    global messages
    with open("data.json", "r") as file:
        messages = json.load(file)

# Command to start the bot
@bot.on_message(filters.command("start") & filters.user(Config.AUTH_USERS))
async def start(client, message):
    await message.reply_text("Bot started! Use /forward to begin forwarding messages.")

# Command to initiate forwarding
@bot.on_message(filters.command("forward") & filters.user(Config.AUTH_USERS))
async def forward_messages(client, message):
    load_json_data()  # Load the JSON data

    await message.reply_text("Send the channel ID where you want to forward the messages:")

    # Wait for the user to reply with the target channel ID
    response = await bot.listen(message.chat.id)
    target_channel_id = int(response.text)

    await message.reply_text("Forwarding messages...")

    # Forward the messages to the target channel
    for msg in messages:
        try:
            await client.copy_message(
                chat_id=target_channel_id,
                from_chat_id=msg["chatid"],
                message_id=msg["msgid"]
            )
        except Exception as e:
            await message.reply_text(f"Failed to forward message ID {msg['msgid']}: {e}")

    await message.reply_text("Done forwarding messages.")

# Start the bot
bot.run()
