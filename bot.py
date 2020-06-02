import asyncio
import json
import os
import random
import sys
import time
import traceback
import typing
from datetime import datetime

import discord
import pymongo
from discord.ext import commands
from pydactyl import PterodactylClient
from pymongo import MongoClient

bot = commands.Bot(command_prefix = ',', case_insensitve=True)
bot.launch_time = datetime.utcnow()

client = PterodactylClient('PANEL_LINK', 'SECRET_APPLICATION_API')

# ONLINE + STATUS EVENT
@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    activity = discord.Activity(name='CUSTOM_STATUS', type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)
    print(f'Successfully logged in and booted...!')
    
# UPTIME COMMAND
@bot.command()
async def uptime(ctx):
    delta_uptime = datetime.utcnow() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    await ctx.send(f"{days}d, {hours}h, {minutes}m, {seconds}s")

# PING LATENCY
@bot.command()
async def ping(ctx):
    start = time.perf_counter()
    message = await ctx.send("Ping...")
    end = time.perf_counter()
    duration = (end - start) * 1000
    await message.edit(content='Pong! {:.2f}ms'.format(duration))
    
# CREATE PANEL SERVER    
@bot.command()
@commands.has_permissions(manage_messages=True)
async def create(ctx, *, arg1 = None):
    if arg1 == "server":
        def check(m):
            return m.author == ctx.message.author
        try:
            await ctx.send('Server Name?')
            q1 = await bot.wait_for('message', timeout=120.0, check=check)
            await ctx.send(f"Panel User ID?")
            q2 = await bot.wait_for('message', timeout=120.0, check=check)
            await ctx.send(f"Nest ID?")
            q3 = await bot.wait_for('message', timeout=120.0, check=check)
            await ctx.send(f"Egg ID?")
            q4 = await bot.wait_for('message', timeout=120.0, check=check)
            await ctx.send(f"Memory Limit?")
            q5 = await bot.wait_for('message', timeout=120.0, check=check)
            await ctx.send("Disk Limit?")
            q6 = await bot.wait_for('message', timeout=120.0, check=check)
            await ctx.send("CPU Limit?")
            q7 = await bot.wait_for('message', timeout=120.0, check=check)
        
            client.servers.create_server(name=str(q1.content), user_id=int(q2.content), nest_id=int(q3.content), 
                                        egg_id=int(q4.content), memory_limit=int(q5.content), cpu_limit=int(q7.content), swap_limit=0, 
                                        disk_limit=int(q6.content), location_ids=[1])
    
            await ctx.send("Server installing... [Please wait: 5 minutes]")
    
        except asyncio.TimeoutError:
            await ctx.send("You ran out of time!")
        else:
            return
    else:
        await ctx.send("What are you creating? ``Example: ?create server``")

# GET PANEL USER        
@bot.command()
async def getuser(ctx, *, arg1 = None):
    user = client.user.list_users(search=str(arg1))
    if user['data'][0]['attributes']['id'] is None:
        await ctx.send(user)
    else:
        user_id = user['data'][0]['attributes']['id']
        username = user['data'][0]['attributes']['username']
        first_name = user['data'][0]['attributes']['first_name']
        last_name = user['data'][0]['attributes']['last_name']
        language = user['data'][0]['attributes']['language']
        admin = user['data'][0]['attributes']['root_admin']
        twofa = user['data'][0]['attributes']['2fa']
        created_at = user['data'][0]['attributes']['created_at']
        await ctx.send(f"```User ID: {user_id}\nUsername: {username}\nFirst Name: {first_name}\nLast Name: {last_name}\nPanel Language: {language}\nAdmin Access: {admin}\n2FA: {twofa}\nCreated at: {created_at}```")

# LINK PANEL USERS
@bot.command()
@commands.has_permissions(manage_roles=True)
async def link(ctx, arg:int=0, *, member: discord.Member):
    openf = json.loads(open('linked.json').read())
    openf[str(member.id)] = {'user_id': str(member.id), 'panel_id': int(arg)}
    with open("linked.json", 'w') as f:
        json.dump(openf, f, indent=4)
        await ctx.send(f"Succesfully linked: ``{member}`` with Panel ID: ``{int(arg)}``")
        

bot.run('BOT_TOKEN', reconnect=True, bot=True)
