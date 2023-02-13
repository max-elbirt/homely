import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ForceReply
from telegram.ext import CommandHandler, CallbackContext, Updater, MessageHandler, Filters, CallbackQueryHandler, \
    ConversationHandler

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

EXPECT_CATEGORY_SELECT_BUTTON_CLICK, EXPECT_ITEM_SELECTION = range(3)


def start(update: Update, context: CallbackContext):
    ''' Replies to start command '''
    update.message.reply_text('Hi! I am alive')


def select_category_by_user(update: Update, context: CallbackContext):

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
    update.message.reply_text('Select the category of the item you are looking for:', reply_markup=keyboard)

    return EXPECT_CATEGORY_SELECT_BUTTON_CLICK


def category_button_click_handler(update: Update, context: CallbackContext):
    ''' This gets executed on button click '''
    category = update.callback_query.data
    context.user_data['category'] = category
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f'You item is saved under {category}')
    ##get 5 items from DB
    # for item in items:
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Item 1", callback_data='item1')],
                                     [InlineKeyboardButton("Item 2",
                                                           callback_data='item2')],
                                     [InlineKeyboardButton("Item 3",
                                                           callback_data='item3')],
                                     [InlineKeyboardButton("Item 4",
                                                           callback_data='item4')],
                                     [InlineKeyboardButton("Item 5",
                                                           callback_data='item5')],
                                     ])
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='These are the top five items currently available. '
                                  'Select an item to borrow it')
    return EXPECT_ITEM_SELECTION


def get_item_info(update: Update, context: CallbackContext):
    item = update.callback_query.data
    #getinfo from DB
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Here is the photo of your item:')
    # photo = get from DB
    # context.bot.send_photo(chat_id=update.effective_chat.id,
    #                        photo=photo['file'])


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Conversation cancelled by user. Bye. Send /borrowtool to start again')
    return ConversationHandler.END


_handlers = {}

_handlers['start_handler'] = CommandHandler('start', start)

_handlers['borrow_conversation_handler'] = ConversationHandler(
    entry_points=[CommandHandler('borrowtool', select_category_by_user)],
    states={
        EXPECT_CATEGORY_SELECT_BUTTON_CLICK: [CallbackQueryHandler(category_button_click_handler)],
        EXPECT_ITEM_SELECTION: [CallbackQueryHandler(get_item_info)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    # per_message=True,
)

for name, _handler in _handlers.items():
    print(f'Adding handler {name}')
    dispatcher.add_handler(_handler)

logger.info("* Start polling...")
updater.start_polling()  # Starts polling in a background thread.
updater.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")
