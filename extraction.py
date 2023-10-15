import sqlite3
import pandas as pd
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

messages = messages.drop(index=[i for i in range(len(messages)-10)])

for message in zip(messages['text'], messages['is_from_me']) :
    if message[1] == True : # this works beacues 1==True
        print(" "*20, end='')
    print(message[0])



#print(messages.columns.tolist())
# sends to csv file on desktop
#messages.iloc[244:600].to_csv('test.csv', index=False, header=False)