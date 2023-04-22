from argparse import ArgumentParser
from typing import Optional
import discord
from discord.ext import commands
from discord.ext.commands import Context, Greedy
from discord import app_commands
import assets
import utillities

intents = discord.Intents.default()
intents.message_content = True
# Normal server 981259218122338354  |||||| Dev server 1038431009676460082
MY_GUILD = discord.Object(id=1038431009676460082)
reader = utillities.load_json(assets.jsonfiles)
appID = reader["appid"]


class FoxGuard(commands.Bot):
    def __init__(self, intents=intents):
        super().__init__(intents=intents, command_prefix=commands.when_mentioned,
                         application_id=appID, description="Adding more projects on our website.")

    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=MY_GUILD)

    async def on_ready(self):
        """On ready event."""
        link = utillities.load_json(assets.jsonfiles)
        linkurl = link["inv_uri"]
        print(f"[INFO]  {self.user} has connected to the discord gateaway!")
        for extension in assets.modules:
            await bot.load_extension(extension)
            print(f"[INFO]  Loaded {extension}")
        await bot.change_presence(activity=discord.Game(name="Use /help to get help!"))
        print(f"[INFO]  {linkurl}\n")
        print("[INFO]    Loaded all slash commands\n")


bot = FoxGuard(intents=intents)
bot.remove_command("help")
tree = bot.tree
"""
*sync -> global sync
*sync guild -> sync current guild
*sync copy -> copies all global app commands to current guild and syncs
*sync delete -> clears all commands from the current guild target and syncs (removes guild commands)
*sync id_1 id_2 -> sync  guilds with 1 and 2
"""


@bot.command(name="synccmd")
@utillities.is_bot_admin()
async def sync(
        ctx: Context, guilds: Greedy[discord.Object], spec: Optional[str] = None) -> None:
    if not guilds:
        if spec == "guild":
            synced = await ctx.bot.tree.sync()
        elif spec == "copy":
            ctx.bot.tree.copy_global_to(guild=MY_GUILD)
            synced = await ctx.bot.tree.sync()
        elif spec == "delete":
            ctx.bot.tree.clear_commands()
            await ctx.bot.tree.sync()
            synced = []
        else:
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        print(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return
    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1
    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

@bot.command()
async def help(ctx):
    await ctx.reply("You can find all commands at https://little-fox.info/foxguard/documentation ")

json = utillities.load_json(assets.jsonfiles)
token = json["token"]

def run():
    bot.run(token)


@tree.error
async def on_app_command_error(interaction : discord.Interaction, error: discord.app_commands.errors.AppCommandError):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        if str(interaction.command.checks.copy()).__contains__("check_blacklist"):
            await interaction.response.send_message("You are blacklisted. Please read our terms of service to appeal. <https://little-fox.info/general-bot-terms-of-service>", ephemeral=True)
    else:
        print(error)
if __name__ == "__main__":
    run()