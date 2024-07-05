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
    @bot.on_message(filters.document & filters.user(Config.AUTH_USERS))
    async def handle_document(client, document_message):
        if document_message.document.file_name == "data.json":
            file_path = await document_message.download()
            await load_json_data(file_path)  # Load the JSON data from the file
            os.remove(file_path)  # Clean up the file after loading

            await message.reply_text("Send the channel ID where you want to forward the messages:")
            
            # Wait for the user to reply with the target channel ID
            @bot.on_message(filters.text & filters.user(Config.AUTH_USERS))
            async def handle_channel_id(client, channel_id_message):
                target_channel_id = int(channel_id_message.text)
                
                await message.reply_text("Forwarding messages...")

                # Forward the messages to the target channel
                for msg in messages:
                    try:
                        await client.get_chat(target_channel_id)  # Ensure the bot has met the target channel
                        await client.copy_message(
                            chat_id=target_channel_id,
                            from_chat_id=msg["chatid"],
                            message_id=msg["msgid"]
                        )
                    except Exception as e:
                        await message.reply_text(f"Failed to forward message ID {msg['msgid']}: {e}")

                await message.reply_text("Done forwarding messages.")
                # Remove the inner handler after use
                bot.remove_handler(handle_channel_id)

        else:
            await message.reply_text("Uploaded file is not data.json. Please try again.")
        # Remove the inner handler after use
        bot.remove_handler(handle_document)

# Start the bot
bot.run()
