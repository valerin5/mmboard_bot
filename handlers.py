from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from settings import WELCOME_MESSAGE, TELEGRAM_ADMIN_CHAT_ID, REPLY_TO_THIS_MESSAGE, WRONG_REPLY, TELEGRAM_CHANNEL_ID

def start(update, context):
    update.message.reply_text(WELCOME_MESSAGE)


def button(update, context):
    query = update.callback_query
    if query.data == '1':
        query.message.copy(chat_id=TELEGRAM_CHANNEL_ID)
        context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=query.message.text + '\n\nЗапощено',
        )
        context.bot.edit_message_reply_markup(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=[]
        )
    else:
        context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=query.message.text + '\n\nОтклонено',
        )
        context.bot.edit_message_reply_markup(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=[]
        )



def forward_to_chat(update, context):
    # ссылка не работает(
    url = 'tg://user?id=%s' % update.message.from_user.id
    keyboard = [
        [
            InlineKeyboardButton("Запостить", callback_data='1'),
            InlineKeyboardButton("Отклонить", callback_data='2'),
        ],
        [InlineKeyboardButton("Отправивший", url=url)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.copy_message(
        message_id=update.message.message_id,
        chat_id=TELEGRAM_ADMIN_CHAT_ID,
        from_chat_id=update.message.chat_id,
        reply_markup = reply_markup
    )


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.chat_type.private, forward_to_chat))
    dp.add_handler(CallbackQueryHandler(button))
    return dp