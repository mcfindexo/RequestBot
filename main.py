from pyrogram import filters , Client
from pyrogram.types import InlineKeyboardButton , InlineKeyboardMarkup
import os
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

LOGGER = logging.getLogger(__name__)
bot = Client(
    "notesbot",
    api_id=os.environ['API_ID'],
    api_hash=os.environ['API_HASH'],
    bot_token=os.environ['BOT_TOKEN'],
    
)

CHAT_ID = os.environ.get('CHAT_ID')
owner = int(os.environ.get('OWNER'))

def call_back_in_filter(data):
    return filters.create(
        lambda flt, _, query: flt.data in query.data,
        data=data
    )



@bot.on_message(filters.command('start'))
def start(_,message):
    message.reply_text('🔥𝓗𝓲 𝓣𝓱𝓮𝓻𝓮 ,\n\n✅ 24 Hour Active ✓ \n⚡️ Super Fast Response ✓ \n\nServer  : Heroku\nLibrary : Pyrogram\n\n☘️ Dᴇᴠᴇʟᴏᴘᴇʀ : @MyzoneMy\n\n🤖By Using Our Service You Must Agree To Our Privacy Policy 👀')
    
@bot.on_message(filters.command('help'))
def help(_,message):
    message.reply_text('💯 If you want, you can contact us using this format \n\n Ex:- /request Hello, I need a help')
    
@bot.on_message(filters.command('request'))
def req(_,message):
    message.reply('Your request have been sent ✔')
    global req_
    req_ = message.text.replace(message.text.split(' ')[0] , '')
    keyboard = []
    keyboard.append([InlineKeyboardButton("✅ Accept" , callback_data=f"request:accept:{message.from_user.id}")])
    keyboard.append([InlineKeyboardButton("❌ Reject" , callback_data=f'request:reject:{message.from_user.id}')])
    bot.send_message(int(CHAT_ID) , f'Requested by @{message.from_user.username}\n\n{req_}' , reply_markup=InlineKeyboardMarkup(keyboard))
    

@bot.on_callback_query(call_back_in_filter('request'))
def botreq(_,query):
    result = query.data.split(':')

    if result[1] == "accept" and query.from_user.id == owner:
        bot.send_message(result[2] , "✔ You request has been approved")
        query.message.edit('Request approved\n\n{}'.format(req_))

    elif result[1] == "reject" and query.from_user.id == owner:
        bot.send_message(result[2] , "✘ Sorry your request has been rejected")
        query.message.edit('✘ Rejected !')
    
    else:
        query.answer('You are not allowed')


bot.run()
