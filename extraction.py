import sqlite3
import pandas as pd

# connect to the database
conn = sqlite3.connect('chat.db')
cur = conn.cursor()

# define command
SQL = """
SELECT datetime(message.date/1000000000 + strftime("%s", "2001-01-01"), "unixepoch", "localtime") AS date_uct, id, text, is_from_me
FROM message
LEFT JOIN handle
ON message.handle_id = handle.ROWID
WHERE id='+16176826385'
"""

# WHERE id='+16176826385' AND text LIKE '%hi%' 

# get messages using the sql
messages = pd.read_sql_query(SQL, conn)

# limit to last few
messages = messages.drop(index=[i for i in range(len(messages)-100)])

print(messages['is_from_me'])

questions, answers = [], []
last_message_from, message_buildup = messages['is_from_me'][0], ""

for message, is_from_me, date_uct in zip(messages['text'], messages['is_from_me'], messages['date_uct']) :
    
    """ This will only be used for in-dept training.
    # check if it's a new chat
    processed_time = int(date_uct[11:].split(':')[:2][0])*60 + int(date_uct[11:].split(':')[:2][1])
    difference = processed_time-last_message
    if difference > 60 : # in minutes
        print('-'*10, "NEW CHAT", '-'*10)
    last_message = processed_time
    """

    # print message
    if last_message_from == is_from_me : # if this is still the same "thought"
        message_buildup.join(message)
        continue
    else :
        if questions == True : # this works beacues 1==Ture
            answers.append(message) # from me
        else :
            answers.append(message) # from her
        message_buildup=""
        
        
export_dataframe = pd.DataFrame(data={'QUESTIONS':questions, 'ANSWERS':answers })
print(export_dataframe)
    
