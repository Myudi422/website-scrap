import asyncio
	import telepot
	import telepot.aio
	from telepot.aio.loop import MessageLoop
	from pprint import pprint
	from bs4 import BeautifulSoup
	import requests
	
	async def handle(msg):
	    global chat_id
	    # These are some useful variables
	    content_type, chat_type, chat_id = telepot.glance(msg)
	    # Log variables
            print(content_type, chat_type, chat_id)
	    pprint(msg)
	    username = msg['chat']['first_name']
	    # Check that the content type is text and not the starting
	    if content_type == 'text':
	        if msg['text'] != '/start':
	            text = msg['text']
	            # it's better to strip and lower the input
	            text = text.strip()
	            await getMeaning(text.lower())

	async def getMeaning(text):
	    # create url
	    url = 'https://www.oxfordlearnersdictionaries.com/definition/english/' + text
	    # get page
	    page = requests.get(url)
	    # let's soup the page
	    soup = BeautifulSoup(page.text, 'html.parser')
	    pprint(soup)
	    try:
	        # get MP3 and definition
	        try:
	            # get MP3
	            mp3link = soup.find('div', {'class': 'sound audio_play_button pron-uk icon-audio'}).get('data-src-mp3')
	            await bot.sendAudio(chat_id=chat_id, audio=mp3link)
	        except:
	            await bot.sendMessage(chat_id, 'Pronunciation not found!')
	        try:
	            # get definition
	            definition = soup.find('span', {'class': 'def'}).text
	            await bot.sendMessage(chat_id, definition)
	        except:
	            await bot.sendMessage(chat_id, 'Meaning not found!')
	    except:
	        await bot.sendMessage(chat_id, 'Something went wrong...')

	# Program startup
	TOKEN = 1811863530:AAFFYY_EqvKapAYf93HiO2j3qD-pGKNHgLg
	bot = telepot.aio.Bot(TOKEN)
	loop = asyncio.get_event_loop()
	loop.create_task(MessageLoop(bot, handle).run_forever())
	print('Listening ...')

	# Keep the program running
	loop.run_forever()
