import pyodbc
import pandas as pd
import colored

def query_calls(cursor, username):
    call_query = ("SELECT MIN(predID),"
                  "MAX(predID),"
                  "COUNT(predID),"
                  "COUNT(DISTINCT predID),"
                  "MIN(row_date),"
                  "MAX(row_date)"
                  "FROM [SERVER].[SCHEMA].[TABLE];"
                  "SELECT TOP (1) *"
                  "FROM [SERVER].[SCHEMA].[TABLE]"
                  "ORDER BY row_date ASC, start_Time_interval ASC;"
                  "SELECT TOP (1) *"
                  "FROM [SERVER].[SCHEMA].[TABLE]"
                  "ORDER BY row_date DESC, start_Time_interval DESC"
                  )

    cursor.execute(call_query)
    predID_info = cursor.fetchall()

    cursor.nextset()
    min_entry = cursor.fetchall()

    cursor.nextset()
    max_entry = cursor.fetchall()
    print('\n')
    print('DATA IN CDW (Test_Day_CO_Pred)')
    print('------------------------------')
    print('Earliest prediction is:', min_entry[0][1],'at interval',min_entry[0][2])
    print('Latest prediction:',max_entry[0][1],'at interval',max_entry[0][2])
    print("Minimum prediction ID is:",predID_info[0][0])
    print("Maximum prediction ID is:",predID_info[0][1])
    print("Number of rows in the table are:",predID_info[0][2])
    print("Number of distinct prediction IDs in the table are:",predID_info[0][3])
    print('******************************')
    if predID_info[0][1] == predID_info[0][2] and predID_info[0][1] == predID_info[0][3]:
        color = colored.fg('green')
        print(colored.stylize('Each prediction ID in the SQL table is unique and no gaps in entries',color))
    else:
        color = colored.fg('red')
        print(colored.stylize('Predictions in the SQL table may not be unique or there may be a predictions missing',color))
    print('******************************')
    print('\n')
    print('DATA IN CSV FILE')

    path = r'CHANGE PATH HERE'.format(username)
    latest_preds = pd.read_csv(path)
    print('Total rows in upload file is:',len(latest_preds))
    print('------------------------------')
    print('Number of unique predIDs in upload file is:', latest_preds['predID'].nunique())
    print('Min predID:', latest_preds['predID'].min())
    print('Max predID:', latest_preds['predID'].max())
    print('------------------------------')
    print('First row:\n', latest_preds.head(1))
    print('Last row:\n', latest_preds.tail(1))
    print('******************************')
    if (latest_preds['predID'].min() == predID_info[0][1]+1):
        color = colored.fg('green')
        print(colored.stylize('Minimum predID continues where SQL table leaves off',color))
    else:
        color = colored.fg('red')
        print(colored.stylize('predIDs are not lined up to SQL table or file may have already been uploaded',color))
    print('******************************')
    print('\n')

def query_chats(cursor, username):
    chat_query = ("SELECT MIN(predID),"
                  "MAX(predID),"
                  "COUNT(predID),"
                  "COUNT(DISTINCT predID),"
                  "MIN(Date),"
                  "MAX(Date)"
                  "FROM [SERVER].[SCHEMA].[TABLE];"
                  "SELECT TOP (1) *"
                  "FROM [SERVER].[SCHEMA].[TABLE]"
                  "ORDER BY Date ASC, Hour ASC;"
                  "SELECT TOP (1) *"
                  "FROM [SERVER].[SCHEMA].[TABLE]"
                  "ORDER BY Date DESC, Hour DESC"
                  )

    cursor.execute(chat_query)
    predID_info = cursor.fetchall()

    cursor.nextset()
    min_entry = cursor.fetchall()

    cursor.nextset()
    max_entry = cursor.fetchall()
    print('\n')
    print('DATA IN CDW (model_ChatOfferedAHTPred)')
    print('------------------------------')
    print('Earliest prediction is:', min_entry[0][1],'at interval',min_entry[0][2])
    print('Latest prediction:',max_entry[0][1],'at interval',max_entry[0][2])
    print("Minimum prediction ID is:",predID_info[0][0])
    print("Maximum prediction ID is:",predID_info[0][1])
    print("Number of rows in the table are:",predID_info[0][2])
    print("Number of distinct prediction IDs in the table are:",predID_info[0][3])
    print('******************************')
    if predID_info[0][1] == predID_info[0][2] and predID_info[0][1] == predID_info[0][3]:
        color = colored.fg('green')
        print(colored.stylize('Each prediction ID in the SQL table is unique and no gaps in entries',color))
    else:
        color = colored.fg('red')
        print(colored.stylize('Predictions in the SQL table may not be unique or there may be a predictions missing',color))
    print('******************************')
    print('\n')
    print('DATA IN CSV FILE')

    path = r'PATH GOES HERE'.format(username)
    latest_preds = pd.read_csv(path)
    print('Total rows in upload file is:',len(latest_preds))
    print('------------------------------')
    print('Number of unique predIDs in upload file is:', latest_preds['predID'].nunique())
    print('Min predID:', latest_preds['predID'].min())
    print('Max predID:', latest_preds['predID'].max())
    print('------------------------------')
    print('First row:\n', latest_preds.head(1))
    print('Last row:\n', latest_preds.tail(1))
    print('******************************')
    if (latest_preds['predID'].min() == predID_info[0][1]+1):
        color = colored.fg('green')
        print(colored.stylize('Minimum predID continues where SQL table leaves off',color))
    else:
        color = colored.fg('red')
        print(colored.stylize('predIDs are not lined up to SQL table or file may have already been uploaded',color))
    print('******************************')
    print('\n')

def query_texts(cursor, username):
    text_query = ("SELECT MIN(predID),"
                  "MAX(predID),"
                  "COUNT(predID),"
                  "COUNT(DISTINCT predID),"
                  "MIN(Date),"
                  "MAX(Date)"
                  "FROM [SERVER].[SCHEMA].[TABLE];"
                  "SELECT TOP (1) *"
                  "FROM [SERVER].[SCHEMA].[TABLE]"
                  "ORDER BY Date ASC, Hour ASC;"
                  "SELECT TOP (1) *"
                  "FROM [SERVER].[SCHEMA].[TABLE]"
                  "ORDER BY Date DESC, Hour DESC"
                  )

    cursor.execute(text_query)
    predID_info = cursor.fetchall()

    cursor.nextset()
    min_entry = cursor.fetchall()

    cursor.nextset()
    max_entry = cursor.fetchall()
    print('\n')
    print('DATA IN CDW (model_TextOfferedAHTPred)')
    print('------------------------------')
    print('Earliest prediction is:', min_entry[0][1],'at interval',min_entry[0][2])
    print('Latest prediction:',max_entry[0][1],'at interval',max_entry[0][2])
    print("Minimum prediction ID is:",predID_info[0][0])
    print("Maximum prediction ID is:",predID_info[0][1])
    print("Number of rows in the table are:",predID_info[0][2])
    print("Number of distinct prediction IDs in the table are:",predID_info[0][3])
    print('******************************')
    if predID_info[0][1] == predID_info[0][2] and predID_info[0][1] == predID_info[0][3]:
        color = colored.fg('green')
        print(colored.stylize('Each prediction ID in the SQL table is unique and no gaps in entries',color))
    else:
        color = colored.fg('red')
        print(colored.stylize('Predictions in the SQL table may not be unique or there may be a predictions missing',color))
    print('******************************')
    print('\n')
    print('DATA IN CSV FILE')

    path = r'PATH GOES HERE'.format(username)
    latest_preds = pd.read_csv(path)
    print('Total rows in upload file is:',len(latest_preds))
    print('------------------------------')
    print('Number of unique predIDs in upload file is:', latest_preds['predID'].nunique())
    print('Min predID:', latest_preds['predID'].min())
    print('Max predID:', latest_preds['predID'].max())
    print('------------------------------')
    print('First row:\n', latest_preds.head(1))
    print('Last row:\n', latest_preds.tail(1))
    print('******************************')
    if (latest_preds['predID'].min() == predID_info[0][1]+1):
        color = colored.fg('green')
        print(colored.stylize('Minimum predID continues where SQL table leaves off',color))
    else:
        color = colored.fg('red')
        print(colored.stylize('predIDs are not lined up to SQL table or file may have already been uploaded',color))
    print('******************************')
    print('\n')


def main():
    print('Hello, this program is used to check the current prediction IDs (predID) in CDW for the '
          'call, chat, and text predictions')

    server = 'SERVERNAME'
    database = 'DATABASENAME'
    driver = '{SQL Server}'
    Trusted_Connection = True
    username = input('Enter username ():')

    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database}'
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        # Perform your database operations here
        while True:
            integer = int(input('Enter 1 for Calls, 2 for Chats, 3 for Texts or 4 to end:'))
            if integer == 1:
                query_calls(cursor, username)
            elif integer == 2:
                query_chats(cursor, username)
            elif integer == 3:
                query_texts(cursor, username)
            elif integer == 4:
                break

    # Connection is automatically closed when leaving the 'with' block


if __name__ == "__main__":
    main()
