from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
import mysql.connector

#chromedriver options
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

url = 'https://www.mohfw.gov.in/'

#getting data from url and adding it to a list
data_1 = []
while len(data_1)<36:
        #send http get request using chromedriver
        wd = webdriver.Chrome('C:/Users/utkar/ChromeWebdriver/chromedriver', options=options)
        wd.get(url)
        html = wd.page_source
        df = pd.read_html(html)

        #preparing and adding data
        data = df[0].values.tolist()
        data = data[:36]

        for row in data:
                temp = []
                temp.append(row[1])
                temp.append(row[2])
                temp.append(row[4])
                temp.append(row[6])
                data_1.append(temp)

# converting list to dataframe to remove nan values
data_1 = pd.DataFrame(data_1,
                columns=['State Name', 'Active Today', 'Total Deaths', 'Total Discharged'])

# converting dataframe to record list
record = data_1.values.tolist()

# filling current date as a column in record list
curr_date = date.today()
for i in range(len(record)):
    record[i].append(curr_date)

print('\n--------------------------------------------\n')

# inserting records into database
try:
    # Initializing MySql Connection
    my_conn = mysql.connector.connect(
    host="localhost",
    database="covid_tracker",
    user="root",
    password="admin"
    )

    # Checking if Data for current date is already present or not
    my_cursor = my_conn.cursor()
    sql = "SELECT COUNT(*) FROM cv_state_wise WHERE data_date = %s"
    val = [curr_date]
    my_cursor.execute(sql, val)
    result = my_cursor.fetchall()

    if result[0][0] == 0:
        # Data for current date IS NOT PRESENT
        sql = "INSERT INTO cv_state_wise (state_name, active_today, total_death, total_discharged, data_date) VALUES (%s, %s, %s, %s, %s)"
        my_cursor.executemany(sql, record)
        my_conn.commit()

        print("Rows added : ",my_cursor.rowcount)

    else:
        # Data for current date PRESENT
        print("No rows inserted. Data for",curr_date, "already present")

except mysql.connector.Error as error:
    print("Failed to insert record into MySQL table {}".format(error))

# Closing connection
finally:
    if my_conn.is_connected():
        my_cursor.close()
        my_conn.close()
        print("MySQL connection is closed")

print('\n--------------------------------------------\n')