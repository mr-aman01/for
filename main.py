import json
import time
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

# Load JSON data
json_data = '''
[{"batch": "74 Biology (12th Class) (KUMAREDUTAINMENT)", "index": "1", "chatid": -1002079646989, "msgid": 294059, "title": "Sexual Reproduction in Flowering Plants Part-11", "topic": "74 Biology (12th Class) (KUMAREDUTAINMENT)"}, {"batch": "74 Biology (12th Class) (KUMAREDUTAINMENT)", "index": "2", "chatid": -1002079646989, "msgid": 294049, "title": "Sexual Reproduction in Flowering Plants Part-11_notes", "topic": "74 Biology (12th Class) (KUMAREDUTAINMENT)"}, ... ]
'''

# Parse JSON data
messages = json.loads(json_data)

@bot.on_message(
    filters.chat(Config.AUTH_USERS) & filters.private &
    filters.incoming & filters.command("startforward", prefixes=["/", "!", "."])
)
async def start_forwarding(bot: Client, m: Message):
    await m.reply_text("Starting to forward messages...")

    # Iterate through each message in the JSON data
    for message_info in messages:
        chat_id = message_info["chatid"]
        message_id = message_info["msgid"]
        title = message_info["title"]

        try:
            # Forward the message to the target channel
            await bot.forward_messages(
                chat_id=Config.TARGET_CHAT_ID,
                from_chat_id=chat_id,
                message_ids=message_id
            )
            await bot.send_message(
                chat_id=Config.TARGET_CHAT_ID,
                text=f"Title: {title}"
            )

            # Optional: Add a delay between forwarding messages to avoid hitting rate limits
            time.sleep(2)
        except Exception as e:
            await m.reply_text(f"Error forwarding message {message_id}: {e}")

    await m.reply_text("Done forwarding all messages.")

if __name__ == "__main__":
    bot.run()