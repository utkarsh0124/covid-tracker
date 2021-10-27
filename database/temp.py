


### SCRIPT USED TO POPULATE DATABASE FROM csv FILES

import re
import glob
import mysql.connector
import pandas as pd
from datetime import datetime, date

record = []
path = "C:\\Users\\utkar\\CovidData"
file_names = glob.glob(path+'\\*.csv')

data_1 = []
for name in file_names:
    df = pd.read_csv(name)

    s = re.sub(r'^(([A-Za-zA-Z]*:\\)([A-Za-zA-Z]*\\){3})', "", name)
    year, month, day = int(s[6:10]), int(s[3:5]), int(s[:2])
    temp = date(year, month, day)
    df['data_date'] = temp
    df = df.drop(['SNo'], axis=1)
    l = len(df)
    if len(df)>35:
        df = df.drop([36], axis=0)
    data_1.append(df.values.tolist())


try:
    my_conn = mysql.connector.connect(
    host="localhost",
    database="covid_tracker",
    user="root",
    password="admin"
    )

    my_cursor = my_conn.cursor()

    for files in data_1:
        sql = """INSERT INTO cv_state_wise (state_name, active_today, total_death, total_discharged, data_date)
                VALUES (%s, %s, %s, %s, %s)"""
        my_cursor.executemany(sql, files)
        my_conn.commit()

except mysql.connector.Error as error:
    print("Failed to insert record into MySQL table {}".format(error))

finally:
    if my_conn.is_connected():
        my_cursor.close()
        my_conn.close()
        print("MySQL connection is closed")