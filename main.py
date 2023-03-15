import datetime
import json
import time
import threading
import asyncio
import re
import time
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot, MessageEntity ,InputMediaPhoto
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
loop = asyncio.new_event_loop()
app = ApplicationBuilder().token(TOKEN).build()
messagee = None
but = {}
message_id = []
chat_id = None
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


async def button_callback(update, context):
    global but
    query = update.callback_query
    id = str(query.data).split('_')[1]
    print(query.data)
    if query.data == f'previous_{id}':
        but[id]['c_p'] -= 1
        # keyboard = getKeyboard(id)
        # await query.edit_message_reply_markup(reply_markup=keyboard)
        await getMessage(update, id, 1)
    elif query.data == f'next_{id}':
        but[id]['c_p'] += 1
        # keyboard = getKeyboard(id)
        # await query.edit_message_reply_markup(reply_markup=keyboard)
        await getMessage(update,id, 1)
    else:
        # Handle button press here
        pass



def getKeyboard(id):
    page_buttons = but[str(id)]['a_b'][but[str(id)]['c_p'] * 8:(but[str(id)]['c_p'] + 1) * 8]
    keyboard = []
    for b in page_buttons:
        keyboard.append([InlineKeyboardButton(text=b['text'], url=b['url'], callback_data=b['text'].ljust(70))])
    previous_button = InlineKeyboardButton('<< Previous', callback_data=f'previous_{id}')
    next_button = InlineKeyboardButton('Next >>', callback_data=f'next_{id}')

    # Add next and previous buttons to keyboard
    row = []
    if but[str(id)]['c_p'] > 0:
        row.append(previous_button)
    if (but[str(id)]['c_p'] + 1) * 8 < len(but[str(id)]['a_b']):
        row.append(next_button)
    if row:
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)


async def getMessage(update, id, rep):
    page_buttons = but[str(id)]['a_b'][but[str(id)]['c_p'] * 8:(but[str(id)]['c_p'] + 1) * 8]
    q = page_buttons[0]['text'].split(' ')
    sq = q[0] + " " + q[1]
    if not rep:
        sq = update.message.text
    reply = f"╒═════════════════════╕\n<code>🍿 {sq} </code>\n═══════════════════════\n"
    entities = []
    for button in page_buttons:
        response = requests.get(
            f'https://oggylink.com/api?api=d3cd560e0d296f93a4933b8ff33a04180f22a87d&url={button["url"]}')
        if response.status_code == 200:
            data = response.json()
            button['url'] = f'https://linkerin.vercel.app/blog/63c3f2375ec080775ec71186?q={data["shortenedUrl"]}'
        text = button['text']
        reply += '🔗 <a href="{0}"><strong>{1}</strong></a>\n*-.-*-.-*-.-*-.-*-.-*-.-*-.-*-.-*-.-*-.-*-.-*-.-\n'.format(
            button['url'], text)
        entities.append(MessageEntityTextUrl(url=button['url'], length=len(text), offset=0).to_dict())

    previous_button = InlineKeyboardButton('<< Previous', callback_data=f'previous_{id}')
    next_button = InlineKeyboardButton('Next >>', callback_data=f'next_{id}')
    row = []
    if but[str(id)]['c_p'] > 0:
        row.append(previous_button)
    if (but[str(id)]['c_p'] + 1) * 8 < len(but[str(id)]['a_b']):
        row.append(next_button)
    if rep:
        await update.callback_query.edit_message_text(f'{reply}\n░░░░░░░░░░░░░░░░░░░░░░░', parse_mode='HTML', entities=entities, reply_markup=InlineKeyboardMarkup([row]))
    else:
        mes = await update.message.reply_text(f'{reply}\n░░░░░░░░░░░░░░░░░░░░░░░', parse_mode='HTML', entities=entities, reply_markup=InlineKeyboardMarkup([row]))
        return mes
async def extract_link(string):
    link_regex = re.compile('((https?):(( //) | (\\\\))+([\w\d:  # @%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links = re.findall(link_regex, string)
    urls = extractor.find_urls(string)
    if len(urls):
        return urls
    else:
        return links


async def delete_message(message, id):
    # create an event
    global but
    await asyncio.sleep(150)
    await message.delete()
    del but[str(id)]
    print(but)
    # wait for the event to be set


def wrapper(message, id):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(delete_message(message, id))
def stop_loop():
    loop.stop()

async def send_initial(update, context):
    mes = await update.message.reply_text(f'Searching for "{str(update.message.text)}" 🔍')
    await asyncio.sleep(1)
    await mes.delete()
async def message_handler(update, context):
    global but, message_id, chat_id, loop
    id = update.message.id
    status = 1
    search_query = str(update.message.text).title()
    print(search_query)
    mov = client.iter_messages('backup_linker', search=search_query)
    seen = []
    b= []
    messi = await update.message.reply_text(f'Searching for "{str(search_query)}" 🔍')
    async for m in mov:
        if isinstance(m.entities, MessageEntityTextUrl):
            await update.message.reply_text(f"{m.message.splitlines()[0]}\n{m.entities[0].url}")
        else:
            links = await extract_link(str(m.message))
            lines = m.message.splitlines()
            title = lines[0]
            for link in links:
                if link in seen:
                    continue
                seen.append(link)
                if link.find('t.me') == -1:
                    for line_i in range(len(lines)):
                        index = lines[line_i].find(link)
                        if not index == -1:
                            current_line = lines[line_i][:index]
                            if index < 5 or not current_line.find('Link') == -1:
                                current_line = lines[line_i - 1]
                                if len(current_line) < 3:
                                    current_line = lines[line_i - 2]
                            # response = requests.get(
                            #     f'https://oggylink.com/api?api=d3cd560e0d296f93a4933b8ff33a04180f22a87d&url={link}')
                            # if response.status_code == 200:
                            #     data = response.json()
                            #     link = data['shortenedUrl']
                            text = f'{title} ➠ {current_line}'
                            b.append({'text': text , 'url': f'https://linkerin.vercel.app/blog/63c3f2375ec080775ec71186?q={link}'})
    but[str(id)] = {'a_b': b, 'c_p': 0}
    app.add_handler(CallbackQueryHandler(button_callback))
    await messi.delete()
    if b:
        mes = await getMessage(update, id, 0)
        # await update.message.reply_text(text=f"🍿 *RESULTS FOR ➠ {search_query}*", reply_markup=getKeyboard(id), parse_mode='MarkdownV2')
        # reply = f"╒═════════════════════════╕\n<code>🍿 {search_query} </code>\n═══════════════════════════\n"
        # entities = []
        # for button in b:
        #     text = button['text']
        #     reply += '🔗 <a href="{0}"><strong>{1}</strong></a>\n*-.-*-.-*-.-*-.-*-.-*-.-*-.-*-.-*-.-*-.-*-.-*-.-.-*-.-*-.-*\n'.format(button['url'], text )
        #     entities.append(MessageEntityTextUrl(url=button['url'], length=len(text), offset=0).to_dict())
        # await update.message.reply_text(f'{reply}\n░░░░░░░░░░░░░░░░░░░░░░░░░░░', parse_mode='HTML', entities=entities)
        # message_id.append(mes.message_id)
        # t = threading.Timer(20.0, wrapper, args=[mes, id])
        # t.start()
        task = asyncio.create_task(delete_message(mes, id))
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
    global message_id
    for m in message_id:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=m)
    message_id = []

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


async def movie(update, context):
    count = 1
    search_query = str(update.message.text)
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
                response = requests.get(
                    f'https://oggylink.com/api?api=d3cd560e0d296f93a4933b8ff33a04180f22a87d&url={links[i]}')
                if response.status_code == 200:
                    data = response.json()
                    links[i] = data['shortenedUrl']
                for line_i in range(len(lines)):
                    index = lines[line_i].find(links[i])
                    if not index == -1:
                        current_line = lines[line_i][:index]
                        if index < 2 or not current_line.find('Link') == -1:
                            current_line = lines[line_i - 1]
                buttons.append([InlineKeyboardButton(url=f"https://linkerin.vercel.app/blog/63c3f2375ec080775ec71186?q={links[i]}",
                                                     text=f'{i + 1}. ⚡️{current_line} ➠ Click here 👉'.strip())])
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
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("course", course))
    app.add_handler(CommandHandler("movie", movie))
    app.add_handler(CommandHandler('flood', flood))
    app.add_handler(MessageHandler(filters.TEXT, message_handler))
    app.add_error_handler(error)
    app.run_polling()

main()




