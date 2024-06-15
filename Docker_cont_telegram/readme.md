# Docker based Telegram bot

## mount container volume and add /usr/src/app

### add a env file with

telegram_bot_api_token = XXXXXXXXXXXXXXXXXXXXXXXXX
mykey = your key works fine

### now set a folder to access the docker saved photos data

mount a volume /usr/src/app/datacollection
