import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, Updater, MessageHandler, Filters, CallbackQueryHandler

import bot_settings

import homelyDB_API
from classes.Tool import Tool
import User

# from classes.User import User

logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

updater = Updater(token=bot_settings.TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    print(update.to_json())
    chat_id = update.effective_chat.id
    logger.info(f"> Start chat #{chat_id}")
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("I need a tool", callback_data="need")],
                                     [InlineKeyboardButton("I want to share my tool", callback_data="share")]])
    context.bot.send_message(chat_id=chat_id, text="Welcome! What would you like to do?", reply_markup=keyboard)


# https://pythonprogramming.org/making-a-telegram-bot-using-python/
# https://docs.python-telegram-bot.org/

def respond(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if user_state(update.message.from_user.id) == 0:
        context.bot.send_message(chat_id=chat_id, text="Please select one of the options")
        return
    share(update, context)


def callback(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    choice = update.callback_query.data  # WORKS!!!!
    logger.info(f'User chose {update.callback_query.data}')
    if choice == "need":
        need(update, context)
    if choice == "share":
        context.bot.send_message(chat_id=chat_id, text="What tool would you like to add?")
    if choice == 'showall':
        showall(update, context)
        logger.info(f"> Start chat #{chat_id}")
    if choice == 'showcatagories':
        showcatagories(update, context)



def showall(update: Update, context: CallbackContext):
    pass


def showcatagories(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Power Tools", callback_data='powertools')],
                                     [InlineKeyboardButton("Furniture",
                                                           callback_data='furniture')],
                                     [InlineKeyboardButton("Kitchen Appliances",
                                                           callback_data='appliances')],
                                     [InlineKeyboardButton("For kids",
                                                           callback_data='kids')],
                                     [InlineKeyboardButton("Electronics",
                                                           callback_data='electronics')],
                                     ])
    context.bot.send_message(chat_id=chat_id, text="Select a category", reply_markup=keyboard)


def need(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Show ALL tools", callback_data='showall')],
                                     [InlineKeyboardButton("Show available catagories",
                                                           callback_data='showcatagories')]])
    context.bot.send_message(chat_id=chat_id, text="Select one of the below:", reply_markup=keyboard)


def share(update, context):
    if update.message.text[0]=='/' :
        return
    chat_id = update.effective_chat.id
    user_id = int(update.message.from_user.id)
    user_name =str(update.message.from_user.first_name)
    tool_name = update.message.text
    tool = Tool(user_id, tool_name)
    user = User.BOTUser(user_id, user_name)
    logger.info(f'User: {user}, Tool: {tool}')
    homelyDB_API.add_tool(tool, user)
    update.message.reply_text("Got the description, add a picture! You can use your camera or upload from your device")
    # context.bot.send_message(chat_id=chat_id, text="Got name, add picture!")

def share_from_command(update, context):
    context.bot.send_message(update.effective_chat.id, text="Describe your tool")
    share(update, context)


def save_image(update, context):
    file_id = update.message.photo[-1].file_id
    new_file = context.bot.get_file(file_id)
    new_file.download(f'image_{file_id[:5]}.jpg')
    print(f'image_{file_id[:5]}.jpg')
    update.message.reply_text("Image saved!")

dispatcher.add_handler(CallbackQueryHandler(callback))

dispatcher.add_handler(CommandHandler('start', start))

dispatcher.add_handler(MessageHandler(Filters.photo, save_image))

dispatcher.add_handler(CommandHandler('borrowtool', need))

dispatcher.add_handler(CommandHandler('landtool', share_from_command))

dispatcher.add_handler(MessageHandler(Filters.text, respond))





logger.info("* Start polling...")
updater.start_polling()  # Starts polling in a background thread.
updater.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")
