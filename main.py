from datetime import datetime
from tkinter.filedialog import askopenfilename
import csv
import pandas as pd

filename = askopenfilename()
print(filename)

schedule = pd.DataFrame({'Subject': [], 'Description': [], 'Start Date': [], 'Start Time': [], 'End Time': []})

def findOffsets(reader):
    columnCounter = 0
    rowCounter = 0

    for row in reader:
        # print(f'Row {counter}: {row}')

        for column in row:
            try:
                # print(f'[{rowCounter}][{columnCounter}]:{column}')
                # print('Trying to convert to date')
                date = datetime.strptime(column, '%d.%m.%Y')
                print(f'Date found in col [{rowCounter}][{columnCounter}]:{column}: {date}')
                return columnCounter, rowCounter - 1
            except:
                pass
            columnCounter += 1

        columnCounter = 0
        rowCounter += 1

    return None

def find_classes(column_offset, row_offset, df, date):

    while True:
        try:
            date = datetime.strptime(df.iloc[row_offset].iloc[column_offset], '%d.%m.%Y')
            return row_offset, False
        except:
            if row_offset + 1 >= df.shape[0]:
                return row_offset, True
            
            subject = df.iloc[row_offset].iloc[column_offset + 6]
            prof_name = df.iloc[row_offset].iloc[column_offset + 3]

            if is_nan(subject) or is_nan(prof_name):
                row_offset += 1
                continue

            start_time = df.iloc[row_offset].iloc[column_offset]
            end_time = df.iloc[row_offset].iloc[column_offset + 2]
            
            total_time = df.iloc[row_offset].iloc[column_offset + 4]
            
            room = df.iloc[row_offset].iloc[column_offset + 7]

            description = f"{prof_name} - {room}"

            schedule.loc[len(schedule)] = [subject, description, date, start_time, end_time]
            print_schedule_info(date, start_time, end_time, prof_name, total_time, subject, room)

            row_offset += 1

def is_nan(obj):
    return obj != obj


def print_schedule_info(date, start_time, end_time, prof_name, total_time, subject, room):
    print(f'Date: {date}')
    print(f'Start Time: {start_time}')
    print(f'End Time: {end_time}')
    print(f'Prof Name: {prof_name}')
    print(f'Total Time: {total_time}')
    print(f'Subject: {subject}')
    print(f'Room: {room}')

with open(filename, encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=',')

    column_offset, row_offset = findOffsets(reader)
    print(f'Offset: {column_offset}')

    df = pd.read_csv(filename, sep=',', encoding='utf-8')
    print(f'xdd\n{df.iloc[row_offset].iloc[column_offset]}')

    rows, cols = df.shape
    
    print(f'Rows: {rows}, Cols: {cols}')
    
    while row_offset < rows:
        
        try:
            date = datetime.strptime(df.iloc[row_offset].iloc[column_offset], '%d.%m.%Y').strftime('%d.%m.%Y')

            row_offset += 1

            row_offset, done = find_classes(column_offset, row_offset, df, date)

            if done:
                break
        except:
            pass

    print(schedule)
    
schedule.to_csv(filename.removesuffix('.csv') + ' - importable.csv', index=False, float_format='%.2f')
        
    
