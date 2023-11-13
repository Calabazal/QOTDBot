import discord
from discord.ext import commands, tasks
import asyncio
import json
import mysql.connector
import datetime, sys, traceback, os, random
import logging

logger = logging.getLogger(__name__)
## -------------------------------------------------------
## ??? ???
class QOTDcog(commands.Cog, name="Question Of The Day setup"):
## -------------------------------------------------------
## This is how Commands are run, currently the command prefix is set to use "?"
    def __init__(self, bot, *args, **kawrgs):
        self.bot = bot
        self.host = 'localhost'
        self.port = '3306'
        self.password = 'YOUR PASSWORD HERE'
        self.question.start() # When Started INIT will be called and start task "Question"
## -------------------------------------------------------
## Below are Commands are for the Bot on request.
    @commands.group(invoke_without_command=True)
    async def qotd(self, ctx):
        """- use '?help qotd' to see avaliable commands..."""
## -------------------------------------------------------
## Welcome command to change the channel that the bot inputs into!
    @qotd.command()
    async def channel(self, ctx, channel:discord.TextChannel):
        """- use '?qotd channel' to set the question to a specific channel."""
        if ctx.message.author.guild_permissions.administrator:
            db = mysql.connector.connect(database="questions", user = "root", password = self.password, host = self.host, port = self.port)
            logger.info(f"Database Connected for Bot QOTD edit.")
            cursor = db.cursor()
            cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(guild_id, channel_id) VALUES(%s,%s)")
                val = (ctx.guild.id, channel.id )
                logger.info('Guild ID:', ctx.guild.id)
                logger.info('Channel ID:', channel.id)
                await ctx.send(f"QOTD channel has been set to {channel.mention}")
            elif result is not None:
                sql = ("UPDATE main SET channel_id = %s WHERE guild_id = %s")
                val = (channel.id, ctx.guild.id)
                logger.info('Guild ID:', ctx.guild.id)
                logger.info('Channel ID:', channel.id)
                await ctx.send(f"QOTD channel has been updated to {channel.mention}")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
## -------------------------------------------------------
## This will allow a Question of the day to be ran...
    @tasks.loop(seconds=60)
    async def question(self):
        now = datetime.datetime.now()
        if now.hour==16 and now.minute==00:
            print('It is now time to run the code!')
            # Don't forget to reset the password above with export BOTDBPASSWORD
            db = mysql.connector.connect(database="questions", user = "root", password = self.password, host = self.host, port = self.port)
            logger.info(f"Database Connected for Selecting a Question.")
            cursor = db.cursor()
            cursor.execute("SELECT id, qotd_msg, timesused FROM questionoftheday")
            allquestions = cursor.fetchall()
            cursor.execute("SELECT channel_id, qotd_toggle FROM main")
            logger.info("It is now time to run the code for Server")
            for row in cursor.fetchall():
                if row[1] == 0:
                    continue
                selectedquestion = random.choice(allquestions)
                cursor.execute (f"UPDATE questionoftheday SET timesused = {selectedquestion[2]+1} WHERE ID = {selectedquestion[0]}")
                db.commit()
                channel_id = row[0]
                logger.info("Sending to channel ", channel_id)
                message_channel = self.bot.get_channel(int(channel_id))
                if message_channel is None:
                    logger.info("Could not get channel_id ", channel_id)
                    continue
                await message_channel.send(selectedquestion[1])
            cursor.close()
            db.close()
            return

    @question.before_loop
    async def before(self):
        await self.bot.wait_until_ready()
## -------------------------------------------------------
## This will allow a Question of the day to be ran...
    @qotd.command()
    async def again(self, ctx):
        print('It is now time to run the code!')
        # Don't forget to reset the password above with export BOTDBPASSWORD
        if ctx.message.author.guild_permissions.administrator:
            db = mysql.connector.connect(database="questions", user = "root", password = self.password, host = self.host, port = self.port)
            logger.info(f"Database Connected for Selecting a Question.")
            cursor = db.cursor()
            cursor.execute("SELECT id, qotd_msg, timesused FROM questionoftheday")
            allquestions = cursor.fetchall()
            cursor.execute(f"SELECT channel_id, qotd_toggle FROM main WHERE guild_id = {ctx.guild.id}")
            logger.info("It is now time to run the code for Specific Server")
            for row in cursor.fetchall():
                if row[1] == 0:
                    continue
                selectedquestion = random.choice(allquestions)
                cursor.execute (f"UPDATE questionoftheday SET timesused = {selectedquestion[2]+1} WHERE ID = {selectedquestion[0]}")
                db.commit()
                channel_id = row[0]
                logger.info("Sending to channel ", channel_id)
                await ctx.send(selectedquestion[1])
        cursor.close()
        db.close()
        return
## -------------------------------------------------------
## Turns the qotd command off!
    @qotd.command()
    async def off(self, ctx):
        """- use '?qotd off' to turn off the QOTD command."""
        if ctx.message.author.guild_permissions.administrator:
            db = mysql.connector.connect(database="questions", user = "root", password = self.password, host = self.host, port = self.port)
            logger.info(f"Database Connected for turning qotd command off ")
            cursor = db.cursor()
            cursor.execute(f"SELECT qotd_toggle FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result[0] == 1:
                sql = (f"UPDATE main SET qotd_toggle = 0 WHERE guild_id = {ctx.guild.id}")
                logger.info(f"Guild ID: {ctx.guild.id}")
                cursor.execute(sql)
                db.commit()
                cursor.close()
                db.close()
                await ctx.send(f"qotd message has been disabled.")
            elif result[0] == 0:
                await ctx.send(f"qotd message is already disabled")
## -------------------------------------------------------
## Welcome command to change the channel that the bot inputs into!
    @qotd.command()
    async def input(self, ctx, *, text):
        """- This command is only for use by Ashe."""
        if ctx.message.author.id == YOUR ID HERE:
            db = mysql.connector.connect(database="questions", user = "root", password = self.password, host = self.host, port = self.port)
            logger.info(f"Database Connected for Bot QOTD edit.")
            cursor = db.cursor()
            sql = ("INSERT INTO questionoftheday(qotd_msg) VALUES(%s)")
            val = (text,)
            await ctx.send(f"{text} has been added to the database")
##            if result is None:
##                sql = ("INSERT INTO main(guild_id, channel_id) VALUES(%s,%s)")
##                val = (ctx.guild.id, channel.id )
##                logger.info('Guild ID:', ctx.guild.id)
##                logger.info('Channel ID:', channel.id)
##                await ctx.send(f"QOTD channel has been set to {channel.mention}")
##            elif result is not None:
##                sql = ("UPDATE main SET channel_id = %s WHERE guild_id = %s")
##                val = (channel.id, ctx.guild.id)
##                logger.info('Guild ID:', ctx.guild.id)
##               logger.info('Channel ID:', channel.id)
##                await ctx.send(f"QOTD channel has been updated to {channel.mention}")
            cursor.execute(sql, val)
            logger.info(cursor.rowcount)
            db.commit()
            cursor.close()
            db.close()

## -------------------------------------------------------
## Turns the qotd command on!
    @qotd.command()
    async def on(self, ctx):
        """- use '?qotd on' to turn on the qotd command."""
        if ctx.message.author.guild_permissions.administrator:
            db = mysql.connector.connect(database="questions", user = "root", password = self.password, host = self.host, port = self.port)
            logger.info(f"Database Connected for turning qotd command off ")
            cursor = db.cursor()
            cursor.execute(f"SELECT qotd_toggle FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result[0] == 0:
                sql = (f"UPDATE main SET qotd_toggle = 1 WHERE guild_id = {ctx.guild.id}")
                logger.info(f"Guild ID: {ctx.guild.id}")
                cursor.execute(sql)
                db.commit()
                cursor.close()
                db.close()
                await ctx.send(f"qotd message has been enabled.")
            elif result[0] == 1:
                await ctx.send(f"qotd message is already enabled")

## -------------------------------------------------------
## Complete Cog Setup
async def setup(bot):
    await bot.add_cog(QOTDcog(bot))
    print('------ ------ ------ ')
    print('QOTDCog has Loaded')
    print('------ ------ ------ ')
