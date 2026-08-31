
import os

import discord
from dotenv import load_dotenv

import re
from random import randint
from datetime import datetime
import zoneinfo

import api_cnt
import chr_import
from sec import bin
from gr import gr

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
    #currentWorkLoop = asyncio.get_event_loop() #no need now
    
    if message.author == client.user:
        return
    if message.author.bot:
        return
    
    if message.content.startswith('.'):
        if message.content.startswith('.help'):
            from helpmsg import help
            await message.channel.send(embeds=help)
            return
        if message.content.startswith('.gr'):
            #.gr 70 5,6,4,3,1,2 A
            contents = message.content.split(' ')
            contents.pop(0)
            count = int(contents[0])
            if count < 1 or count >= 1000:
                await message.channel.send('成長數值超過範圍。')
                return
            pr = contents[1].split(',')
            prior = [int(i) for i in pr]
            is_in_range = all(1 <= x <= 6 for x in prior)
            if len(prior) != 6:
                await message.channel.send('順序指定缺少/超過')
                return
            if len(prior) != len(set(prior)):
                await message.channel.send('順序存在重複')
                return
            if not is_in_range:
                await message.channel.send('順序數字超過範圍')
                return
            try:
                if contents[2] not in ['A','B','C']:
                    tp = None
                else:
                    tp = contents[2]
            except:
                tp = None

            await message.channel.send(gr(count,prior,tp))
            return


        if message.content.startswith('.import'):
            contents = message.content.split(' ', 1)
            if len(contents) < 2:
                await message.channel.send("Please provide a URL to import.")
                return
            url = contents[1]
            try:
                rp = await chr_import.import_chr(url)
                
            except Exception as e:
                print(f"Error occurred while importing character: {e}")
                rp = "Character import failed."
            await message.channel.send(rp)
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
    match_nd = re.match(pattern_normal_d, message.content, re.IGNORECASE)
    match_md = re.match(pattern_multiply_d, message.content, re.IGNORECASE)
    match_sw = re.match(pattern_multiply_s, message.content, re.IGNORECASE)
    if match_nd or match_md or match_sw:
        rp = await api_cnt.roll_dice_async('sw', message.content)
        if rp:
            await message.channel.send(rp)
        return
    
    if message.content.startswith('d66') or message.content.startswith('D66'):
        rt = str(randint(1,6)) + str(randint(1,6))
        await message.channel.send(rt)
        return
    
@client.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.author.bot:
        return
    if not before.guild:
        return
    if before.guild.id not in bin.monitor_guild.keys():
        return
    if before.content == after.content:
        return
    zone = zoneinfo.ZoneInfo("Asia/Taipei")
    now = datetime.now(zone)
    log_ch = client.get_channel(bin.monitor_guild[before.guild.id])

    rt = f"[{now}] Edited Message from [ {before.author.name} ( {before.author.nick} ) ] [{after.jump_url}]\n\
Before: Created at {before.created_at.astimezone(zone)}\n```{before.content}```\
After: Edit at {after.edited_at.astimezone(zone)}\n```{after.content}```\
---------------------------------------------------"
    #print(rt)
    await log_ch.send(rt)

@client.event
async def on_message_delete(message: discord.Message):
    if message.author.bot:
        return
    if not message.guild:
        return
    if message.guild.id not in bin.monitor_guild.keys():
        return
    zone = zoneinfo.ZoneInfo("Asia/Taipei")
    now = datetime.now(zone)
    log_ch = client.get_channel(bin.monitor_guild[message.guild.id])
    
    rt = f"[{now}] Delete Message from [ {message.author.name} ( {message.author.nick} ) ] [{message.jump_url}]\n\
Content: Created at {message.created_at.astimezone(zone)}\n```{message.content}```\
---------------------------------------------------"
    #print(rt)
    await log_ch.send(rt)


client.run(token)
    



        


        
        

