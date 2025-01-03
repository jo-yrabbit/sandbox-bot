#!/usr/bin/env python
import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from config import Config
from parser import Parser
from api_client import MessageAPIClient

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

DEBUG = False
c = Config()
api = MessageAPIClient(c.bot_id, c.api_url)


async def fetch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show last messages when the command /fetch is issued."""
    state = 'test_state'  # TODO: get from parser
    messages = api.get_messages(state)

    if not messages:
        await update.message.reply_text(f'Nothing stored for state: {state}')
        return

    print_me = []
    for i,m in enumerate(messages):
        if (type(m) is dict) and ('text' in m.keys()):
            print_me.append(m['text'])
        else:
            logger.error(f'Message#{i} has invalid format: {str(m)}')
            print_me.append('')

    lines = [f'Message #{i}:\n{m}' for i,m in enumerate(print_me)]
    await update.message.reply_text('\n\n'.join(lines))


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

    # Finally, respond to user:
    await update.message.reply_text(response)

    # Store response
    try:
        state = 'test_state'  # TODO: get from parser
        if not api.store_message(state, response):
            await update.message.reply_text(f'Stored response:\n\n({state}) - \"{response}\"')
    except Exception as e:
        logger.error('Failed to store message - {}', e.args[0])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user.username
    await update.message.reply_text(f"Hello {user}!\nI am  , hello!")


def main() -> None:
    # Create the Application and pass it your bot's token
    application = Application.builder().token(c.bot_token).build()

    # Handle commands (/command) - answer in Telegram
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('fetch', fetch))

    # Handle non commands (e.g. messages from user) - answer in Telegram with parsed response
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer_if_user_responds_to_claude))

    # Run the bot until process is terminated (e.g. user presses Ctrl-C)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()