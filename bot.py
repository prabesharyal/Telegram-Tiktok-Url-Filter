#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to Delete to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Deleting Messsage Bot example, Deletes Tiktok URL using regex.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
from telegram import __version__ as TG_VER

API_Hash = os.environ.get('BOT_TOKEN')

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Dear {user.mention_html()}, Bot is active and will remove Tiktok links now onwards.",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("There's No help available here. Call 911.")


async def developer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """About the Bot Developer!"""
    await update.message.reply_text("Bot is developed by @PrabeshAryalNP on Telegram.")


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Deletes the Tiktok URL."""
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(API_Hash).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("developerinfoPA", developer))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.Regex('(https:\/\/)?([vt]+|[www]+)\.?([tiktok]+)\.([com]{2,6})([\/\w@?=&\.-]*)') & ~filters.COMMAND, delete))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()