import logging
from telegram import Chat, ChatMember, ChatMemberUpdated, Update,InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler,MessageHandler,filters,CallbackQueryHandler
import os
import logging
from dotenv import load_dotenv
# import tracemalloc
import requests
import json
import asyncio
# import time
# import millify
from web3 import Web3,exceptions
import time
import threading
# import schedule
from PIL import Image,ImageSequence
from io import BytesIO
from getpair import *
BUY_EMOJI=['🟢']
chat_idd='1'
last_message={}
keys=[]
demo={
    chat_idd:{
        'emoji':'🟢'
    }
}
change_gif={
    
}
load_dotenv()
TOKEN=os.getenv('API_KEY')
ETHER_KEY=os.getenv('ether_key')
URL=os.getenv('url')
group_info={}
users_details={}
group_info_lock=threading.Lock()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
rpc_url = "https://mainnet.infura.io/v3/7c2a5e84734b44e6a9af8b545ffbbdb3"
# uniswap_helper = UniswapHelper(rpc_url)

w3 = Web3(Web3.HTTPProvider(rpc_url))

abi=abi = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [
            {"name": "", "type": "string"}
        ],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {"name": "", "type": "string"}
        ],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {"name": "", "type": "uint256"}
        ],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [
            {"name": "balance", "type": "uint256"}
        ],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {"name": "", "type": "uint8"}
        ],
        "type": "function",
    },
]
# Make sure it's a list containing the dictionary


# Check connection
if not w3.is_connected():
    print("Failed to connect to Ethereum node.")
    exit()

async def start(update:Update, context :ContextTypes.DEFAULT_TYPE):
    chat_type:str =update.message.chat.type
    # print(chat_type)
    if chat_type == 'private':
        response=(
        f"Welcome to <a href='https://t.me/OxBuy_bot'>@oxbuy_bot</a>\n\n"
        f"<a href='https://t.me/oxbuy_botDATA/3'>-Disclaimer</a>\n"
        f"<a href='https://t.me/oxbuy_botDATA/5'>-Tutorial</a>\n"
        f"<a href='https://t.me/oxbuy_botDATA/12'>-Marketing</a>\n"
        f"<a href='https://t.me/oxbuy_botDATA/15'>-Trending</a>\n"
        f"<a href='#'>-Premium</a>\n"
    )
        # user_id = update.message.from_user.id
        user_id = update.message.from_user.id
        user_name = update.message.from_user.first_name
        original_message_id = update.message.message_id
        await context.bot.send_message(chat_id=user_id, text=response,parse_mode='HTML',disable_web_page_preview=True, reply_to_message_id=original_message_id)  

async def is_user_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    # Get the list of admins for the chat
    admins = await context.bot.get_chat_administrators(chat_id)
    # Check if the user is in the list of admins
    return any(admin.user.id == user_id for admin in admins)

async def add(update:Update, context :ContextTypes.DEFAULT_TYPE):
    chat_type:str =update.message.chat.type
    original_message_id = update.message.message_id
    if not await is_user_admin(update, context):
        await update.message.reply_text("You're not authorized to use this bot.")
    else:
        if chat_type == 'group':
            chat_id = update.message.chat_id
            message_text = update.message.text
            bot_chat_member = await context.bot.get_chat_member(chat_id, context.bot.id)

            if bot_chat_member.status == "administrator":
                if chat_id  in group_info:
                    await context.bot.send_message(chat_id, text=f'❗️ Bot already in use in this group for token {group_info[chat_id]} ') 
                else:
                    text = "Choose a chain:"
                    keyboard = [
                    [InlineKeyboardButton("Ethereum (ETH)", callback_data='eth')],
                    [InlineKeyboardButton("Binance Smart Chain (BSC)", callback_data='bsc')],
                ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await context.bot.send_message(chat_id, text, reply_markup=reply_markup,reply_to_message_id=original_message_id)
                    
###################  the thread 
                    # with group_info_lock:
                    #     group_info[chat_id] = message_text
                    #     await context.bot.send_message(chat_id, text=f"Token {message_text} received! I will now share information based on this token in this group.")  
                    #     print(group_info)

            else:
                await context.bot.send_message(chat_id, text=f'❗️ Administrator permission needed. Make me admin please!') 

async def add_btn(update:Update, context :ContextTypes.DEFAULT_TYPE):
    global mode
    global sent_text,query,mode
    query = update.callback_query
    chat_id = query.message.chat_id
    original_message_id = query.message.message_id
    await query.answer()
    # Handle the callback data
    if query.data == 'eth':
        sent_message=await context.bot.send_message(chat_id, text="➡[ETH] Token address?",reply_to_message_id=original_message_id)
        ###c heck if the token is eth before saving
        users_details[str(chat_id)] = {"awaiting_token": True}
        # user_details[str(chat_id)+query.data] = 
        mode='eth'
    elif query.data == 'bsc':
        sent_message= await query.edit_message_text(text="➡[BSC] Token address?")
        mode='bsc'

async def handle_text_message(update:Update, context: ContextTypes.DEFAULT_TYPE):
    global mode,contract_address
    original_message_id = update.message.message_id
    chat_id = update.message.chat_id
    text_message = update.message.text


    import re

    # Regular expression pattern to match common emojis
    emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"  # Emoticons
                            u"\U0001F300-\U0001F5FF"  # Symbols & Pictographs
                            u"\U0001F680-\U0001F6FF"  # Transport & Map Symbols
                            u"\U0001F700-\U0001F77F"  # Alchemical Symbols
                            u"\U0001F780-\U0001F7FF"  # Geometric Shapes
                            u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-B
                            u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                            u"\U0001FA00-\U0001FA6F"  # Extended-A
                            u"\U0001FA70-\U0001FAFF"  # Extended-B
                            u"\U0001F004"  # Mahjong Tile Red Dragon
                            u"\U0001F0CF"  # Playing Card Back
                            u"\U0001F170-\U0001F251"  # Enclosed Characters
                            "]+", flags=re.UNICODE)


    # Check if the text contains emojis
    
    if emoji_pattern.search(text_message):
        print("Emojis found in the text.")
        print(update.message.text)
        try:
            if last_message[keys[-1]]=='➡️ Send me new emoji (custom emojis can be used 🤖)':
                print('goodddd')
                BUY_EMOJI.append(update.message.text)
                chat_idd==chat_id
                demo[chat_idd]={'emoji':update.message.text}
                # print(groups)
                print(BUY_EMOJI)

            else:
                print('not')

        except IndexError:
            print('Not last message')

        else:
            print('done')
            await context.bot.send_message(chat_id,'✅Buy Emoji Changed Successfully',reply_to_message_id=original_message_id)
 
        # BUY_EMOJI=''
        # BUY_EMOJI+=update.message.text
        # print(buy_emoji)
    else:
        print('suppose previous')

    try:
        global token_name
        valid_token=w3.is_address(text_message)
        print(valid_token)
        contract_address=text_message
        print(mode)
        if mode == 'eth':
            if valid_token == True:
                if str(chat_id) in users_details and users_details[str(chat_id)].get("awaiting_token"):
                    # Save the token address in user_data
                    users_details[str(chat_id)]["token_address"] = text_message
                    print(users_details)
                    try:   
                        token_contract = w3.eth.contract(address=contract_address, abi=abi)  # Replace [] with the actual ABI
                        token_name = token_contract.functions.name().call()
                        token_symbol = token_contract.functions.symbol().call()
                    except Exception as e:
                        print(f"An error occurred: {str(e)}")
                        await context.bot.send_message(chat_id, text="Token not found")

                    else:
                        text = "⏺Select pair Listed Below"
                        keyboard = [
                        [InlineKeyboardButton(f"✅ {token_symbol} / ETH (UniSwap)", callback_data='selected')],
                    
                    ]
                        reply_markup_pair = InlineKeyboardMarkup(keyboard)

                        await context.bot.send_message(chat_id,text, reply_markup=reply_markup_pair,reply_to_message_id=original_message_id)
                        # Clear the awaiting_token flag
                        users_details[str(chat_id)]["awaiting_token"] = False
                else:
                    print('kkkkk')

            else:
                print('Token not found')
                # await context.bot.send_message(chat_id, text="Token not found")
        elif mode== 'bsc':
            pass
    except NameError:
        await context.bot.send_message(chat_id, text='Unrecognized input😊')

async def pulling(update:Update,context:ContextTypes.DEFAULT_TYPE):
    global contract_address,mode,token_name
    query = update.callback_query
    chat_id = query.message.chat_id
    original_message_id = query.message.message_id
    await query.answer()

    if query.data=='selected':
        print('pooling')
    with group_info_lock:
        group_info[chat_id] = contract_address
        # await context.bot.send_message(chat_id, text=f"Token message_text received! I will now share information based on this token in this group.")  
        print(group_info)

        # print('ok')
        # await context.bot.send_message(chat_id, text="Saved",reply_to_message_id=original_message_id)
        text = f"🤖{token_name} was added to OxBuy_bot"
        keyboard = [
        [InlineKeyboardButton("🟢Buy Bot Settings", callback_data='settings')],
        [InlineKeyboardButton("  #️⃣Portal or Group Link", callback_data='link')],
        [InlineKeyboardButton("⚙Buy Competition Settings", callback_data='competition')],
        [InlineKeyboardButton("🕖Last Buy Setting", callback_data='buy_settings')],
        
    ]

        reply_markup_pair = InlineKeyboardMarkup(keyboard)

        await context.bot.send_message(chat_id,text, reply_markup=reply_markup_pair,reply_to_message_id=original_message_id)


async def option(update:Update,context:ContextTypes.DEFAULT_TYPE):
    option_btn = update.callback_query
    chat_id = option_btn.message.chat_id
    original_message_id = option_btn.message.message_id
    await option_btn.answer()
    print(chat_id)

    if option_btn.data=='settings':
        text = f"🤖 Oxbuybot"
        print(chat_idd)
        if len(change_gif)==0:
            gif_emoji='🚫'

        else:
            gif_emoji='✅'
        btn1=InlineKeyboardButton(f"{gif_emoji}Gif / Image", callback_data='buy_gif')
        btn2=InlineKeyboardButton("⏫Min Buy $0", callback_data='settings')
        btn3=InlineKeyboardButton(f"{demo[chat_idd]['emoji']}Buy Emoji", callback_data='emoji_set')
        btn4=InlineKeyboardButton("💲Buy Step $10", callback_data='settings')
        btn5=InlineKeyboardButton("Big Buy Comp⏩", callback_data='settings')
        btn6=InlineKeyboardButton("Last Buy Comp⏩", callback_data='last_buy')
        btn7=InlineKeyboardButton("⚙Group Settings", callback_data='settings')
                     
        row1=[btn1,btn2]
        row2=[btn3,btn4]
        row3=[btn5,btn6]
        row4=[btn7]
        
        reply_markup_pair = InlineKeyboardMarkup([row1,row2,row3,row4])
        await context.bot.send_message(chat_id,text, reply_markup=reply_markup_pair,reply_to_message_id=original_message_id)

async def go(update:Update, context:ContextTypes.DEFAULT_TYPE):
    text='➡️ Send me new emoji (custom emojis can be used 🤖)'
    go_btn=update.callback_query
    chat_id=go_btn.message.chat_id
    original_message_id=go_btn.message.message_id
    await go_btn.answer()

    if go_btn.data == 'emoji_set':
        last_message[original_message_id] = text
        print(last_message)
        print(original_message_id)
        if last_message[original_message_id]== text:
            print('good')
            keys.append(original_message_id)
        await context.bot.send_message(chat_id,text,reply_to_message_id=original_message_id)
        if update and update.message:
            text_message = update.message.text
            print(f'{text_message}ffk')
        else:
            print('no messgae yet')               

    elif go_btn.data =='buy_gif':
        message=(
            f"➡️ Send the URL of your gif image\n"
            f"Sample looks like this 'https://media.giphy.com/media/3oxOCgMHgPtSUULjzO/giphy.gif'"
        )
        await context.send_message(chat_id,message,reply_to_message_id=original_message_id)
async def settings(update:Update, context :ContextTypes.DEFAULT_TYPE):
    chat_type:str =update.message.chat.type
    original_message_id = update.message.message_id

    if chat_type == 'group':
        message_text=update.message.text
        chat_id=update.message.chat_id
        bot_chat_member = await context.bot.get_chat_member(chat_id, context.bot.id)
        
        if bot_chat_member.status == "administrator":
            with open('user_tokens.json','r')as file_data:
                data=json.load(file_data)
                # print(data)
            checker=str(chat_id)
            print(checker)
            if f'{checker}eth' in data or f'{checker}bsc'  in data:
                text = "⚙Settings"
                if len(change_gif)==0:
                    gif_emoji='🚫'

                else:
                    gif_emoji='✅'

                await context.bot.send_message(chat_id, text=f'settings show here') 
                btn1=InlineKeyboardButton(f"{gif_emoji}Gif / Image", callback_data='buy_gif')
                btn2=InlineKeyboardButton("⏫Min Buy $0", callback_data='settings')
                btn3=InlineKeyboardButton(f"{demo[chat_idd]['emoji']}Buy Emoji", callback_data='emoji_set')
                btn4=InlineKeyboardButton("💲Buy Step $10", callback_data='settings')
                btn5=InlineKeyboardButton("Big Buy Comp⏩", callback_data='big_buy')
                btn6=InlineKeyboardButton("Last Buy Comp⏩", callback_data='last_buy')
                btn7=InlineKeyboardButton("⚙Group Settings", callback_data='settings')
                            
                row1=[btn1,btn2]
                row2=[btn3,btn4]
                row3=[btn5,btn6]
                row4=[btn7]
                
                reply_markup_pair = InlineKeyboardMarkup([row1,row2,row3,row4])
                await context.bot.send_message(chat_id,text, reply_markup=reply_markup_pair,reply_to_message_id=original_message_id)

            else:
                await context.bot.send_message(chat_id, text=f'Firstly type /add to start tracking your coin🤨') 

                
        else:
            await context.bot.send_message(chat_id, text=f'❗️ Administrator permission needed. Make me admin please!') 

async def tutorial(update:Update, context :ContextTypes.DEFAULT_TYPE):
    chat_type:str =update.message.chat.type
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    original_message_id = update.message.message_id
    # print(chat_type)
    if chat_type == 'private':
        response=(
        f"<a href='https://t.me/OxBuy_bot'>@OxBuy_bot</a>Tutorial\n\n"
        f"Step 1: Add @OxBuy_bot as an Administrator in your Group"
        f"Step 2: Type /add in your Group"
        f"Step 3: Enter the contract address"
        f"Step 4: Type /settings to Adjust Emoji, or start a Buy Comp!"
    )
        await context.bot.send_message(chat_id=user_id, text=response,parse_mode='HTML',disable_web_page_preview=True, reply_to_message_id=original_message_id)  

async def remove(update:Update, context :ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    with group_info_lock:
        if chat_id in group_info:
            del group_info[chat_id]
            await context.bot.send_message(chat_id,text="I have stopped sharing information in this group.")
        else:
            await context.bot.send_message(chat_id,text="I'm not currently active in this group.")
async def the_event():
    global bot,last_block
    while True:
        with group_info_lock:
            for chat_id ,token in list(group_info.items()):
                uniswap_helper = UniswapHelper(rpc_url,token)

                if mode =='eth':
                    weth_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
                    contract_address=token
                    pair_address = uniswap_helper.get_uniswap_pair_address(contract_address, weth_address)
                    # print(pair_address)

                    uniswap_helper.get_market_cap(contract_address)
                    print(uniswap_helper.contract_address)
                    print(uniswap_helper.bought)
                    mkt,token_amount,final_usd,transaction_hash,buyers_address=uniswap_helper.query_swap_events(pair_address,contract_address)
                    # print(address)
                    weth_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
                    pair_address=uniswap_helper.get_uniswap_pair_address(contract_address,weth_address)
                    if uniswap_helper.bought==1:
                        name,symbol,token_address,decimal= uniswap_helper.get_token_details(contract_address)
                        # address = urls[0].split('/')[-1]
                        shortened_address = f'{buyers_address[:4]}…{buyers_address[-4:]}'
                        etherscan_address_url = f'https://etherscan.io/address/{contract_address}'
                       
                        fft=f'<a href="{etherscan_address_url}">{shortened_address}</a> | <a href="https://etherscan.io/tx/{transaction_hash}">Txn</a>'
                        chart_url=f"https://dexscreener.com/ethereum/{pair_address}"
                        chart=f'<a href="{chart_url}">Chart</a>'
                        trend_url=f"https://t.me/BSCTRENDING/5431871"
                        trend=f"<a href='{trend_url}'>Trending</a>"
                        divide_by=int(final_usd//20) 
                        print(divide_by)

                        token_amount='{:,}'.format(token_amount)
                        mkt='{:,}'.format(int(mkt))

                        print(symbol)
                        message=(
                                        f"<b> ✅{name}</b> Buy!\n\n"
                                        f"{demo[chat_idd]['emoji']*divide_by}\n\n"
                                        f"💵 {round(uniswap_helper.amount1In/(10**18),5)}ETH (${round(final_usd,2)})\n"
                                        f"🪙{token_amount}<b> {symbol}</b>\n"
                                        f"🔷{fft}\n"
                                        # f"🔼 Position +{position_percentage}\n"
                                        f"🔼 Market Cap <b>{mkt}</b>\n"
                                        f"🦎{chart} 🔷{trend}"
                                        
                                    )
                        print(f'send message amount out {uniswap_helper.amount1In/10**18}')
                      
                        def resize_gif(url, new_dimensions, output_path):
                            # Open the GIF from URL
                            response = requests.get(url)
                            gif = Image.open(BytesIO(response.content))

                            # Create a list to hold each frame
                            frames = []

                            # Loop through each frame in the GIF
                            for frame in ImageSequence.Iterator(gif):
                                # Resize the frame
                                resized_frame = frame.resize(new_dimensions,Image.AFFINE)
                                frames.append(resized_frame)

                            # Save the resized frames as a new GIF
                            frames[0].save(
                                output_path,
                                save_all=True,
                                append_images=frames[1:],
                                optimize=False,
                                duration=gif.info['duration'],
                                loop=0
                            )
                        try:
                            gif_url = 'https://media.giphy.com/media/xUPJPAA3ovxrz3HSik/giphy.gif'
                            new_dimensions = (200, 120)  # Set your desired dimensions
                            output_path = "resized_gif.gif"  # Set the output path
                            resize_gif(gif_url, new_dimensions, output_path)   

                            await bot.send_document(chat_id,document=open('resized_gif.gif', 'rb'),caption=message,parse_mode='HTML')
                        except Exception as e:
                            print(e)
                            await bot.send_message(chat_id,message,parse_mode='HTML',disable_web_page_preview=True)
                    await asyncio.sleep(1)
        
if __name__ == '__main__':
    global bot
    application = ApplicationBuilder().token(TOKEN).build()


    bot=application.bot
    start_handler = CommandHandler('start', start)
    add_handler = CommandHandler('add', add)
    # process_handler = CommandHandler('tutorial', query_swap_event)
    remove_handler = CommandHandler('remove', remove)
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add))
    application.add_handler(start_handler)
    application.add_handler(add_handler)
    application.add_handler(CommandHandler('settings',settings))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    application.add_handler(CallbackQueryHandler(add_btn,pattern='eth'))
    application.add_handler(CommandHandler('tutorial',tutorial))
    application.add_handler(CallbackQueryHandler(add_btn,pattern='bsc'))
    application.add_handler(CallbackQueryHandler(pulling,pattern='selected'))
    application.add_handler(CallbackQueryHandler(option,pattern='settings'))
    application.add_handler(CallbackQueryHandler(go,pattern='emoji_set'))
    application.add_handler(CallbackQueryHandler(go,pattern='buy_gif'))


    # application.add_handler(process_handler)``
    application.add_handler(remove_handler)
    message_thread = threading.Thread(target=lambda: asyncio.run(the_event()))
    message_thread.daemon = True
    message_thread.start()
    application.run_polling()




