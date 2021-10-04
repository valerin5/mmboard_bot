from telegram.ext import Updater
from mmboard_bot.handlers import setup_dispatcher
from mmboard_bot.settings import TELEGRAM_TOKEN

updater = Updater(TELEGRAM_TOKEN)

dp = updater.dispatcher
dp = setup_dispatcher(dp)

updater.start_polling()

updater.idle()