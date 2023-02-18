import datetime
import json
import re
import time
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot, MessageEntity
from telegram.ext import *
from telethon.tl.types import MessageEntityTextUrl

import response as R
from telethon import TelegramClient, sync
from urlextract import URLExtract

extractor = URLExtract()
# Define the token of your bot
TOKEN = '5673905050:AAFOUxkIDikmrP4kdlNcTn2hMr9341aoEFA'

api_id = 27575247
api_hash = '44f4ce1ee458039f7500b0bce10fbc63'
user_name = 'two_backup'
session_string = '1BVtsOKEBuzhwIpU_AuhlauBM9-30gEf7-jovu5m8AdAkBhWhof7wshA1ES4kWqIHzVt4M4ecii8Numw6teG72pQI5J7aV2qnA7vQXSwrZUdMa-bIBHNIQySMoqEZTCh25HRQwCCDQjcUf40RcmcAllmXYvn71xcWfPHU193zF7P-IDGykcZZXif84AqOG0UaJLVdyPoDCtT3TxpkbUFBY7EcstvYuH1PJGfD47yEczxDTR7LP2fyUy2_27iZ_7VAlU_KcmXpILdn8U8eZdtLp1DH1SAvIvV5iKg086vLeUe8XBmvEECzWew7uN2a2RfjJPss2uyTtOF3x37MUH4Ldv0HgdhKWO8='
client = TelegramClient("toa", api_id, api_hash)
client.start()
entity = client.get_entity("backup_linker")


async def start(update, context):
    await update.message.reply_text("Welcome to linkerin! Type /help for more information.", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("LinkerIn", url='https://linkerin.ga')],
        [InlineKeyboardButton("About", url='https://linkerin.ga/about')]
    ]))

class AsyncIter:
    def __init__(self, items):    
        self.items = items    

    async def __aiter__(self):    
        for item in self.items:    
            yield item    


async def link_to_hyperlink(string):
    http_links = await extract_link(string)
    async for link in AsyncIter(http_links):
        string = string.replace(link, f"[{link}]({link})")
    return string


async def extract_link(string):
    link_regex = re.compile('((https?):(( //) | (\\\\))+([\w\d:  # @%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links = re.findall(link_regex, string)
    print(string)
    urls = extractor.find_urls(string)
    if len(urls):
        return urls
    else:
        return links


async def movie(update, context):
    status = 1
    search_query = ""
    for i in context.args:
        search_query += f" {i.upper()}"
    await update.message.reply_text("Cooking results...")
    await update.message.reply_text("Almost done...")
    mov = client.iter_messages('backup_linker', search=search_query.upper())
    print(mov)
    mov2 = client.iter_messages('blinkeringa', search=search_query.upper())
    async for m in mov:
        print(m)
        if isinstance(m.entities[0], MessageEntityTextUrl):
            await update.message.reply_text(f"{m.message.splitlines()[0]}\n{m.entities[0].url}")
        else:
            links = await extract_link(str(m.message))
            if not links:
                continue
            buttons = []
            for i in range(len(links)):
                if not links[i].find('t.me') == -1:
                    status = 0
                    break
                response = requests.get(f'https://mdiskshortner.in/api?api=2051f08cab4bb3bce088f884d1d9c4ad60fb6a60&url={links[i]}&alias=CustomAlias')
                if response.status_code == 200:
                    data = await response.json()
                    print(data)
                    buttons.append([InlineKeyboardButton(url=data.shortenedUrl, text=f'{m.message.splitlines()[0].strip()}...{(i + 1)*360}P')])
            if not status:
                status = 1
                continue
            await update.message.reply_text("These are your results", reply_markup=InlineKeyboardMarkup(
                    buttons
            ))
    if not mov:
        await update.message.reply_text(f"No results founds...\n{search_query.strip()} will be added within 5 mins...\nCheck later...")
        async with client.conversation(entity='blinkeringa') as conv:
            await conv.send_message(search_query.upper())
            await update.message.reply_text("Wait searching...\nThis could take around 10 seconds")
            time.sleep(10)
            response = await conv.get_response()
            mov = response
        return await update.message.reply_text(str(mov))


async def flood(update, context):
    messages = client.iter_messages("latest2022newmovies", limit=50)
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
    count = 1
    search_query = str(update.message.text)
    print(search_query)
    status = 1
    mov = client.iter_messages('backup_linker', search=search_query.upper())
    # print(mov)
    seen = []
    async for m in mov:
        if m.message in seen:
            continue
        seen.append(str(m.message))
        title = m.message.splitlines()[0]
        if isinstance(m.entities, type(None)):
            continue
        elif isinstance(m.entities[0], MessageEntityTextUrl):
            await update.message.reply_text(f"✅ RESULT {count}\n\n{m.entities[0].url}")
            return
        else:
            links = await extract_link(m.message)
            lines = m.message.splitlines()
            if not links:
                continue
            if not status:
                continue
            buttons = []
            for i in range(len(links)):
                current_line = title
                if not links[i].find('t.me') == -1:
                    continue
                # response = requests.get(
                #     f'https://mdiskshortner.in/api?api=2051f08cab4bb3bce088f884d1d9c4ad60fb6a60&url=https://linkerin.ga/blog/63c3f2375ec080775ec71186?q={links[i]}')
                # if response.status_code == 200:
                #     data = response.json()
                #     print(data)
                #     buttons.append([InlineKeyboardButton(url=data['shortenedUrl'],
                #                                      text=f'{i + 1}. {m.message.splitlines()[0].strip()}...')])
                for line_i in range(len(lines)):
                    index = lines[line_i].find(links[i])
                    if not index == -1:
                        current_line = lines[line_i][:index]
                        if index < 2 or not current_line.find('Link') == -1:
                            current_line = lines[line_i - 1]
                buttons.append([InlineKeyboardButton(url=f"https://linkerin.vercel.app/blog/63c3f2375ec080775ec71186?q={links[i]}",
                                                     text=f'{i + 1}. ⚡️{current_line}  Click here 👉'.strip())])
            if not len(buttons):
                continue
            await update.message.reply_text(text=f"✅ RESULT {count}\n\n🎬 {title} ", reply_markup=InlineKeyboardMarkup(
                buttons
            ))
            if count > 4:
                status = 0
            count = count + 1
    if not mov:
        return
        await update.message.reply_text(
            f"No results founds...\n{search_query.strip()} will be added within 5 mins...\nCheck later...")
        async with client.conversation(entity='blinkeringa') as conv:
            await conv.send_message(search_query.upper())
            await update.message.reply_text("Wait searching...\nThis could take around 10 seconds")
            time.sleep(10)
            response = await conv.get_response()
            mov = response
        return await update.message.reply_text(str(mov))


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




