import re
from datetime import datetime as dt
import pandas as pd

def preprocess(chat):
    pattern = "\[\d+/\d+/\d+,\s\d+:\d+:\d+\s[APM]+\]\s"
    messages = re.split(pattern, chat)[1:]
    dates = re.findall(pattern,chat)

    df = pd.DataFrame({'user_message': messages,'date':dates})
    df['date'] = pd.to_datetime(df['date'], format = "[%m/%d/%y, %I:%M:%S %p] ")
    users = []
    messages = []
    for message in df['user_message']:
        text = re.split('([\w\W]+?):\s', message)
        # if text[1:]:
        users.append(text[1])
        messages.append(" ".join(text[2:]))
        # else:
        #     users.append('group_notification')
        #     messages.append(text[0])

    df['user'] = users
    df['message'] = messages

    df['date_'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['weekday'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['weekday','hour']]['hour']:
        if hour == 23:
            period.append(str(hour)+ "-"+str('00'))
        elif hour == 0:
            period.append(str('00')+"-"+str(hour+1))
        else:
            period.append(str(hour)+"-"+str(hour+1))
    df['period'] = period

    df.drop(columns=['user_message', 'date'], inplace=True)
    df = df[1:]
    return df
