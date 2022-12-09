import discord
from discord.ext import commands
import os
import requests
from bs4 import BeautifulSoup
import json
import asyncio


with open('deta.json', 'r', encoding='utf8') as jfile:
    jf = json.load(jfile)

intent_used = discord.Intents.all()

prefixes = ['^', '.', '/']

bot = commands.Bot(command_prefix=prefixes, intents=intent_used)

@bot.event
async def on_ready():
    print(f'{bot.user} is running')

@bot.event   
async def on_message(message):
    if message.author == bot.user:
        return
    else:
        if message.content.lower() == 'test':
            await message.channel.send('bot.event check')
        if message.content.lower() == '.ptt':
            await message.channel.send('ptt網址:\nhttps://www.ptt.cc/bbs/index.html\n完整的命令\n.ptt [看版名稱(英文)] [頁數(找最新的一頁輸入數字以外的東西)]')
    await bot.process_commands(message)

@bot.command()
async def test(ctx):
    await ctx.send("cmd check")

def ptt_reptile(text, page_num):
  
    result=''
    url = 'https://www.ptt.cc/'
    try:
        int(page_num)
        web = requests.get(f'https://www.ptt.cc/bbs/{jf[text]}/index{page_num}.html', cookies={'over18': '1'})
    except:
        web = requests.get(f'https://www.ptt.cc/bbs/{jf[text]}/index.html', cookies={'over18': '1'})

    soup = BeautifulSoup(web.text, 'html5lib')
    titles = soup.find_all('div', class_='title')

    for i in titles:
        if i.find('a') != None:
            result+=(i.find('a').get_text())
            result+='\n'
            result+=str(url+i.find('a')['href'])
            result+='\n\n'
    return result

 
@bot.command()
async def ptt(ctx, text, page_num):
    await ctx.send(ptt_reptile(text.lower(), page_num))
    


async def main():
    #keep_alive.keep_alive()
    
    try:
        await bot.start(os.environ['Token'])
    except:
        await os.system("kill 1")
asyncio.run(main())