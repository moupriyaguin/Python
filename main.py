import discord
from discord import app_commands
from util import(
    getResponse,
    initializeConversation,
)
import functools
import typing
import asyncio
GUILD_ID = 1097080051406737468
MY_GUILD = discord.Object(id=1097080051406737468)
AI_LOADED = False
BOT_TOKEN = "MTA5NzA3ODczNzY3MTAzMjg3Mw.G4b8yj.tFIFmobQuOVkPlOQhKp6G_18Jc9rveC_r0QQCw"
class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)
# We need to use asyncio.to_thread to run the functions in a separate thread
def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper

# Get response from the AI
@to_thread
def get_ai(promt):
    resp = getResponse(promt)
    return resp

# Initialize/Reload the conversation
@to_thread
def start_ai():
    global AI_LOADED
    initializeConversation()
    AI_LOADED = True
    return
# Used to send a prompt to the AI
@client.tree.command()
@app_commands.guild_only()
@app_commands.describe(prompt="The prompt you want to send to the AI")
async def prompt(interaction: discord.Interaction, prompt: str):
    """Sends a prompt to the AI."""
    await interaction.response.defer()
    if not AI_LOADED:
        embed = discord.Embed(
            color=discord.colour.Color.dark_orange(), title="AI Not Loaded"
        )
        embed.description = "Ask the bot owner to reload the AI"
        return await interaction.followup.send(embed=embed)

    resp = await get_ai(prompt)
    # if len(resp) > 1024:
    embed = discord.Embed(color=discord.colour.Color.teal(), title=prompt)

    embed.description = resp
    embed.set_author(
        name=interaction.user.display_name,
        icon_url=interaction.user.display_avatar.url,
    )
    embed.timestamp = interaction.created_at

    return await interaction.followup.send(embed=embed)


# admin only
# reloads the AI
@client.tree.command()
@app_commands.default_permissions()
@app_commands.guild_only()
async def start(interaction: discord.Interaction):
    """Reloads/Starts the AI"""
    await interaction.response.defer()
    await start_ai()
    embed = discord.Embed(color=discord.colour.Color.yellow(), title="AI Reloaded")
    embed.description = "To use the AI, use the `/prompt` command"
    return await interaction.followup.send(embed=embed)


# help command
# lists all the commands
@client.tree.command()
@app_commands.guild_only()
async def help(interaction: discord.Interaction):
    """Lists all the commands"""
    embed = discord.Embed(
        color=discord.colour.Color.blurple(),
        title="Help",
        description="Here are the commands you can use",
    )

    embed.add_field(name="`/hello`", value="Says hello!", inline=False)
    embed.add_field(name="`/ping`", value="Simple Ping Pong!", inline=False)
    embed.add_field(name="`/prompt`", value="Sends a prompt to the AI.", inline=False)
    embed.add_field(name="`/reload`", value="Reloads/Starts the AI", inline=False)
    embed.add_field(name="`/help`", value="Shows this message", inline=False)
    embed.add_field(
        name="`/invite`", value="Sends the invite link for the bot", inline=False
    )
    embed.add_field(name="`/shutdown`", value="Shuts down the AI", inline=False)

    await interaction.response.send_message(embed=embed)


# invite link
# sends the invite link for the bot
@client.tree.command()
# @app_commands.guild_only()
async def invite(interaction: discord.Interaction):
    """Sends the invite link for the bot"""
    embed = discord.Embed(
        color=discord.colour.Color.blurple(),
        title="Invite 🔗",
        description="Here is the invite link for the bot 😊",
    )
    embed.url = "https://discord.com/api/oauth2/authorize?client_id=930499355918602250&permissions=8&scope=bot%20applications.commands"
    await interaction.response.send_message(embed=embed)


# shutdown command
# shuts down the AI
# admin only
@client.tree.command()
@app_commands.guild_only()
@app_commands.default_permissions()
async def shutdown(interaction: discord.Interaction):
    """Shuts down the AI"""
    global AI_LOADED
    AI_LOADED = False
    embed = discord.Embed(color=discord.colour.Color.red(), title="AI Shut Down")
    embed.description = "Start the AI again using `/reload`"
    await interaction.response.send_message(embed=embed)
    # await client.close()


# This is a special event that is called when an interaction is received/created it is not handled by a command.
@client.event
async def on_interaction(interaction: discord.Interaction):
    # This is a special event that is called when an interaction is received
    # that is not handled by a command. This is useful for things like slash
    # commands that are not registered in the tree.
    if (
        interaction.type is discord.InteractionType.application_command
        and not interaction.command
    ):
        await interaction.response.send_message("Unknown command.", ephemeral=True)


if __name__ == "__main__":
    client.run("MTA5NzA3ODczNzY3MTAzMjg3Mw.G4b8yj.tFIFmobQuOVkPlOQhKp6G_18Jc9rveC_r0QQCw")