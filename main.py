import discord
from discord.ext import commands
import os
import requests
from bs4 import BeautifulSoup
import json
import asyncio


with open('deta.json', 'r', encoding='utf8') as jfile:    
    jf = json.load(jfile)
#開啟json檔案(用於存放資料的地方)

intent_used = discord.Intents.all()
#給機器人權限
prefixes = ['^', '.', '/']
#使用指令之前要加的前綴符號
bot = commands.Bot(command_prefix=prefixes, intents=intent_used)
#設定機器人

@bot.event
async def on_ready():
    print(f'{bot.user} is running')
#機器人上線通知

@bot.event   
async def on_message(message):#對話事件
    if message.author == bot.user:
        return
    else:
        if message.content.lower() == 'test':
            await message.channel.send('bot.event check')
        if message.content.lower() == '.ptt':
            await message.channel.send('ptt網址:\nhttps://www.ptt.cc/bbs/index.html\n完整的命令\n.ptt [看版名稱(英文)] [頁數(找最新的一頁輸入數字以外的東西)]')
    await bot.process_commands(message)#啟用指令command這個功能


@bot.command()#測試用指令
async def test(ctx):
    await ctx.send("cmd check")

def ptt_spider(text, page_num):#ptt爬蟲副函式
  
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

 
@bot.command()#ptt爬蟲的指令
async def ptt(ctx, text, page_num):
    await ctx.send(ptt_spider(text.lower(), page_num))
    


async def main():#迴圈
    
    try:
        await bot.start(os.environ['Token'])#執行機器人
    except:
        await os.system("kill 1")#如果無法執行就換一個執行器

asyncio.run(main())#執行main迴圈