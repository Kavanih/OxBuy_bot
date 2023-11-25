from telegram import Chat, ChatMember, ChatMemberUpdated, Update,InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes,CallbackContext,ChatMemberHandler, CallbackQueryHandler
import os 
from dotenv import load_dotenv
import tracemalloc
import requests
import json
import asyncio
import time
import millify
from web3 import Web3
import time
from tryout import SwapScanner
import threading
from telegram.ext import JobQueue




load_dotenv()
BUY_EMOJI=['🟢']
TIMER_INTERVAL = 5 * 60  # 5 minutes
UPDATE_INTERVAL = 5  # every 5 seconds


API_KEY=os.getenv('API_KEY')
ETHER_KEY=os.getenv('ether_key')
URL=os.getenv('url')
user_data={}
chat_ids=[]
last_message={}
keys=[]
li={}

price_array=[]
liquid_array=[]
MKTCap=[]
urls=[]
min_5=[]
symb=[]
pair_name=[]
price_usd=[]
tr_hash=[]
groups= {}
checker={}
group_tracker={}
chat_idd='1'
buyer=[]
connect=[]
gg={}
topic_array=[]
demo={
    chat_idd:{
        'emoji':'🟢'
    }
}


print(group_tracker)
# update.message.chat_id
rpc_url = "https://mainnet.infura.io/v3/c182d33f6fa949a294257059d5dd4248"
print(rpc_url)
w3 = Web3(Web3.HTTPProvider(rpc_url))
w3_bsc=Web3(Web3.HTTPProvider("https://binance.llamarpc.com"))

# Replace with the address of the Uniswap pair contract you're interested in
event_signature = w3.keccak(
    text="Swap(address,uint256,uint256,uint256,uint256,address)"
).hex()

bsc_event_signature = w3_bsc.keccak(
    text="Swap(address,uint256,uint256,uint256,uint256,address)"
).hex()
last_block = w3.eth.block_number
bsc_last_block=w3_bsc.eth.block_number
swap_event_abi = {
    "anonymous": False,
    "inputs": [
        {"indexed": True, "internalType": "address", "name": "sender", "type": "address"},
        {"indexed": False, "internalType": "uint256", "name": "amount0In", "type": "uint256"},
        {"indexed": False, "internalType": "uint256", "name": "amount1In", "type": "uint256"},
        {"indexed": False, "internalType": "uint256", "name": "amount0Out", "type": "uint256"},
        {"indexed": False, "internalType": "uint256", "name": "amount1Out", "type": "uint256"},
        {"indexed": True, "internalType": "address", "name": "to", "type": "address"}
    ],
    "name": "Swap",
    "type": "event"
}

contract_abi = [swap_event_abi]  # Make sure it's a list containing the dictionary

global_bot = None

async def timing(context: ContextTypes.DEFAULT_TYPE):
    global global_bot
    
    keys = list(group_tracker.keys())
    key = keys.pop(0)

    chat_id, contract_address = key, group_tracker[key]
    print(f'chat_id {key}')
    QUERY_INTERVAL = 5*60
    MAX_RETRIES = 10
    print('starting competition ....... ')
    

    message_id=None

    # Define the initial message
    message = ("🟢 Last Buy Competition (LIVE)\n\n"
               "⚙️ 05:00 remaining time!\n"
               "✅ Minimum Buy 0.10 ETH\n"
               "⬇️ Winning Prize 1 ETH")


    try:
        # Start with 4 minutes
        minutes_remaining = 5
        seconds_remaining = 0

        # Send the initial message and capture its message_id
        message= f"🟢 Last Buy Competition (LIVE)\n\n⏳ {minutes_remaining:02d}:{seconds_remaining:02d} remaining time!\n✅ Minimum Buy 0.10 ETH\n⬇️ Winning Prize 1 ETH"
        mesg_sent= await global_bot.send_message(key, message)
        await global_bot.pin_chat_message(key, message_id=mesg_sent.message_id)
    except Exception as e:
        await global_bot.send_message(key,'unknown error occured')
        print(e)
        return
    retries = 0
    while retries < MAX_RETRIES:
        try:
            current_time_file={'current_time':minutes_remaining}
            with open('timmer.json','w')as time_file:
                json.dump(current_time_file,time_file)
            start_time = time.time()
            while time.time() - start_time < QUERY_INTERVAL:
                elapsed_time = int(time.time() - start_time)
                minutes_remaining = 4 - (elapsed_time // 60)
                seconds_remaining = 59 - (elapsed_time % 60)

                message= f"🟢 Last Buy Competition (LIVE)\n\n⏳ {minutes_remaining:02d}:{seconds_remaining:02d} remaining time!\n✅ Minimum Buy 0.10 ETH\n⬇️ Winning Prize 1 ETH"
                await global_bot.edit_message_text(message, key, mesg_sent.message_id)
                # print(topics)
                
                import random
                # Wait for two seconds before the next update
                ratio=[2,4,8,10,12,7,4,5,3]
                print(topic_array)
                time.sleep(4)
                if minutes_remaining == 0 and seconds_remaining <= 3:

                    print('done')
                    message=(
                        f"<b>🏁 Last Buy Competition Finished</b>\n\n"
                        f"✅ <b>Minimum Buy</b> 0.10 USDT\n"
                        f"🔶 <b>Winning Prize</b> 1 USDT\n"
                        f'😊Buyer {topic_array[-1][0]} won\n'
                        # f'{topic_array[-1][2]}'
                    )
                    finish=await global_bot.send_message(key,message,parse_mode='HTML')
                    # await global_bot.pin_chat_message(key, message_id=finish.message_id)

        except Exception as e:
            print(f'an error {e} occured')
            retries += 1
            print(minutes_remaining,seconds_remaining)
            print(f"Error updating the countdown. Retrying... (Attempt {retries}/{MAX_RETRIES})")
            time.sleep(5)  # Wait for a longer interval before retrying
        else:
            break
    else:
        print('Error updating the countdown after retries. Please try again later.')


async def big_buy_timing(context: ContextTypes.DEFAULT_TYPE):
    global global_bot
    
    keys = list(group_tracker.keys())
    key = keys.pop(0)

    chat_id, contract_address = key, group_tracker[key]
    print(f'chat_id {key}')
    QUERY_INTERVAL = 5*60
    MAX_RETRIES = 10
    print('starting big buy competition ....... ')
    

    message_id=None

    # Define the initial message
    message = ("🟢 Last Buy Competition (LIVE)\n\n"
               "⚙️ 05:00 remaining time!\n"
               "✅ Minimum Buy 0.10 ETH\n"
               "⬇️ Winning Prize 1 ETH")


    try:
        # Start with 4 minutes
        minutes_remaining = 5
        seconds_remaining = 0

        # Send the initial message and capture its message_id
        message= f"🟢 Biggest Buy Competition (LIVE)\n\n⏳ {minutes_remaining:02d}:{seconds_remaining:02d} remaining time!\n✅ Minimum Buy 0.10 ETH\n⬇️ Winning Prize 1 ETH"
        mesg_sent= await global_bot.send_message(key, message)
        await global_bot.pin_chat_message(key, message_id=mesg_sent.message_id)
    except Exception as e:
        await global_bot.send_message(key,'unknown error occured')
        print(e)
        return
    retries = 0
    while retries < MAX_RETRIES:
        try:
            current_time_file={'current_time':minutes_remaining}
            start_time = time.time()
            while time.time() - start_time < QUERY_INTERVAL:
                elapsed_time = int(time.time() - start_time)
                minutes_remaining = 4 - (elapsed_time // 60)
                seconds_remaining = 59 - (elapsed_time % 60)

                message= f"🟢 Biggest Buy Competition (LIVE)\n\n⏳ {minutes_remaining:02d}:{seconds_remaining:02d} remaining time!\n✅ Minimum Buy 0.10 ETH\n⬇️ Winning Prize 1 ETH"
                await global_bot.edit_message_text(message, key, mesg_sent.message_id)
                # print(topics)
                
                import random
                # Wait for two seconds before the next update
                ratio=[2,4,8,10,12,7,4,5,3]
                print(topic_array)
                time.sleep(6)
                if minutes_remaining == 0 and seconds_remaining <= 3:
                    max_value_tuple = max(topic_array, key=lambda x: x[1])
                    print('done')
                    message=(
                        f"<b>🏁 Biggest Buy Competition Finished</b>\n\n"
                        f"✅ <b>Minimum Buy</b> 0.10 USDT\n"
                        f"🔶 <b>Winning Prize</b> 1 USDT\n"
                        f'😊Buyer {max_value_tuple[0]} won\n'
                        # f'{topic_array[-1][2]}'
                    )
                    finish=await global_bot.send_message(key,message,parse_mode='HTML')
                    # await global_bot.pin_chat_message(key, message_id=finish.message_id)

                    # break
        except Exception as e:
            print(f'an error {e} occured')
            retries += 1
            print(minutes_remaining,seconds_remaining)
            print(f"Error updating the countdown. Retrying... (Attempt {retries}/{MAX_RETRIES})")
            time.sleep(5)  # Wait for a longer interval before retrying
        else:
            break
    else:
        print('Error updating the countdown after retries. Please try again later.')

    time.sleep(QUERY_INTERVAL)
def query_swap_events(app):
    global global_bot
    QUERY_INTERVAL = 10
    while True:
        keys = list(group_tracker.keys())
        while keys:
            key = keys.pop(0)
            chat_id, contract_address = key, group_tracker[key]  
            global last_block,bsc_last_block
            current_block = w3.eth.block_number
            bsc_current_block=w3_bsc.eth.block_number
            if mode == 'eth':
                if current_block > last_block:
                    print(f'current address eth {contract_address}')
                    filter_params = {
                        "fromBlock": last_block + 1,
                        "toBlock": current_block,
                        "topics": [event_signature],
                        "address": contract_address  
                    }
                    new_entries = w3.eth.get_logs(filter_params)
                    for entry in new_entries:
                        event_data = w3.eth.contract(abi=contract_abi, address=contract_address).events.Swap().process_log(entry)
                        
                        transaction_hash = entry['transactionHash'].hex()  # This will give you the transaction hash
                        tr_hash.append(transaction_hash)
                        amount0In = event_data['args']['amount0In']
                        amount1In = event_data['args']['amount1In']
                        amount0Out = event_data['args']['amount0Out']
                        amount1Out = event_data['args']['amount1Out']

                        # Determine whether the event is a buy or sell and print the details
                        for chat_id in chat_ids:
                            if amount0In > 0 and amount1Out > 0:
                                print(f"sell: {amount0In} token0 for {amount1Out} token1")
                            elif amount1In > 0 and amount0Out > 0:
                                print(f"buy: {amount1In} token1 for {amount0Out} token0")
                                # buyer.append(transaction_hash)
                                try:
                                    address = urls[0].split('/')[-1]
                                    shortened_address = f'{address[:4]}…{address[-4:]}'
                                    etherscan_address_url = f'https://etherscan.io/address/{address}'
                                    transc_hash = f'https://etherscan.io/tx/{tr_hash[-1]}'
                                    transaction_hash = entry['transactionHash'].hex()  # This will give you the transaction hash

                                    
                                    fft=f'<a href="{etherscan_address_url}">{shortened_address}</a> | <a href="https://etherscan.io/tx/{transaction_hash}">Txn</a>'
                                    chart_url=f"https://dexscreener.com/ethereum/{checker[str(chat_id)]['p_address']}"
                                    chart=f'<a href="{chart_url}">Chart</a>'
                                    formatted_number = millify.millify(checker[str(chat_id)]['market_cap'], precision=1)  # Output: '455.6M'
                                    token_amount = round(amount0Out / 1_000_000_000)
                                    token_amount = '{:,}'.format(token_amount)
                                    formatted_number = '${:,.0f}'.format(MKTCap[0])
                                    loop = asyncio.new_event_loop()

                                    number = amount0Out
                                    print(f'nu{number}')
                                    formatted_tokennumber = number / 1000000000

                                    print(f"you{formatted_tokennumber:.2f}")
                                    ratio=checker[str(chat_id)]['USD']
                                    ratio=float(ratio)
                                    # print(type(round(formatted_tokennumber,2)))
                                    price_in_usd=(round(formatted_tokennumber,2)) * ratio
                                    divide_by=int(price_in_usd//10)
                                    message=(
                                        f"<b> ✅ {checker[str(chat_id)]['token_symbols']}</b> Buy!\n\n"
                                        f"{demo[chat_idd]['emoji']*divide_by}\n\n"
                                        f"💵 {round(amount1In/(10**18),5)} ETH (${round(price_in_usd,2)})\n"
                                        f"🪙 {formatted_tokennumber:.2f} <b>{checker[str(chat_id)]['token_symbols']}</b>\n"
                                        f"🔷 {fft}\n"
                                        # f"🔼 Position +{position_percentage}\n"
                                        f"🔼 Market Cap <b>{formatted_number}</b>\n"
                                        f"🦎 {chart} 🔹<a href='https://t.me/ETHTRENDING/3777258'>Trending</a>"
                                        
                                    )
                                    asyncio.set_event_loop(loop)
                                    print(key)
                                    try:
                                        loop.run_until_complete(global_bot.send_message(key, message,parse_mode='HTML',disable_web_page_preview=True))
                                    except Exception as e:
                                        print(f'asd {e} Error')
                                    finally:
                                        print('one done')
                                except Exception as e:
                                    print(f'anggg error {e} occured')
                    last_block = current_block

                    time.sleep(QUERY_INTERVAL)

            elif mode == 'bsc':
                if bsc_current_block > bsc_last_block:
                    print(f'current address bsc {contract_address}')
                    
                    filter_params = {
                        "fromBlock": bsc_last_block + 1,
                        "toBlock": bsc_current_block,
                        "topics": [bsc_event_signature],
                        "address": contract_address  # Filter for events from the specified contract
                    }
                    bsc_new_entries = w3_bsc.eth.get_logs(filter_params)
                    for bsc_entry in bsc_new_entries:
                        print(f'my log {bsc_new_entries}')

                        topics = bsc_new_entries[0]['topics']
                        topics=topics[-1]
                        topics = '0x{:x}'.format(int.from_bytes(topics, 'big'))
                        formatted_hex = '0x' + topics[2:].lower()

                        print(f'topics {formatted_hex}')

                        # Use the ABI of the contract to decode the log entry
                        bsc_event_data = w3_bsc.eth.contract(abi=contract_abi, address=contract_address).events.Swap().process_log(bsc_entry)
                        transaction_hash = bsc_entry['transactionHash'].hex()  # This will give you the transaction hash
                        print(f'my hash {transaction_hash}')

                        # Extract the values from the decoded data
                        amount0In = bsc_event_data['args']['amount0In']
                        amount1In = bsc_event_data['args']['amount1In']
                        amount0Out = bsc_event_data['args']['amount0Out']
                        amount1Out = bsc_event_data['args']['amount1Out']
                        print(chat_ids)

                        # Determine whether the event is a buy or sell and print the details
                        for chat_id in chat_ids:
                            if amount0In > 0 and amount1Out > 0:
                                print(f"bsc_sell: {amount0In} token0 for {amount1Out} token1")
                            elif amount1In > 0 and amount0Out > 0:
                                print(f"bsc_buy: {amount1In} token1 for {amount0Out} token0")

                                try:
                                    address = urls[0]
                                    print(urls)
                                    # print(address)
                                    shortened_address = f'{topics[:4]}…{topics[-4:]}'
                                    bsc_url = f'https://bscscan.com/address/{topics}'
                                    # transc_hash = f'https://etherscan.io/tx/{tr_hash[-1]}'
                                    
                                    fft=f'<a href="{bsc_url}">{shortened_address}</a> | <a href="https://bscscan.com/tx/{transaction_hash}">Txn</a>'
                                    chart_url=f"https://dexscreener.com/bsc/{checker[str(chat_id)]['p_address']}"
                                    chart=f'<a href="{chart_url}">Chart</a>'
                                    formatted_number = millify.millify(checker[str(chat_id)]['market_cap'], precision=1)  # Output: '455.6M'
                                    token_amount = round(amount0Out / 1_000_000_000)
                                    token_amount = '{:,}'.format(token_amount)

                                    formatted_number = '${:,.0f}'.format(MKTCap[0])
                                    loop = asyncio.new_event_loop()

                                    number = amount0Out
                                    print(f'you{number}')
                                    formatted_tokennumber = number / 1000000000000000000

                                    print(f"{formatted_tokennumber:.2f}")

                                    ratio=checker[str(chat_id)]['USD']
                                    ratio=float(ratio)
                                    # print(type(round(formatted_tokennumber,2)))
                                    price_in_usd=(number/10**9) * ratio
                                    print(price_in_usd)
                                    divide_by=int(price_in_usd//10)
                                    topic_array.append((formatted_hex,round(price_in_usd,2),f"{formatted_tokennumber:.2f} {checker[str(chat_id)]['token_symbols']}"))

                                    message=(
                                        f"<b> ✅ {checker[str(chat_id)]['token_symbols']}</b> Buy!\n\n"
                                        f"{demo[chat_idd]['emoji']*divide_by}\n\n"
                                        f"💵 {round(amount1In/(10**18),3)} BSC (${round(price_in_usd,2)})\n"
                                        f"🪙 {formatted_tokennumber:.2f} <b>{checker[str(chat_id)]['token_symbols']}</b>\n"
                                        f"🔷 {fft}\n"
                                        # f"🔼 Position +{position_percentage}\n"
                                        f"🔼 Market Cap <b>{formatted_number}</b>\n"
                                        f"🦎 {chart} 🔹<a href='https://t.me/ETHTRENDING/3777258'>Trending</a>"
                                        
                                    )
                                    asyncio.set_event_loop(loop)
                                    print(key)
                                    try:
                                        print(type(key))

                                        # Run the coroutine until it completes
                                        loop.run_until_complete(global_bot.send_message(key, message,parse_mode='HTML',disable_web_page_preview=True))
                                    except Exception as e:
                                        print(f'aaa {e} Error')
                                    finally:
                                        print('one done')
                                except IndexError:
                                    print(f'ang error  occured')

                                except IndexError:
                                    print(f'ang error index occured')
                bsc_last_block = bsc_current_block
                time.sleep(QUERY_INTERVAL)           
async def sticker_hand(update:Update,context:ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_type:str =update.message.chat.type
    sticker = update.message.sticker
    sticker_id = sticker.file_id
    emoji = sticker.emoji
    response = f"You sent a sticker with ID {sticker_id} and {emoji} emoji."
    if chat_type == 'group':
        chat_id=update.message.chat_id
        print(response)
        # await context.bot.send_message(chat_id, text=response)
    else:
        print('nothing')

async def competitons(update:Update, context :ContextTypes.DEFAULT_TYPE):
    pass


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
    elif chat_type == 'group':
        original_message_id = update.message.message_id
        message_text=update.message.text
        chat_id=update.message.chat_id
        bot_chat_member = await context.bot.get_chat_member(chat_id, context.bot.id)
        if '@thbuybot' in message_text:
            if bot_chat_member.status == "administrator":
                await context.bot.send_message(chat_id, text=f'from group {message_text}',reply_to_message_id=original_message_id)  
            else:
                await context.bot.send_message(chat_id, text=f'❗️ Administrator permission needed. Make me admin please!')  

async def echo(update:Update, context :ContextTypes.DEFAULT_TYPE):
    user_message=update.message.text
    user_id = update.message.from_user.id
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    original_message_id = update.message.message_id
    await context.bot.send_message(chat_id=user_id, text=user_message, reply_to_message_id=original_message_id)
    # await update.message.reply_text(user_message)
    print(user_id)

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
    if chat_type == 'group':
        message_text=update.message.text
        print(message_text)
        chat_id = update.message.chat_id
        bot_chat_member = await context.bot.get_chat_member(chat_id, context.bot.id)
        
        if bot_chat_member.status == "administrator":
            print(chat_id in chat_ids)
            if chat_id  in gg:
                await context.bot.send_message(chat_id, text=f'❗️ Bot already in use in this group for token {gg[chat_id]} ') 
            else:
                chat_ids.append(chat_id)
                text = "Choose a chain:"
                keyboard = [
                [InlineKeyboardButton("Ethereum (ETH)", callback_data='eth')],
                [InlineKeyboardButton("Binance Smart Chain (BSC)", callback_data='bsc')],
            ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await context.bot.send_message(chat_id, text, reply_markup=reply_markup,reply_to_message_id=original_message_id)

        else:
            await context.bot.send_message(chat_id, text=f'❗️ Administrator permission needed. Make me admin please!') 
        
            # print('private')
    print(update.message.text)

async def add_btn(update:Update, context :ContextTypes.DEFAULT_TYPE):

    global sent_text,query,mode
    query = update.callback_query
    chat_id = query.message.chat_id
    original_message_id = query.message.message_id


    await query.answer()
    # Handle the callback data
    if query.data == 'eth':
        sent_message=await context.bot.send_message(chat_id, text="➡[ETH] Token address?",reply_to_message_id=original_message_id)
        user_data[str(chat_id)] = {"awaiting_token": True}
        

        mode='eth'
    elif query.data == 'bsc':
        user_data[f"{str(chat_id)}bsc"]={"awaiting_token":True}
        # text_message = update.message.text
        sent_message= await query.edit_message_text(text="➡[BSC] Token address?")
        
        mode='bsc'
        # print(text_message)

        # user_data[chat_id] = {"awaiting_token @bsc": True}

    # message_id = sent_message.message_id
    # sent_text = sent_message.text
async def handle_text_message(update:Update, context: ContextTypes.DEFAULT_TYPE):
    global mode
    original_message_id = update.message.message_id
    chat_id = update.message.chat_id
    text_message = update.message.text

    print(text_message)
    print(mode)



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
                print(groups)
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

    if mode == 'eth':
        rpc_url= "https://mainnet.infura.io/v3/c182d33f6fa949a294257059d5dd4248"
        connect.append(rpc_url)
        # print("No emojis found in the text.")
        # print(BUY_EMOJI[-1])
        if str(chat_id) in user_data and user_data[str(chat_id)].get("awaiting_token"):
            # Save the token address in user_data
            user_data[str(chat_id)]["token_address@"] = text_message

            


    #### the inline wld depend on the number of pair returns ##
            
            url=URL
            print(user_data[str(chat_id)])
            print(type(user_data[str(chat_id)]['token_address@']))
            contract_address = user_data[str(chat_id)]['token_address@']
            # print(user_data)
            
            api_key =ETHER_KEY
            params = {
                "module": "account",
                "action": "tokentx",
                "contractaddress": contract_address,
                "apikey": api_key,
            }

            file_details={f'{str(chat_id)}{query.data}':{'id':str(chat_id),'token':contract_address}}
            try:
            # Make the API request
                response = requests.get(url, params=params)

                if response.status_code == 200:
                    print("Token found on Ethereum blockchain.")

                    data = response.json()    

                    if "result" in data and isinstance(data["result"], list):
                        print("Token found on Ethereum blockchain.")
                        gg[chat_id]=contract_address


                        other_url=f'https://api.dexscreener.com/latest/dex/tokens/{contract_address}'

                        from decimal import Decimal
                        other_response=requests.get(other_url)
                        data=other_response.json()
                        print(other_response.status_code)
                        # print(data)

                        with open('token_details.json','w') as details:
                            json.dump(data,details,indent=4)


                        with open('token_details.json', 'r') as file:
                            contract_abi = json.load(file)

                        # for txn in data['result']:
                        #     transaction_hash=txn['hash']
                            # tr_hash.append(transaction_hash)

       
                        ethereum_pair = next(((pair['baseToken']['name'], pair['pairAddress'], pair['priceUsd'], pair['url'], pair['fdv'],pair['baseToken']['symbol']) for pair in data['pairs'] if pair['chainId'] == 'ethereum'), None)

                        if ethereum_pair:
                            name, address, price_usd, url, fdv,symbol= ethereum_pair
                            # print(f'Name: {name}, Pair Address: {address}, Price in USD: {price_usd}, URL: {url}, FDV: {fdv}')
                            MKTCap.append(fdv)
                            urls.append(url)
                            symb.append(symbol)
                            pair_name.append(address)
                      
                            checker[str(chat_id)]={'market_cap':fdv,'web_url':url,'token_symbols':symbol,'p_address':address,'USD':price_usd,'name':name}
                            theaddress_details={
                                chat_id:{
                                    'token':text_message,
                                    'name':name
                                }
                            }
                            try:
                                with open('address.json','r')as theaddress:
                                    thecontent=json.load(theaddress)

                            except FileNotFoundError:
                                with open('address.json','w')as theaddress:
                                    json.dump(theaddress_details,theaddress,indent=4)

                                
                            
                            except json.decoder.JSONDecodeError:
                                with open('address.json','w')as theaddress:
                                    json.dump(theaddress_details,theaddress,indent=4)


                            else:
                                thecontent.update(theaddress_details)
                                with open('address.json','w')as theaddress:
                                    json.dump(thecontent,theaddress,indent=4)
                        else:
                            print('No ethereum pair found')
                            

                        contract_address=checker[str(chat_id)]['p_address']
                        group_tracker[chat_id]=contract_address
                       
                        keys.append(chat_id)
                        print(contract_address)

                        user_data[str(chat_id)]["token_address@"] = text_message
                #### the inline wld depend on the number of pair returns ##
                        text = "⏺Select pair Listed Below"
                        print(checker)
                        keyboard = [
                        [InlineKeyboardButton(f"✅ {checker[str(chat_id)]['token_symbols']} / ETH (UniSwap)", callback_data='selected')],
                    
                    ]
                        reply_markup_pair = InlineKeyboardMarkup(keyboard)

                        await context.bot.send_message(chat_id,text, reply_markup=reply_markup_pair,reply_to_message_id=original_message_id)
                        # Clear the awaiting_token flag
                        user_data[str(chat_id)]["awaiting_token"] = False

                        # print('started listening ....... ')

                        try:
                            print('checked')
                            with open('user_tokens.json','r')as file_data:
                                content=json.load(file_data)
                                print(content)


                        except FileNotFoundError:
                            with open('user_tokens.json','w')as file_data:
                                json.dump(file_details,file_data,indent=4)
                        except json.decoder.JSONDecodeError:
                            with open('user_tokens.json','w')as file_data:
                                json.dump(file_details,file_data,indent=4)

                        else:
                            with open('user_tokens.json','w')as file_data:
                                content.update(file_details)
                                print(content)
                                json.dump(content,file_data,indent=4)
                else: # Token not found
                    print("Token not found on Ethereum blockchain.")
            except Exception as e:
                print(f'A {e} Error Occured')
            else:
                print('move on')
                # print('An Error Occured')  
    print('gooooooooood')

    if mode == 'bsc':
        token_address=text_message
        rpc_url="https://bsc-dataseed.binance.org/"
        connect.append(rpc_url)
        
        w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))
        print(w3.is_connected())
    # Check if the contract exists
        code = w3.eth.get_code(token_address)

        if code :
            print(f"Token contract {token_address} found on BSC.")
            if str(chat_id)+'bsc' in user_data and user_data[str(chat_id)+'bsc'].get("awaiting_token"):
                user_data[str(chat_id)+'bsc']["token_address@"] = text_message

                

                print(user_data)
                contract_address =user_data[str(chat_id)+'bsc']['token_address@']
                url=URL
                print(user_data)
                api_key =ETHER_KEY
                params = {
                    "module": "account",
                    "action": "tokentx",
                    "contractaddress": contract_address,
                    "apikey": api_key,
                }

                file_details={f'{str(chat_id)}{query.data}':{'id':str(chat_id),'token':contract_address}}
                # print(file_details)
                try:
                # Make the API request
                    response = requests.get(url, params=params)
                    if response.status_code == 200:
                        print("Token found on Bsc blockchain.")

                        data = response.json()    

                        if "result" in data and isinstance(data["result"], list):
                            print("Token found on Bsc blockchain.")
                            gg[chat_id]=contract_address


                            other_url=f'https://api.dexscreener.com/latest/dex/tokens/{contract_address}'

                            from decimal import Decimal
                            other_response=requests.get(other_url)
                            data=other_response.json()
                            print(other_response.status_code)
                            # print(data)

                            with open('token_details.json','w') as details:
                                json.dump(data,details,indent=4)


                            with open('token_details.json', 'r') as file:
                                contract_abi = json.load(file)
                                
                            # print(data)
                            bsc_pair = next(((pair['baseToken']['name'], pair['pairAddress'], pair['priceUsd'], pair['url'], pair['fdv'],pair['baseToken']['symbol'],pair['quoteToken']['symbol']) for pair in data['pairs'] if pair['chainId'] =="bsc" and pair['labels']== ["v2"]), None)
                            if bsc_pair:
                                name, address, price_usd, url, fdv,symbol,quote_token= bsc_pair
                                # print(f'Name: {name}, Pair Address: {address}, Price in USD: {price_usd}, URL: {url}, FDV: {fdv}')
                                MKTCap.append(fdv)
                                urls.append(url)
                                symb.append(symbol)
                                pair_name.append(address)
                                checker[str(chat_id)]={'market_cap':fdv,'web_url':url,'token_symbols':symbol,'p_address':address,'USD':price_usd,'name':name}
                                theaddress_details={
                                            chat_id:{
                                                    'token':text_message,
                                                    'name':name
                                                }
                                            }
                                    
                                try:
                                    with open('address.json','r')as theaddress:
                                        thecontent=json.load(theaddress)

                                except FileNotFoundError:
                                    with open('address.json','w')as theaddress:
                                        json.dump(theaddress_details,theaddress,indent=4)

                                except json.decoder.JSONDecodeError:
                                    with open('address.json','w')as theaddress:
                                        json.dump(theaddress_details,theaddress,indent=4)
                                else:
                                    thecontent.update(theaddress_details)
                                    with open('address.json','w')as theaddress:
                                        json.dump(thecontent,theaddress,indent=4)

                                print(checker) 

                                print(quote_token)
                            else:
                                print('not found')

                            contract_address=checker[str(chat_id)]['p_address']
                            group_tracker[str(chat_id)]=contract_address
                            keys.append(chat_id)
                            print(f'my{contract_address}')

                            user_data[str(chat_id)+'bsc']["token_address@"] = text_message
                    #### the inline wld depend on the number of pair returns ##
                            text = "⏺Select pair Listed Below"
                            print(checker)
                            keyboard = [
                            [InlineKeyboardButton(f"✅ {checker[str(chat_id)]['token_symbols']} / BSC (UniSwap)", callback_data='selected')],
                        
                        ]
                            reply_markup_pair = InlineKeyboardMarkup(keyboard)
                            # print(checker)
                            # print(str(chat_id))

                            await context.bot.send_message(chat_id,text, reply_markup=reply_markup_pair,reply_to_message_id=original_message_id)
                            # Clear the awaiting_token flag
                            user_data[str(chat_id)+'bsc']["awaiting_token"] = False
                            print(file_details)
                            try:
                                print('checked')
                                with open('user_tokens.json','r')as file_data:
                                    content=json.load(file_data)
                                    print(content)
                            except FileNotFoundError:
                                with open('user_tokens.json','w')as file_data:
                                    json.dump(file_details,file_data,indent=4)
                            except json.decoder.JSONDecodeError:
                                with open('user_tokens.json','w')as file_data:
                                    json.dump(file_details,file_data,indent=4)

                            else:
                                with open('user_tokens.json','w')as file_data:
                                    content.update(file_details)
                                    print(content)
                                    json.dump(content,file_data,indent=4)
                except Exception as e:
                    return f"An error occurred: {str(e)}"

        else:
            print('No bsc pair found')

        
    
async def selected_pair(update:Update,context:ContextTypes.DEFAULT_TYPE):
    global mode
    selected = update.callback_query
    chat_id = selected.message.chat_id
    original_message_id = selected.message.message_id

    await selected.answer()
    print(selected.data)
    # Handle the callback data
    if selected.data == 'selected':
        print('ok')
        # await context.bot.send_message(chat_id, text="Saved",reply_to_message_id=original_message_id)
        text = f"✅ {checker[str(chat_id)]['name']} {checker[str(chat_id)]['token_symbols']} ({mode.upper()}) added to Oxbuybot"
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
        btn1=InlineKeyboardButton("🚫Gif / Image", callback_data='settings')
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

                await context.bot.send_message(chat_id, text=f'settings show here') 
                btn1=InlineKeyboardButton("🚫Gif / Image", callback_data='settings')
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
            

async def happen(update:Update,context:ContextTypes.DEFAULT_TYPE):
    happen_btn = update.callback_query
    chat_id = happen_btn.message.chat_id
    original_message_id = happen_btn.message.message_id
    await happen_btn.answer()
    if happen_btn.data=='last_buy':
        print('last buy')
        text='🤖 OxBuyBot '
    
        bbt1= InlineKeyboardButton("⏳ Countdown (5 minute)", callback_data="countdown")
        bbt2=InlineKeyboardButton("🔼 Minimum Buy (0.1 ETH)", callback_data="minimum_buy")
        bbt3=InlineKeyboardButton("🏆 Prize (1 ETH)", callback_data="prize")
        bbt4=InlineKeyboardButton("💎 Must Hold (not set)", callback_data="must_hold")
        bbt5=InlineKeyboardButton("🏆 Start Last Buy Competition!", callback_data="start_competition")
        bbt6=InlineKeyboardButton("⬅️ Go Back to Bot Settings", callback_data="settings")

        row1=[bbt1]
        row2=[bbt2]
        row3=[bbt3,bbt4]
        row4=[bbt5]
        row5=[bbt6]
        
        reply_markup_pair = InlineKeyboardMarkup([row1,row2,row3,row4,row5])
        await context.bot.send_message(chat_id,text, reply_markup=reply_markup_pair,reply_to_message_id=original_message_id)

    

    elif happen_btn.data=='big_buy':
        print('big buy')
        text='🤖 OxBuyBot '
    
        bbt1= InlineKeyboardButton("⏳ Countdown (5 minute)", callback_data="countdown")
        bbt2=InlineKeyboardButton("🔼 Minimum Buy (0.1 ETH)", callback_data="minimum_buy")
        bbt3=InlineKeyboardButton("🏆 Prize (1 ETH)", callback_data="prize")
        bbt4=InlineKeyboardButton("💎 Must Hold (not set)", callback_data="must_hold")
        bbt5=InlineKeyboardButton("🏆 Start Biggest Buy Competition!", callback_data="start_bigbuy_competition")
        bbt6=InlineKeyboardButton("⬅️ Go Back to Bot Settings", callback_data="settings")

        row1=[bbt1]
        row2=[bbt2]
        row3=[bbt3,bbt4]
        row4=[bbt5]
        row5=[bbt6]
        
        reply_markup_pair = InlineKeyboardMarkup([row1,row2,row3,row4,row5])
        await context.bot.send_message(chat_id,text, reply_markup=reply_markup_pair,reply_to_message_id=original_message_id)

async def comp_clicked(update:Update, context:ContextTypes.DEFAULT_TYPE):
    competition_btn = update.callback_query
    chat_id = competition_btn.message.chat_id
    original_message_id = competition_btn.message.message_id
    await competition_btn.answer()
    

    if competition_btn.data == 'start_competition':
        message_id=original_message_id
        context.job_queue.run_once(timing, 0)
        print('good')
        message_content = """
🟢Last Buy Competition (LIVE)

⏲️ 04:04 remaining time!

✅ Minimum Buy 0.10 ETH
🔽 Winning Prize 1 ETH

🟢Chart 🟢Events 🔽Trending
    """

    elif competition_btn.data == 'start_bigbuy_competition':
        message_id=original_message_id
        context.job_queue.run_once(big_buy_timing, 0)
        print('good')

        # await context.send_message()
        

async def error_handlerr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'update {update} caused error {context.error}')



def main():
    global global_bot 
    app=Application.builder().token(API_KEY).build()
    global_bot = app.bot
    app.add_handler(CommandHandler('start',start))
    app.add_handler(CommandHandler('settings',settings))
    # app.add_handler(CommandHandler('competitions',set_timer))
    app.add_handler(CommandHandler('tutorial',tutorial))
    # app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, happen))
    app.add_handler(MessageHandler(filters.Sticker.ALL, sticker_hand))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CallbackQueryHandler(add_btn,pattern='eth'))
    app.add_handler(CallbackQueryHandler(add_btn,pattern='bsc'))
    app.add_handler(CallbackQueryHandler(selected_pair,pattern='selected'))
    app.add_handler(CallbackQueryHandler(option,pattern='settings'))
    app.add_handler(CallbackQueryHandler(option,pattern='link'))
    app.add_handler(CallbackQueryHandler(option,pattern='competition'))
    app.add_handler(CallbackQueryHandler(option,pattern='buy_settings'))
    app.add_handler(CallbackQueryHandler(go,pattern='emoji_set'))
    app.add_handler(CallbackQueryHandler(happen,pattern='last_buy'))
    app.add_handler(CallbackQueryHandler(happen,pattern='big_buy'))
    app.add_handler(CallbackQueryHandler(comp_clicked,pattern='start_competition'))
    app.add_handler(CallbackQueryHandler(comp_clicked,pattern='start_bigbuy_competition'))
    event_listener_thread = threading.Thread(target=query_swap_events,args=(app,),daemon=True)
    event_listener_thread.start()

    
    # asyncio.create_task(okY())
    # app.add_error_handler(error_handlerr)
    # app.add_error_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, error_handlerr))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()







