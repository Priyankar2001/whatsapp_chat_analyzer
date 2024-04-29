import re
import pandas as pd
from datetime import datetime


def preprocess(data):
    d = '\u202f'

    data = data.replace(d, " ")
    data = data.replace("-", "")
    y = data.splitlines()

    # Regular Expression Pattern

    pattern = '\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s*[ap]m\s\s'
    pattern2 = '\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s*[ap]m'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern2, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # To convert the given date and time string "16/09/19, 8:53 am" to a Python datetime object,
    # you can use the datetime module's strptime function

    def change(text):
        date_format = "%d/%m/%y, %I:%M %p"
        return datetime.strptime(text, date_format)

    df['message_date'] = df['message_date'].apply(change)
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # dividing user name and messages:

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages

    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

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
