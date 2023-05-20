import html
import math
import os
import random
import asyncio
import re
import time
import requests
import telegram
from pyrogram.enums import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputFile
from telegram.ext import *
from telethon.tl.types import MessageEntityTextUrl
from io import BytesIO
from bs4 import BeautifulSoup
import socks
from pyrogram import  Client


# Define the token of your bot
TOKEN = '5673905050:AAFOUxkIDikmrP4kdlNcTn2hMr9341aoEFA'
mdisk_api_key = 'GrG0naDSbxAqEjp0Owz0'
api_id = 27575247
api_hash = '44f4ce1ee458039f7500b0bce10fbc63'
user_name = 'two_backup'
session_string = '1BVtsOKEBuzhwIpU_AuhlauBM9-30gEf7-jovu5m8AdAkBhWhof7wshA1ES4kWqIHzVt4M4ecii8Numw6teG72pQI5J7aV2qnA7vQXSwrZUdMa-bIBHNIQySMoqEZTCh25HRQwCCDQjcUf40RcmcAllmXYvn71xcWfPHU193zF7P-IDGykcZZXif84AqOG0UaJLVdyPoDCtT3TxpkbUFBY7EcstvYuH1PJGfD47yEczxDTR7LP2fyUy2_27iZ_7VAlU_KcmXpILdn8U8eZdtLp1DH1SAvIvV5iKg086vLeUe8XBmvEECzWew7uN2a2RfjJPss2uyTtOF3x37MUH4Ldv0HgdhKWO8='

bot = telegram.Bot(token=TOKEN)
loop = asyncio.new_event_loop()
app = ApplicationBuilder().token(TOKEN).build()
messagee = None
but = {}
req = {}
message_id = []
chat_id = None
client = Client('my_account', api_id, api_hash)
client.start()

def getHTMLdocument(url):
    # request for HTML document of given url
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36'})
    # response will be provided in JSON format
    return response.text



async def starte(update, context):
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
    print(update)
    print(but)
    query = update.callback_query
    print(req)
    qu = str(query.data).split('|')
    q = qu[0]
    idm = qu[2]
    ide = None
    user = None
    id = None
    if not q == 'RC':
        ide = but[str(idm)]['ide']
        user = but[str(idm)]['user']
        id = but[str(idm)]['id']
    print(str(idm) + "bc")
    user_id = update.callback_query.from_user.id
    print(f'{user_id}  {ide}')
    if qu[0] == 'RC':
        re = req[str(idm)]['mes']
        user = req[str(idm)]['user']
        id = req[str(idm)]['id']
        user = f'[{user}](tg://user?id={id})'
        del req[str(idm)]
        await re.edit_text("Movie added.")
        await bot.send_message(chat_id=qu[3], text=f'Hey!! {user}\n"{qu[1]}" movie is added to the database\nPlease search again...', parse_mode='Markdown')
    elif not str(user_id) == str(ide):
        await query.answer("Don't touch others property search on your own", show_alert=True)
    elif q == f'p':
        but[str(idm)]['c_p'] -= 1
        # keyboard = getKeyboard(id)1
        # await query.edit_message_reply_markup(reply_markup=keyboard)
        await getMessage(update, ide,  idm, 0)
    elif q == f'n':
        but[str(idm)]['c_p'] += 1
        print('asdfjasldf')
        # keyboard = getKeyboard(id)
        # await query.edit_message_reply_markup(reply_markup=keyboard)
        await getMessage(update,ide, idm, 0)
    elif q == 'r':
        chat_id = update.callback_query.message.chat.id
        print(user)
        await client.send_message(chat_id='requ18',text=f'Request\n{qu[1]}\n{idm}\n{chat_id}')
        m = but[str(idm)]['reply']
        mention = f'[{user}](tg://user?id={id})'
        await m.delete()
        await bot.send_message(chat_id=chat_id, text=f'🎉 {mention} Your request for "{qu[1]}" was successful! 🎉', parse_mode='Markdown')
    else:
        chat_id = update.callback_query.message.chat.id
        m = but[str(idm )]['reply']
        htmL_doc = getHTMLdocument(f'https://www.imdb.com/find/?s=tt&q={qu[1]}&ref_=nv_sr_sm')
        soap = BeautifulSoup(htmL_doc, 'html.parser')
        t_id = soap.find('li', attrs={'class': 'ipc-metadata-list-summary-item'}).a['href']
        b = await get_results(qu[1])
        if b:
            pho = requests.get(
                'https://gamespot.com/a/uploads/screen_small/mig/4/4/1/5/2104415-169_darkesthour_ot_pc_022411.jpg')
            photo = BytesIO(pho.content)
            but[str(idm )]['a_b'] = b
            await m.delete()
            me = await bot.send_photo(chat_id=chat_id, caption='🎥🔍 Fetching movie details...',
                                      photo=photo, parse_mode='HTML')
            but[str(idm )]['reply'] = me
            me = await getMessage(update, ide, idm , 1)
            me = await send_photo(me, t_id, idm)
            but[str(idm  )]['reply'] = me
            task = asyncio.create_task(delete_message(idm , me))


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


async def getMessagde(update, ide, rep):
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
    previous_button = InlineKeyboardButton('◄◄ Back', callback_data=f'previous|{ide}|{id}')
    next_button = InlineKeyboardButton('Next ►►', callback_data=f'next|{ide}|{id}')
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


async def getMessage(update,ide,  rep, sug):
    print(str(rep) + "getMsg")
    id = rep
    # if update.message:
    #     id = update.message.message_id
    # else:
    #     id = update.callback_query.message.message_id - 2
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
    entities = [[InlineKeyboardButton('How to download', url='https://t.me/how_to_download_movie_mmd/2')]]
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
    previous_button = InlineKeyboardButton('◄◄ Back', callback_data=f'p|{ide}|{id}')
    next_button = InlineKeyboardButton('Next ►►', callback_data=f'n|{ide}|{id}')
    backup = [InlineKeyboardButton('📢 Join our channel and stay informed! 📲', url='https://t.me/movie_paradize')]
    money = [InlineKeyboardButton('💰 GPT-4 Plus subscription for free! 💰', url='https://youtu.be/ziJzG3kskEY')]
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
        row.append(InlineKeyboardButton(text=page_nos, callback_data=f'page_no|{ide}'))
    if (but[str(id)]['c_p'] + 1) * 8 < len(but[str(id)]['a_b']):
        if(not len(row)):
            row.append(InlineKeyboardButton(text=page_nos, callback_data=f'page_no|{ide}'))
        row.append(next_button)
    entities.extend([row, backup, money])
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
    await asyncio.sleep(150)
    # await message.delete()
    await me.edit_caption(caption=me.caption + "\n\n🔍🕵️‍♀️ *SEARCH AGAIN!* 🤔👀\n", parse_mode='Markdown')
    del but[str(id)]
    # wait for the event to be set




async def send_initial(update, context):
    mes = await update.message.reply_text(f'Searching for "{str(update.message.text)}" 🔍')
    await asyncio.sleep(1)
    await mes.delete()


def get_movie_info(title_id):
    info_doc = getHTMLdocument(f'https://www.imdb.com/{title_id}')
    soap_d = BeautifulSoup(info_doc, 'html.parser')
    main_info = soap_d.find('ul', attrs={'class':'ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt'})
    main_info = main_info.findChildren()
    print(main_info)
    genre = []
    for item in soap_d.find_all('span', attrs={'class': 'ipc-chip__text'}):
        genre.append(item.string)
    image = soap_d.find('a', attrs={'class': 'ipc-lockup-overlay ipc-focusable'})
    print(len(main_info))
    detail = {
        'title': soap_d.title.string,
        'ratings': soap_d.find('span', attrs={'class': 'sc-bde20123-1 iZlgcd'}).string,
        'type': main_info[0].string,
        'genre': genre,
        'release':main_info[0].string.split('–')[0],
        'age': main_info[0].string,
        'dur':'NA',
        'desc':soap_d.find('span', attrs={'class': 'sc-2eb29e65-0 hOntMS'}).string
    }
    if len(main_info) > 5:
        detail['dur'] = main_info[5].string
        detail['type'] = main_info[4].string
    elif len(main_info) >= 4:
        detail['dur'] = main_info[4].string
        detail['type'] = main_info[2].string
    genre = genre.remove('Back to top')
    title = detail["title"].split("-")[0]
    genre = array_prettify(detail["genre"])
    rating = detail["ratings"]
    # Escape special characters in title to prevent parse_mode errors
    title = html.escape(title)
    text = f'\n🎥 *Title:* {title}\n\n📅 *Release date:* {detail["release"]}\n\n🎭 *Genre:* {genre}\n\n⏰ *Duration: *{detail["dur"]}\n\n📺 *Type: *{detail["type"]}\n\n⭐ *IMDB Rating:* {rating}/10\n\n📝 *Description: * {detail["desc"]}\n'
    return text


async def get_results(search_query):
    mov = client.search_messages(chat_id='backup_linker', query=search_query)
    seen = []
    b = []
    print(mov)
    async for m in mov:
        content = m.text
        if not content:
            content = m.caption
        if isinstance(m.entities, MessageEntityTextUrl):
            continue
        elif content:
            links = await extract_link(content)
            lines = content.splitlines()
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
                                      'url': f'https://linkerin.vercel.app/blog/63c3f2375ec080775ec71186?q={link}'})
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


async def send_photo(mes, title_id, idm):
    print(title_id)
    text = get_movie_info(title_id)
    title_id = title_id[7:17]
    print(title_id)

    g_doc = getHTMLdocument(f'https://www.cinematerial.com/search?q={title_id}')
    sop = BeautifulSoup(g_doc, 'html.parser')
    img = sop.find('a', attrs={'style': 'font-weight: bold; font-size: 1.1em'})
    if img:
        t_doc = getHTMLdocument(f'https://www.cinematerial.com{img["href"]}')
        toap = BeautifulSoup(t_doc, 'html.parser')
        img = toap.find('img', attrs={'class': 'lazy'})
    photo = None
    user = but[str(idm)]['user']
    id = but[str(idm)]['id']
    mention = f'[{user}](tg://user?id={id})'
    if img:
        img = img['data-src']
        pho = requests.get(img)
        photo = BytesIO(pho.content)

        mes = await mes.edit_media(media=InputMediaPhoto(photo), reply_markup=mes.reply_markup)
        mess = await mes.edit_caption(caption=f'*Requested by:  *{mention}\n{text}', parse_mode='Markdown',
                                      reply_markup=mes.reply_markup)
        return mess
    # photo = BytesIO(image_bytes)
            # photo.close()
    else :
        # t_doc = getHTMLdocument(f'https://www.movieposterdb.com/search?q={title_id}')
        # toap = BeautifulSoup(t_doc, 'html.parser')
        # imgd = toap.find('img', attrs={'class': 'poster_img'})
        # print(imgd)
        # print(imgd['src'])
        # if imgd:
        #     img = imgd['src']
        #     pho = requests.get(img)
        #     photo = BytesIO(pho.content)
        mess = await mes.edit_caption(caption=f'*Requested by:  *{mention}\n{text}', parse_mode='Markdown',
                                      reply_markup=mes.reply_markup)
        return mess
    # photo = poster(search_query)



async def message_handler(update, context):
    global but, message_id, chat_id, loop, req
    ide = update.message.from_user.id
    print(update)
    status = 1
    idm = update.message.message_id
    search_query = str(update.message.text).title()
    print(search_query)
    if search_query.splitlines()[0] == 'Request':
        request = search_query.splitlines()[1]
        m_id = search_query.splitlines()[2]
        c_id = search_query.splitlines()[3]
        r = await update.message.reply_text(f'"{request}" added?', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Yes', callback_data=f'RC|{request}|{idm}|{c_id}')]]))
        req[str(idm)] = {'mes' : r, 'user': but[str(m_id)]['user'] , 'id': but[str(m_id)]['id']}
        return
    print(str(idm))
    print(update.message)
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
    but[str(idm)] = {'a_b': b, 'c_p': 0, 'ide':ide, 'user': update.message.from_user.first_name, 'id': update.message.from_user.id}
    me = None
    markup = []
    htmL_doc = getHTMLdocument(f'https://www.imdb.com/find/?s=tt&q={search_query}&ref_=nv_sr_sm')
    title_id = None
    soap = BeautifulSoup(htmL_doc, 'html.parser')
    results = soap.find_all('li', attrs={
        'class': 'ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click find-result-item find-title-result'},
                            limit=8)

    title_id = results[0].a['href']
    img = results[0].img['src']
    for item in results:
        print(item)
        markup.append([InlineKeyboardButton(text=item.a.string, callback_data=f's|{item.a.string[:25]}|{idm}')])
    markup.append([InlineKeyboardButton(text="Click here to request", callback_data=f'r|{search_query}|{idm}')])
    if b:
        await messi.delete()
        pho = requests.get(img)
        photo = BytesIO(pho.content)
        me = await bot.send_photo(chat_id=update.message.chat.id, caption='🎥🔍 Fetching movie...',photo=photo, parse_mode='HTML')
        but[str(idm)]['reply'] = me

    app.add_handler(CallbackQueryHandler(button_callback))

    if b:
        mes = await getMessage(update, ide,  idm, 0)
        mess = await send_photo(mes, title_id, idm)
        but[str(idm)]['reply'] = mess
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
        task = asyncio.create_task(delete_message(idm, mess))
    else:
        await messi.delete()
        meu = await update.message.reply_text(text="🤔🎥 Can't find the movie. What's the name?" , reply_markup=InlineKeyboardMarkup(markup))
        but[str(idm)]['reply'] = meu



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


async def handle_traffic():
    movie = ['wednesday', 'lucifer', 'pathaan', 'bholaa', 'farzi', 'rana naidu', 'peaky blinders', 'avatar', 'fall']
    for i in range(18):
        await client.send_message(entity='MovieMdiskDownload', message=random.choice(movie))
        await asyncio.sleep(250)
async def update(update, context):
    task = asyncio.create_task(handle_traffic())

# def main():
#     print('im in main')
#
#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(CommandHandler("help", help_command))
#     app.add_handler(CommandHandler("course", course))
#     app.add_handler(CommandHandler("movie", movie))
#     app.add_handler(CommandHandler('flood', flood))
#     app.add_handler(CommandHandler('update', update))
#     app.add_handler(MessageHandler(filters.TEXT, message_handler))
#     app.add_error_handler(error)
#     app.run_polling()

# main()

print('im in main')

app.add_handler(CommandHandler("start", starte))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("course", course))
app.add_handler(CommandHandler("movie", movie))
app.add_handler(CommandHandler('flood', flood))
app.add_handler(CommandHandler('update', update))
app.add_handler(MessageHandler(filters.TEXT, message_handler))
app.add_error_handler(error)
app.run_polling()

#
# port = int(os.getenv('VCAP_APP_PORT', 5000))









