import discord
from discord.ext import commands
import json
from utils import checks
from utils import setting

class Config():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.check(checks.is_admin)
    async def logging(self, ctx):
        """Turns logging on or off in the desired channel
        Logging may only be active in one channel per sever"""

        server = ctx.message.server
        channel = ctx.message.channel

        # Checking for config file
        if not setting.is_in_data(ctx.message):
            await self.bot.say("Failed to initialise server file")
            return

        # Open file
        with open("config/serversettings.json") as file:
            data = json.load(file)

            # If logging is active in channel > Disable
            if channel.id == data[server.id]["log_channel"]:
                data[server.id]["logging"] = False
                data[server.id]["log_channel"] = ""
                await self.bot.say("Logging disabled for **{0}**".format(server.name))

                with open("config/serversettings.json", "w") as edit:
                    save = json.dumps(data)
                    edit.write(save)

                return

            # Change channel to new channel
            else:
                data[server.id]["logging"] = True
                data[server.id]["log_channel"] = channel.id

                with open("config/serversettings.json", "w") as edit:
                    save = json.dumps(data)
                    edit.write(save)

                await self.bot.say("Logging set to **{0}** in channel **{1}** for **{2}**:pencil: "
                                   .format(data[server.id]["logging"], channel.name, server.name))
                return

    @commands.command(pass_context=True)
    @commands.check(checks.is_admin)
    async def join_role(self, ctx, role = None):
        """Turns the role on join system on and selects role
        e.g. $join_role Guest
        Will grant the role Guest to users as they join
        To disable:
        $join_role False"""

        server = ctx.message.server

        # Check if server has server
        if not setting.is_in_data(ctx.message):
            await self.bot.say("Failed to initialise server file")
            return

        if role.lower() == "false" or "off":
            with open("config/serversettings.json") as file:
                data = json.load(file)
                data[server.id]["role_on_join"] = False

                # Save to file
                with open("config/serversettings.json", "w") as edit:
                    save = json.dumps(data)
                    edit.write(save)

                # Output
                await self.bot.say("Role on join disabled for {0.name} :pencil:".format(server))
                return

        # Search for role
        role = discord.utils.find(lambda m: m.name == role, server.roles)
        # Return if nothing is found
        if role is None:
            await self.bot.say("No role found.\n(This is case sensitive, it may help if you @mention the role)")
            return

        if toggle is True:
            # Open server config
            with open("config/serversettings.json") as file:
                data = json.load(file)
                data[server.id]["role_on_join"] = True
                data[server.id]["join_role"] = role.id

                # Save to file
                with open("config/serversettings.json", "w") as edit:
                    save = json.dumps(data)
                    edit.write(save)

                # Output message
                await self.bot.say("Role {0.name} will be granted to users as they join {1.name}".format(role, server))
                return

        else:
            await self.bot.say("Please specify True / False")
            return

def setup(bot):
    bot.add_cog(Config(bot))