import discord
from discord.ext import commands
import pymysql

from Commands.CallCommand import Call
from Commands.MeetingCommand import Meeting
from Private.mydb import return_db_info
from Private.token import return_token

mydb = return_db_info()
TOKEN = return_token()

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents) # prefix=!로 설정

@client.event
async def on_ready():
    """ 봇은 자리비움, 노래 듣는 중으로 설정 """
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="노래"), status=discord.Status.dnd)
    await client.add_cog(Call(client)) # 사람들 부르는 클래스 
    await client.add_cog(Meeting(client)) # 미팅 클래스
    print(f"BotName: {client.user.name}")

@client.event
async def on_shutdown():
    if mydb.open:
        mydb.close()
        print('database shutdown')

client.run(TOKEN)