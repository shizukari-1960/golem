
import os

import discord
from dotenv import load_dotenv

import asyncio
import re

import tools
import api_cnt

os.chdir(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()
token = os.getenv('TOKEN')
client = discord.Client(intents=discord.Intents.all())


@client.event
# 當機器人完成啟動時在終端機顯示提示訊息
async def on_ready():
    print(f'目前登入身份：{client.user}')
    await client.change_presence(activity=discord.CustomActivity(name='.help | Handle by akatsuki_4379'))

@client.event
async def on_message(message: discord.message.Message):
    currentWorkLoop = asyncio.get_event_loop()
    
    if message.author == client.user:
        return
    if message.author.bot:
        return
    
    if message.content.startswith('.'):
        if message.content.startswith('.help'):
            from helpmsg import help
            await message.channel.send(embeds=help)
            return
        ctx = message.content.split(' ',1)
        if len(ctx) > 1:
            sys,cmd = ctx[0].lstrip('.'), ctx[1]
        
        #await message.channel.send(sw.comment_parse(cmd)) abandon
            ct = await api_cnt.roll_dice_async(sys, cmd)
            if ct:
                await message.channel.send(ct)
        return
    pattern_normal_d = r'(\d+)d(\d+)'
    pattern_multiply_d = r'x(\d+)'
    pattern_multiply_s = r'k(\d+)@'
    match_nd = re.search(pattern_normal_d, message.content, re.IGNORECASE)
    match_md = re.search(pattern_multiply_d, message.content, re.IGNORECASE)
    match_sw = re.search(pattern_multiply_s, message.content, re.IGNORECASE)
    if match_nd or match_md or match_sw:
        rp = await api_cnt.roll_dice_async('sw', message.content)
        if rp:
            await message.channel.send(rp)
        return
    
    if message.content.startswith('d66') or message.content.startswith('D66'):
        await message.channel.send(tools.d66())
    
    
    


client.run(token)
    



        


        
        

