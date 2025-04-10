#!/usr/bin/python3

from datetime import date, datetime, timedelta
import mysql.connector
from mysql.connector import errorcode

try:
    mysql = mysql.connector.connect(host='localhost', user='pi', passwd='12zxcv', database='weather')
    mysql_cursor = mysql.cursor()
    sql_select_query = "select count(*) from WEATHER_MEASUREMENT;"
    mysql_cursor.execute(sql_select_query)
    mysql_result = mysql_cursor.fetchall()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Connection error, check credential")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    print("Resultfrom selecting database is") %mysql_result
    mysql_cursor.close()
    mysql.close()
    print("MySQL connection is closed")
