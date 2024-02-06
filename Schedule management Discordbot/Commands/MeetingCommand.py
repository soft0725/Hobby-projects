import discord
import re
from discord.ext import commands

from DataBase.upload_database import upload

class Meeting(commands.Cog):
    def __init__(self, client):
        self.client = client

    def show_meeting_list_user(self): # 모든 스케줄 목록 
        pass

    def show_meeting_list_all(self): # 특정 유저의 스케줄 목록 
        pass

    def upload_database(self, match, userid): # 데이터베이스 스케줄 업로드 
        upload(match, userid)

    def delete_database(self): # 데이터베이스 스케쥴 삭제
        pass

    @commands.Cog.listener()  
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        else:
            """ 오늘, 내일, 년도를 사용할 수 있도록 정규표현식 사용 """
            pattern = r'(오늘|내일|\d{4}년 \d{1,2}월 \d{1,2}일)\s*(오전|오후)?\s*(\d{1,2})시\s*(\d{1,2})분\s*(.+)?'
            match = re.match(pattern, message.content)
            if match: # 임베드 생성 
                embed = discord.Embed(title="회의 정보", color=discord.Color.blue())
                embed.add_field(name="회의 이름", value=match.group(5) if match.group(5) else "없음", inline=False)
                embed.add_field(name="날짜", value=match.group(1), inline=False)
                embed.add_field(name="오전/오후", value=match.group(2))
                embed.add_field(name="시간", value=match.group(3))
                embed.add_field(name="분", value=match.group(4))
                embed.add_field(name="등록한 사람", value=message.author.display_name)
                await message.channel.send(embed=embed)

                self.upload_database(match, message.author.id) # match 결과와 사용자 고유 ID를 넘겨줌

def setup(client):
    client.add_cog(Meeting(client))
