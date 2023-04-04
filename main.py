import base64
import datetime
import html
import json
import math
import random
import textwrap
import time
import threading
import asyncio
import re
import urllib.request
import time
import requests
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputFile
from telegram.ext import *
from telethon.tl.types import MessageEntityTextUrl
from io import BytesIO
import response
import response as R
from telethon import TelegramClient, sync
from urlextract import URLExtract
extractor = URLExtract()
from mdisky import Mdisk
from bs4 import BeautifulSoup
# Define the token of your bot
TOKEN = '5673905050:AAFOUxkIDikmrP4kdlNcTn2hMr9341aoEFA'
mdisk_api_key = 'GrG0naDSbxAqEjp0Owz0'
api_id = 27575247
api_hash = '44f4ce1ee458039f7500b0bce10fbc63'
user_name = 'two_backup'
session_string = '1BVtsOKEBuzhwIpU_AuhlauBM9-30gEf7-jovu5m8AdAkBhWhof7wshA1ES4kWqIHzVt4M4ecii8Numw6teG72pQI5J7aV2qnA7vQXSwrZUdMa-bIBHNIQySMoqEZTCh25HRQwCCDQjcUf40RcmcAllmXYvn71xcWfPHU193zF7P-IDGykcZZXif84AqOG0UaJLVdyPoDCtT3TxpkbUFBY7EcstvYuH1PJGfD47yEczxDTR7LP2fyUy2_27iZ_7VAlU_KcmXpILdn8U8eZdtLp1DH1SAvIvV5iKg086vLeUe8XBmvEECzWew7uN2a2RfjJPss2uyTtOF3x37MUH4Ldv0HgdhKWO8='
client = TelegramClient("mdisk_as", api_id, api_hash)
bot = telegram.Bot(token=TOKEN)
client.start()
entity = client.get_entity("backup_linker")
loop = asyncio.new_event_loop()
mdisk = Mdisk(mdisk_api_key)
app = ApplicationBuilder().token(TOKEN).build()
messagee = None
but = {}
message_id = []
chat_id = None


def getHTMLdocument(url):
    # request for HTML document of given url
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36'})
    # response will be provided in JSON format
    return response.text




async def start(update, context):
    backup = [InlineKeyboardButton('📢 Join our channel and stay informed! 📲', url='https://t.me/movie_paradize')]
    money = [InlineKeyboardButton('💰 Click here to make some cash! 💰', url='https://t.me/MovieMdiskDownload/3866')]
    await update.message.reply_text("🎥🤖 Hey there! I'm your personal movie link bot 🤖🎥\nJust tell me the name of the movie you want to watch, and I'll provide you with the links to watch it online! 🍿👀\nWhether you're in the mood for action 💥, romance 💕, comedy 😂, or horror 😱, I've got you covered! So sit back, relax, and let me take care of finding the perfect movie for you. 🎞️👌", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("LinkerIn: Dheeraj", url='https://linkerin.ga')],
        backup,
        money
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
    qu = str(query.data).split('|')
    id = qu[1]
    q = qu[0]
    if q == f'p':
        but[id]['c_p'] -= 1
        # keyboard = getKeyboard(id)
        # await query.edit_message_reply_markup(reply_markup=keyboard)
        await getMessage(update, id, 1)
    elif q == f'n':
        but[id]['c_p'] += 1
        # keyboard = getKeyboard(id)
        # await query.edit_message_reply_markup(reply_markup=keyboard)
        await getMessage(update,id, 1)
    else:
        m = but[id]['reply']
        htmL_doc = getHTMLdocument(f'https://www.imdb.com/find/?s=tt&q={q}&ref_=nv_sr_sm')
        soap = BeautifulSoup(htmL_doc, 'html.parser')
        t_id = soap.find('li', attrs={'class': 'ipc-metadata-list-summary-item'}).a['href']
        b = await get_results(q)
        if b:
            pho = requests.get(
                'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9RFoSyLQORtrxvqbYq5MY_HfWsCYNooRrzxHhuU9vBDU2sIW_9D1GjfapiBM8S_Ux52k&usqp=CAU')
            photo = BytesIO(pho.content)
            but[id]['a_b'] = b
            await m.delete()
            me = await bot.send_photo(chat_id=qu[2], caption='🎥🔍 Fetching movie details...',
                                      photo=photo, parse_mode='HTML')
            but[id]['reply'] = me
            me = await getMessage(update, id, 1)
            me = await send_photo(me, t_id, q)
            but[str(id)]['reply'] = me
            task = asyncio.create_task(delete_message(id, me))


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


async def getMessagde(update, id, rep):
    current_page = but[str(id)]['c_p'] + 1
    total_pages = math.ceil(len(but[str(id)]['a_b'])/8)
    width = len(str(total_pages)) + len(str(current_page))
    page_buttons = but[str(id)]['a_b'][but[str(id)]['c_p'] * 8:(but[str(id)]['c_p'] + 1) * 8]
    q = page_buttons[0]['text']
    sq = f'{q[:10]}...'.upper()
    if not rep:
        sq = update.message.text.upper()
    heading = "•❅──────✧❅✦❅✧──────❅•".center(49)
    reply = f"<strong>{heading}</strong>\n"
    entities = []
    for button in page_buttons:
        # response = requests.get(
        #     f'https://oggylink.com/api?api=d3cd560e0d296f93a4933b8ff33a04180f22a87d&url={button["url"]}')
        # if response.status_code == 200:
        #     data = response.json()
        #     button['url'] = f'https://linkerin.vercel.app/blog/63c3f2375ec080775ec71186?q={data["shortenedUrl"]}'
        text = button['text'].ljust(20)
        #design = f'───※ ·❆· ※───'.center(49)
        cl = '🔗 <a href="{0}"><strong>{1}</strong></a>\n\n'.format(
            button['url'], f'{text}')
        reply += cl
        entities.append(MessageEntityTextUrl(url=button['url'], length=len(text), offset=0).to_dict())
    previous_button = InlineKeyboardButton('◄◄ Back', callback_data=f'previous|{id}')
    next_button = InlineKeyboardButton('Next ►►', callback_data=f'next|{id}')
    backup = [InlineKeyboardButton('📢 Join our channel and stay informed! 📲', url='https://t.me/movie_paradize')]
    money = [InlineKeyboardButton('💰 Click here to make some cash! 💰', url='https://t.me/MovieMdiskDownload/3866')]
    if width == 2:
        width = 48
    elif width == 3:
        width = 47
    else:
        width = 45
    page_nos = f'PAGE {current_page}/{total_pages}'.center(width)
    page_details = f'╭───────༺♡༻───────╮\n{page_nos}\n╰───────༺♡༻───────╯'
    row = []
    if but[str(id)]['c_p'] > 0:
        row.append(previous_button)
    if (but[str(id)]['c_p'] + 1) * 8 < len(but[str(id)]['a_b']):
        row.append(next_button)
    if rep:
        mes = await update.callback_query.edit_message_text(f'{reply}\n{page_details}', parse_mode='HTML', entities=entities, reply_markup=InlineKeyboardMarkup([row, backup, money]))
        return mes
    else:
        mes = await update.message.reply_text(f'{reply}\n{page_details}', parse_mode='HTML', entities=entities, reply_markup=InlineKeyboardMarkup([row, backup, money]))
        return mes


def array_prettify(a):
    print(a)
    b = ""
    for item in a:
        b = b + f"{item} "
    return b


async def getMessage(update, id, rep):
    m = but[str(id)]['reply']
    print(update)
    prompts = ["🎬 Voila! Your movie results are here.", "🍿 Sit tight, your movie results are about to roll in.",
               "🎉 Your movie results are ready! Let's celebrate with some 🍾",
               "📺 Lights, camera, action! Your movie results are on screen.",
               "🎥 Get ready for the big reveal - your movie results are in."]
    current_page = but[str(id)]['c_p'] + 1
    total_pages = math.ceil(len(but[str(id)]['a_b'])/8)
    width = len(str(total_pages)) + len(str(current_page))
    page_buttons = but[str(id)]['a_b'][but[str(id)]['c_p'] * 8:(but[str(id)]['c_p'] + 1) * 8]
    q = page_buttons[0]['text']
    sq = f'{q[:10]}...'.upper()
    if not rep:
        sq = update.message.text.upper()
    entities = []
    for button in page_buttons:
        # response = requests.get(
        #     f'https://oggylink.com/api?api=d3cd560e0d296f93a4933b8ff33a04180f22a87d&url={button["url"]}')
        # if response.status_code == 200:
        #     data = response.json()
        #     button['url'] = f'https://linkerin.vercel.app/blog/63c3f2375ec080775ec71186?q={data["shortenedUrl"]}'
        text = f'🔗 {button["text"]}'
        text.replace("\n", "%0A")
        #design = f'───※ ·❆· ※───'.center(49)
        entities.append([InlineKeyboardButton(text, url=button['url'])])
    previous_button = InlineKeyboardButton('◄◄ Back', callback_data=f'p|{id}')
    next_button = InlineKeyboardButton('Next ►►', callback_data=f'n|{id}')
    backup = [InlineKeyboardButton('📢 Join our channel and stay informed! 📲', url='https://t.me/movie_paradize')]
    money = [InlineKeyboardButton('💰 Click here to make some cash! 💰', url='https://t.me/MovieMdiskDownload/3866')]
    if width == 2:
        width = 48
    elif width == 3:
        width = 47
    else:
        width = 45
    page_nos = f'PAGE {current_page}/{total_pages}'
    page_details = f'╭───────༺♡༻───────╮\n{page_nos}\n╰───────༺♡༻───────╯'
    row = []
    if but[str(id)]['c_p'] > 0:
        row.append(previous_button)
        row.append(InlineKeyboardButton(text=page_nos, callback_data='page_no'))
    if (but[str(id)]['c_p'] + 1) * 8 < len(but[str(id)]['a_b']):
        if(not len(row)):
            row.append(InlineKeyboardButton(text=page_nos, callback_data='page_no'))
        row.append(next_button)
    entities.extend([row, backup, money])
    if rep:
        mes = await m.edit_reply_markup( reply_markup=InlineKeyboardMarkup(entities))
        but[str(id)]['reply'] = mes
        return mes
    else:
        mes = await m.edit_reply_markup( reply_markup=InlineKeyboardMarkup(entities))
        but[str(id)]['reply'] = mes
        return mes


async def extract_link(string):
    link_regex = re.compile(r'https?://\S+')
    links = re.findall(link_regex, string)
    return links


async def delete_message(id, me):
    # create an event
    global but
    await asyncio.sleep(180)
    # await message.delete()
    await me.edit_caption(caption=me.caption + "\n\n🔍🕵️‍♀️ SEARCH AGAIN! 🤔👀\n")
    del but[str(id)]
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


def get_movie_info(title_id):
    info_doc = getHTMLdocument(f'https://www.imdb.com/{title_id}')
    soap_d = BeautifulSoup(info_doc, 'html.parser')
    genre = []
    for item in soap_d.find_all('a', attrs={'class': 'ipc-chip ipc-chip--on-baseAlt'}):
        genre.append(item.string)
    image = soap_d.find('a', attrs={'class': 'ipc-lockup-overlay ipc-focusable'})
    detail = {
        'title': soap_d.title.string,
        'ratings': soap_d.find('span', attrs={'class': 'sc-e457ee34-1 squoh'}).string,
        'genre': genre,
        'release':soap_d.find('a', attrs={'class': 'ipc-link ipc-link--baseAlt ipc-link--inherit-color'}).string,
        'desc':soap_d.find('span', attrs={'class': 'sc-35061649-1 NHBDz'}).string
    }
    title = detail["title"].split("-")[0]
    genre = array_prettify(detail["genre"])
    rating = detail["ratings"]

    # Escape special characters in title to prevent parse_mode errors
    title = html.escape(title)
    text = f'\n🎥 <b>Title:</b> {title}\n\n📅 <b>Release date:</b> {detail["release"]}\n\n🎭 <b>Genre:</b> {genre}\n\n⭐ <b>Rating:</b> {rating}/10\n\n📝 <b>Description</b>: {detail["desc"]}\n'
    return text


async def get_results(search_query):
    mov = client.iter_messages('backup_linker', search=search_query)
    seen = []
    b = []
    async for m in mov:

        content = str(m.message)
        if isinstance(m.entities, MessageEntityTextUrl):
            continue
        else:
            links = await extract_link(content)
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
                            trun = 30 - len(current_line)
                            text = f'{title[:trun]}-{current_line}'
                            b.append({'text': text,
                                      'url': f'https://oggylink.com/st?api=d3cd560e0d296f93a4933b8ff33a04180f22a87d&url={link}'})
    return b


def poster(search):
    main_doc = getHTMLdocument(f'https://www.cinematerial.com/search?q={search}')
    sop = BeautifulSoup(main_doc, 'html.parser')
    link = sop.find('a', attrs={'href': re.compile('^/tv')})['href']
    pos_doc = getHTMLdocument(f'https://www.cinematerial.com/{link}')
    sopp = BeautifulSoup(pos_doc, 'html.parser')
    img = sopp.find('img', attrs={'class': 'lazy'})
    print(img)
    pho = requests.get(img)
    photo = BytesIO(pho.content)
    return photo

async def send_photo(mes, title_id, search_query):
    text = get_movie_info(title_id)
    g_doc = getHTMLdocument(f'https://hdmoviehub.click/?s={search_query}')
    sop = BeautifulSoup(g_doc, 'html.parser')
    img = sop.find('img', attrs={'class': 'wp-post-image'})
    # print(img)
    # image_bytes = base64.b64decode(img.split(',')[1])
    # t_doc = getHTMLdocument(f'https://search.brave.com/images?q={search_query}&source=web')
    # toap = BeautifulSoup(t_doc, 'html.parser')
    # img = toap.find('img', attrs={'class': 'image svelte-qd248k'})
    photo = None
    if img:
        print('asdf')
        img = img['src']
        pho = requests.get(img)
        photo = BytesIO(pho.content)
    # photo = BytesIO(image_bytes)
            # photo.close()
    else :
        t_doc = getHTMLdocument(f'https://screenrant.com/search/?q={search_query}')
        toap = BeautifulSoup(t_doc, 'html.parser')
        imgd = toap.find('source')
        print(imgd)
        if imgd:
            img = imgd['srcset']
            pho = requests.get(img)
            photo = BytesIO(pho.content)
    # photo = poster(search_query)
    mes = await mes.edit_media(media=InputMediaPhoto(photo), reply_markup=mes.reply_markup)
    mess = await mes.edit_caption(caption=text, parse_mode='HTML', reply_markup=mes.reply_markup)
    return mess

async def message_handler(update, context):
    global but, message_id, chat_id, loop
    id = update.message.id
    status = 1
    search_query = str(update.message.text).title()
    responses = [
        f"Great choice! {search_query} is awesome! 🔥 Check it out:",
        f"{search_query} is a classic! 🎥 Here's the link:",
        f"Love the movie {search_query}! 😍 You've got to watch it again! ",
        f"Have you seen {search_query} yet? 🤔 You've got to check it out:",
        f"{search_query} is a must-watch! 🍿 Don't miss it:"
    ]
    print(search_query)
    messi = await update.message.reply_text(
        text='🍿 Get ready to cook up some excitement with your movie results! But wait, the suspense is killing us... 🍳🍿⏳',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='join this group for movies', url='https://t.me/MovieMdiskDownload')]]))

    b = await get_results(search_query)
    but[str(id)] = {'a_b': b, 'c_p': 0}
    me = None
    if b:
        await messi.delete()
        pho = requests.get('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9RFoSyLQORtrxvqbYq5MY_HfWsCYNooRrzxHhuU9vBDU2sIW_9D1GjfapiBM8S_Ux52k&usqp=CAU')
        photo = BytesIO(pho.content)
        me = await bot.send_photo(chat_id=update.message.chat.id, caption='🎥🔍 Fetching movie details...',photo=photo, parse_mode='HTML')
        but[str(id)]['reply'] = me

    app.add_handler(CallbackQueryHandler(button_callback))
    markup = []
    htmL_doc = getHTMLdocument(f'https://www.imdb.com/find/?s=tt&q={search_query}&ref_=nv_sr_sm')
    title_id = None
    soap = BeautifulSoup(htmL_doc, 'html.parser')
    results = soap.find_all('li', attrs={'class': 'ipc-metadata-list-summary-item'}, limit=8)
    title_id = results[0].a['href']
    for item in results:
        markup.append([InlineKeyboardButton(text=item.a.string, callback_data=f'{item.a.string}|{id}|{update.message.chat.id}')])
    if b:
        mes = await getMessage(update, id, 0)
        mess = await send_photo(mes, title_id, search_query)
        but[str(id)]['reply'] = mess
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
        task = asyncio.create_task(delete_message(id, mess))
    else:
        await messi.delete()
        meu = await update.message.reply_text(text="🤔🎥 Can't find the movie. What's the name?" , reply_markup=InlineKeyboardMarkup(markup))
        but[str(id)]['reply'] = meu



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
    backup = [InlineKeyboardButton('📢 Join our channel and stay informed! 📲', url='https://t.me/movie_paradize')]
    money = [InlineKeyboardButton('💰 Click here to make some cash! 💰', url='https://t.me/MovieMdiskDownload/3866')]
    await update.message.reply_text("🤖🎥 Movie Link Bot Rules 🎥🤖\n- To use Movie Link Bot, please follow these rules:\n- Type only the name of the movie you want to watch.\n- Do not include the movie name in any language other than English.\n- Include the year of the movie for better results.\n- If you don't find the movie you're looking for, please make a request.\nThat's all there is to it! If you have any questions or need further assistance, don't hesitate to reach out to me. Happy movie watching! 🍿👀",parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([backup, money]))


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




