## Telegram bot
A telegram bot that responds to messages

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
* Stored BOT_TOKEN in <pardir>/.env (do not commit!)

## Next
* Fun, but don't spend more time on bot. Focus on infrastructure:
  * Deploy to EC2, use Docker
  * Automate deployment to AWS
  * Integrate with AWS backend (redis) to store messages
* Regarding integration:
  * Eventually, website will display stored messages
  * Host bot message database on cloud (ElastiCache)
  * Create API server between website and database (EC2)
* On database side, will probably store messages like this:
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
