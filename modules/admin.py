import discord
from discord.ext import commands
from utils import checks
import json

class Admin():
    def __init__(self, bot):
        self.bot = bot

    # Changes the bot's game
    @commands.command(pass_conext=True)
    @commands.check(checks.is_owner)
    async def status(self, *, status: str):
        """Updates the Bot's status"""
        # Update the bots game
        await self.bot.change_status(discord.Game(name=status))
        await self.bot.say("Status updated to {}".format(status))
        print("Updated Bot's status to {}".format(status))

    # Lists bot's servers
    @commands.group()
    async def servers(self):
        """Manages the servers the bot is in"""

    @servers.command(pass_context=True)
    async def list(self):
        """Lists the servers the bot is in"""
        list = []
        for x in self.bot.servers:
            list.append(x.name)
        await self.bot.say(list)

    # Makes the bot leave a server
    @servers.command(pass_context=True)
    async def leave(self, server: str):
        server = discord.utils.get(self.bot.servers, name=server)
        if server is None:
            await self.bot.say("No server found")
            return
        self.bot.leave_server(server)

def setup(bot):
    bot.add_cog(Admin(bot))
