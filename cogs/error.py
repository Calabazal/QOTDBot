import discord
from discord.ext import commands
import asyncio, json
import datetime, sys, traceback, os
import logging
## -------------------------------------------------------

logger = logging.getLogger(__name__)

logger.debug("")
logger.info("")
logger.warning("")
logger.error("")
logger.critical("")
## -------------------------------------------------------
## ??? ??? ???
class ErrorCog(commands.Cog, name="Error Commands"):
## -------------------------------------------------------
## Member Join Error Mo
    def __init__(self, bot):
        self.bot = bot
## -------------------------------------------------------
## Complete Cog Setup
async def setup(bot):
    await bot.add_cog(ErrorCog(bot))
    print('------ ------ ------ ')
    print('ErrorCog has Loaded')
    print('------ ------ ------ ')
