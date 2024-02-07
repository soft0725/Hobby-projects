import pymysql
import re
from datetime import datetime, timedelta

from Private.mydb import return_db_info

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
    mydb = return_db_info()
    
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
        print(f'{userid}가 {title}을 업로드함.')