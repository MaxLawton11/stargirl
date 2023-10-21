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

# loop thoguh all of the message to put them in one list
# this is they can all be used for both qwestions ans aswers
# also, this allows us to maintain there order
compiled_messages = []
last_message = messages['is_from_me'].iloc[0]
message_buildup = ''
for message, is_from_me  in zip(messages['text'], messages['is_from_me']) :
    
    # if we are still on the same "thought"
    if last_message==is_from_me :
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
      
# to prevent memory leak, we will remove all the vars that are no longer needed for the rest of time
#del messages # this is no longer needed becacue the list takes its place
#del conn; del cur; del SQL # database no longer needed
#del last_message; del message_buildup # remove bullshit

questions,answers=[],[]

# now we need to make the questions and answers list
for counter, message, in enumerate(compiled_messages) :
    if counter < len(compiled_messages)-1 :
        questions.append(message)
        answers.append(compiled_messages[counter+1])

print(questions, len(questions))
print(answers, len(answers))
export_dataframe = pd.DataFrame(data={'QUESTIONS':questions, 'ANSWERS':answers })
print(export_dataframe)