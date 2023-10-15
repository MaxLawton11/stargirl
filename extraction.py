import sqlite3
import pandas as pd
import time
import datetime

# substitute username with your username
conn = sqlite3.connect('chat.db')
# connect to the database
cur = conn.cursor()
# get the names of the tables in the database
cur.execute(" select name from sqlite_master where type = 'table' ") 

SQL = """
SELECT datetime(message.date/1000000000 + strftime("%s", "2001-01-01") ,"unixepoch","localtime") AS date_uct, id, text, is_from_me
FROM message
LEFT JOIN handle
ON message.handle_id = handle.ROWID
WHERE id='+16176826385'
"""

# WHERE id='+16176826385' AND text LIKE '%stella%' 

# get messages using the sql
messages = pd.read_sql_query(SQL, conn)

print(messages)

messages = messages.drop(index=[i for i in range(len(messages)-100)])

last_message=0
for message, is_from_me, date_uct  in zip(messages['text'], messages['is_from_me'], messages['date_uct']) :
    """
    difference = int(date_uct)-int(last_message)
    if difference > 3600 :
        print('-'*10, "NEW CHAT", '-'*10)
    last_message = date_uct"""
    
    print(date_uct)
    print( (str(date_uct[12:]).split(':'))[0]*60 )
    
    """if is_from_me == True : # this works beacues 1==True
        print(" "*20, end='')
    print(message)"""



#print(messages.columns.tolist())
# sends to csv file on desktop
#messages.iloc[244:600].to_csv('test.csv', index=False, header=False)