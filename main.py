import os
from zoneinfo import ZoneInfo

import discord

#BOT TOKEN
TOKEN = os.environ['DISCORD_TOKEN']

#CHANNEL ID FOR ALERTS ABOUT DELETED MESSAGES
CHANNEL_ID = int(os.environ['LOG_CHANNEL_ID'])

#ROLE ID OTHER BOTS
BOT_ROLE_ID = 760474688102727690

#TIME ZONE FOR MESSAGE DATES
TIMEZONE = ZoneInfo('Europe/Warsaw')

#DISCORD EMBED FIELD VALUE LIMIT
FIELD_LIMIT = 1024

intents = discord.Intents.default()
intents.typing = True
intents.messages = True
intents.message_content = True

bot = discord.Client(intents=intents)

def truncate(text):
    if len(text) > FIELD_LIMIT:
        return text[:FIELD_LIMIT - 3] + '...'
    return text

@bot.event
async def on_ready():
    print("Bot ready")

@bot.event
async def on_raw_message_delete(payload):

    #IGNORE DMS
    if payload.guild_id is None:
        return

    log_channel = bot.get_channel(CHANNEL_ID)
    if log_channel is None:
        print(f'Log channel {CHANNEL_ID} not found')
        return

    #ONLY LOG DELETIONS FROM THE SERVER THE LOG CHANNEL BELONGS TO
    if payload.guild_id != log_channel.guild.id:
        return

    message = payload.cached_message

    embed = discord.Embed(title='DELETED MESSAGE', color=discord.Color.red())

    #MESSAGE NOT IN CACHE (SENT BEFORE BOT STARTED) - CONTENT IS UNKNOWN
    if message is None:
        embed.add_field(name='Channel', value=f'<#{payload.channel_id}>', inline=True)
        embed.add_field(name='Message', value='*(content unavailable - message not in cache)*', inline=False)
        embed.set_footer(text=f'Message ID: {payload.message_id}')
        await log_channel.send(embed=embed)
        return

    if message.author.bot:
        return

    localized_time = message.created_at.astimezone(TIMEZONE)
    formatted_time = localized_time.strftime("%A, %d %B %Y | %H:%M:%S")

    embed.add_field(name='Author', value=message.author.mention, inline=True)
    embed.add_field(name='Date', value=formatted_time, inline=True)
    embed.add_field(name='Channel', value=message.channel.mention, inline=True)
    embed.add_field(name='Message', value=truncate(message.content) or '*(no text)*', inline=False)

    if message.attachments:
        attachments = '\n'.join(attachment.url for attachment in message.attachments)
        embed.add_field(name='Attachments', value=truncate(attachments), inline=False)

    embed.set_footer(text=f'Message ID: {message.id} | Author ID: {message.author.id}')

    await log_channel.send(embed=embed)

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    #RESPONDING ON MESSAGES
    if 'message' in message.content.lower():
        await message.channel.send('BOT ANSWER')

bot.run(TOKEN)
