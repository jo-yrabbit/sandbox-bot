#!/usr/bin/env python
import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from config import Config
from parser import Parser

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

DEBUG = False

async def answer_if_user_responds_to_claude(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Detect if is reply to text chat"""
    message = update.message
    # Check if message is a reply
    if not message.reply_to_message:
        return

    # Access the original message that was replied to
    prompt = message.reply_to_message.text

    # Process it
    p = Parser(debug=DEBUG, logger=logger)
    p.process(prompt, message.text)

    # Respond
    response = p.get_text()
    if not response:
        logger.debug(f'Doing nothing. Response was not generated for user input \"{message.text}\"')
    await update.message.reply_text(response)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user.username
    await update.message.reply_text(f"Hello {user}!\nI am  , hello!")


def main() -> None:
    c = Config()

    # Create the Application and pass it your bot's token
    application = Application.builder().token(c.bot_token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler('start', start))

    # on non command i.e message - answer in Telegram with parsed response
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer_if_user_responds_to_claude))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()