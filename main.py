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

# Load the JSON data from the uploaded file
async def load_json_data(file_path):
    global messages
    with open(file_path, "r") as file:
        messages = json.load(file)

# Command to start the bot
@bot.on_message(filters.command("start") & filters.user(Config.AUTH_USERS))
async def start(client, message):
    await message.reply_text("Bot started! Use /forward to begin forwarding messages.")

# Command to initiate forwarding
@bot.on_message(filters.command("forward") & filters.user(Config.AUTH_USERS))
async def forward_messages(client, message):
    await message.reply_text("Please upload the data.json file.")
    
    # Wait for the user to upload the data.json file
    response = await bot.ask(message.chat.id, "Upload the data.json file:")

    # Check if the response contains a document (file)
    if response.document:
        file_path = await response.download()
        await load_json_data(file_path)  # Load the JSON data from the file
        os.remove(file_path)  # Clean up the file after loading
    else:
        await message.reply_text("No file uploaded. Please try again.")
        return

    await message.reply_text("Send the channel ID where you want to forward the messages:")

    # Wait for the user to reply with the target channel ID
    response = await bot.ask(message.chat.id, "Provide the target channel ID:")
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
