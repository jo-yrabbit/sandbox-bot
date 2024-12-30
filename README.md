## Telegram bot
A telegram bot that responds to messages

### What it does
* Responds to `/start` command with welcome message
* If user replies to a question `Would you like... [content])`, with something like a Y/N, it will (try) to respond

### What I did
* Messaged @botfather in TG to create bot and get a bot token
* Started chatting with new bot on TG
* Stored BOT_TOKEN in <pardir>/.env (do not commit!)
* Created main `bot.py` and `config.py`, `parser.py`
* Run `python ./bot.py` to poll for activity on TG chat until `Ctrl+C`

### Next
* Fun, but don't spend more time on bot. Focus on infrastructure:
  * Deploy to EC2, use Docker
  * Automate deployment to AWS
  * Integrate with AWS backend (redis) to store messages
* On Redis side, store messages like this:
```json
[
  { id: 1, content: "Message 1", timestamp: "2024-12-29T12:00:00Z" },
  { id: 2, content: "Message 2", timestamp: "2024-12-29T12:01:00Z" }
]
```

### Reference
* https://core.telegram.org/bots/tutorial#echo-bot
* https://gitlab.com/Athamaxy/telegram-bot-tutorial/-/blob/main/TutorialBot.py
* https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot.py
