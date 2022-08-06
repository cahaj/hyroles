import discord
import pycord
from discord import CategoryChannel
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from aiohttp import request
import json
from jsondiff import diff
import requests
import asyncio
from pprint import pprint
from collections import Counter
import threading
import datetime
#setup
file = open('vars.json', 'r', encoding='unicode_escape')
json_object = json.load(file)
file.close()
token = json_object["token"]

bot = commands.Bot(command_prefix = 'hr!')
bot.remove_command('help')
slash = SlashCommand(bot, sync_commands=True)

url = "https://api.hypixel.net"

@bot.event
async def on_ready():
    print('Bot online.')
    servers = str(len(bot.guilds))
    print(f"In: {servers} servers.")
    await bot.change_presence(activity=discord. Activity(type=discord.ActivityType.watching, name=f'data for {servers} servers'))

@slash.slash(
    name="setup",
    description="[ADMIN] setup command",
    options=[
        create_option(name="apikey",description="Hypixel api key",required=True, option_type=3),
    ]
)
async def _setup(ctx: SlashContext, apikey: str):
    if ctx.author.guild_permissions.administrator:
        HYPIXELKEY = apikey
        headers = {
        "API-KEY": f"{HYPIXELKEY}",
        "Content-Type": "application/json"}
        r = requests.get(url=f"{url}/key", headers = headers)
        data = r.json()
        if data["success"]:
            embed = discord.Embed(title=f'SETUP - {ctx.author}',timestamp=datetime.datetime.utcnow())

            file = open('keys.json', 'r',encoding='unicode_escape')
            json_object = json.load(file)
            file.close()
            guild_id = f"{ctx.guild.id}"
            if guild_id not in json_object:
                print(f"New user - {str(ctx.guild.id)}")
                json_object[guild_id] = []
                print(json_object)
                json_object[guild_id].append(apikey)
                file = open('keys.json', 'w',encoding='utf-8')
                json.dump(json_object, file, indent=2)
                file.close()
                embed.add_field(name="APIKEY", value="added new")
                embed.set_footer(text='\u200b',icon_url='https://cdn.discordapp.com/attachments/834726051485057084/1005426772545900594/hyroles512.png')
                await ctx.send(embed=embed)
            elif guild_id in json_object:
                print(f"Login change - {str(ctx.guild.id)}")
                json_object[guild_id] = []
                print(json_object)
                json_object[guild_id].append(apikey)
                file = open('keys.json', 'w',encoding='utf-8')
                json.dump(json_object, file, indent=2)
                file.close()
                embed.add_field(name="APIKEY", value="changed")
                embed.set_footer(text='\u200b',icon_url='https://cdn.discordapp.com/attachments/834726051485057084/1005426772545900594/hyroles512.png')
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f'HYROLES SETUP',timestamp=datetime.datetime.utcnow())
            embed.add_field(name="APIKEY", value=f"{data['cause']}")
            embed.set_footer(text='\u200b',icon_url='https://cdn.discordapp.com/attachments/834726051485057084/1005426772545900594/hyroles512.png')
            await ctx.send(embed=embed)


@bot.command(aliases=['keyinfo'])
async def printapikey(ctx):
    global headers
    try:
        file = open('keys.json', 'r',encoding='unicode_escape')
        json_object = json.load(file)
        file.close()
        guild_id = f"{ctx.guild.id}"
        if guild_id in json_object:
            HYPIXELKEY = json_object[guild_id][0]
            headers = {
            "API-KEY": f"{HYPIXELKEY}",
            "Content-Type": "application/json"}
            r = requests.get(url=f"{url}/key", headers = headers)
            data = r.json()
            embed = discord.Embed(title='Hypixel API key info for this server',timestamp=datetime.datetime.utcnow())
            embed.add_field(name="key owner", value=f"{data['record']['owner']}")
            embed.set_footer(text='\u200b',icon_url='https://cdn.discordapp.com/attachments/834726051485057084/1005426772545900594/hyroles512.png')
            await ctx.send(embed=embed)
        else:
            await ctx.send("Not registered, do /setup")
    except Exception as e:
        embed = discord.Embed(title='EXCEPTION OCCURED',timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Exception", value=f"{e}")
        embed.set_footer(text='\u200b',icon_url='https://cdn.discordapp.com/attachments/834726051485057084/1005426772545900594/hyroles512.png')
        await ctx.send(embed=embed)


#bot run
bot.run(token)