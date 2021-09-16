from telegram import CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from settings import WELCOME_MESSAGE, TELEGRAM_ADMIN_CHAT_ID, REPLY_TO_THIS_MESSAGE, WRONG_REPLY, TELEGRAM_CHANNEL_ID

def start(update, context):
    update.message.reply_text(WELCOME_MESSAGE)


def button(update, _):
    query = update.callback_query
    if query.data == '1':
        update.message.forward(chat_id=TELEGRAM_CHANNEL_ID)


def forward_to_chat(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Запостить", callback_data='1'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    forwarded = update.message.forward(chat_id=TELEGRAM_ADMIN_CHAT_ID)

    if not forwarded.forward_from:
        context.bot.send_message(
            chat_id=TELEGRAM_ADMIN_CHAT_ID,
            reply_to_message_id=forwarded.message_id,
            text=f'{update.message.from_user.id}\n{REPLY_TO_THIS_MESSAGE}',
            reply_markup=reply_markup
        )

def forward_to_user(update, context):
    user_id = None
    if update.message.reply_to_message.forward_from:
        user_id = update.message.reply_to_message.forward_from.id
    elif REPLY_TO_THIS_MESSAGE in update.message.reply_to_message.text:
        try:
            user_id = int(update.message.reply_to_message.text.split('\n')[0])
        except ValueError:
            user_id = None
    if user_id:
        context.bot.copy_message(
            message_id=update.message.message_id,
            chat_id=user_id,
            from_chat_id=update.message.chat_id
        )
    else:
        context.bot.send_message(
            chat_id=TELEGRAM_ADMIN_CHAT_ID,
            text=WRONG_REPLY
        )


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.chat_type.private, forward_to_chat))
    dp.add_handler(MessageHandler(Filters.chat(TELEGRAM_ADMIN_CHAT_ID) & Filters.reply, forward_to_user))
    dp.add_handler(CallbackQueryHandler(button))
    return dp