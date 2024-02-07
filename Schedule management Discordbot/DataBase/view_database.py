import discord
import pymysql 

from Private.mydb import return_db_info

mydb = return_db_info()

async def select_all(message):
    try:
        with mydb.cursor() as cursor:
            sql_query = "select * from schedule order by schedule_datetime asc"
            cursor.execute(sql_query)
            result = cursor.fetchall()
            
            embed = discord.Embed(title="등록된 회의 리스트 (최대 10개까지 빠른 날짜)", color=discord.Color.blue())

            for row in result[:10]:
                member = await message.guild.fetch_member(row[-3]) # 고유 ID를 이름으로 변환 
                if member:
                    username = member.display_name  # 사용자의 이름
                else:
                    username = "알 수 없음"

                embed.add_field(name="회의 이름", value=row[-1] if row[-1] else "없음")
                embed.add_field(name="날짜", value=row[-2])
                embed.add_field(name="등록한 사람", value=username)

            await message.channel.send(embed=embed)
            print("select_all() 함수를 실행하여 전체 일정을 조회함")


    except Exception as e:
        print("Error:", e)

async def select_user(message):
    try:
        with mydb.cursor() as cursor:
            sql_query = f"select * from schedule where userid = {message.author.id} order by schedule_datetime asc"
            cursor.execute(sql_query)
            result = cursor.fetchall()
            
            embed = discord.Embed(title="등록된 회의 리스트 (최대 10개까지 빠른 날짜)", color=discord.Color.blue())

            for row in result[:10]:
                member = await message.guild.fetch_member(row[-3]) # 고유 ID를 이름으로 변환 
                if member:
                    username = member.display_name  # 사용자의 이름
                else:
                    username = "알 수 없음"

                embed.add_field(name="회의 이름", value=row[-1] if row[-1] else "없음")
                embed.add_field(name="날짜", value=row[-2])
                embed.add_field(name="등록한 사람", value=username)

            await message.channel.send(embed=embed)
            print(f"select_user() 함수를 실행하여 특정 유저의 일정을 조회함. 조회한 사람: {username}")

    except Exception as e:
        print("Error:", e)