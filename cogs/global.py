import discord
from discord.ext import commands
import asyncio
import sqlite3, json
import mysql.connector
import datetime, sys, traceback, os
import logging
logger = logging.getLogger(__name__)

## -------------------------------------------------------
## ??? ??? ???
class GlobalCog(commands.Cog, name="Global Commands"):
## -------------------------------------------------------
## Member Join Error Mo
    def __init__(self, bot):
        self.bot = bot
        self.host = 'localhost'
        self.port = '3306'
        self.password = 'PASSWORD HERE'
## -------------------------------------------------------
## Manual Announcements to all servers
    @commands.command()
    async def announcement(self, ctx, *, text):
        if ctx.message.author.id == YOUR USER ID HERE
            db = mysql.connector.connect(database="questions", user = "root", password = self.password, host = self.host, port = self.port)
            logger.info(f"Database Connected for Manual Announcement.")
            cursor = db.cursor()
            cursor.execute(f"SELECT channel_id FROM main")
            for row in cursor.fetchall():
                channel_id = row[0]
                logger.info(f"Sending to channels, {channel_id}")
                message_channel = self.bot.get_channel(int(channel_id))
                if message_channel is None:
                    logger.info("Could not get channel_id ", channel_id)
                    continue
                await message_channel.send(text)
            cursor.close()
        else:
            await ctx.send("You're not Ashe! Get Rolled! https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            logger.info('A user got Rick Rolled!')
## -------------------------------------------------------
## Complete Cog Setup
async def setup(bot):
    await bot.add_cog(GlobalCog(bot))
    print('------ ------ ------ ')
    print('GlobalCog has Loaded')
    print('------ ------ ------ ')
