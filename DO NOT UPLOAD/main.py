import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, Updater, MessageHandler, Filters, CallbackQueryHandler

import bot_settings

import homelyDB_API
from classes.Tool import Tool
from classes import User

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
    context.bot.send_message(chat_id=chat_id, text="👋 Welcome! What would you like to do? You can /landtool or /borrowtool " )



def respond(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    # if user_state(update.message.from_user.id) == 0:
    #     context.bot.send_message(chat_id=chat_id, text="Please select one of the options")
    #     return
    share(update, context)


def callback(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    choice = update.callback_query.data  # WORKS!!!!
    logger.info(f'User chose {update.callback_query.data}')
    if choice == "need":
        need(update, context)
    if choice == "share":
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Power Tools", callback_data='powertools')],
                                         [InlineKeyboardButton("Furniture",
                                                               callback_data='add_furniture')],
                                         [InlineKeyboardButton("Kitchen Appliances",
                                                               callback_data='add_appliances')],
                                         [InlineKeyboardButton("For kids",
                                                               callback_data='add_kids')],
                                         [InlineKeyboardButton("Electronics",
                                                               callback_data='add_electronics')],
                                         ])
        context.bot.send_message(chat_id=chat_id, text="What tool would you like to add?", reply_markup=keyboard)
    if choice == 'showall':
        showall(update, context)
        logger.info(f"> Start chat #{chat_id}")
    if choice == 'showcatagories':
        showcatagories(update, context)
    if choice == 'done':
        gif_url='https://media.giphy.com/media/1xucXbDnMIYkU/giphy.gif'
        context.bot.send_animation(chat_id=chat_id, animation=gif_url)
        # set_user_state (update.message.from_user.id, 0)
    if choice == 'add_kids':
        pass

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
    if update.message.text[0] == '/':
        return
    # category = set_category()
    user_id = int(update.message.from_user.id)
    # print (category)
    user_name = str(update.message.from_user.first_name)
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
    # if get_user_state(update.message.from_user.id, 0) == 0:
    #     return
    file_id = update.message.photo[-1].file_id
    new_file = context.bot.get_file(file_id)
    new_file.download(f'image_{file_id[:5]}.jpg')
    print(f'image_{file_id[:5]}.jpg')
    update.message.reply_text("Image saved!")

    # set_user_state(update.message.from_user.id,0)
    chat_id = update.effective_chat.id
    buttons = [[InlineKeyboardButton("Add another item", callback_data="landtool")],
               [InlineKeyboardButton("Borrow an item", callback_data="borrowtool")],
               [InlineKeyboardButton("I'm done for now!", callback_data="done")],
               ]
    update.message.reply_text(text="Your tool has been added and now available for borrowing. \n Thanks for being such a great neghbor, neighbor!\n\n What would you like to do now?",
                             reply_markup=InlineKeyboardMarkup(buttons, one_time_keyboard=True))


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
