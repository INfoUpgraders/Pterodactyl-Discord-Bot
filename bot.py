import asyncio
import json
import os
import random
import sys
import time
import traceback
import typing
from datetime import datetime, date, time, timezone

import discord
import pymongo
from discord.ext import commands
from pydactyl import PterodactylClient

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
        scEmbed = discord.Embed(description="Successfully Cancelled!",
        colour=0x6a8dd3, timestamp=ctx.message.created_at)

        toEmbed = discord.Embed(description="Cancelled.",
        colour=0x6a8dd3, timestamp=ctx.message.created_at)

        sEmbed = discord.Embed(description="Creating Server!",
        colour=0x6a8dd3, timestamp=ctx.message.created_at)

        def check(m):
            return m.author == ctx.message.author and m.channel == ctx.channel
        try:
            #f95439
            await ctx.send("Server Name?")
            q1 = await bot.wait_for('message', timeout=300.0, check=check)
            if "cancel" in q1.content.lower():
                return await ctx.send(embed=scEmbed)
            await ctx.send(f"Panel User ID?")
            q2 = await bot.wait_for('message', timeout=300.0, check=check)
            if "cancel" in q2.content.lower():
                return await ctx.send(embed=scEmbed)
            await ctx.send(f"Nest ID?")
            q3 = await bot.wait_for('message', timeout=300.0, check=check)
            if "cancel" in q3.content.lower():
                return await ctx.send(embed=scEmbed)
            await ctx.send(f"Egg ID?")
            q4 = await bot.wait_for('message', timeout=300.0, check=check)
            if "cancel" in q4.content.lower():
                return await ctx.send(embed=scEmbed)
            await ctx.send(f"Memory Limit?")
            q5 = await bot.wait_for('message', timeout=300.0, check=check)
            if "cancel" in q5.content.lower():
                return await ctx.send(embed=scEmbed)
            await ctx.send("Disk Limit?")
            q6 = await bot.wait_for('message', timeout=300.0, check=check)
            if "cancel" in q6.content.lower():
                return await ctx.send(embed=scEmbed)
            await ctx.send("CPU Limit?")
            q7 = await bot.wait_for('message', timeout=300.0, check=check)
            if "cancel" in q7.content.lower():
                return await ctx.send(embed=scEmbed)

            mEmbed = discord.Embed(description="Is this correct?",
            colour=0x6a8dd3, timestamp=ctx.message.created_at)
            mEmbed.add_field(name="Server Name", value=f"{str(q1.content)}", inline=True)
            mEmbed.add_field(name="Panel User ID", value=f"#{str(q2.content)}", inline=True)
            mEmbed.add_field(name="Nest ID", value=f"#{str(q3.content)}", inline=True)
            mEmbed.add_field(name="Egg ID", value=f"#{str(q4.content)}", inline=True)
            mEmbed.add_field(name="Memory Limit", value=f"{str(q5.content)}MB", inline=True)
            mEmbed.add_field(name="Disk Limit", value=f"{str(q6.content)}MB", inline=True)
            mEmbed.add_field(name="CPU Limit", value=f"{str(q7.content)}%", inline=True)
            mEmbed.add_field(name="Swap Limit", value="0%", inline=True)
            mEmbed.add_field(name="Location", value="1", inline=True)
            await ctx.send(embed=mEmbed)

            q8 = await bot.wait_for('message', timeout=300.0, check=check)
            if "cancel" in q8.content.lower():
                return await ctx.send(embed=scEmbed)
            elif "yes" in q8.content.lower():
                client.servers.create_server(name=str(q1.content), user_id=int(q2.content), nest_id=int(q3.content),
                egg_id=int(q4.content), memory_limit=int(q5.content), cpu_limit=int(q7.content), swap_limit=0,
                disk_limit=int(q6.content), location_ids=[1])
                await ctx.send(embed=sEmbed)
            elif "no" in q8.content.lower():
                return await ctx.send(embed=scEmbed)
            else:
                embed = discord.Embed(description="An error occured.",
                colour=0xf95439, timestamp=ctx.message.created_at)
                return await ctx.send(embed=embed)

        except asyncio.TimeoutError:
            embed = discord.Embed(description="You ran out of time!",
            colour=0xf95439, timestamp=ctx.message.created_at)
            return await ctx.send(embed=embed)

        except:
            embed = discord.Embed(description="An error occured.",
            colour=0xf95439, timestamp=ctx.message.created_at)
            return await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description="An error occured.",
            colour=0xf95439, timestamp=ctx.message.created_at)
            return await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description="What are you creating? ``Example: ?create server``",
        colour=0x6a8dd3, timestamp=ctx.message.created_at)
        return await ctx.send(embed=embed)

# GET PANEL USER
@bot.command()
async def getuser(ctx, *, arg1 = None):
    user = client.user.list_users(search=str(arg1))
    try:
        user_id = user['data'][0]['attributes']['id']
        username = user['data'][0]['attributes']['username']
        first_name = user['data'][0]['attributes']['first_name']
        last_name = user['data'][0]['attributes']['last_name']
        email = user['data'][0]['attributes']['email']
        language = user['data'][0]['attributes']['language']
        admin = user['data'][0]['attributes']['root_admin']
        twofa = user['data'][0]['attributes']['2fa']
        created_at = user['data'][0]['attributes']['created_at']
        dt = str(created_at)
        t = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S%z")
        pt = datetime.strftime(t, "%B %d, %Y %I:%M%p")

        embed = discord.Embed(description="User Info",
        colour=0x6a8dd3, timestamp=ctx.message.created_at)
        embed.add_field(name="User ID", value=user_id, inline=True)
        embed.add_field(name="Username", value=username, inline=True)
        embed.add_field(name="Email", value=email, inline=True)
        embed.add_field(name="First Name", value=first_name, inline=True)
        embed.add_field(name="Last Name", value=last_name, inline=True)
        embed.add_field(name="Admin Access", value=admin, inline=True)
        embed.add_field(name="2FA", value=twofa, inline=True)
        embed.add_field(name="Language", value=language, inline=True)
        embed.add_field(name="Created At", value=pt, inline=True)
        await ctx.send(embed=embed)
    except IndexError:
        embed = discord.Embed(description="User Not Found!",
        colour=0xf95439, timestamp=ctx.message.created_at)
        await ctx.send(embed=embed)

# LINK PANEL USERS
@bot.command()
@commands.has_permissions(manage_roles=True)
async def link(ctx, arg:int=0, *, member: discord.Member):
    openf = json.loads(open('linked.json').read())
    openf[str(member.id)] = {'user_id': str(member.id), 'panel_id': int(arg)}
    with open("linked.json", 'w') as f:
        json.dump(openf, f, indent=4)
        embed = discord.Embed(description=f"Succesfully linked: ``{member}`` with Panel ID: ``{int(arg)}``",
        colour=0x6a8dd3, timestamp=ctx.message.created_at)
        await ctx.send(embed=embed)


bot.run('BOT_TOKEN', reconnect=True, bot=True)
