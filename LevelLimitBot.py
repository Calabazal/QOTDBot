import discord
from discord.ext import commands, tasks
import asyncio, json
import mysql.connector
import datetime, sys, traceback, os
import logging

logging.basicConfig(level=logging.INFO, filename="log.log", filemode="a", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)
## -------------------------------------------------------
##Bot Description when using "Help" Command
description = '''LevelLimit Bot, created by LetsGoAshe'''
## Discords Intents are needed for permissions to do things in Discord
intents = discord.Intents.all()
## Bot Commands Initial and collectives
bot = commands.Bot(command_prefix='?', case_insensitive=True, description=description, intents=intents)
## --------------------------------------------------------
initial_extensions = []
## --------------------------------------------------------
## This is the unique Bot TOKEN
TOKEN = os.getenv('BOT TOKEN HERE')
## -------------------------------------------------------
## This sets the Bot's Status in Discord for us and also displays a print out of Username and ID in Terminals
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('With The Code'))
    print('Logged In!')
##By adding the commar after the text you can add text to a print function
    print('Username: ', bot.user.name)
    print('ID: ', bot.user.id)
    print('------ ------ ------')
## -------------------------------------------------------
# Here we load our extensions(cogs) listed above in [initial_extensions].
for filenames in os.listdir('./cogs'):
    if filenames.endswith('.py'):
        initial_extensions.append("cogs." + filenames[:-3])
## -------------------------------------------------------
## Load the Cog Extension Files
if __name__ == '__main__':
    @bot.event
    async def on_ready():
        for extension in initial_extensions:
            try:
                await bot.load_extension(extension)
                print('------ ------ ------')
                print(f'Loaded extension {extension}')
            except:
                print('------ ------ ------')
                print(f'Failed to load extension {extension}')
                traceback.print.exc()
## -------------------------------------------------------

bot.run('BOT TOKEN HERE')
