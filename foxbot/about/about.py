import discord
import  time
import datetime 
from discord import app_commands
from discord.ext import commands
import platform
from discord.app_commands import Choice
import utillities
from utillities import load_json as jsonloader
up_time = time.time()

class about(commands.Cog):
    """Learn about the people who work on this bot and other information"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="devinfo")
    @app_commands.choices(dev=[
        Choice(name="Little Fox", value="littlefox")
    ])
    @utillities.check_blacklist()
    @app_commands.describe(dev = "The developer you want to know more of.")
    async def dev_info(self, interaction : discord.Interaction, dev:str):
        embed = discord.Embed(title=f"About {dev}", color = discord.Color.dark_gold())
        fileread = jsonloader(f"./jsonfiles/{dev}.json")
        if dev == "littlefox":
            user = await self.bot.fetch_user(521028748829786134)
            embed.set_thumbnail(url = user.avatar.url)
            embed.add_field(name="Name:", value=fileread["name"], inline=False)
            embed.add_field(name="Age:", value=fileread["age"], inline=False)
            embed.add_field(name="Function:", value=fileread["function"],inline=False)
            embed.add_field(name="About:", value=fileread["about"], inline=False)
            embed.add_field(name="Skills:", value=fileread["skills"], inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            return await interaction.response.send_message("Sorry that developer does not have a about page yet.", ephemeral=True)

    @app_commands.command(name="test")
    @utillities.check_blacklist()
    async def testcommand(self, interaction : discord.Interaction):
        await interaction.response.send_message("Hi!")

    @app_commands.command(name="botinfo", description="All bot information in one clean view.")
    @utillities.check_blacklist()
    async def botinfo(self, interaction : discord.Interaction):
        discord_version = str(discord.__version__)
        python_version = str(platform.python_version())
        python_build = str(platform.python_build())
        guilds = len(self.bot.guilds)
        current_time = time.time()
        difference = int(round(current_time - up_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(title="Bot information", color = discord.Color.red())
        embed.add_field(name="Bot Version:", value=utillities.bot_version)
        embed.add_field(name="Library version:", value=discord_version, )
        embed.add_field(name="Python version:", value=python_version, )
        embed.add_field(name="Python build:", value=python_build, )
        embed.add_field(name="Total guilds", value=guilds)
        embed.add_field(name="Latency Bot > Discord", value='Pong! `{0} ms `'.format(round(self.bot.latency * 1000)))
        embed.add_field(name="Uptime", value=text, inline=False)
        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="av", description="Get an user's avatar")
    async def av(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        await interaction.response.send_message(member.avatar.url, ephemeral=False)

    @app_commands.command(name="whois", description="Get user information")
    async def whois(self, interaction: discord.Interaction, user: discord.Member = None):
        """Check to see who this person is, their roles and other stuff. format: whois @user"""
        if user is None:
            user = interaction.user
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(color=discord.Color.orange(),
                              description=user.mention)
        embed.set_author(name=str(user), icon_url=user.avatar.url)
        embed.set_thumbnail(url=user.avatar.url)
        embed.add_field(
            name="Joined", value=user.joined_at.strftime(date_format))
        members = sorted(interaction.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position",
                        value=str(members.index(user) + 1))
        embed.add_field(name="Registered",
                        value=user.created_at.strftime(date_format))

        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name="Roles [{}]".format(
                len(user.roles) - 1), value=role_string, inline=False)
            embed.set_footer(text='ID: ' + str(user.id))
            return await interaction.response.send_message(embed=embed)
        else:
            embed.add_field(name="Roles:", value="None")
        return await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(about(bot))