# Discord Message Tracker Bot
This bot is built with discord.py, and is designed to monitor message deletions in your Discord server. The bot also has a response functionality for a specific phrase

## Features

- **Message Deletion Tracking:** whenever a message is deleted, the bot will post a detailed embed message about the deletion in a specific channel
- **Phrase Response:** whenever a user types a message containing the phrase, the bot will send a message in response

## Technologies
The Discord Message Tracker Bot is built with Python and uses the following libraries and technologies:

- discord.py
- zoneinfo (Python standard library)



## Setup

1. Enable the **Message Content Intent** for your bot in the Discord Developer Portal
2. Install dependencies: `pip install -r requirements.txt`
3. Set the environment variables and run the bot:

```bash
export DISCORD_TOKEN="your-bot-token"
export LOG_CHANNEL_ID="123456789012345678"
python main.py
```

Only deletions from the server that contains the log channel are reported. Messages sent before the bot started are not cached, so for those only the channel and message ID are logged.
