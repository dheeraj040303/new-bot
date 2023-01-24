import json
import re
import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot, MessageEntity
from telegram.ext import *
import response as R
from telethon import TelegramClient, sync

# Define the token of your bot
TOKEN = '5614384317:AAHGylxcrCqfJ-XvuNGmxF_mrFgqhKuxljw'

api_id = 27575247
api_hash = '44f4ce1ee458039f7500b0bce10fbc63'
user_name = 'two_backup'

client = TelegramClient('session_name', api_id, api_hash).start()


async def start(update, context):
    await update.message.reply_text("Welcome to linkerin! Type /help for more information.", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("LinkerIn", url='https://linkerin.ga')],
        [InlineKeyboardButton("About", url='https://linkerin.ga/about')]
    ]))


def extract_url(message):
    entities = message.entities
    for entity in entities:
        if isinstance(entity, type(MessageEntity.URL)):
            url = entity.url
            return url
    return None


async def movie(update, context):
    search_query = ""
    for i in context.args:
        search_query += f" {i.upper()}"
    await update.message.reply_text("Cooking results...")
    time.sleep(1)
    await update.message.reply_text("Almost done...")
    mov = client.iter_messages('backup_linker', search=search_query.upper())
    print(mov)
    async for m in mov:
        if isinstance(m.entities, type(None)):
            await update.message.reply_text(f"No results founds...\n{search_query} will be added within 5mins...\nCheck later...")
            await client.send_message('backup_linker', message=search_query.upper())
            return
        await update.message.reply_text(m.entities[0].url)
        return
    await update.message.reply_text(
        f"No results founds...\n{search_query} will be added within 5mins...\nCheck later...")
    await client.send_message('backup_linker', message=search_query.upper())


async def flood(update, context):
    messages = client.iter_messages("Movies_Series_Search", limit=200);
    async for m in messages:
        await client.send_message("backup_linker", message=m)
    await update.message.reply_text("successfully flooded")


async def course(update, context):
    search_query = ""
    for i in context.args:
        search_query += f" {i}"
    print(search_query)
    # Get the channel object
    # Search for messages in the channel
    messages = client.iter_messages('two_backup', search=search_query, limit=10)
    # Iterate through the results
    if not messages:
        return
    async for message in messages:
        await update.message.reply_text((re.search("https?://.*/", message.text)).group())


async def help_command(update, context):
    await update.message.reply_text("1. Use /start to start the bot\n2. Use /course + course_name to get the course link")


async def message_handler(update, context):
    text = str(update.message.text)
    response = R.sample_response(text)
    await update.message.reply_text(response)


async def error(update, context):
    print(f"Update {update} cause error {context.error}")


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("course", course))
    app.add_handler(CommandHandler("movie", movie))
    app.add_handler(CommandHandler('flood', flood))
    app.add_handler(MessageHandler(filters.TEXT, message_handler))
    app.add_error_handler(error)
    app.run_polling()


main()