import discord
from discord.ext import commands
import json
from utils import setting
from utils import checks

# Set's bot's desciption and prefixes in a list
description = "An autistic bot for an autistic group"
bot = commands.Bot(command_prefix=['$'], description=description, pm_help=True)

###################
## Startup Stuff ##
###################

@bot.event
async def on_ready():
    # Outputs login data to console
    print("---------------------------")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print("---------------------------")
    # Changes the bot's game to default
    await bot.change_status(discord.Game(name="Long Live GAF"))

    # Outputs the state of loading the modules to the console
    # So I know they have loaded correctly
    print("Loading Modules")
    print("---------------------------")
    bot.load_extension("modules.misc")
    print("Loaded Misc")
    bot.load_extension("modules.moderation")
    print("Loaded Moderation")
    bot.load_extension("modules.rng")
    print("loaded RNG")
    bot.load_extension("modules.subscriptions")
    print("Loaded Subscriptions")
    bot.load_extension("rss.rss")
    print("Loaded RSS")
    bot.load_extension("modules.csgo")
    print("Loaded CSGO")
    bot.load_extension("modules.configsetup")
    print("Loaded Config")
    bot.load_extension("modules.tags")
    print("Loaded Tags")
    print("---------------------------")

@bot.event
async def on_message(message):
    with open("config/ignored.json") as file:
        ignored = json.load(file)
    file.close()
    if message.author.id in ignored:
        return
    await bot.process_commands(message)

######################
## Misc and Testing ##
######################

# Command to update the bot's profile picture
# Because Fuyu told me off for doing it every time
@bot.command(hidden=True)
@commands.check(checks.is_owner)
async def updateprofile():
    """Updates the bot's profile image"""
    # Loads and sets the bot's profile image
    with open("logo.jpg","rb") as logo:
        await bot.edit_profile(avatar=logo.read())

@bot.command(hidden=True)
@commands.check(checks.is_owner)
async def ignore(user: discord.Member = None):
    """Ignores a user from using the bot"""
    if user is None:
        return
    if user.id is "95953002774413312":
        return
    with open("config/ignored.json") as file:
        ignored = json.load(file)
        if user.id not in ignored:
            ignored.append(user.id)
            with open("config/ignored.json", "w") as file:
                save = json.dumps(ignored)
                file.write(save)
            await bot.say("User {0} ignored :no_entry_sign:".format(user.name))
        else:
            ignored.remove(user.id)
            with open("config/ignored.json", "w") as file:
                save = json.dumps(ignored)
                file.write(save)
            await bot.say("User {0} unignored :white_check_mark:".format(user.name))


# Greet command
# Also for testing the response of the bot
# Was originally a trial for me learning how to mention people
# But I couldn't really think of a use so here it is
@bot.command(pass_context=True, hidden=True)
async def greet(ctx):
    """Greets the user"""
    member = ctx.message.author
    server = member.server
    message = "Hello {0.mention}, you're on {1.name}"
    await bot.say(message.format(member, server))
    print("Greeted {0.name}".format(member))

# Ping Pong
# Testing the response of the bot
@bot.command(pass_context=True, hidden=True)
async def ping():
    """Pong"""
    await bot.say("Pong")
    print("Ping Pong")

# Invite link to the bot server
@bot.command()
async def server():
    """The bot's server, for updates or something"""
    await bot.say("https://discord.gg/Eau7uhf")
    print("Run: Server")

# Bot's source code
@bot.command()
async def source():
    """Source code"""
    await bot.say("https://github.com/DiNitride/GAFBot")
    print("Run: Source")

@bot.command()
async def botinfo():
    """Info on the bot"""
    await bot.say("""```xl\nOwner: DiNitride\nGithub: https://github.com/DiNitride/GAFBot\nServer: https://discord.gg/Eau7uhf\n```""")

#############
## Logging ##
#############

# Displays a message when a user joins the server
@bot.event
async def on_member_join(member):
    server = member.server
    if not setting.is_in_data(server):
        await bot.say("Failed to initialise server file")
        return
    with open("config/serversettings.json") as file:
        data = json.load(file)
        if server.id in data:
            if data[server.id]["logging"] is True:
                fmt = '**{0.name}** joined {1.name}'
                channel = discord.Object(data[server.id]["log_channel"])
                await bot.send_message(channel, fmt.format(member, server))
                print(fmt.format(member, server))
            if data[server.id]["role_on_join"] is True:
                role = discord.Object(data[server.id]["join_role"])
                await bot.add_roles(member, role)

# Displays a message when a user leaves the server
@bot.event
async def on_member_remove(member):
    server = member.server
    if not setting.is_in_data(server):
        await bot.say("Failed to initialise server file")
        return
    with open("config/serversettings.json") as file:
        data = json.load(file)
        if data[server.id]["logging"] is True:
            fmt = '**{0.name}** left {1.name}'
            channel = discord.Object(data[server.id]["log_channel"])
            await bot.send_message(channel, fmt.format(member, server))
            print(fmt.format(member, server))
        else:
            return

# Displays a message when a user is banned
@bot.event
async def on_member_ban(member):
    server = member.server
    if not setting.is_in_data(server):
        await bot.say("Failed to initialise server file")
        return
    with open("config/serversettings.json") as file:
        data = json.load(file)
        if data[server.id]["logging"] is True:
            fmt = '**{0.name}** was banned from {1.name}'
            channel = discord.Object(data[server.id]["log_channel"])
            await bot.send_message(channel, fmt.format(member, server))
            print(fmt.format(member, server))

# Displays a message when a user is unbanned
@bot.event
async def on_member_unban(member):
    server = member.server
    if not setting.is_in_data(server):
        await bot.say("Failed to initialise server file")
        return
    with open("config/serversettings.json") as file:
        data = json.load(file)
        if data[server.id]["logging"] is True:
            fmt = '**{0.name}** was unbanned from {1.name}'
            channel = discord.Object(data[server.id]["log_channel"])
            await bot.send_message(channel, fmt.format(member, server))
            print(fmt.format(member, server))


##############################
## FANCY TOKEN LOGIN STUFFS ##
##############################

with open("config/token.txt") as token:
    bot.run(token.read())
token.close()