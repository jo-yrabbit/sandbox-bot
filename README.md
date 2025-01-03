## Telegram bot
A telegram bot that responds to messages

### How to run
1. Create a `.env` file:
* BOT_TOKEN (Telegram bot token from @botfather)
* BOT_ID (For now, make one up)
* API_URL (For now, http://localhost:5000. Once api-server is deployed to AWS, replace)
2. Make sure [`api-server`](https://github.com/jo-yrabbit/sandbox-api-server)
3. Run `python ./bot.py` to poll for activity on TG chat until `Ctrl+C`

### What it does
* Responds to `/start` command with welcome message
* If user replies to a question `Would you like... [content])`, with something like a Y/N, it will (try) to respond

### What I did
* Messaged @botfather in TG to create bot and get a bot token
* Started chatting with new bot on TG
* Designed to make REST api calls to a separate [`api-server`](https://github.com/jo-yrabbit/sandbox-api-server) to store messages and `/fetch` them

### Next
Fun, but don't spend more time on bot. Focus on infrastructure:
* Deploy to EC2, use Docker
* Integrate with AWS backend (ElastiCache) to store messages
* Automate deployment to AWS (Github Action)

### Reference
* https://core.telegram.org/bots/tutorial#echo-bot
* https://gitlab.com/Athamaxy/telegram-bot-tutorial/-/blob/main/TutorialBot.py
* https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot.py
