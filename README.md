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

#### Interacts with user
* Responds to `/start` command with welcome message
* If user replies to a question `Would you like... [content])`, with something like a Y/N, it will (try) to respond

#### Stores messages
* Sends messages to database for storage (redis)
* Responds to `/fetch` command to show last 2 messages

## How-to
WIP, jotting notes for now

### Set up Redis on Docker in local PC

* Install redis in Docker
```sh
# Pull the Redis image
docker pull redis

# Run Redis container
# If running locally, configurations are:
#   - REDIS_HOST="localhost"
#   - REDIS_PORT=6379
#   - REDIS_PASSWORD=""
docker run --name local-redis -p 6379:6379 -d redis

# To check if it's running
docker ps

# To see Redis logs
docker logs local-redis
```

* When you're done, stop and remove the Redis container
```sh
docker stop local-redis
docker rm local-redis
```

### Run bot
Bot will poll for activity on TG chat until `Ctrl+C`
```sh
python ./bot.py
```

### Talk to bot on Telegram
Things to try:
1. Pose question in one message:
* Start question with `Would you like`
* Follow question a new line showing the reward in square brackets `[here]`
```sh
# For example:
Would you like <to have lots of fun>?
[Angels will guide you]
```

2. Quote-reply to question with `Y` or `N`
3. Bot will respond
4. Type `/fetch` to recall last few messages

### What I did
* Messaged @botfather in TG to create bot and get a bot token
* Started chatting with new bot on TG
* Designed to make REST api calls to a separate [`api-server`](https://github.com/jo-yrabbit/sandbox-api-server) to store messages and `/fetch` them

### Next
Fun, but don't spend more time on bot. Focus on infrastructure:
* Deploy to EC2, use Docker
* Integrate with AWS backend (ElastiCache) to store messages
* Automate deployment to AWS (Github Action)
* Eventually, website will display stored messages

### Reference
* https://core.telegram.org/bots/tutorial#echo-bot
* https://gitlab.com/Athamaxy/telegram-bot-tutorial/-/blob/main/TutorialBot.py
* https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot.py
