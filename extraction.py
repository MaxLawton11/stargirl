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

# get messages using the sql
messages = pd.read_sql_query(SQL, conn)

# loop thoguh all of the message to put them in one list
# this is they can all be used for both qwestions ans aswers
# also, this allows us to maintain there order
compiled_messages = []
last_message = messages['is_from_me'].iloc[0]
message_buildup = ''
for message, is_from_me  in zip(messages['text'], messages['is_from_me']) :
    if last_message==is_from_me : # if we are still on the same "thought"
        message = ''.join(message.splitlines()) # remove all whitespace
        if message_buildup != '' :
            message_buildup = f"{message_buildup}. {message}" #add to last if there is already somthing in the bulidup
        else :
            message_buildup = message # make new buildup
    else : # new "thought"
        compiled_messages.append(message_buildup)
        message_buildup = message
    last_message=is_from_me # change/check current person
compiled_messages.append(message_buildup) # empty buildup

# now we need to make the questions and answers list
# take current for question and take next for answer
questions,answers=[],[]
for counter, message, in enumerate(compiled_messages) :
    if counter < len(compiled_messages)-1 : # if there is room for more
        questions.append(message) 
        answers.append(compiled_messages[counter+1])

# make frame for exporting
export_dataframe = pd.DataFrame(data={'QUESTIONS':questions, 'ANSWERS':answers })
export_dataframe.to_csv('dataset.csv', index=False)
print("-- Compilation Complete --")