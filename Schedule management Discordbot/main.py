import discord
from discord.ext import commands

from Commands.CallCommand import Call
from Commands.MeetingCommand import Meeting

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

client.run('TOKEN')