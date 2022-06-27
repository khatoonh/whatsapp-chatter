import pandas as pd
import re
def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    message = re.split(pattern, data)[1:]
    ptr = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}'
    date_time = re.findall(ptr, data)
    df = pd.DataFrame({'User_message': message, 'message_date': date_time})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M')
    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []
    for msg in df['User_message']:
        entry = re.split('([\w\W]+?):\s', msg)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['messages'] = messages
    df.drop(columns=['User_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minutes'] = df['date'].dt.minute
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period
    return df