import pymysql
import re
from datetime import datetime, timedelta


def get_schedule_datetime(match):
    hour = int(match.group(3))
    minute = int(match.group(4))
    hour += 12 if match.group(2) == '오후' else 0

    if match.group(1) == '오늘':
        schedule_datetime = datetime.now()
    elif match.group(1) == '내일':
        schedule_datetime = datetime.now() + timedelta(days=1)
    else:
        date_match = re.search(r'(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일', match.group(1))
        year, month, day = map(int, date_match.groups())
        schedule_datetime = datetime(year, month, day)

    return schedule_datetime.replace(hour=hour, minute=minute)


def upload(match, userid):
    mydb = pymysql.connect(
        host="localhost",
        user="user",
        password="passwod",
        database="database"
    )
    
    pattern = r'(오늘|내일|\d{4}년 \d{1,2}월 \d{1,2}일)\s*(오전|오후)?\s*(\d{1,2})시\s*(\d{1,2})분\s*(.+)?'
    if match:
        title = match.group(5) if match.group(5) else "없음"
        schedule_datetime = get_schedule_datetime(match)
        schedule_datetime = schedule_datetime.strftime("%Y-%m-%d %H:%M:%S")
        # print(schedule_datetime.strftime("%Y-%m-%d %H:%M:%S"))
        
        mycursor = mydb.cursor()
        insert_query = f"INSERT INTO schedule (userid, schedule_datetime, title) VALUES ({userid}, '{schedule_datetime}', '{title}')"
        mycursor.execute(insert_query)
        mydb.commit()
        mydb.close()
        print('업로드 완료')